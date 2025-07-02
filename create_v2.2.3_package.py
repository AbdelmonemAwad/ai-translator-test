#!/usr/bin/env python3
"""
Create AI Translator v2.2.3 GitHub Package
إنشاء حزمة الترجمان الآلي v2.2.3 للنشر على GitHub مع إصلاحات القوائم المنسدلة
"""

import os
import shutil
import zipfile
from pathlib import Path

def create_github_package():
    """Create clean GitHub package for v2.2.3 with dropdown fixes"""
    
    print("🔧 Creating AI Translator v2.2.3 GitHub Package...")
    
    # Package configuration
    version = "v2.2.3"
    package_name = f"ai-translator-{version}"
    zip_filename = f"{package_name}.zip"
    
    # Create clean package directory
    if os.path.exists(package_name):
        shutil.rmtree(package_name)
    os.makedirs(package_name)
    
    # Essential files for GitHub distribution
    essential_files = [
        # Main application files
        'app.py',
        'main.py', 
        'models.py',
        'background_tasks.py',
        'process_video.py',
        'database_setup.py',
        'translations.py',
        'gpu_manager.py',
        'security_config.py',
        
        # Fixed dropdown issues
        'fix_dropdown_issues.py',
        'DROPDOWN_FIXES_INSTRUCTIONS.md',
        
        # Installation and deployment
        'install_ubuntu_server_v2.2.2.sh',
        'install.sh',
        'nginx_static_fix.sh',
        'test_ubuntu_installation.sh',
        
        # Configuration files
        'pyproject.toml',
        '.replit',
        '.gitignore',
        '.gitattributes',
        'setup.py',
        
        # Documentation
        'README.md',
        'README_GITHUB.md',
        'README_GITHUB_v2.2.2.md',
        'INSTALL.md',
        'LICENSE',
        'CHANGELOG.md',
        'RELEASE_NOTES_v2.2.2.md',
        'UBUNTU_SERVER_TEST_GUIDE.md',
        'GITHUB_RELEASE_GUIDE.md',
        'DEPENDENCIES.md',
        'CONTRIBUTING.md',
        
        # Version and release information
        'VERSION_SUMMARY.md',
        'RELEASES.md',
        'CHANGELOG_v2.1.0.md',
        'CHANGELOG_v2.2.0.md',
        'USER_GUIDE_v2.1.0.md',
        
        # Additional scripts
        'create_v2.2.2_package.py',
        'complete_system_reset.sh',
        'quick_cleanup.sh',
        'fresh_install.sh',
        'env_setup.sh',
        
        # Project metadata
        'replit.md'
    ]
    
    # Essential directories
    essential_dirs = [
        'static',
        'templates', 
        'services',
        'docs'
    ]
    
    print(f"📁 Copying {len(essential_files)} essential files...")
    
    # Copy files
    copied_files = 0
    for file in essential_files:
        if os.path.exists(file):
            shutil.copy2(file, package_name)
            copied_files += 1
            print(f"✓ {file}")
        else:
            print(f"⚠ Missing: {file}")
    
    # Copy directories
    copied_dirs = 0
    for dir_name in essential_dirs:
        if os.path.exists(dir_name):
            dest_dir = os.path.join(package_name, dir_name)
            shutil.copytree(dir_name, dest_dir)
            copied_dirs += 1
            print(f"✓ {dir_name}/")
        else:
            print(f"⚠ Missing directory: {dir_name}")
    
    print(f"\n📦 Creating package archive: {zip_filename}")
    
    # Create ZIP archive
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(package_name):
            # Skip unnecessary directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'node_modules']]
            
            for file in files:
                if file.endswith(('.pyc', '.pyo', '.DS_Store')):
                    continue
                    
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, package_name)
                zipf.write(file_path, arcname)
    
    # Get package size
    package_size = os.path.getsize(zip_filename)
    size_mb = round(package_size / (1024 * 1024), 2)
    
    # Count files in package
    with zipfile.ZipFile(zip_filename, 'r') as zipf:
        file_count = len(zipf.namelist())
    
    print(f"\n✅ Package created successfully!")
    print(f"📄 File: {zip_filename}")
    print(f"📊 Size: {size_mb} MB")
    print(f"📁 Files: {file_count}")
    print(f"🔧 Copied: {copied_files} files, {copied_dirs} directories")
    
    # Create release notes
    release_notes = f"""# AI Translator v2.2.3 - Dropdown Fixes Release

## 🔧 Critical Fixes in v2.2.3

### ✅ Dropdown Menu Issues Fixed
- Fixed dropdown menus showing "true/false" instead of translated options
- Corrected all settings page dropdown processing
- Enhanced multilingual support for select options
- Improved JSON parsing for dropdown values

### 🛠 New Tools Added
- `fix_dropdown_issues.py`: Comprehensive dropdown repair script
- `DROPDOWN_FIXES_INSTRUCTIONS.md`: Step-by-step fix guide
- Enhanced PostgreSQL settings management

### 📦 Package Information
- **Version**: {version}
- **Size**: {size_mb} MB
- **Files**: {file_count}
- **Installation**: Ubuntu Server 22.04/24.04

### 🚀 Quick Installation
```bash
wget https://github.com/AbdelmonemAwad/ai-translator/releases/download/{version}/{zip_filename}
unzip {zip_filename}
cd {package_name}
chmod +x install_ubuntu_server_v2.2.2.sh
sudo ./install_ubuntu_server_v2.2.2.sh
```

### 🔧 Fix Existing Installation
```bash
cd /root/ai-translator
python3 fix_dropdown_issues.py
sudo systemctl restart ai-translator
```

### 📋 What's Fixed
- Language dropdown: العربية/English options
- Theme dropdown: داكن/فاتح/تلقائي options  
- Items per page: 12/24/48/96 options
- Whisper model: All model options properly displayed
- Ollama model: All model options properly displayed
- GPU settings: Auto/GPU 0/GPU 1/CPU Only options
- Development settings: Enabled/Disabled options

Default credentials: admin / your_strong_password
"""
    
    with open(f"RELEASE_NOTES_{version}.md", "w", encoding="utf-8") as f:
        f.write(release_notes)
    
    print(f"\n📝 Release notes created: RELEASE_NOTES_{version}.md")
    
    # Cleanup temporary directory
    shutil.rmtree(package_name)
    
    return zip_filename, size_mb, file_count

if __name__ == "__main__":
    try:
        zip_file, size, count = create_github_package()
        print(f"\n🎉 AI Translator v2.2.3 package ready for GitHub!")
        print(f"📦 Upload {zip_file} to GitHub releases")
        
    except Exception as e:
        print(f"❌ Error creating package: {str(e)}")
        exit(1)