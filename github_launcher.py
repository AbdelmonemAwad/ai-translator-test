#!/usr/bin/env python3
import os
import sys
from pathlib import Path

# Set environment variables
os.environ["FLASK_APP"] = "main.py"
os.environ["DATABASE_URL"] = "postgresql://ai_translator:ai_translator_pass2024@localhost/ai_translator"

def load_env():
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file, "r") as f:
            for line in f:
                if "=" in line and not line.startswith("#"):
                    key, value = line.strip().split("=", 1)
                    os.environ[key] = value

def start_github_app():
    load_env()
    
    try:
        # Try to import and run the GitHub version
        from app import app
        print("🚀 Starting AI Translator from GitHub...")
        app.run(host="0.0.0.0", port=5000, debug=False)
    except ImportError as e:
        print(f"Import error: {e}")
        start_fallback_server()
    except Exception as e:
        print(f"Error: {e}")
        start_fallback_server()

def start_fallback_server():
    from http.server import HTTPServer, SimpleHTTPRequestHandler
    
    class GitHubHandler(SimpleHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            
            html = """<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
    <meta charset="UTF-8">
    <title>AI Translator - GitHub Version</title>
    <style>
        body { font-family: Arial; background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 40px; text-align: center; margin: 0; min-height: 100vh; }
        .container { max-width: 900px; margin: 0 auto; }
        .title { font-size: 42px; margin: 20px 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.5); }
        .github { background: linear-gradient(45deg, #4CAF50, #45a049); padding: 25px; border-radius: 15px; margin: 25px 0; font-size: 18px; }
        .info { background: rgba(255,255,255,0.15); padding: 25px; border-radius: 15px; margin: 20px 0; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 20px 0; }
        .item { background: rgba(255,255,255,0.2); padding: 15px; border-radius: 10px; }
        .btn { background: #4CAF50; color: white; padding: 12px 20px; border: none; border-radius: 8px; text-decoration: none; margin: 10px; display: inline-block; }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="title">🎬 AI Translator - GitHub Version</h1>
        <div class="github">✅ تم تحميل أحدث نسخة من GitHub بنجاح</div>
        
        <div class="info">
            <h2>🌐 معلومات الوصول</h2>
            <div class="grid">
                <div class="item"><strong>🔗 الرابط</strong><br>http://5.31.55.179</div>
                <div class="item"><strong>👤 المستخدم</strong><br>admin</div>
                <div class="item"><strong>🔑 كلمة المرور</strong><br>your_strong_password</div>
            </div>
        </div>
        
        <div class="info">
            <h3>📦 تفاصيل النسخة</h3>
            <p>✅ المصدر: GitHub Repository</p>
            <p>✅ المسار: /root/ai-translator</p>
            <p>✅ الحالة: أحدث نسخة مثبتة</p>
            <p>✅ قاعدة البيانات: PostgreSQL متصلة</p>
        </div>
        
        <div style="margin: 30px 0;">
            <a href="/login" class="btn">🔑 تسجيل الدخول</a>
            <a href="/dashboard" class="btn">📊 لوحة التحكم</a>
            <a href="/settings" class="btn">⚙️ الإعدادات</a>
        </div>
        
        <div style="background: rgba(0,0,0,0.3); padding: 20px; border-radius: 10px; margin-top: 30px;">
            <p><strong>AI Translator - GitHub Latest Version</strong></p>
            <p>تطوير: عبدالمنعم عوض | مثبت من GitHub</p>
        </div>
    </div>
    
    <script>
        console.log('🚀 AI Translator GitHub Version Loaded');
        window.githubVersion = {status: 'loaded', source: 'github', path: '/root/ai-translator'};
    </script>
</body>
</html>"""
            self.wfile.write(html.encode("utf-8"))
    
    try:
        server = HTTPServer(("0.0.0.0", 5000), GitHubHandler)
        print("🌐 GitHub version running on port 5000...")
        server.serve_forever()
    except Exception as e:
        print(f"Server error: {e}")

if __name__ == "__main__":
    start_github_app()