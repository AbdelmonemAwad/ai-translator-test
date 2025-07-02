# دليل التثبيت اليدوي لـ AI Translator v2.2.4

## الوصول للجهاز الافتراضي

### الطريقة 1: واجهة الويب
1. اذهب إلى: `http://mocd01.synology.me:5000`
2. سجل دخول بـ: `support1` / `Mocd@1209`
3. من القائمة الرئيسية > Package Center > Virtual Machine Manager
4. افتح الجهاز الافتراضي Ubuntu
5. اضغط "Connect" للوصول لـ Terminal

### الطريقة 2: SSH المحلي
إذا كان لديك وصول محلي للشبكة:
```bash
ssh eg2@192.168.x.x  # IP المحلي للـ VM
# كلمة المرور: 1q1
```

## أوامر التثبيت (نسخ ولصق)

### الخطوة 1: تحديث النظام
```bash
sudo apt update -y
sudo apt upgrade -y
```

### الخطوة 2: تثبيت المتطلبات
```bash
sudo apt install -y wget curl git unzip python3 python3-pip python3-venv postgresql postgresql-contrib nginx ffmpeg build-essential pkg-config software-properties-common apt-transport-https ca-certificates
```

### الخطوة 3: تحميل المشروع
```bash
cd /home/eg2
sudo rm -rf ai-translator
wget -O ai-translator.zip https://github.com/AbdelmonemAwad/ai-translator/archive/refs/heads/main.zip
unzip ai-translator.zip
mv ai-translator-main ai-translator
rm ai-translator.zip
cd ai-translator
```

### الخطوة 4: إعداد Python
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install flask flask-sqlalchemy gunicorn psycopg2-binary requests psutil pynvml email-validator werkzeug sendgrid
```

### الخطوة 5: إعداد قاعدة البيانات
```bash
sudo systemctl start postgresql
sudo systemctl enable postgresql
sudo -u postgres createuser -s ai_translator 2>/dev/null || true
sudo -u postgres createdb ai_translator 2>/dev/null || true
sudo -u postgres psql -c "ALTER USER ai_translator WITH PASSWORD 'ai_translator_pass2024';"
```

### الخطوة 6: متغيرات البيئة
```bash
cat > .env << 'ENV_EOF'
DATABASE_URL=postgresql://ai_translator:ai_translator_pass2024@localhost/ai_translator
PGHOST=localhost
PGPORT=5432
PGUSER=ai_translator
PGPASSWORD=ai_translator_pass2024
PGDATABASE=ai_translator
SESSION_SECRET=$(openssl rand -hex 32)
FLASK_APP=main.py
FLASK_ENV=production
ENV_EOF
```

### الخطوة 7: إعداد قاعدة البيانات
```bash
source .env
python3 database_setup.py
```

### الخطوة 8: إصلاح التبويبات المتطور
```bash
mkdir -p static/js
cat > static/js/comprehensive-tabs-fix.js << 'TABS_EOF'
console.log('🚀 Comprehensive Tabs Fix Loading...');

document.addEventListener('DOMContentLoaded', function() {
    let isInitialized = false;
    
    function initializeComprehensiveTabs() {
        if (isInitialized) return;
        
        console.log('🔧 Initializing Comprehensive Tabs System...');
        
        const categorySelect = document.getElementById('category-select');
        const subcategorySelect = document.getElementById('subcategory-select');
        
        if (!categorySelect || !subcategorySelect) {
            console.warn('⚠️ Tab controls not found, retrying...');
            setTimeout(initializeComprehensiveTabs, 1000);
            return;
        }
        
        const comprehensiveMapping = {
            'general': {
                sections: [
                    { id: 'DEFAULT', name: 'الإعدادات الأساسية / Basic Settings' },
                    { id: 'LANGUAGE', name: 'إعدادات اللغة / Language Settings' },
                    { id: 'FOOTER', name: 'إعدادات التذييل / Footer Settings' }
                ]
            },
            'ai': {
                sections: [
                    { id: 'WHISPER', name: 'إعدادات Whisper' },
                    { id: 'OLLAMA', name: 'إعدادات Ollama' },
                    { id: 'GPU', name: 'إدارة GPU / GPU Management' },
                    { id: 'API', name: 'إعدادات API / API Settings' }
                ]
            },
            'media': {
                sections: [
                    { id: 'PLEX', name: 'Plex Media Server' },
                    { id: 'JELLYFIN', name: 'Jellyfin Media Server' },
                    { id: 'EMBY', name: 'Emby Media Server' },
                    { id: 'KODI', name: 'Kodi Media Center' },
                    { id: 'RADARR', name: 'Radarr (أفلام / Movies)' },
                    { id: 'SONARR', name: 'Sonarr (مسلسلات / TV Shows)' }
                ]
            },
            'system': {
                sections: [
                    { id: 'PATHS', name: 'مسارات الملفات / File Paths' },
                    { id: 'REMOTE_STORAGE', name: 'التخزين البعيد / Remote Storage' },
                    { id: 'DATABASE', name: 'قاعدة البيانات / Database' },
                    { id: 'SECURITY', name: 'الأمان / Security' },
                    { id: 'SERVER', name: 'إعدادات الخادم / Server Settings' }
                ]
            },
            'development': {
                sections: [
                    { id: 'DEBUG', name: 'أدوات التطوير / Debug Tools' },
                    { id: 'TESTING', name: 'الاختبار / Testing' },
                    { id: 'DEVELOPMENT', name: 'أدوات التطوير / Development Tools' }
                ]
            }
        };
        
        function findAvailableSections() {
            const available = [];
            Object.values(comprehensiveMapping).flatMap(category => category.sections).forEach(section => {
                if (document.getElementById('tab-' + section.id)) {
                    available.push(section.id);
                }
            });
            console.log('📋 الأقسام المتاحة:', available);
            return available;
        }
        
        const availableSections = findAvailableSections();
        
        function forceHideAllTabs() {
            document.querySelectorAll('[id^="tab-"]').forEach(tab => {
                tab.style.display = 'none';
                tab.style.visibility = 'hidden';
                tab.style.opacity = '0';
                tab.classList.add('hidden');
                tab.setAttribute('hidden', '');
            });
        }
        
        function forceShowTab(sectionId) {
            console.log('👁️ Force showing section:', sectionId);
            forceHideAllTabs();
            
            const targetTab = document.getElementById('tab-' + sectionId);
            if (targetTab) {
                targetTab.style.display = 'block';
                targetTab.style.visibility = 'visible';
                targetTab.style.opacity = '1';
                targetTab.classList.remove('hidden');
                targetTab.removeAttribute('hidden');
                
                targetTab.scrollIntoView({ behavior: 'smooth', block: 'start' });
                console.log('✅ Successfully force showed:', sectionId);
                return true;
            } else {
                console.error('❌ Tab not found:', sectionId);
                return false;
            }
        }
        
        function updateSubcategories(categoryKey) {
            console.log('📝 Updating subcategories for:', categoryKey);
            
            subcategorySelect.innerHTML = '<option value="">اختر القسم الفرعي / Choose Subcategory</option>';
            
            const category = comprehensiveMapping[categoryKey];
            if (!category) {
                subcategorySelect.disabled = true;
                forceHideAllTabs();
                return;
            }
            
            const availableInCategory = category.sections.filter(section => 
                availableSections.includes(section.id)
            );
            
            if (availableInCategory.length === 0) {
                subcategorySelect.disabled = true;
                forceHideAllTabs();
                return;
            }
            
            availableInCategory.forEach(section => {
                const option = document.createElement('option');
                option.value = section.id;
                option.textContent = section.name;
                subcategorySelect.appendChild(option);
            });
            
            subcategorySelect.disabled = false;
            
            if (availableInCategory.length > 0) {
                subcategorySelect.value = availableInCategory[0].id;
                forceShowTab(availableInCategory[0].id);
            }
        }
        
        categorySelect.addEventListener('change', function() {
            updateSubcategories(this.value);
        });
        
        subcategorySelect.addEventListener('change', function() {
            if (this.value) {
                forceShowTab(this.value);
            } else {
                forceHideAllTabs();
            }
        });
        
        window.switchCategory = () => categorySelect.dispatchEvent(new Event('change'));
        window.switchTab = () => subcategorySelect.dispatchEvent(new Event('change'));
        
        const initialCategory = categorySelect.value || 'general';
        categorySelect.value = initialCategory;
        updateSubcategories(initialCategory);
        
        isInitialized = true;
        console.log('✅ Comprehensive Tabs System Initialized!');
        
        window.debugTabsSystem = function() {
            console.log('=== معلومات تشخيص التبويبات ===');
            console.log('الفئة:', categorySelect.value);
            console.log('القسم الفرعي:', subcategorySelect.value);
            console.log('الأقسام المتاحة:', availableSections);
            
            const visibleTabs = Array.from(document.querySelectorAll('[id^="tab-"]')).filter(tab => {
                const computed = window.getComputedStyle(tab);
                return computed.display !== 'none' && computed.visibility !== 'hidden';
            });
            
            console.log('التبويبات المرئية:', visibleTabs.map(tab => tab.id));
            return { category: categorySelect.value, subcategory: subcategorySelect.value, availableSections, visibleTabs: visibleTabs.map(tab => tab.id) };
        };
        
        window.forceShowSection = function(sectionId) {
            return forceShowTab(sectionId);
        };
        
        window.refreshTabsSystem = function() {
            isInitialized = false;
            setTimeout(initializeComprehensiveTabs, 500);
        };
    }
    
    setTimeout(initializeComprehensiveTabs, 800);
    
    const observer = new MutationObserver(function(mutations) {
        let shouldReinitialize = false;
        mutations.forEach(function(mutation) {
            if (mutation.type === 'childList') {
                mutation.addedNodes.forEach(function(node) {
                    if (node.nodeType === 1 && (node.id && node.id.startsWith('tab-') || node.querySelector && node.querySelector('[id^="tab-"]'))) {
                        shouldReinitialize = true;
                    }
                });
            }
        });
        if (shouldReinitialize && !isInitialized) {
            setTimeout(initializeComprehensiveTabs, 300);
        }
    });
    
    observer.observe(document.body, { childList: true, subtree: true });
});

console.log('✅ Comprehensive Tabs Fix Loaded!');
TABS_EOF
```

### الخطوة 9: تحديث layout.html
```bash
if [[ -f "templates/layout.html" ]]; then
    sed -i '/tabs-fix\.js/d' templates/layout.html
    sed -i '/final-tabs-fix\.js/d' templates/layout.html
    if ! grep -q "comprehensive-tabs-fix.js" templates/layout.html; then
        sed -i 's|</body>|    <script src="{{ url_for('\''static'\'', filename='\''js/comprehensive-tabs-fix.js'\'') }}"></script>\n</body>|' templates/layout.html
        echo "✅ تم تحديث layout.html"
    fi
fi
```

### الخطوة 10: إعداد خدمة systemd
```bash
sudo tee /etc/systemd/system/ai-translator.service > /dev/null << 'SERVICE_EOF'
[Unit]
Description=AI Translator Service
After=network.target postgresql.service
Wants=postgresql.service

[Service]
Type=simple
User=eg2
Group=eg2
WorkingDirectory=/home/eg2/ai-translator
Environment=PATH=/home/eg2/ai-translator/venv/bin
EnvironmentFile=/home/eg2/ai-translator/.env
ExecStart=/home/eg2/ai-translator/venv/bin/gunicorn --bind 0.0.0.0:5000 --workers 2 --timeout 300 main:app
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
SERVICE_EOF
```

### الخطوة 11: إعداد Nginx
```bash
sudo tee /etc/nginx/sites-available/ai-translator > /dev/null << 'NGINX_EOF'
server {
    listen 80;
    server_name _;
    
    client_max_body_size 2G;
    client_body_timeout 300s;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 300s;
    }
    
    location /static/ {
        alias /home/eg2/ai-translator/static/;
        expires 30d;
    }
}
NGINX_EOF

sudo ln -sf /etc/nginx/sites-available/ai-translator /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
```

### الخطوة 12: بدء الخدمات
```bash
sudo chown -R eg2:eg2 /home/eg2/ai-translator
sudo systemctl daemon-reload
sudo systemctl enable ai-translator
sudo systemctl restart postgresql
sudo systemctl restart nginx
sudo systemctl start ai-translator
```

### الخطوة 13: فحص النتائج
```bash
sleep 5
echo "📊 حالة الخدمات:"
sudo systemctl status ai-translator --no-pager
sudo systemctl status nginx --no-pager
sudo systemctl status postgresql --no-pager

echo "🔌 فحص المنافذ:"
ss -tlnp | grep -E ':(80|5000|5432) '

echo "🌐 اختبار الاتصال:"
curl -I http://localhost:5000/
curl -I http://localhost/
```

## بعد التثبيت

### معلومات الوصول:
- **الرابط**: http://mocd01.synology.me
- **المستخدم**: admin  
- **كلمة المرور**: your_strong_password

### أوامر مفيدة:
```bash
# مراقبة السجلات
sudo journalctl -u ai-translator -f

# إعادة تشغيل التطبيق
sudo systemctl restart ai-translator

# فحص حالة الخدمات
sudo systemctl status ai-translator nginx postgresql
```

### اختبار إصلاحات التبويبات:
1. سجل دخول للتطبيق
2. اذهب لصفحة الإعدادات
3. اضغط F12 وشغل: `debugTabsSystem()`
4. جرب تغيير الفئات والأقسام الفرعية

إذا واجهت مشاكل في التبويبات:
- `refreshTabsSystem()` - إعادة تحميل نظام التبويبات
- `forceShowSection('DEFAULT')` - إظهار قسم معين بالقوة