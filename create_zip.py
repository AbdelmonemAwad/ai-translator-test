#!/usr/bin/env python3
import os
import zipfile
import shutil

# قائمة الملفات والمجلدات المطلوبة
files_to_zip = [
    'README_GITHUB.md',
    'RELEASES.md',
    'CONTRIBUTING.md', 
    'DEPENDENCIES.md',
    '.gitignore',
    'app.py',
    'main.py',
    'models.py',
    'database_setup.py',
    'translations.py',
    'install.sh'
]

folders_to_zip = ['templates', 'static', 'services']

# إنشاء ملف ZIP
zip_name = 'ai-translator-github.zip'
with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
    # إضافة الملفات
    for file in files_to_zip:
        if os.path.exists(file):
            zipf.write(file, f'ai-translator/{file}')
            print(f"تم إضافة: {file}")
    
    # إضافة المجلدات
    for folder in folders_to_zip:
        if os.path.exists(folder):
            for root, dirs, files in os.walk(folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    arc_path = f'ai-translator/{file_path}'
                    zipf.write(file_path, arc_path)
            print(f"تم إضافة مجلد: {folder}")

print(f"\n✅ تم إنشاء ملف ZIP: {zip_name}")
print(f"الحجم: {os.path.getsize(zip_name)} bytes")