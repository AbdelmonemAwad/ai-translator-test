# Cleanup Commands - أوامر التنظيف الشامل

## 🗑️ Quick Cleanup - تنظيف سريع

```bash
# Copy and paste this single command:
sudo systemctl stop ai-translator nginx 2>/dev/null; sudo pkill -f python 2>/dev/null; sudo rm -rf /opt/ai-translator ~/ai-translator* ./ai-translator*; sudo rm -f /etc/systemd/system/ai-translator* /etc/nginx/sites-*/ai-translator; sudo -u postgres dropdb ai_translator 2>/dev/null; sudo deluser ai-translator 2>/dev/null; rm -f *.zip *.tar.gz *.log *.db install*.sh; echo "✅ Quick cleanup done!"
```

## 🔥 Complete System Reset - إعادة تعيين شاملة

```bash
# Step 1: Download cleanup script
cat > cleanup.sh << 'EOF'
#!/bin/bash
echo "🗑️ Complete AI Translator Cleanup"
sudo systemctl stop ai-translator nginx postgresql 2>/dev/null
sudo pkill -f python 2>/dev/null
sudo rm -rf /opt/ai-translator ~/ai-translator* ./ai-translator* ~/.cache/pip
sudo apt remove --purge -y postgresql* 2>/dev/null
sudo rm -rf /var/lib/postgresql /etc/postgresql
pip3 freeze | xargs pip3 uninstall -y 2>/dev/null
sudo deluser ai-translator postgres 2>/dev/null
sudo rm -f /etc/systemd/system/ai-translator* /etc/nginx/sites-*/ai-translator
sudo systemctl daemon-reload
rm -f *.zip *.tar.gz *.log *.db install*.sh
sudo apt autoremove -y
echo "✅ Complete cleanup finished!"
EOF

# Step 2: Run cleanup
chmod +x cleanup.sh
./cleanup.sh
```

## 🚀 Fresh Installation - تثبيت جديد

### Method 1: Direct Download from GitHub
```bash
# Download source code
cd /tmp
wget https://github.com/AbdelmonemAwad/ai-translator/archive/refs/heads/main.zip
unzip main.zip
cd ai-translator-main

# Install
sudo apt update
sudo apt install -y python3 python3-pip postgresql
chmod +x install_fixed.sh
sudo ./install_fixed.sh
```

### Method 2: Manual Installation
```bash
# 1. Install Python and dependencies
sudo apt update
sudo apt install -y python3 python3-pip python3-venv python3-dev
sudo apt install -y postgresql postgresql-contrib nginx ffmpeg

# 2. Install Python packages
python3 -m pip install flask flask-sqlalchemy gunicorn psutil psycopg2-binary

# 3. Setup PostgreSQL
sudo systemctl start postgresql
sudo -u postgres createdb ai_translator
sudo -u postgres createuser ai_translator
sudo -u postgres psql -c "ALTER USER ai_translator WITH PASSWORD 'ai_pass123';"

# 4. Download and extract AI Translator
cd /opt
sudo wget https://github.com/AbdelmonemAwad/ai-translator/archive/refs/heads/main.zip
sudo unzip main.zip
sudo mv ai-translator-main ai-translator
sudo chown -R www-data:www-data ai-translator

# 5. Create service
sudo tee /etc/systemd/system/ai-translator.service << EOF
[Unit]
Description=AI Translator
After=network.target postgresql.service

[Service]
Type=exec
User=www-data
WorkingDirectory=/opt/ai-translator
ExecStart=/usr/bin/python3 -m gunicorn --bind 0.0.0.0:5000 app:app
Environment=DATABASE_URL=postgresql://ai_translator:ai_pass123@localhost/ai_translator

[Install]
WantedBy=multi-user.target
EOF

# 6. Start service
sudo systemctl daemon-reload
sudo systemctl enable ai-translator
sudo systemctl start ai-translator
```

## 🔍 Check Installation Status

```bash
# Check service status
sudo systemctl status ai-translator

# Check logs
sudo journalctl -u ai-translator -f

# Check if running
curl http://localhost:5000

# Get server IP
hostname -I
```

## ⚠️ Troubleshooting

### If Python not found:
```bash
sudo apt install -y python3 python3-pip
python3 --version
```

### If PostgreSQL issues:
```bash
sudo systemctl restart postgresql
sudo -u postgres psql -l
```

### If service won't start:
```bash
sudo journalctl -u ai-translator --no-pager
cd /opt/ai-translator && python3 app.py
```

### If port 5000 blocked:
```bash
sudo ufw allow 5000
sudo netstat -tlnp | grep 5000
```

## 🎯 One-Line Commands

### Quick Start (after cleanup):
```bash
cd /tmp && wget -q https://github.com/AbdelmonemAwad/ai-translator/archive/refs/heads/main.zip && unzip -q main.zip && cd ai-translator-main && sudo apt update && sudo apt install -y python3 python3-pip postgresql && python3 -m pip install flask flask-sqlalchemy gunicorn psutil psycopg2-binary && sudo systemctl start postgresql && sudo -u postgres createdb ai_translator && echo "✅ Ready to start!"
```

### Test Installation:
```bash
cd ai-translator-main && python3 -c "import flask, psycopg2; print('✅ Dependencies OK')" && python3 app.py &
```