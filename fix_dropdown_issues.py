#!/usr/bin/env python3
"""
AI Translator v2.2.2 - Dropdown Issues Fix
إصلاح جميع مشاكل القوائم المنسدلة والخيارات في التطبيق
"""

import os
import sys
import psycopg2
import json
from datetime import datetime

def fix_postgresql_settings():
    """Fix all dropdown settings in PostgreSQL database"""
    try:
        # Get database connection from environment
        database_url = os.environ.get("DATABASE_URL")
        if not database_url:
            print("❌ DATABASE_URL not found in environment")
            return False
            
        print("🔧 Connecting to PostgreSQL database...")
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        # Check if settings table exists
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'settings'
            );
        """)
        
        result = cursor.fetchone()
        if not result or not result[0]:
            print("❌ Settings table does not exist")
            return False
            
        print("📋 Fixing all dropdown settings with proper options...")
        
        # Define all settings with proper multilingual options
        settings_fixes = [
            # Language Settings
            {
                'key': 'default_language',
                'value': 'ar',
                'section': 'DEFAULT',
                'type': 'select',
                'description': '{"ar": "اللغة الافتراضية للواجهة", "en": "Default interface language"}',
                'options': '{"ar": "ar:العربية,en:English", "en": "ar:Arabic,en:English"}'
            },
            
            # Theme Settings
            {
                'key': 'default_theme',
                'value': 'dark',
                'section': 'DEFAULT',
                'type': 'select',
                'description': '{"ar": "المظهر الافتراضي للتطبيق", "en": "Default application theme"}',
                'options': '{"ar": "dark:داكن,light:فاتح,system:تلقائي", "en": "dark:Dark,light:Light,system:System"}'
            },
            
            # Items per page
            {
                'key': 'items_per_page',
                'value': '24',
                'section': 'DEFAULT',
                'type': 'select',
                'description': '{"ar": "عدد العناصر في كل صفحة", "en": "Number of items per page"}',
                'options': '{"ar": "12:12 عنصر,24:24 عنصر,48:48 عنصر,96:96 عنصر", "en": "12:12 items,24:24 items,48:48 items,96:96 items"}'
            },
            
            # Whisper Model
            {
                'key': 'whisper_model',
                'value': 'medium.en',
                'section': 'MODELS',
                'type': 'select',
                'description': '{"ar": "نموذج Whisper للتعرف على الكلام", "en": "Whisper model for speech recognition"}',
                'options': '{"ar": "tiny.en:صغير جداً,base.en:أساسي,small.en:صغير,medium.en:متوسط,large:كبير", "en": "tiny.en:Tiny,base.en:Base,small.en:Small,medium.en:Medium,large:Large"}'
            },
            
            # Ollama Model
            {
                'key': 'ollama_model',
                'value': 'llama3',
                'section': 'MODELS',
                'type': 'select',
                'description': '{"ar": "نموذج Ollama للترجمة", "en": "Ollama model for translation"}',
                'options': '{"ar": "llama3:Llama 3,llama3.1:Llama 3.1,mistral:Mistral,codellama:Code Llama", "en": "llama3:Llama 3,llama3.1:Llama 3.1,mistral:Mistral,codellama:Code Llama"}'
            },
            
            # GPU Settings
            {
                'key': 'whisper_model_gpu',
                'value': 'auto',
                'section': 'GPU',
                'type': 'select',
                'description': '{"ar": "GPU المخصص لنموذج Whisper", "en": "GPU allocation for Whisper model"}',
                'options': '{"ar": "auto:تلقائي,0:GPU 0,1:GPU 1,cpu:معالج فقط", "en": "auto:Auto,0:GPU 0,1:GPU 1,cpu:CPU Only"}'
            },
            
            {
                'key': 'ollama_model_gpu',
                'value': 'auto',
                'section': 'GPU',
                'type': 'select',
                'description': '{"ar": "GPU المخصص لنموذج Ollama", "en": "GPU allocation for Ollama model"}',
                'options': '{"ar": "auto:تلقائي,0:GPU 0,1:GPU 1,cpu:معالج فقط", "en": "auto:Auto,0:GPU 0,1:GPU 1,cpu:CPU Only"}'
            },
            
            # Development Settings
            {
                'key': 'debug_mode',
                'value': 'false',
                'section': 'DEVELOPMENT',
                'type': 'select',
                'description': '{"ar": "وضع التطوير والتشخيص", "en": "Development and debugging mode"}',
                'options': '{"ar": "true:مفعل,false:معطل", "en": "true:Enabled,false:Disabled"}'
            },
            
            {
                'key': 'log_level',
                'value': 'INFO',
                'section': 'DEVELOPMENT',
                'type': 'select',
                'description': '{"ar": "مستوى السجلات", "en": "Logging level"}',
                'options': '{"ar": "DEBUG:تشخيص,INFO:معلومات,WARNING:تحذير,ERROR:خطأ", "en": "DEBUG:Debug,INFO:Info,WARNING:Warning,ERROR:Error"}'
            },
            
            {
                'key': 'enable_testing_features',
                'value': 'false',
                'section': 'DEVELOPMENT',
                'type': 'select',
                'description': '{"ar": "تفعيل ميزات الاختبار", "en": "Enable testing features"}',
                'options': '{"ar": "true:مفعل,false:معطل", "en": "true:Enabled,false:Disabled"}'
            },
            
            # Server Settings
            {
                'key': 'server_host',
                'value': '0.0.0.0',
                'section': 'SERVER',
                'type': 'text',
                'description': '{"ar": "عنوان IP للخادم", "en": "Server IP address"}',
                'options': None
            },
            
            {
                'key': 'server_port',
                'value': '5000',
                'section': 'SERVER',
                'type': 'number',
                'description': '{"ar": "منفذ الخادم", "en": "Server port"}',
                'options': None
            }
        ]
        
        # Apply all settings fixes
        for setting in settings_fixes:
            cursor.execute("""
                INSERT INTO settings (key, value, section, type, description, options, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (key) DO UPDATE SET
                    value = EXCLUDED.value,
                    section = EXCLUDED.section,
                    type = EXCLUDED.type,
                    description = EXCLUDED.description,
                    options = EXCLUDED.options,
                    updated_at = EXCLUDED.updated_at
            """, (
                setting['key'],
                setting['value'],
                setting['section'],
                setting['type'],
                setting['description'],
                setting['options'],
                datetime.utcnow(),
                datetime.utcnow()
            ))
            print(f"✅ Fixed setting: {setting['key']}")
        
        # Commit changes
        conn.commit()
        print(f"✅ Successfully fixed {len(settings_fixes)} dropdown settings")
        
        # Test a few settings
        cursor.execute("SELECT key, value, options FROM settings WHERE type = 'select' LIMIT 5")
        test_settings = cursor.fetchall()
        
        print("\n📝 Testing fixed settings:")
        for key, value, options in test_settings:
            print(f"  {key}: {value} (options: {options[:50]}...)")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error fixing settings: {str(e)}")
        return False

def main():
    print("🔧 AI Translator v2.2.2 - Dropdown Issues Fix")
    print("=" * 50)
    
    if fix_postgresql_settings():
        print("\n✅ All dropdown issues have been fixed!")
        print("🌐 Restart the application to see the changes:")
        print("   sudo systemctl restart ai-translator")
    else:
        print("\n❌ Failed to fix dropdown issues")
        print("🔍 Check the error messages above for details")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())