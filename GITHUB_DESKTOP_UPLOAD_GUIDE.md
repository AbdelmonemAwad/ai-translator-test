# دليل رفع AI Translator v2.2.0 باستخدام GitHub Desktop

## 📥 المتطلبات الأولية

### 1. تحميل GitHub Desktop
- اذهب إلى: https://desktop.github.com/
- حمل التطبيق وثبته على جهازك
- سجل دخول بحساب GitHub الخاص بك

### 2. تحضير الملف
- اذهب إلى: `http://localhost:5000/download`
- حمل ملف `ai-translator-v2.2.0.zip`
- فك الضغط في مجلد على سطح المكتب

## 🚀 خطوات الرفع باستخدام GitHub Desktop

### الخطوة 1: إنشاء Repository على الويب
1. اذهب إلى: https://github.com/new
2. املأ البيانات:
   - **Repository name:** `ai-translator`
   - **Description:** `Advanced AI-powered multilingual translation system`
   - **Public** ✅
   - لا تختر أي خيارات إضافية
3. اضغط "Create repository"

### الخطوة 2: استنساخ Repository في GitHub Desktop
1. افتح GitHub Desktop
2. اضغط "Clone a repository from the Internet"
3. اختر "GitHub.com"
4. ابحث عن `ai-translator` في قائمة repositories
5. اختر المجلد المناسب لحفظ المشروع
6. اضغط "Clone"

### الخطوة 3: نسخ الملفات
1. افتح مجلد المشروع المستنسخ
2. احذف أي ملفات موجودة (إن وجدت)
3. انسخ جميع محتويات `ai-translator-v2.2.0` المفكوك
4. الصق الملفات في مجلد المشروع

### الخطوة 4: رفع التغييرات (Commit)
1. ارجع إلى GitHub Desktop
2. ستظهر جميع الملفات الجديدة في قسم "Changes"
3. في خانة "Summary":
   ```
   AI Translator v2.2.0 - Interactive Slideshow & Clean Distribution
   ```
4. في خانة "Description":
   ```
   ✨ Features:
   - Interactive slideshow interface with CSS-based mockups
   - Coming Soon OS support (Casa OS, Zima OS, Linux distributions)
   - Advanced GitHub language detection with .gitattributes
   - Complete Arabic subtitle translation system
   - Professional documentation and release packaging

   🔧 Technical:
   - 62 files, clean distribution package
   - No internal download functionality for public use
   - Enhanced translations and UI improvements
   - PostgreSQL database integration
   ```
5. اضغط "Commit to main"

### الخطوة 5: دفع التغييرات (Push)
1. اضغط "Push origin" في الشريط العلوي
2. انتظر انتهاء الرفع
3. ستظهر رسالة نجاح العملية

### الخطوة 6: إنشاء Release من الموقع
1. اذهب إلى repository على GitHub
2. اضغط "Releases" في الشريط الجانبي
3. اضغط "Create a new release"

### الخطوة 7: تعبئة بيانات Release
**🏷️ Tag version:** `v2.2.0`

**📝 Release title:** `AI Translator v2.2.0 - Interactive Slideshow & Clean Distribution`

**📄 Description:**
```markdown
# 🚀 AI Translator v2.2.0

نظام ترجمة متقدم مدعوم بالذكاء الاصطناعي لتحويل الأفلام والمسلسلات إلى العربية

## ✨ المميزات الجديدة

### 🎬 عرض شرائح تفاعلي
- عرض تلقائي مع تقدم كل 4 ثوانٍ
- أزرار التنقل ومؤشرات الشرائح
- عناصر CSS تفاعلية بدلاً من الصور

### 🖥️ دعم الأنظمة المستقبلية
- تكامل Casa OS - نظام سحابة شخصي
- دعم Zima OS - نظام سحابة كامل
- خريطة توزيعات Linux

### 🔧 تحسينات تقنية
- إصلاح اكتشاف اللغة في GitHub
- تحسين نظام الترجمة مع 25+ ترجمة جديدة
- واجهة نظيفة بدون ميزات تحميل داخلية

## 📊 الإحصائيات
- **62 ملف** في حزمة الإصدار
- **238KB** حجم مضغوط
- **دعم كامل** للغتين العربية والإنجليزية

## 🛠️ متطلبات النظام
- Ubuntu Server 22.04+ أو Debian 11+
- Python 3.9+
- كارت رسوميات NVIDIA
- 16GB+ RAM موصى به

## 📥 التثبيت السريع
```bash
curl -fsSL https://github.com/YOUR_USERNAME/ai-translator/releases/latest/download/install.sh | sudo bash
```

## 👨‍💻 المطور
**عبدالمنعم عوض (AbdelmonemAwad)**
- 📧 Email: Eg2@live.com
- 🐙 GitHub: [@AbdelmonemAwad](https://github.com/AbdelmonemAwad)

## 📄 الترخيص
GNU General Public License v3.0
```

### الخطوة 8: رفع الملفات
1. اضغط "Attach binaries by dropping them here"
2. اسحب وأفلت الملفات التالية:
   - الملف الأصلي المحمل: `ai-translator-v2.2.0.zip`
   - ملف التثبيت: `install.sh` (من داخل الملف المفكوك)
3. اضغط "Publish release"

## ✅ التحقق من النجاح

بعد الانتهاء تأكد من:
- [ ] صفحة Repository تظهر الملفات
- [ ] README.md يعرض بشكل صحيح
- [ ] Release متاح في قسم Releases
- [ ] الملفات قابلة للتحميل

## 🔗 الروابط النهائية

ستحصل على الروابط التالية:
- **المشروع:** `https://github.com/YOUR_USERNAME/ai-translator`
- **الإصدار:** `https://github.com/YOUR_USERNAME/ai-translator/releases/tag/v2.2.0`
- **التحميل:** `https://github.com/YOUR_USERNAME/ai-translator/releases/download/v2.2.0/ai-translator-v2.2.0.zip`

## 📝 ملاحظات مهمة

1. **استبدل YOUR_USERNAME** باسم المستخدم الحقيقي
2. **تأكد من رفع install.sh** في Assets
3. **اختبر روابط التحميل** بعد النشر
4. **الملف نظيف** وجاهز للتوزيع العام

## 🆘 حل المشاكل الشائعة

### إذا لم تظهر الملفات في GitHub Desktop:
- تأكد من نسخ الملفات في المجلد الصحيح
- اضغط "Refresh" في التطبيق

### إذا فشل Push:
- تأكد من اتصال الإنترنت
- تأكد من صحة بيانات تسجيل الدخول

### إذا لم يظهر Repository:
- تأكد من تسجيل الدخول بنفس الحساب
- حدث قائمة Repositories في GitHub Desktop

---

تم إعداد هذا الدليل خصيصاً لاستخدام GitHub Desktop مع AI Translator v2.2.0