#!/usr/bin/env python3
"""
AI Translator - Stable Version v2.2.4
المترجم الآلي - النسخة المستقرة
"""

import os
import sys
import json
import logging
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify

# Flask app setup
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "ai_translator_secret_2024")

# PostgreSQL Database Setup
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Import database models
try:
    from models import db, Settings, MediaFile, Log
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        
        # Initialize basic settings if not exist
        if not Settings.query.filter_by(key='admin_username').first():
            basic_settings = [
                Settings(key='admin_username', value='admin', section='DEFAULT'),
                Settings(key='admin_password', value='your_strong_password', section='DEFAULT'),
                Settings(key='items_per_page', value='24', section='DEFAULT', type='select', 
                        options='12:12,24:24,48:48,96:96'),
                Settings(key='default_language', value='ar', section='LANGUAGE', type='select',
                        options='ar:العربية,en:English'),
                Settings(key='user_theme', value='dark', section='UI', type='select',
                        options='dark:داكن,light:فاتح,system:النظام'),
                Settings(key='debug_mode', value='false', section='DEVELOPMENT', type='select',
                        options='true:نعم,false:لا'),
                Settings(key='whisper_model', value='medium.en', section='MODELS'),
                Settings(key='ollama_model', value='llama3', section='MODELS'),
                Settings(key='ollama_url', value='http://localhost:11434', section='API'),
            ]
            
            for setting in basic_settings:
                db.session.add(setting)
            
            db.session.commit()
            print("✓ Basic settings initialized")
            
except Exception as e:
    print(f"Database setup error: {e}")

# Authentication helper
def is_authenticated():
    return session.get('authenticated', False)

def get_settings():
    """Get all settings as dictionary"""
    try:
        settings = {}
        for setting in Settings.query.all():
            settings[setting.key] = setting.value
        return settings
    except:
        return {}

def get_setting(key, default=None):
    """Get specific setting"""
    try:
        setting = Settings.query.filter_by(key=key).first()
        return setting.value if setting else default
    except:
        return default

def update_setting(key, value):
    """Update or create setting"""
    try:
        setting = Settings.query.filter_by(key=key).first()
        if setting:
            setting.value = value
        else:
            setting = Settings(key=key, value=value)
            db.session.add(setting)
        db.session.commit()
        return True
    except:
        return False

# Routes
@app.route('/')
def index():
    if not is_authenticated():
        return redirect(url_for('login'))
    return redirect(url_for('dashboard'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        
        admin_username = get_setting('admin_username', 'admin')
        admin_password = get_setting('admin_password', 'your_strong_password')
        
        if username == admin_username and password == admin_password:
            session['authenticated'] = True
            session['username'] = username
            flash('تم تسجيل الدخول بنجاح')
            return redirect(url_for('dashboard'))
        else:
            flash('اسم المستخدم أو كلمة المرور غير صحيحة')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('تم تسجيل الخروج بنجاح')
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if not is_authenticated():
        return redirect(url_for('login'))
    
    try:
        # Get basic statistics
        total_files = MediaFile.query.count()
        translated_files = MediaFile.query.filter_by(translated=True).count()
        pending_files = total_files - translated_files
        
        stats = {
            'total_files': total_files,
            'translated_files': translated_files,
            'pending_files': pending_files
        }
    except:
        stats = {
            'total_files': 0,
            'translated_files': 0,
            'pending_files': 0
        }
    
    return render_template('dashboard.html', stats=stats)

@app.route('/settings', methods=['GET', 'POST'])
def settings_page():
    if not is_authenticated():
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # Update settings
        for key, value in request.form.items():
            if not key.startswith('_'):  # Skip Flask form fields
                update_setting(key, value)
        
        flash('تم حفظ الإعدادات بنجاح')
        return redirect(url_for('settings_page'))
    
    # Get settings grouped by section
    settings_by_section = {}
    try:
        for setting in Settings.query.order_by(Settings.section, Settings.key).all():
            if setting.section not in settings_by_section:
                settings_by_section[setting.section] = []
            
            # Process options for select fields
            if setting.type == 'select' and setting.options:
                setting.option_list = []
                for option_pair in setting.options.split(','):
                    if ':' in option_pair:
                        value, label = option_pair.split(':', 1)
                        setting.option_list.append({
                            'value': value.strip(),
                            'label': label.strip()
                        })
                    else:
                        setting.option_list.append({
                            'value': option_pair.strip(),
                            'label': option_pair.strip()
                        })
            
            settings_by_section[setting.section].append(setting)
    except Exception as e:
        print(f"Settings error: {e}")
        settings_by_section = {}
    
    return render_template('settings.html', settings_by_section=settings_by_section)

@app.route('/file-management')
def file_management():
    if not is_authenticated():
        return redirect(url_for('login'))
    
    try:
        files = MediaFile.query.limit(50).all()
    except:
        files = []
    
    return render_template('file_management.html', files=files)

@app.route('/system-monitor')
def system_monitor():
    if not is_authenticated():
        return redirect(url_for('login'))
    
    return render_template('system_monitor.html')

@app.route('/logs')
def logs_page():
    if not is_authenticated():
        return redirect(url_for('login'))
    
    try:
        logs = Log.query.order_by(Log.created_at.desc()).limit(100).all()
    except:
        logs = []
    
    return render_template('logs.html', logs=logs)

# API Routes
@app.route('/api/status')
def api_status():
    if not is_authenticated():
        return jsonify({'error': 'Unauthorized'}), 401
    
    return jsonify({
        'status': 'running',
        'version': '2.2.4',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/system-stats')
def api_system_stats():
    if not is_authenticated():
        return jsonify({'error': 'Unauthorized'}), 401
    
    import psutil
    
    try:
        stats = {
            'cpu_percent': psutil.cpu_percent(),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_percent': psutil.disk_usage('/').percent,
            'timestamp': datetime.now().isoformat()
        }
    except:
        stats = {
            'cpu_percent': 0,
            'memory_percent': 0,
            'disk_percent': 0,
            'timestamp': datetime.now().isoformat()
        }
    
    return jsonify(stats)

if __name__ == '__main__':
    print("✓ AI Translator Stable Version Starting...")
    app.run(host='0.0.0.0', port=5000, debug=True)