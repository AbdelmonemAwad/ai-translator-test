#!/usr/bin/env python3
"""
Create AI Translator v2.2.1 GitHub Package
إنشاء حزمة الترجمان الآلي v2.2.1 للنشر على GitHub
"""

import os
import shutil
import zipfile
from datetime import datetime

def create_github_package():
    """Create clean GitHub package for v2.2.1"""
    
    print("🔧 Creating AI Translator v2.2.1 GitHub Package...")
    
    # Package info
    package_name = "ai-translator-github-v2.2.1"
    package_dir = f"{package_name}"
    
    # Clean previous package
    if os.path.exists(package_dir):
        shutil.rmtree(package_dir)
    if os.path.exists(f"{package_name}.zip"):
        os.remove(f"{package_name}.zip")
    
    # Create package directory
    os.makedirs(package_dir)
    
    # Files to include
    files_to_copy = [
        # Core application files
        'app.py', 'main.py', 'models.py', 'wsgi.py',
        'background_tasks.py', 'process_video.py', 'database_setup.py',
        'translations.py', 'gpu_manager.py', 'security_config.py',
        
        # Installation scripts with fixes
        'install_ubuntu_venv.sh', 'install_fixed.sh', 'install_venv.sh',
        'complete_system_reset.sh', 'fresh_install.sh', 'quick_cleanup.sh',
        'test_install.sh', 'verify_installation.sh', 'env_setup.sh',
        
        # Configuration files
        'pyproject.toml', 'uv.lock', '.gitignore', '.gitattributes',
        
        # Documentation
        'README.md', 'README_GITHUB.md', 'INSTALL.md', 'LICENSE',
        'CHANGELOG.md', 'CHANGELOG_v2.2.0.md', 'RELEASE_NOTES_v2.2.1.md',
        'CONTRIBUTING.md', 'DEPENDENCIES.md', 'SECURITY_CHANGELOG.md',
        'GITHUB_RELEASE_GUIDE.md', 'QUICK_GITHUB_STEPS.md',
        
        # Version info
        'replit.md', 'VERSION_SUMMARY.md', 'USER_GUIDE_v2.1.0.md'
    ]
    
    # Directories to copy
    dirs_to_copy = [
        'templates', 'static', 'services'
    ]
    
    # Copy files
    copied_files = 0
    for file in files_to_copy:
        if os.path.exists(file):
            shutil.copy2(file, package_dir)
            copied_files += 1
            print(f"✓ Copied {file}")
    
    # Copy directories
    for dir_name in dirs_to_copy:
        if os.path.exists(dir_name):
            shutil.copytree(dir_name, os.path.join(package_dir, dir_name))
            print(f"✓ Copied directory {dir_name}")
    
    # Create GitHub-specific README
    readme_content = """# AI Translator v2.2.1 (الترجمان الآلي)

## 🚀 Quick Installation

### Ubuntu Server (Recommended)
```bash
# Download and run installation script
wget https://github.com/AbdelmonemAwad/ai-translator/releases/latest/download/install_ubuntu_venv.sh
sudo chmod +x install_ubuntu_venv.sh
sudo ./install_ubuntu_venv.sh
```

### Alternative Installation
```bash
# Fixed installation for Python 3.12+
wget https://github.com/AbdelmonemAwad/ai-translator/releases/latest/download/install_fixed.sh
sudo chmod +x install_fixed.sh
sudo ./install_fixed.sh
```

## ✨ What's New in v2.2.1

- ✅ **Python 3.12 Compatibility**: Fixed externally-managed-environment issues
- ✅ **Virtual Environment Support**: All installations now use virtual environments
- ✅ **Enhanced Installation Scripts**: Multiple installation options for different scenarios
- ✅ **Complete System Reset**: Comprehensive cleanup and fresh installation tools
- ✅ **Improved Translation Interface**: Fixed Arabic translation issues in development tools
- ✅ **Better Documentation**: Enhanced installation guides and troubleshooting

## 🔧 Installation Options

1. **install_ubuntu_venv.sh** - Complete Ubuntu installation with virtual environment
2. **install_fixed.sh** - Fixed installation for Python 3.12+ systems
3. **install_venv.sh** - Basic virtual environment installation
4. **complete_system_reset.sh** - Complete system cleanup before fresh install
5. **verify_installation.sh** - Verify installation success

## 📋 System Requirements

- Ubuntu Server 22.04+ / Debian 11+
- Python 3.9+ (automatically detected)
- PostgreSQL 12+
- NVIDIA GPU (recommended for AI processing)
- 4GB+ RAM, 20GB+ disk space

## 🔐 Default Credentials

- **Username**: admin
- **Password**: your_strong_password

## 🛠️ Advanced Features

- **Multi-language Support**: Arabic and English interface
- **Media Server Integration**: Plex, Jellyfin, Emby, Kodi, Radarr, Sonarr
- **AI-Powered Translation**: Whisper + Ollama integration
- **GPU Management**: Automatic GPU detection and allocation
- **Security Features**: Comprehensive file system protection
- **Responsive Design**: Mobile-friendly interface

## 🆘 Support

- **Documentation**: See included INSTALL.md and README.md
- **GitHub Issues**: Report bugs and request features
- **Community**: Join our growing community of users

## 📄 License

GNU General Public License v3.0 - Open source with copyleft protection.

---
**Developer**: عبدالمنعم عوض (AbdelmonemAwad)  
**Version**: 2.2.1  
**Build Date**: """ + datetime.now().strftime("%Y-%m-%d") + """
"""
    
    # Write GitHub README
    with open(os.path.join(package_dir, 'README_GITHUB.md'), 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    # Create ZIP package
    print(f"📦 Creating ZIP package...")
    with zipfile.ZipFile(f"{package_name}.zip", 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(package_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, package_dir)
                zipf.write(file_path, arcname)
    
    # Get package info
    package_size = os.path.getsize(f"{package_name}.zip")
    size_mb = round(package_size / (1024 * 1024), 2)
    
    # Count files
    total_files = 0
    for root, dirs, files in os.walk(package_dir):
        total_files += len(files)
    
    # Cleanup temp directory
    shutil.rmtree(package_dir)
    
    print(f"✅ Package created successfully!")
    print(f"📦 File: {package_name}.zip")
    print(f"📊 Size: {size_mb} MB")
    print(f"📁 Files: {total_files}")
    print(f"🗓️ Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return f"{package_name}.zip"

if __name__ == "__main__":
    create_github_package()