# دليل التنصيب اليدوي للخادم البعيد
## AI Translator v2.2.4 - Manual Deployment Guide

### معلومات الخادم البعيد
- **عنوان IP**: 5.31.55.179
- **اسم المستخدم**: eg2  
- **كلمة المرور**: 1q1
- **المنفذ**: 22

---

## الخطوة 1: الاتصال بالخادم البعيد

```bash
ssh eg2@5.31.55.179
# أدخل كلمة المرور: 1q1
```

## الخطوة 2: التنظيف الشامل للنظام

```bash
# الحصول على صلاحيات root
sudo -i

# إيقاف جميع الخدمات
systemctl stop ai-translator 2>/dev/null || true
systemctl stop nginx 2>/dev/null || true
systemctl disable ai-translator 2>/dev/null || true

# حذف التنصيبات السابقة
rm -rf /root/ai-translator
rm -rf /opt/ai-translator-venv
rm -f /etc/systemd/system/ai-translator.service
rm -f /etc/nginx/sites-available/ai-translator
rm -f /etc/nginx/sites-enabled/ai-translator

# إنهاء العمليات العالقة
pkill -f 'gunicorn.*ai-translator' 2>/dev/null || true
pkill -f 'python.*app.py' 2>/dev/null || true
pkill -f 'python.*main.py' 2>/dev/null || true

echo "✓ تم التنظيف الشامل"
```

## الخطوة 3: تحديث النظام وتثبيت المتطلبات

```bash
# تحديث النظام
apt update
apt upgrade -y

# تثبيت المتطلبات الأساسية
apt install -y python3 python3-pip python3-venv postgresql postgresql-contrib nginx curl wget git

echo "✓ تم تثبيت المتطلبات"
```

## الخطوة 4: إعداد قاعدة البيانات PostgreSQL

```bash
# بدء خدمة PostgreSQL
systemctl start postgresql
systemctl enable postgresql

# إنشاء قاعدة البيانات والمستخدم
sudo -u postgres createdb ai_translator
sudo -u postgres psql -c "CREATE USER ai_translator WITH PASSWORD 'ai_translator_pass2024';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE ai_translator TO ai_translator;"

echo "✓ تم إعداد قاعدة البيانات"
```

## الخطوة 5: تحميل وتثبيت AI Translator

```bash
# إنشاء مجلد التثبيت
mkdir -p /root/ai-translator
cd /root/ai-translator

# تحميل الملفات من GitHub (أو نسخ من مصدر آخر)
# يمكنك استخدام أحد الطرق التالية:

# الطريقة 1: تحميل من GitHub
wget https://github.com/AbdelmonemAwad/ai-translator/archive/refs/heads/main.zip
unzip main.zip
mv ai-translator-main/* .
rm -rf ai-translator-main main.zip

# أو الطريقة 2: نسخ الملفات يدوياً إذا كان لديك أرشيف
# tar -xzf ai-translator-v2.2.4.tar.gz

echo "✓ تم تحميل الملفات"
```

## الخطوة 6: إعداد البيئة الافتراضية Python

```bash
cd /root/ai-translator

# إنشاء البيئة الافتراضية
python3 -m venv venv

# تفعيل البيئة الافتراضية
source venv/bin/activate

# تحديث pip
pip install --upgrade pip

# تثبيت المكتبات المطلوبة
pip install flask flask-sqlalchemy gunicorn psycopg2-binary psutil requests pynvml werkzeug

echo "✓ تم إعداد البيئة الافتراضية"
```

## الخطوة 7: إعداد قاعدة البيانات

```bash
cd /root/ai-translator

# تعيين متغير البيئة لقاعدة البيانات
export DATABASE_URL='postgresql://ai_translator:ai_translator_pass2024@localhost/ai_translator'

# تشغيل إعداد قاعدة البيانات
python database_setup.py

echo "✓ تم إعداد قاعدة البيانات"
```

## الخطوة 8: إنشاء خدمة Systemd

```bash
# إنشاء ملف الخدمة
cat > /etc/systemd/system/ai-translator.service << 'EOF'
[Unit]
Description=AI Translator v2.2.4
After=network.target postgresql.service

[Service]
Type=notify
User=root
WorkingDirectory=/root/ai-translator
Environment=DATABASE_URL=postgresql://ai_translator:ai_translator_pass2024@localhost/ai_translator
Environment=SESSION_SECRET=ai-translator-super-secret-key-2024
ExecStart=/root/ai-translator/venv/bin/gunicorn --bind 0.0.0.0:5000 --workers 2 --timeout 300 main:app
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

echo "✓ تم إنشاء خدمة Systemd"
```

## الخطوة 9: إعداد Nginx

```bash
# إنشاء تكوين Nginx
cat > /etc/nginx/sites-available/ai-translator << 'EOF'
server {
    listen 80 default_server;
    server_name _;
    
    client_max_body_size 100M;
    proxy_read_timeout 300;
    proxy_connect_timeout 300;
    proxy_send_timeout 300;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

# تفعيل التكوين
rm -f /etc/nginx/sites-enabled/default
ln -sf /etc/nginx/sites-available/ai-translator /etc/nginx/sites-enabled/

# اختبار تكوين Nginx
nginx -t

echo "✓ تم إعداد Nginx"
```

## الخطوة 10: بدء الخدمات

```bash
# تحديث Systemd
systemctl daemon-reload

# تفعيل وبدء الخدمات
systemctl enable ai-translator
systemctl start ai-translator
systemctl restart nginx

echo "✓ تم بدء جميع الخدمات"
```

## الخطوة 11: التحقق من حالة النظام

```bash
# فحص حالة الخدمات
systemctl status ai-translator --no-pager
systemctl status nginx --no-pager
systemctl status postgresql --no-pager

# اختبار الاتصال
curl -I http://localhost/

echo "✓ تم التحقق من النظام"
```

---

## معلومات الوصول بعد التثبيت

### 🌐 الوصول للتطبيق
- **الرابط**: http://5.31.55.179
- **اسم المستخدم**: admin
- **كلمة المرور**: your_strong_password

### 📋 أوامر إدارة النظام

```bash
# بدء الخدمة
systemctl start ai-translator

# إيقاف الخدمة  
systemctl stop ai-translator

# فحص حالة الخدمة
systemctl status ai-translator

# مراقبة سجلات النظام
journalctl -u ai-translator -f

# إعادة تشغيل Nginx
systemctl restart nginx

# مراقبة استخدام الموارد
htop
```

### 🔧 استكشاف الأخطاء

```bash
# فحص سجلات AI Translator
journalctl -u ai-translator --no-pager -l

# فحص سجلات Nginx
tail -f /var/log/nginx/error.log

# فحص اتصال قاعدة البيانات
sudo -u postgres psql ai_translator -c "SELECT version();"

# فحص المنافذ المستخدمة
netstat -tulpn | grep :5000
netstat -tulpn | grep :80
```

---

## ✅ التحقق من نجاح التثبيت

1. **اختبار HTTP**: `curl -I http://5.31.55.179`
2. **فحص الخدمات**: `systemctl status ai-translator nginx postgresql`
3. **الوصول عبر المتصفح**: http://5.31.55.179
4. **تسجيل الدخول**: admin / your_strong_password

---

## 📝 ملاحظات مهمة

- تأكد من أن منافذ 22, 80, 5000 مفتوحة في جدار الحماية
- قم بإجراء نسخ احتياطية دورية لقاعدة البيانات
- راقب استخدام الموارد خاصة الذاكرة والمساحة
- حدث النظام دورياً لضمان الأمان

---

## 🆘 الدعم والمساعدة

في حالة وجود مشاكل:
1. راجع سجلات النظام أولاً
2. تأكد من عمل جميع الخدمات  
3. اتحقق من اتصال قاعدة البيانات
4. تأكد من صحة تكوين Nginx