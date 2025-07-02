# دليل التثبيت خطوة بخطوة - AI Translator v2.2.4
## للخادم: 5.31.55.179 | المستخدم: eg2 | كلمة المرور: 1q1

---

## 🚀 التثبيت الفوري - انسخ والصق مباشرة

### الخطوة 1: الاتصال بالخادم
```bash
ssh eg2@5.31.55.179
# كلمة المرور: 1q1
```

### الخطوة 2: تحديث النظام
```bash
sudo apt update -y && sudo apt upgrade -y
```

### الخطوة 3: تثبيت المتطلبات الأساسية
```bash
sudo apt install -y wget curl git unzip python3 python3-pip python3-venv postgresql postgresql-contrib nginx ffmpeg build-essential pkg-config
```

### الخطوة 4: تحميل المشروع
```bash
cd /home/eg2
sudo rm -rf ai-translator 2>/dev/null
wget -O ai-translator.zip https://github.com/AbdelmonemAwad/ai-translator/archive/refs/heads/main.zip
unzip ai-translator.zip
mv ai-translator-main ai-translator
rm ai-translator.zip
cd ai-translator
```

### الخطوة 5: إعداد Python
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install flask flask-sqlalchemy gunicorn psycopg2-binary requests psutil pynvml email-validator werkzeug sendgrid
```

### الخطوة 6: إعداد قاعدة البيانات
```bash
sudo systemctl start postgresql
sudo systemctl enable postgresql
sudo -u postgres createuser -s ai_translator 2>/dev/null || true
sudo -u postgres createdb ai_translator 2>/dev/null || true
sudo -u postgres psql -c "ALTER USER ai_translator WITH PASSWORD 'ai_translator_pass2024';"
```

### الخطوة 7: إنشاء ملف البيئة
```bash
cat > .env << 'EOF'
DATABASE_URL=postgresql://ai_translator:ai_translator_pass2024@localhost/ai_translator
PGHOST=localhost
PGPORT=5432
PGUSER=ai_translator
PGPASSWORD=ai_translator_pass2024
PGDATABASE=ai_translator
FLASK_APP=main.py
FLASK_ENV=production
EOF

echo "SESSION_SECRET=$(openssl rand -hex 32)" >> .env
```

### الخطوة 8: تهيئة قاعدة البيانات
```bash
source .env
python3 database_setup.py
```

### الخطوة 9: إنشاء إصلاح التبويبات المتطور
```bash
mkdir -p static/js

cat > static/js/ultimate-tabs-fix.js << 'JSFIX'
console.log('🚀 Ultimate Tabs Fix Loading...');

document.addEventListener('DOMContentLoaded', function() {
    let isInitialized = false;
    
    function initializeTabs() {
        if (isInitialized) return;
        
        const categorySelect = document.getElementById('category-select');
        const subcategorySelect = document.getElementById('subcategory-select');
        
        if (!categorySelect || !subcategorySelect) {
            setTimeout(initializeTabs, 1000);
            return;
        }
        
        const mapping = {
            'general': {
                sections: [
                    { id: 'DEFAULT', name: 'الإعدادات الأساسية' },
                    { id: 'LANGUAGE', name: 'إعدادات اللغة' },
                    { id: 'UI', name: 'إعدادات الواجهة' }
                ]
            },
            'ai': {
                sections: [
                    { id: 'WHISPER', name: 'إعدادات Whisper' },
                    { id: 'OLLAMA', name: 'إعدادات Ollama' },
                    { id: 'GPU', name: 'إدارة GPU' },
                    { id: 'API', name: 'إعدادات API' }
                ]
            },
            'media': {
                sections: [
                    { id: 'PLEX', name: 'Plex Media Server' },
                    { id: 'JELLYFIN', name: 'Jellyfin Media Server' },
                    { id: 'EMBY', name: 'Emby Media Server' },
                    { id: 'RADARR', name: 'Radarr (أفلام)' },
                    { id: 'SONARR', name: 'Sonarr (مسلسلات)' }
                ]
            },
            'system': {
                sections: [
                    { id: 'PATHS', name: 'مسارات الملفات' },
                    { id: 'DATABASE', name: 'قاعدة البيانات' },
                    { id: 'SERVER', name: 'إعدادات الخادم' }
                ]
            }
        };
        
        function findAvailableSections() {
            const available = [];
            Object.values(mapping).flatMap(cat => cat.sections).forEach(section => {
                if (document.querySelector('#tab-' + section.id)) {
                    available.push(section.id);
                }
            });
            return available;
        }
        
        const availableSections = findAvailableSections();
        
        function hideAllTabs() {
            document.querySelectorAll('[id^="tab-"]').forEach(tab => {
                tab.style.display = 'none';
                tab.classList.add('hidden');
            });
        }
        
        function showTab(sectionId) {
            hideAllTabs();
            const tab = document.querySelector('#tab-' + sectionId);
            if (tab) {
                tab.style.display = 'block';
                tab.classList.remove('hidden');
                setTimeout(() => tab.scrollIntoView({ behavior: 'smooth' }), 100);
                return true;
            }
            return false;
        }
        
        function updateSubcategories(categoryKey) {
            subcategorySelect.innerHTML = '<option value="">اختر القسم</option>';
            
            const category = mapping[categoryKey];
            if (!category) return;
            
            const available = category.sections.filter(s => availableSections.includes(s.id));
            
            available.forEach(section => {
                const option = document.createElement('option');
                option.value = section.id;
                option.textContent = section.name;
                subcategorySelect.appendChild(option);
            });
            
            if (available.length > 0) {
                subcategorySelect.value = available[0].id;
                showTab(available[0].id);
            }
        }
        
        categorySelect.addEventListener('change', function() {
            updateSubcategories(this.value);
        });
        
        subcategorySelect.addEventListener('change', function() {
            if (this.value) showTab(this.value);
            else hideAllTabs();
        });
        
        updateSubcategories(categorySelect.value || 'general');
        
        window.ultimateDebugTabs = function() {
            return { availableSections, category: categorySelect.value, subcategory: subcategorySelect.value };
        };
        
        window.ultimateShowSection = showTab;
        
        isInitialized = true;
        console.log('✅ Ultimate Tabs System Ready!');
    }
    
    setTimeout(initializeTabs, 1000);
});
JSFIX
```

### الخطوة 10: تحديث layout.html
```bash
if [[ -f "templates/layout.html" ]]; then
    sed -i 's|</body>|    <script src="{{ url_for('\''static'\'', filename='\''js/ultimate-tabs-fix.js'\'') }}"></script>\n</body>|' templates/layout.html
    echo "✅ تم تحديث layout.html"
fi
```

### الخطوة 11: إنشاء خدمة systemd
```bash
sudo tee /etc/systemd/system/ai-translator.service > /dev/null << 'SERVICE'
[Unit]
Description=AI Translator Service
After=network.target postgresql.service

[Service]
Type=simple
User=eg2
Group=eg2
WorkingDirectory=/home/eg2/ai-translator
Environment=PATH=/home/eg2/ai-translator/venv/bin
EnvironmentFile=/home/eg2/ai-translator/.env
ExecStart=/home/eg2/ai-translator/venv/bin/gunicorn --bind 0.0.0.0:5000 --workers 2 main:app
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
SERVICE
```

### الخطوة 12: إعداد Nginx
```bash
sudo tee /etc/nginx/sites-available/ai-translator > /dev/null << 'NGINX'
server {
    listen 80;
    server_name _;
    
    client_max_body_size 5G;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /static/ {
        alias /home/eg2/ai-translator/static/;
        expires 1y;
    }
}
NGINX

sudo ln -sf /etc/nginx/sites-available/ai-translator /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
```

### الخطوة 13: بدء الخدمات
```bash
sudo chown -R eg2:eg2 /home/eg2/ai-translator
sudo systemctl daemon-reload
sudo systemctl enable ai-translator
sudo systemctl restart postgresql
sudo systemctl restart nginx
sudo systemctl start ai-translator
```

### الخطوة 14: فحص النتائج
```bash
echo "⏳ انتظار بدء الخدمات..."
sleep 10

echo "📊 فحص الخدمات:"
for service in ai-translator nginx postgresql; do
    if systemctl is-active --quiet $service; then
        echo "✅ $service: يعمل"
    else
        echo "❌ $service: متوقف"
        sudo journalctl -u $service -n 3
    fi
done

echo ""
echo "🔌 فحص المنافذ:"
for port in 80 5000 5432; do
    if ss -tlnp | grep -q ":$port "; then
        echo "✅ منفذ $port: مفتوح"
    else
        echo "❌ منفذ $port: مغلق"
    fi
done

echo ""
echo "🌐 اختبار الاتصال:"
if curl -s http://localhost/ | grep -q "title\|html"; then
    echo "✅ التطبيق يعمل بنجاح!"
    echo "🌐 الرابط: http://5.31.55.179"
    echo "🔑 المستخدم: admin"
    echo "🔑 كلمة المرور: your_strong_password"
else
    echo "❌ مشكلة في التطبيق"
    echo "تحقق من السجلات: sudo journalctl -u ai-translator -n 10"
fi
```

---

## 🚨 استكشاف الأخطاء

### إذا فشل PostgreSQL:
```bash
sudo systemctl restart postgresql
sudo -u postgres psql -c "ALTER USER ai_translator WITH PASSWORD 'ai_translator_pass2024';"
```

### إذا فشل التطبيق:
```bash
cd /home/eg2/ai-translator
source venv/bin/activate
source .env
python3 -c "import app; print('App imports successfully')"
```

### إذا فشل Nginx:
```bash
sudo nginx -t
sudo systemctl restart nginx
```

### فحص السجلات:
```bash
sudo journalctl -u ai-translator -f
sudo journalctl -u nginx -f
sudo journalctl -u postgresql -f
```

---

## ✅ علامات النجاح

- جميع الخدمات تظهر "يعمل" ✅
- المنافذ 80, 5000, 5432 مفتوحة ✅  
- `curl http://localhost/` يعيد HTML ✅
- صفحة http://5.31.55.179 تظهر صفحة تسجيل الدخول ✅

**🎉 عند النجاح، ستحصل على نظام ترجمة متكامل مع إصلاحات التبويبات المتطورة!**