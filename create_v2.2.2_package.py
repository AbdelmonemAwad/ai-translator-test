#!/usr/bin/env python3
"""
Create AI Translator v2.2.2 GitHub Package
إنشاء حزمة الترجمان الآلي v2.2.2 للنشر على GitHub
"""

import os
import zipfile
import shutil
from datetime import datetime

def create_github_package():
    """Create clean GitHub package for v2.2.2"""
    
    package_name = "ai-translator-v2.2.2"
    zip_filename = f"{package_name}.zip"
    
    # Files to include in the package
    files_to_include = [
        # Core application files
        "app.py",
        "main.py", 
        "models.py",
        "background_tasks.py",
        "process_video.py",
        "database_setup.py",
        "gpu_manager.py",
        "translations.py",
        "security_config.py",
        "server_config.py",
        "wsgi.py",
        
        # Configuration files
        "pyproject.toml",
        "uv.lock",
        ".replit",
        ".gitignore",
        ".gitattributes",
        
        # Installation and testing scripts
        "install_ubuntu_server_v2.2.2.sh",
        "test_ubuntu_installation.sh",
        "setup.py",
        
        # Documentation
        "README.md",
        "README_GITHUB_v2.2.2.md",
        "RELEASE_NOTES_v2.2.2.md",
        "GITHUB_RELEASE_v2.2.2.md",
        "UBUNTU_SERVER_TEST_GUIDE.md",
        "GITHUB_READY_CHECKLIST.md",
        "API_DOCUMENTATION.md",
        "CONTRIBUTING.md",
        "DEPENDENCIES.md",
        "CHANGELOG.md",
        "LICENSE",
        "replit.md",
        
        # Additional documentation
        "INSTALL.md",
        "SECURITY_CHANGELOG.md",
        "VERSION_SUMMARY.md",
        "USER_GUIDE_v2.1.0.md",
    ]
    
    # Directories to include
    directories_to_include = [
        "templates/",
        "static/",
        "services/",
        "docs/",
    ]
    
    print(f"Creating AI Translator v2.2.2 package...")
    print(f"Package name: {package_name}")
    
    try:
        # Remove existing package if it exists
        if os.path.exists(zip_filename):
            os.remove(zip_filename)
            print(f"Removed existing {zip_filename}")
        
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            file_count = 0
            
            # Add individual files
            for file_path in files_to_include:
                if os.path.exists(file_path):
                    zipf.write(file_path, f"{package_name}/{file_path}")
                    print(f"Added: {file_path}")
                    file_count += 1
                else:
                    print(f"Warning: {file_path} not found")
            
            # Add directories
            for directory in directories_to_include:
                if os.path.exists(directory):
                    for root, dirs, files in os.walk(directory):
                        # Skip hidden directories and __pycache__
                        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
                        
                        for file in files:
                            # Skip hidden files, Python cache, and temporary files
                            if (not file.startswith('.') and 
                                not file.endswith('.pyc') and
                                not file.endswith('.pyo') and
                                not file.endswith('.tmp')):
                                
                                file_path = os.path.join(root, file)
                                archive_path = f"{package_name}/{file_path}"
                                zipf.write(file_path, archive_path)
                                print(f"Added: {file_path}")
                                file_count += 1
                else:
                    print(f"Warning: Directory {directory} not found")
        
        # Get file size
        file_size = os.path.getsize(zip_filename)
        file_size_mb = file_size / (1024 * 1024)
        
        print("\n" + "="*60)
        print(f"✅ Package created successfully!")
        print(f"📦 File: {zip_filename}")
        print(f"📊 Size: {file_size_mb:.2f} MB ({file_size:,} bytes)")
        print(f"📁 Files: {file_count}")
        print(f"🕒 Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)
        
        # Create download info
        print(f"\n📥 Download Information:")
        print(f"Package Name: {package_name}")
        print(f"Version: v2.2.2")
        print(f"Platform: Ubuntu Server 22.04+ / 24.04")
        print(f"Architecture: Production-ready with complete compatibility")
        
        return zip_filename
        
    except Exception as e:
        print(f"❌ Error creating package: {e}")
        return None

if __name__ == "__main__":
    create_github_package()