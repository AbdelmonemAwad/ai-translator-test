#!/usr/bin/env python3

# Fix Settings Dropdowns - إصلاح القوائم الفرعية في الإعدادات
# This script fixes dropdown menu issues in the settings page

import os
import sqlite3
import psycopg2
import sys

def fix_postgresql_settings():
    """Fix dropdown settings in PostgreSQL database"""
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            host="localhost",
            database="ai_translator",
            user="ai_translator", 
            password="ai_translator_pass2024"
        )
        cursor = conn.cursor()
        
        print("Fixing PostgreSQL dropdown settings...")
        
        # Fix language settings
        cursor.execute("""
            INSERT INTO settings (section, key, value, description) 
            VALUES ('DEFAULT', 'language', 'ar', 'اللغة الافتراضية للواجهة')
            ON CONFLICT (section, key) DO UPDATE SET value = 'ar'
        """)
        
        # Fix theme settings  
        cursor.execute("""
            INSERT INTO settings (section, key, value, description)
            VALUES ('DEFAULT', 'theme', 'dark', 'المظهر الافتراضي للواجهة')
            ON CONFLICT (section, key) DO UPDATE SET value = 'dark'
        """)
        
        # Fix items per page
        cursor.execute("""
            INSERT INTO settings (section, key, value, description)
            VALUES ('DEFAULT', 'items_per_page', '24', 'عدد العناصر لكل صفحة')
            ON CONFLICT (section, key) DO UPDATE SET value = '24'
        """)
        
        # Fix Whisper model
        cursor.execute("""
            INSERT INTO settings (section, key, value, description)
            VALUES ('MODELS', 'whisper_model', 'medium.en', 'نموذج Whisper للتعرف على الكلام')
            ON CONFLICT (section, key) DO UPDATE SET value = 'medium.en'
        """)
        
        # Fix Ollama model
        cursor.execute("""
            INSERT INTO settings (section, key, value, description)
            VALUES ('MODELS', 'ollama_model', 'llama3', 'نموذج Ollama للترجمة')
            ON CONFLICT (section, key) DO UPDATE SET value = 'llama3'
        """)
        
        # Fix GPU settings
        cursor.execute("""
            INSERT INTO settings (section, key, value, description)
            VALUES ('MODELS', 'whisper_model_gpu', 'auto', 'GPU المخصص لـ Whisper')
            ON CONFLICT (section, key) DO UPDATE SET value = 'auto'
        """)
        
        cursor.execute("""
            INSERT INTO settings (section, key, value, description)
            VALUES ('MODELS', 'ollama_model_gpu', 'auto', 'GPU المخصص لـ Ollama')
            ON CONFLICT (section, key) DO UPDATE SET value = 'auto'
        """)
        
        # Fix development settings
        cursor.execute("""
            INSERT INTO settings (section, key, value, description)
            VALUES ('DEFAULT', 'debug_mode', 'false', 'وضع التطوير')
            ON CONFLICT (section, key) DO UPDATE SET value = 'false'
        """)
        
        cursor.execute("""
            INSERT INTO settings (section, key, value, description)
            VALUES ('DEFAULT', 'log_level', 'INFO', 'مستوى السجلات')
            ON CONFLICT (section, key) DO UPDATE SET value = 'INFO'
        """)
        
        cursor.execute("""
            INSERT INTO settings (section, key, value, description)
            VALUES ('DEFAULT', 'enable_testing_features', 'false', 'تفعيل ميزات الاختبار')
            ON CONFLICT (section, key) DO UPDATE SET value = 'false'
        """)
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("✓ Fixed PostgreSQL dropdown settings successfully")
        return True
        
    except Exception as e:
        print(f"✗ Error fixing PostgreSQL settings: {e}")
        return False

def create_settings_js_fix():
    """Create JavaScript fix for settings dropdowns"""
    
    js_fix = '''
// Settings Dropdown Fix - إصلاح القوائم المنسدلة
document.addEventListener('DOMContentLoaded', function() {
    
    // Fix dropdown options display
    function fixDropdownOptions() {
        const selectElements = document.querySelectorAll('select[data-options]');
        
        selectElements.forEach(select => {
            try {
                const optionsData = select.dataset.options;
                let options;
                
                // Parse options data
                try {
                    options = JSON.parse(optionsData);
                } catch(e) {
                    // If JSON parse fails, try to handle string format
                    if (optionsData.includes('|')) {
                        options = optionsData.split('|').map(opt => {
                            const [value, label] = opt.split(':');
                            return { value: value, label: label || value };
                        });
                    } else {
                        console.warn('Invalid options format for select:', select);
                        return;
                    }
                }
                
                // Clear existing options except the first one
                while (select.children.length > 1) {
                    select.removeChild(select.lastChild);
                }
                
                // Add new options
                options.forEach(option => {
                    const optElement = document.createElement('option');
                    optElement.value = option.value;
                    optElement.textContent = option.label;
                    
                    // Set selected if this is current value
                    if (option.value === select.dataset.currentValue) {
                        optElement.selected = true;
                    }
                    
                    select.appendChild(optElement);
                });
                
            } catch(error) {
                console.error('Error fixing dropdown:', error);
            }
        });
    }
    
    // Fix category switching
    function fixCategoryDropdown() {
        const categorySelect = document.getElementById('category');
        const subcategorySelect = document.getElementById('subcategory');
        
        if (!categorySelect || !subcategorySelect) return;
        
        categorySelect.addEventListener('change', function() {
            const selectedCategory = this.value;
            
            // Clear subcategory options
            subcategorySelect.innerHTML = '<option value="">اختر القسم الفرعي / Choose Subcategory</option>';
            
            // Define subcategories for each category
            const subcategories = {
                'general': [
                    { value: 'interface', label: 'الواجهة / Interface' },
                    { value: 'language', label: 'اللغة / Language' },
                    { value: 'display', label: 'العرض / Display' }
                ],
                'ai_services': [
                    { value: 'whisper', label: 'Whisper Settings' },
                    { value: 'ollama', label: 'Ollama Settings' },
                    { value: 'gpu', label: 'GPU Management' }
                ],
                'media_servers': [
                    { value: 'plex', label: 'Plex Media Server' },
                    { value: 'jellyfin', label: 'Jellyfin' },
                    { value: 'emby', label: 'Emby' },
                    { value: 'radarr', label: 'Radarr' },
                    { value: 'sonarr', label: 'Sonarr' }
                ],
                'system': [
                    { value: 'paths', label: 'المسارات / Paths' },
                    { value: 'database', label: 'قاعدة البيانات / Database' },
                    { value: 'development', label: 'أدوات التطوير / Development Tools' }
                ]
            };
            
            // Add subcategory options
            if (subcategories[selectedCategory]) {
                subcategories[selectedCategory].forEach(sub => {
                    const option = document.createElement('option');
                    option.value = sub.value;
                    option.textContent = sub.label;
                    subcategorySelect.appendChild(option);
                });
            }
        });
    }
    
    // Initialize fixes
    fixDropdownOptions();
    fixCategoryDropdown();
    
    // Re-apply fixes when content changes
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'childList') {
                fixDropdownOptions();
            }
        });
    });
    
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
});
'''
    
    # Write to static/js directory
    js_dir = '/root/ai-translator/static/js'
    os.makedirs(js_dir, exist_ok=True)
    
    with open(f'{js_dir}/settings-fix.js', 'w', encoding='utf-8') as f:
        f.write(js_fix)
    
    print("✓ Created JavaScript fix for settings dropdowns")

def update_settings_template():
    """Update settings template to include the fix"""
    
    template_path = '/root/ai-translator/templates/settings.html'
    
    # Check if template exists
    if not os.path.exists(template_path):
        print("✗ Settings template not found")
        return False
    
    try:
        # Read template
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add JavaScript fix if not already present
        if 'settings-fix.js' not in content:
            # Find where to insert the script tag
            if '</body>' in content:
                script_tag = '<script src="{{ url_for(\'static\', filename=\'js/settings-fix.js\') }}"></script>\n</body>'
                content = content.replace('</body>', script_tag)
            elif '{% endblock %}' in content:
                script_tag = '<script src="{{ url_for(\'static\', filename=\'js/settings-fix.js\') }}"></script>\n{% endblock %}'
                content = content.replace('{% endblock %}', script_tag)
            
            # Write updated template
            with open(template_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✓ Updated settings template with JavaScript fix")
        else:
            print("✓ Settings template already includes the fix")
            
        return True
        
    except Exception as e:
        print(f"✗ Error updating settings template: {e}")
        return False

def main():
    print("🔧 إصلاح القوائم الفرعية في الإعدادات...")
    print("🔧 Fixing Settings Dropdown Menus...")
    print("=" * 50)
    
    # Fix database settings
    if fix_postgresql_settings():
        print("✓ Database settings fixed")
    else:
        print("✗ Failed to fix database settings")
    
    # Create JavaScript fix
    create_settings_js_fix()
    
    # Update template
    if update_settings_template():
        print("✓ Template updated")
    else:
        print("✗ Failed to update template")
    
    print("=" * 50)
    print("✅ تم إصلاح القوائم الفرعية!")
    print("✅ Settings dropdowns have been fixed!")
    print("")
    print("يرجى إعادة تشغيل التطبيق:")
    print("systemctl restart ai-translator")

if __name__ == "__main__":
    main()