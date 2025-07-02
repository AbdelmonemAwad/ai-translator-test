#!/usr/bin/env python3
"""
AI Translator - Simplified Ubuntu Server Version
"""
import os
from flask import Flask, render_template_string, request, redirect, url_for, session, flash, jsonify
import datetime

# Create Flask app
app = Flask(__name__)
app.secret_key = "ai_translator_secret_2024"

# Templates
LOGIN_TEMPLATE = '''
<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>تسجيل الدخول - المترجم الآلي</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .login-container {
            background: white;
            padding: 40px;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            width: 400px;
            text-align: center;
        }
        h1 { color: #333; margin-bottom: 30px; font-size: 2em; }
        .form-group { margin-bottom: 20px; text-align: right; }
        label { 
            display: block; 
            margin-bottom: 5px; 
            color: #333; 
            font-weight: bold; 
        }
        input[type="text"], input[type="password"] {
            width: 100%;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        input:focus {
            border-color: #667eea;
            outline: none;
        }
        .login-btn {
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            padding: 12px 30px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            width: 100%;
            margin-top: 20px;
            transition: transform 0.2s;
        }
        .login-btn:hover {
            transform: translateY(-2px);
        }
        .alert {
            padding: 10px;
            margin: 10px 0;
            border-radius: 5px;
        }
        .alert-error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        .alert-success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .default-creds {
            background: #e3f2fd;
            padding: 15px;
            border-radius: 8px;
            margin-top: 20px;
            font-size: 0.9em;
            color: #1565c0;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <h1>🤖 المترجم الآلي</h1>
        
        {% if error %}
            <div class="alert alert-error">{{ error }}</div>
        {% endif %}
        
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ 'error' if category == 'error' else 'success' }}">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        
        <form method="post">
            <div class="form-group">
                <label>اسم المستخدم:</label>
                <input type="text" name="username" required>
            </div>
            <div class="form-group">
                <label>كلمة المرور:</label>
                <input type="password" name="password" required>
            </div>
            <button type="submit" class="login-btn">تسجيل الدخول</button>
        </form>
        
        <div class="default-creds">
            <strong>بيانات الدخول الافتراضية:</strong><br>
            اسم المستخدم: admin<br>
            كلمة المرور: your_strong_password
        </div>
    </div>
</body>
</html>
'''

DASHBOARD_TEMPLATE = '''
<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>المترجم الآلي - لوحة التحكم</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .header {
            background: rgba(255,255,255,0.95);
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .header h1 {
            color: #333;
            font-size: 2em;
        }
        .nav-links {
            display: flex;
            gap: 20px;
        }
        .nav-links a {
            background: #667eea;
            color: white;
            padding: 10px 15px;
            border-radius: 5px;
            text-decoration: none;
            transition: background 0.3s;
        }
        .nav-links a:hover {
            background: #5a67d8;
        }
        .container {
            max-width: 1200px;
            margin: 40px auto;
            padding: 0 20px;
        }
        .dashboard-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 25px;
            margin-bottom: 30px;
        }
        .card {
            background: white;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s;
        }
        .card:hover {
            transform: translateY(-5px);
        }
        .card h3 {
            color: #333;
            margin-bottom: 15px;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }
        .stat-value {
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
            margin: 10px 0;
        }
        .status-active { color: #28a745; }
        .status-warning { color: #ffc107; }
        .status-error { color: #dc3545; }
        .action-buttons {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 30px 0;
        }
        .btn {
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            padding: 15px 20px;
            border: none;
            border-radius: 8px;
            text-decoration: none;
            text-align: center;
            font-weight: bold;
            transition: transform 0.2s;
        }
        .btn:hover {
            transform: translateY(-2px);
        }
        .system-info {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            margin-top: 15px;
        }
        .system-info p {
            margin: 5px 0;
            color: #495057;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🤖 المترجم الآلي v2.2.1</h1>
        <div class="nav-links">
            <a href="/dashboard">الرئيسية</a>
            <a href="/files">إدارة الملفات</a>
            <a href="/settings">الإعدادات</a>
            <a href="/logs">السجلات</a>
            <a href="/logout">خروج</a>
        </div>
    </div>
    
    <div class="container">
        <div class="dashboard-grid">
            <div class="card">
                <h3>📊 حالة النظام</h3>
                <div class="stat-value status-active">نشط ويعمل</div>
                <div class="system-info">
                    <p><strong>الخادم:</strong> {{ server_ip }}</p>
                    <p><strong>المنفذ:</strong> 5000</p>
                    <p><strong>الإصدار:</strong> v2.2.1</p>
                    <p><strong>النظام:</strong> Ubuntu Server 24.04</p>
                </div>
            </div>
            
            <div class="card">
                <h3>🎬 ملفات الوسائط</h3>
                <div class="stat-value">{{ stats.total_files }}</div>
                <div class="system-info">
                    <p>✅ المترجمة: {{ stats.translated_files }}</p>
                    <p>⏳ في الانتظار: {{ stats.pending_files }}</p>
                    <p>🚫 المحظورة: {{ stats.blacklisted_files }}</p>
                </div>
            </div>
            
            <div class="card">
                <h3>🤖 خدمات الذكاء الاصطناعي</h3>
                <div class="system-info">
                    <p>✅ Flask Web Server</p>
                    <p>{{ '✅' if stats.database_connected else '❌' }} PostgreSQL Database</p>
                    <p>✅ Nginx Reverse Proxy</p>
                    <p>🔧 Whisper (قيد الإعداد)</p>
                    <p>🔧 Ollama (قيد الإعداد)</p>
                </div>
            </div>
            
            <div class="card">
                <h3>⚡ إحصائيات النظام</h3>
                <div class="system-info">
                    <p><strong>وقت التشغيل:</strong> {{ stats.uptime }}</p>
                    <p><strong>آخر نشاط:</strong> {{ stats.last_activity }}</p>
                    <p><strong>حالة قاعدة البيانات:</strong> {{ stats.db_status }}</p>
                </div>
            </div>
        </div>
        
        <div class="action-buttons">
            <a href="/files" class="btn">📁 إدارة الملفات</a>
            <a href="/settings" class="btn">⚙️ الإعدادات</a>
            <a href="/monitor" class="btn">📊 مراقبة النظام</a>
            <a href="/logs" class="btn">📋 السجلات</a>
            <a href="/corrections" class="btn">🔧 التصحيحات</a>
            <a href="/blacklist" class="btn">🚫 القائمة السوداء</a>
        </div>
    </div>
</body>
</html>
'''

PLACEHOLDER_TEMPLATE = '''
<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
    <meta charset="UTF-8">
    <title>{{ title }} - المترجم الآلي</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            padding: 50px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .container {
            background: white;
            padding: 40px;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }
        h1 { color: #333; margin-bottom: 20px; }
        p { color: #666; margin-bottom: 20px; }
        .btn {
            background: #667eea;
            color: white;
            padding: 12px 24px;
            text-decoration: none;
            border-radius: 5px;
            display: inline-block;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚧 {{ title }}</h1>
        <p>{{ message }}</p>
        <a href="/dashboard" class="btn">العودة للرئيسية</a>
    </div>
</body>
</html>
'''

# Helper functions
def is_authenticated():
    return session.get('authenticated', False)

def get_server_ip():
    try:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "192.168.0.221"

def get_system_stats():
    return {
        'total_files': 0,
        'translated_files': 0,
        'pending_files': 0,
        'blacklisted_files': 0,
        'database_connected': False,  # Will be updated when DB is connected
        'uptime': 'جديد',
        'last_activity': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'db_status': 'قيد الإعداد'
    }

# Routes
@app.route('/')
def index():
    if not is_authenticated():
        return redirect(url_for('login'))
    return redirect(url_for('dashboard'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        if username == 'admin' and password == 'your_strong_password':
            session['authenticated'] = True
            session['username'] = username
            flash('تم تسجيل الدخول بنجاح', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('اسم المستخدم أو كلمة المرور غير صحيحة', 'error')
            return render_template_string(LOGIN_TEMPLATE, error='بيانات دخول خاطئة')
    
    return render_template_string(LOGIN_TEMPLATE)

@app.route('/logout')
def logout():
    session.clear()
    flash('تم تسجيل الخروج بنجاح', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if not is_authenticated():
        return redirect(url_for('login'))
    
    stats = get_system_stats()
    server_ip = get_server_ip()
    
    return render_template_string(DASHBOARD_TEMPLATE, stats=stats, server_ip=server_ip)

# Placeholder routes
placeholder_routes = [
    ('/files', 'إدارة الملفات', 'هذه الصفحة تتيح إدارة ملفات الوسائط وحالة الترجمة'),
    ('/settings', 'الإعدادات', 'هنا يمكن تكوين إعدادات النظام والخدمات'),
    ('/logs', 'السجلات', 'عرض سجلات النظام وعمليات الترجمة'),
    ('/monitor', 'مراقبة النظام', 'مراقبة أداء النظام والموارد'),
    ('/corrections', 'التصحيحات', 'أدوات تصحيح وإعادة تسمية ملفات الترجمة'),
    ('/blacklist', 'القائمة السوداء', 'إدارة الملفات المحظورة من الترجمة'),
]

for route, title, message in placeholder_routes:
    app.add_url_rule(
        route, 
        f'page_{route.replace("/", "")}',
        lambda title=title, message=message: (
            redirect(url_for('login')) if not is_authenticated() 
            else render_template_string(PLACEHOLDER_TEMPLATE, title=title, message=message)
        )
    )

# API Routes
@app.route('/api/status')
def api_status():
    return jsonify({
        'status': 'operational',
        'version': '2.2.1',
        'mode': 'standalone',
        'database': 'configuring',
        'server_ip': get_server_ip(),
        'timestamp': datetime.datetime.now().isoformat(),
        'authenticated': is_authenticated()
    })

@app.route('/api/system_stats')
def api_system_stats():
    if not is_authenticated():
        return jsonify({'error': 'Unauthorized'}), 401
    
    return jsonify(get_system_stats())

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template_string(PLACEHOLDER_TEMPLATE, 
                                title='صفحة غير موجودة', 
                                message='الصفحة المطلوبة غير موجودة'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template_string(PLACEHOLDER_TEMPLATE, 
                                title='خطأ في الخادم', 
                                message='حدث خطأ في الخادم، يرجى المحاولة مرة أخرى'), 500

if __name__ == '__main__':
    print("Starting AI Translator v2.2.1...")
    print(f"Server IP: {get_server_ip()}")
    print("Login: admin / your_strong_password")
    app.run(host='0.0.0.0', port=5000, debug=False)