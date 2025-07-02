#!/usr/bin/env python3

import os
import shutil
import zipfile
from datetime import datetime

def create_github_package():
    """Create updated GitHub package with virtual environment support"""
    
    print("🔄 Creating updated GitHub package...")
    
    # Package info
    version = "v2.2.1"
    package_name = f"ai-translator-github-{version}"
    
    # Create temporary directory
    temp_dir = f"/tmp/{package_name}"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)
    
    # Essential files to include
    files_to_copy = [
        'app.py', 'main.py', 'models.py', 'background_tasks.py', 'process_video.py',
        'database_setup.py', 'gpu_manager.py', 'translations.py', 'security_config.py',
        'install_fixed.sh', 'install_ubuntu_venv.sh', 'install_venv.sh',
        'complete_system_reset.sh', 'fresh_install.sh', 'quick_cleanup.sh',
        'CLEANUP_COMMANDS.md', 'README.md', 'README_GITHUB.md', 'INSTALL.md',
        'CHANGELOG.md', 'LICENSE', 'CONTRIBUTING.md', 'DEPENDENCIES.md',
        'replit.md', 'pyproject.toml', '.gitignore', '.gitattributes',
        'setup.py', 'wsgi.py'
    ]
    
    # Copy essential files
    copied_files = []
    for file in files_to_copy:
        if os.path.exists(file):
            shutil.copy2(file, temp_dir)
            copied_files.append(file)
            print(f"✓ Copied: {file}")
    
    # Copy directories
    dirs_to_copy = ['templates', 'static', 'services']
    for dir_name in dirs_to_copy:
        if os.path.exists(dir_name):
            shutil.copytree(dir_name, os.path.join(temp_dir, dir_name))
            copied_files.append(f"{dir_name}/")
            print(f"✓ Copied directory: {dir_name}/")
    
    # Create version info file
    version_info = f"""# AI Translator Version Information

Version: {version}
Release Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Python Support: 3.9+
Ubuntu Support: 22.04+ with Virtual Environment

## Key Features in This Release:
- ✅ Python 3.12 Virtual Environment Support
- ✅ Fixed "externally-managed-environment" error
- ✅ Enhanced Installation Scripts
- ✅ Complete System Cleanup Tools
- ✅ Production-Ready Systemd Service
- ✅ PostgreSQL Integration
- ✅ Nginx Reverse Proxy Configuration

## Installation:
```bash
wget https://github.com/AbdelmonemAwad/ai-translator/archive/refs/heads/main.zip
unzip main.zip
cd ai-translator-main
chmod +x install_ubuntu_venv.sh
sudo ./install_ubuntu_venv.sh
```

## Default Credentials:
- Username: admin
- Password: your_strong_password
"""
    
    with open(os.path.join(temp_dir, 'VERSION_INFO.md'), 'w', encoding='utf-8') as f:
        f.write(version_info)
    copied_files.append('VERSION_INFO.md')
    
    # Create zip package
    zip_path = f"{package_name}.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arc_name = os.path.relpath(file_path, temp_dir)
                zipf.write(file_path, arc_name)
    
    # Get package info
    zip_size = os.path.getsize(zip_path) / 1024  # KB
    
    # Cleanup temp directory
    shutil.rmtree(temp_dir)
    
    print(f"""
🎉 Updated GitHub package created successfully!

📦 Package: {zip_path}
📏 Size: {zip_size:.1f} KB
📁 Files: {len(copied_files)} files/directories

Key Updates:
✅ Virtual Environment Support (Python 3.12 compatible)
✅ Enhanced Installation Scripts
✅ System Cleanup Tools
✅ Production-Ready Configuration

Ready for GitHub upload!
""")
    
    return zip_path, len(copied_files), zip_size

if __name__ == "__main__":
    create_github_package()