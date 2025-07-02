# دليل حذف الملفات للتحديث

## 🔍 إذا لم تجد خيار الحذف في GitHub Desktop

### الطريقة 1: من File Explorer مباشرة
```
1. في GitHub Desktop، انسخ مسار المجلد:
   - اضغط Repository في القائمة العلوية
   - اختر "Show in File Explorer"

2. في File Explorer:
   - اضغط Ctrl + A لاختيار جميع الملفات
   - اضغط Delete
   - أو اضغط كليك يمين واختر Delete
```

### الطريقة 2: استخدام PowerShell (Windows)
```
1. في GitHub Desktop:
   - اضغط Repository → Open in Command Prompt

2. في Command Prompt:
   - اكتب: powershell
   - اكتب الأمر التالي:
   
Get-ChildItem -Path . -Exclude .git,.gitignore | Remove-Item -Recurse -Force
```

### الطريقة 3: حذف يدوي انتقائي
```
1. افتح مجلد repository في File Explorer
2. احذف هذه الملفات واحد واحد:
   - احذف مجلد templates
   - احذف مجلد static  
   - احذف مجلد services
   - احذف جميع ملفات .py (app.py, main.py, models.py, etc)
   - احذف ملفات .md (README.md, CONTRIBUTING.md, etc)
   - احذف install.sh
   - احذف LICENSE
   
3. اترك فقط:
   - مجلد .git (مخفي)
   - ملف .gitignore (إن وجد)
```

### الطريقة 4: إعادة تشغيل GitHub Desktop
```
1. أغلق GitHub Desktop
2. احذف الملفات من File Explorer مباشرة
3. افتح GitHub Desktop مرة أخرى
4. ستظهر التغييرات تلقائياً
```

### الطريقة 5: استخدام Git مباشرة
```
1. افتح Command Prompt في مجلد repository
2. اكتب:
   git rm -r --cached .
   git clean -fd
   
3. هذا سيحذف جميع الملفات من Git tracking
```

## ✅ بعد حذف الملفات:

1. انسخ محتويات ai-translator-v2.2.0 المفكوك
2. الصق في مجلد repository الفارغ
3. ارجع لـ GitHub Desktop
4. ستظهر جميع الملفات الجديدة في Changes
5. اكتب commit message وارفع التحديث

أي طريقة من هذه ستعمل لحذف الملفات وتحديث repository.