#!/usr/bin/env python3

import os
import subprocess
import sys
import logging
from logging.handlers import TimedRotatingFileHandler
import shutil

# Configure logging
def configure_logging():
    """Set up the logging system."""
    log_formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] [%(module)s.%(funcName)s]: %(message)s"
    )
    
    # General log file (rotates daily, keeps 7 days of logs)
    general_log = TimedRotatingFileHandler("logs/deployment.log", when="D", interval=1, backupCount=7)
    general_log.setFormatter(log_formatter)
    general_log.setLevel(logging.INFO)
    
    # Error log file
    error_log = logging.FileHandler("logs/errors.log")
    error_log.setFormatter(log_formatter)
    error_log.setLevel(logging.ERROR)
    
    # Stream handler for console output
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_formatter)
    console_handler.setLevel(logging.INFO)
    
    # Add handlers to root logger
    logging.basicConfig(
        level=logging.DEBUG,
        handlers=[general_log, error_log, console_handler]
    )

# Configure logs folder
os.makedirs("logs", exist_ok=True)
configure_logging()

# Configurable variables
source_path = "/mnt/c/Users/snaks/Documents/Notes"
destination_path = "/mnt/c/Users/snaks/Documents/Blog"
repo_url = "https://github.com/Anokxz/Anokxz.github.io.git"

def run_command(command, check=True, capture_output=False):
    """Run a shell command and handle errors."""
    try:
        logging.info(f"Running command: {command}")
        result = subprocess.run(command, shell=True, check=check, text=True, capture_output=capture_output)
        if capture_output:
            return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        logging.error(f"Command failed: {command}")
        logging.error(f"Error: {e.stderr.strip() if e.stderr else str(e)}")
        sys.exit(1)

def check_commands(commands):
    """Check if required commands are available."""
    for cmd in commands:
        if not shutil.which(cmd):
            logging.error(f"{cmd} is not installed or not in PATH.")
            sys.exit(1)

def init_git_repo():
    """Initialize the Git repository if not already initialized."""
    if not os.path.exists(destination_path):
        run_command(f"hugo new site {destination_path}")
    os.chdir(destination_path)

    if not os.path.exists(".git"):
        logging.info("Initializing Git repository...")
        run_command(f"git init")
        run_command(f"git remote add origin {repo_url}")
        try:
            run_command(f"git pull origin main")
        except Exception as e:
            logging.warning(f"Could not pull from remote: {str(e)}")
    else:
        logging.info("Git repository already initialized.")
        if "origin" not in run_command("git remote", capture_output=True):
            logging.info("Adding remote origin...")
            run_command(f"git remote add origin {repo_url}")

def init_theme():
    """Initialize Hugo theme as a Git submodule."""
    theme = "terminal"
    themes_urls = {
        "terminal": "https://github.com/panr/hugo-theme-terminal.git themes/terminal",
        "risotto": "https://github.com/joeroe/risotto themes/risotto"
    }
    if not os.path.exists(f"{destination_path}/themes/{theme}"):
        run_command(f"git submodule add -f {themes_urls[theme]}")
        run_command("wget https://raw.githubusercontent.com/Anokxz/Linux-tools/main/hugo.toml -O hugo.toml")

def sync_posts():
    """Sync posts from source to destination."""
    if not os.path.isdir(source_path):
        logging.error(f"Source path does not exist: {source_path}")
        sys.exit(1)

    if not os.path.isdir(destination_path):
        logging.error(f"Destination path does not exist: {destination_path}")
        sys.exit(1)

    logging.info("Syncing posts from Obsidian...")
    run_command(f"rsync -av --delete {source_path}/posts/ {destination_path}/content/posts/")

def process_markdown():
    """Process image links in Markdown files."""
    os.chdir(current_folder)
    if not os.path.isfile("replace.py"):
        logging.error("Python script replace.py not found.")
        sys.exit(1)

    logging.info("Processing image links in Markdown files...")
    run_command("python3 replace.py")

def build_hugo():
    """Build Hugo site."""
    logging.info("Building the Hugo site...")
    os.chdir(destination_path)
    run_command("hugo")

def commit_and_push_changes():
    """Commit changes and push to the main branch."""
    logging.info("Staging changes for Git...")
    if not run_command("git diff --quiet && git diff --cached --quiet", check=False):
        run_command("git add .")

        commit_message = input("Enter the commit message: ")
        logging.info("Committing changes...")
        run_command(f"git commit -m \"{commit_message}\"")

    logging.info("Deploying to GitHub main...")
    run_command("git push origin main")

def deploy_blog():
    """Deploy the public folder to the blog branch."""
    logging.info("Deploying to GitHub blog...")
    if "blog" in run_command("git branch --list", capture_output=True):
        run_command("git branch -D blog")

    run_command("git subtree split --prefix public -b blog")
    run_command("git push origin blog:blog --force")
    run_command("git branch -D blog")

def main():
    """Main function to orchestrate the deployment process."""
    try:
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        check_commands(["git", "rsync", "python3", "hugo"])
        init_git_repo()
        init_theme()
        sync_posts()
        process_markdown()
        build_hugo()
        commit_and_push_changes()
        deploy_blog()

        logging.info("All done! Site synced, processed, committed, built, and deployed.")
    except Exception as e:
        logging.exception("An unexpected error occurred.")
        sys.exit(1)

if __name__ == "__main__":
    current_folder = os.getcwd()
    main()
