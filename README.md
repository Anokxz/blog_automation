# Hugo Blog Deployment and Markdown Processing

This project contains two Python scripts for automating the deployment of a Hugo-based blog and processing Markdown files with image replacements. 

## Scripts Overview

### 1. `main.py`

The `main.py` script automates the deployment of a Hugo-based blog by syncing posts from an Obsidian-based source, building the Hugo site, committing changes to a Git repository, and deploying the site to GitHub.

#### Key Features:
- **Logging**: Configures logging for deployment with rotating log files for general logs and error logs.
- **Git Operations**: Initializes the Git repository, adds the remote, pulls from the remote repository, and commits changes.
- **Hugo Theme Setup**: Adds a Hugo theme as a Git submodule if not already initialized.
- **Post Synchronization**: Syncs posts from the source directory to the destination directory.
- **Markdown Processing**: Runs a separate script (`replace.py`) to process image links in Markdown files.
- **Hugo Build**: Builds the Hugo site.
- **GitHub Deployment**: Deploys the public folder to the `blog` branch on GitHub.

#### How to Use:
1. Ensure Python 3, Git, rsync, and Hugo are installed on your machine.
2. Clone this repository.
3. Configure the `source_path`, `destination_path`, and `repo_url` variables in `main.py` as per your local setup.
4. Run `main.py` to:
   - Sync posts from the source directory.
   - Process Markdown files.
   - Build the Hugo site.
   - Commit and push the changes to GitHub.
   - Deploy the public folder to the `blog` branch on GitHub.

```bash
python3 main.py
```

### 2. `replace.py`

The `replace.py` script processes Markdown files to find image links in the format `[[image_name.png]]` and replaces them with Hugo-compatible image links (`[Image Description](/images/image_name.png)`). It also copies the images from the source directory to the Hugo `static/images/` directory.

#### How it Works:
- It scans all Markdown files in the `posts_dir` for image links.
- It replaces the image links with proper Markdown format and copies the images to the Hugo `static/images/` directory.

#### How to Use:
1. Run `replace.py` after syncing the posts with `main.py`.
2. It will automatically find the images, replace the links, and copy the images to the appropriate directory.

```bash
python3 replace.py
```

### Prerequisites
- Python 3
- Git
- Hugo
- Golang
- rsync

### File Structure

.
├── main.py                  # Main deployment and blog processing script
├── replace.py               # Script for processing Markdown files and images
├── logs/                    # Folder for storing log files
    ├── deployment.log       # General deployment logs
    └── errors.log           # Error logs


### License
This project is licensed under the MIT License.
