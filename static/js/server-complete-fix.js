// Complete JavaScript Fix for Remote Server - إصلاح شامل للخادم البعيد
console.log('🚀 Loading complete JavaScript fix for remote server...');

// Define global functions first
window.switchCategory = function() {
    console.log('switchCategory called');
    const categorySelect = document.getElementById('category-select');
    if (categorySelect) {
        categorySelect.dispatchEvent(new Event('change'));
    }
};

window.switchTab = function() {
    console.log('switchTab called');
    const subcategorySelect = document.getElementById('subcategory-select');
    if (subcategorySelect) {
        subcategorySelect.dispatchEvent(new Event('change'));
    }
};

window.saveAllSettings = function() {
    console.log('saveAllSettings called');
    const form = document.querySelector('form');
    if (form) {
        form.submit();
    } else {
        console.error('Form not found');
    }
};

// Main initialization
document.addEventListener('DOMContentLoaded', function() {
    console.log('🔧 Settings tabs and dropdowns fix starting...');
    
    // تعريف التصنيفات والتصنيفات الفرعية
    const categoryMappings = {
        'general': {
            label: '🔧 عام / General',
            subcategories: {
                'DEFAULT': 'إعدادات عامة / General Settings',
                'INTERFACE': 'الواجهة / Interface',
                'LANGUAGE': 'اللغة / Language'
            }
        },
        'ai': {
            label: '🤖 الذكاء الاصطناعي / AI',
            subcategories: {
                'WHISPER': 'Whisper (التعرف على الكلام)',
                'OLLAMA': 'Ollama (الترجمة)',
                'GPU': 'إعدادات GPU / GPU Settings'
            }
        },
        'media': {
            label: '📺 خوادم الوسائط / Media Servers',
            subcategories: {
                'PLEX': 'Plex Media Server',
                'JELLYFIN': 'Jellyfin Media Server',
                'EMBY': 'Emby Media Server',
                'KODI': 'Kodi Media Center',
                'RADARR': 'Radarr (Movies)',
                'SONARR': 'Sonarr (TV Shows)'
            }
        },
        'system': {
            label: '⚙️ النظام / System',
            subcategories: {
                'PATHS': 'مسارات الملفات / File Paths',
                'REMOTE_STORAGE': 'التخزين البعيد / Remote Storage',
                'SERVER': 'إعدادات الخادم / Server Settings'
            }
        },
        'development': {
            label: '🛠️ التطوير / Development',
            subcategories: {
                'DEBUG': 'إعدادات التصحيح / Debug Settings',
                'TESTING': 'إعدادات الاختبار / Testing Settings'
            }
        }
    };
    
    // إصلاح القوائم المنسدلة
    function fixDropdowns() {
        const categorySelect = document.getElementById('category-select');
        const subcategorySelect = document.getElementById('subcategory-select');
        
        if (categorySelect && subcategorySelect) {
            console.log('✅ Found category dropdowns, fixing...');
            
            // إضافة مستمع للتغيير في التصنيف الرئيسي
            categorySelect.addEventListener('change', function() {
                const selectedCategory = this.value;
                console.log('Category changed to:', selectedCategory);
                
                // تنظيف التصنيف الفرعي
                subcategorySelect.innerHTML = '';
                
                // إضافة خيارات التصنيف الفرعي
                if (categoryMappings[selectedCategory] && categoryMappings[selectedCategory].subcategories) {
                    Object.entries(categoryMappings[selectedCategory].subcategories).forEach(([key, label]) => {
                        const option = document.createElement('option');
                        option.value = key.toLowerCase();
                        option.textContent = label;
                        subcategorySelect.appendChild(option);
                    });
                }
                
                // تشغيل تغيير التصنيف الفرعي
                subcategorySelect.dispatchEvent(new Event('change'));
            });
            
            // إضافة مستمع للتغيير في التصنيف الفرعي
            subcategorySelect.addEventListener('change', function() {
                const selectedSubcategory = this.value.toUpperCase();
                console.log('Subcategory changed to:', selectedSubcategory);
                showTabContent(selectedSubcategory);
            });
            
            // تشغيل التغيير الأولي
            categorySelect.dispatchEvent(new Event('change'));
        }
    }
    
    // إظهار محتوى التبويب
    function showTabContent(tabId) {
        console.log('Showing tab content for:', tabId);
        
        // إخفاء جميع التبويبات
        const allTabs = document.querySelectorAll('.tab-content');
        allTabs.forEach(tab => {
            tab.classList.add('hidden');
            tab.style.display = 'none';
        });
        
        // إظهار التبويب المحدد
        const targetTab = document.getElementById('tab-' + tabId) || 
                         document.querySelector(`[id*="${tabId}"]`) ||
                         document.querySelector('.tab-content');
        
        if (targetTab) {
            targetTab.classList.remove('hidden');
            targetTab.style.display = 'block';
            console.log('✅ Tab shown:', tabId);
        } else {
            console.log('❌ Tab not found:', tabId);
            // إظهار أول تبويب كبديل
            if (allTabs.length > 0) {
                allTabs[0].classList.remove('hidden');
                allTabs[0].style.display = 'block';
                console.log('✅ Showing first tab as fallback');
            }
        }
    }
    
    // إصلاح القوائم المنسدلة للاختيارات
    function fixAllDropdownOptions() {
        console.log('🔧 Fixing all dropdown options...');
        
        const dropdowns = document.querySelectorAll('select');
        
        dropdowns.forEach(select => {
            // Fix boolean dropdowns
            if (select.name && (select.name.includes('enabled') || select.name.includes('debug'))) {
                const currentValue = select.value;
                select.innerHTML = '';
                
                const yesOption = document.createElement('option');
                yesOption.value = 'true';
                yesOption.textContent = 'نعم / Yes';
                select.appendChild(yesOption);
                
                const noOption = document.createElement('option');
                noOption.value = 'false';
                noOption.textContent = 'لا / No';
                select.appendChild(noOption);
                
                select.value = currentValue;
            }
        });
        
        console.log('✅ Dropdown options fixed');
    }
    
    // تشغيل الإصلاحات
    function runFixes() {
        console.log('🔧 Running all fixes...');
        
        setTimeout(() => {
            fixDropdowns();
            fixAllDropdownOptions();
            
            // إظهار أول تبويب
            const firstTab = document.querySelector('.tab-content');
            if (firstTab) {
                firstTab.classList.remove('hidden');
                firstTab.style.display = 'block';
            }
            
            console.log('✅ All fixes completed');
        }, 500);
    }
    
    // بدء الإصلاحات
    runFixes();
    
    // إعادة تشغيل عند تغيير DOM
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.addedNodes.length > 0) {
                runFixes();
            }
        });
    });
    
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
    
    // إضافة fixAllDropdownOptions كدالة عامة
    window.fixAllDropdownOptions = fixAllDropdownOptions;
});

console.log('🚀 Complete JavaScript fix loaded successfully');