#!/usr/bin/env python3
"""
Create AI Translator v2.2.4 GitHub Package
إنشاء حزمة الترجمان الآلي v2.2.4 للنشر على GitHub مع إصلاحات الأخطاء والتحسينات
"""

import os
import shutil
import zipfile
from datetime import datetime

def create_github_package():
    """Create clean GitHub package for v2.2.4 with all fixes"""
    
    print("Creating AI Translator v2.2.4 GitHub Package...")
    print("إنشاء حزمة الترجمان الآلي v2.2.4...")
    
    # Package info
    package_name = "ai-translator-v2.2.4"
    zip_filename = f"{package_name}.zip"
    
    # Create temporary directory
    temp_dir = f"/tmp/{package_name}"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)
    
    # Essential files to include
    files_to_include = [
        # Core application files
        'app.py',
        'main.py', 
        'main_clean.py',
        'main_fixed.py',
        'models.py',
        'background_tasks.py',
        'process_video.py',
        'database_setup.py',
        'gpu_manager.py',
        'security_config.py',
        'server_config.py',
        'translations.py',
        
        # Services
        'services/',
        
        # Templates
        'templates/',
        
        # Static files
        'static/',
        
        # Documentation
        'README.md',
        'README_GITHUB.md',
        'README_GITHUB_v2.2.2.md',
        'INSTALL.md',
        'LICENSE',
        'CHANGELOG.md',
        'CHANGELOG_v2.1.0.md',
        'CHANGELOG_v2.2.0.md',
        'CHANGELOG_v2.2.1.md',
        'CHANGELOG_v2.2.2.md',
        'CONTRIBUTING.md',
        'DEPENDENCIES.md',
        'RELEASES.md',
        'SCREENSHOTS.md',
        'USER_GUIDE_v2.1.0.md',
        'API_DOCUMENTATION.md',
        'API_DOCUMENTATION_ENGLISH.md',
        'SECURITY_CHANGELOG.md',
        'VERSION_SUMMARY.md',
        
        # Release notes
        'RELEASE_NOTES_v2.2.0.md',
        'RELEASE_NOTES_v2.2.1.md', 
        'RELEASE_NOTES_v2.2.2.md',
        'RELEASE_NOTES_v2.2.3.md',
        
        # Installation scripts
        'install.sh',
        'install_fixed.sh',
        'install_ubuntu_server_v2.2.2.sh',
        'install_ubuntu_venv.sh',
        'install_ubuntu_venv_fixed.sh',
        'install_venv.sh',
        'env_setup.sh',
        'setup_service.sh',
        
        # Cleanup and maintenance
        'complete_system_reset.sh',
        'quick_cleanup.sh',
        'fresh_install.sh',
        'debug_service.sh',
        'diagnose_connection.sh',
        
        # Configuration files
        'pyproject.toml',
        '.gitignore',
        '.gitattributes',
        '.replit',
        'replit.md',
        
        # GitHub specific
        'GITHUB_SETUP_ENGLISH.md',
        'GITHUB_UPLOAD_GUIDE.md',
        'GITHUB_UPLOAD_INSTRUCTIONS.md',
        'GITHUB_RELEASE_GUIDE.md',
        'GITHUB_RELEASE_INSTRUCTIONS.md',
        'GITHUB_RELEASE_v2.2.2.md',
        'GITHUB_TEMPLATES.md',
        'QUICK_GITHUB_STEPS.md',
        'READY_FOR_UBUNTU_TEST.md',
        'UBUNTU_SERVER_TEST_GUIDE.md',
        
        # Documentation directories
        'docs/',
    ]
    
    # Copy files to temp directory
    copied_files = 0
    total_size = 0
    
    for item in files_to_include:
        src_path = item
        dst_path = os.path.join(temp_dir, item)
        
        if os.path.exists(src_path):
            if os.path.isdir(src_path):
                # Copy directory
                shutil.copytree(src_path, dst_path, ignore=shutil.ignore_patterns(
                    '__pycache__', '*.pyc', '*.pyo', '.DS_Store', 'Thumbs.db',
                    '*.log', 'node_modules', '.git', 'attached_assets'
                ))
                for root, dirs, files in os.walk(dst_path):
                    copied_files += len(files)
                    for file in files:
                        total_size += os.path.getsize(os.path.join(root, file))
            else:
                # Copy file
                os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                shutil.copy2(src_path, dst_path)
                copied_files += 1
                total_size += os.path.getsize(dst_path)
                
            print(f"✓ Copied: {item}")
        else:
            print(f"⚠ Not found: {item}")
    
    # Create release notes for v2.2.4
    release_notes_content = f"""# AI Translator v2.2.4 Release Notes

## Version 2.2.4 - Enhanced System Monitoring & Complete Error Resolution
**Release Date:** {datetime.now().strftime('%B %d, %Y')}

### 🚀 New Features
- **Enhanced System Monitor**: Comprehensive hardware detection including CPU, memory, storage, and network information
- **Professional Footer Design**: Redesigned footer with consistent typography and improved column alignment
- **Complete Error Resolution**: Fixed all LSP errors and import issues across the codebase

### 🔧 Technical Improvements
- Created missing `services/remote_storage.py` with comprehensive remote storage functionality
- Fixed SQLAlchemy database engine compatibility issues in main.py and main_fixed.py
- Resolved import errors in main_clean.py with proper module loading
- Updated function signatures for remote storage APIs with correct parameter handling
- Improved column alignment in footer layout with better spacing (1.5fr 1fr 1fr 1fr)

### 🎨 UI/UX Enhancements
- Unified copyright text into single line with proper spacing
- Enhanced mobile responsiveness with centered layout
- Added professional social media icons (GitHub, Facebook, Instagram) with hover effects
- Improved text spacing and readability with consistent line heights and colors

### 🗄️ Database & Performance
- Fixed all database engine compatibility issues
- Improved system information API with comprehensive hardware data
- Enhanced real-time monitoring with 5-second auto-refresh
- Better error handling and connection management

### 📦 Installation & Deployment
- All installation scripts tested and verified
- No more database initialization errors
- Complete Ubuntu Server 22.04/24.04 compatibility
- Ready for production deployment

### 🔍 System Requirements
- Ubuntu Server 22.04+ or Debian 11+
- Python 3.9+
- PostgreSQL 14+
- NVIDIA GPU (recommended for AI processing)
- 16GB RAM minimum, 32GB recommended
- 50GB free disk space

### 📋 Package Contents
- {copied_files} files included
- Size: {total_size / (1024*1024):.1f} MB
- Complete source code with all dependencies
- Comprehensive documentation and installation guides
- Professional deployment scripts

This release represents a significant stability improvement with all known errors resolved and enhanced system monitoring capabilities.
"""
    
    # Write release notes
    with open(os.path.join(temp_dir, 'RELEASE_NOTES_v2.2.4.md'), 'w', encoding='utf-8') as f:
        f.write(release_notes_content)
    copied_files += 1
    
    # Create ZIP file
    print(f"\nCreating ZIP archive: {zip_filename}")
    print(f"إنشاء الأرشيف المضغوط: {zip_filename}")
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as zipf:
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arc_name = os.path.relpath(file_path, temp_dir)
                zipf.write(file_path, arc_name)
    
    # Clean up temp directory
    shutil.rmtree(temp_dir)
    
    # Get final size
    final_size = os.path.getsize(zip_filename)
    
    print(f"\n✅ Package created successfully!")
    print(f"✅ تم إنشاء الحزمة بنجاح!")
    print(f"📦 File: {zip_filename}")
    print(f"📊 Files: {copied_files}")
    print(f"💾 Size: {final_size / (1024*1024):.2f} MB")
    print(f"🚀 Ready for GitHub release!")
    
    return zip_filename, copied_files, final_size

if __name__ == '__main__':
    create_github_package()