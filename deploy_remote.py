#!/usr/bin/env python3
"""
AI Translator v2.2.4 Remote Deployment Script
Deploy to remote server: 5.31.55.179
"""

import os
import sys
import time
import subprocess
import tarfile
from datetime import datetime

# Server configuration
SERVER = "5.31.55.179"
USER = "eg2"
PASSWORD = "1q1"

def run_ssh_command(command, use_sudo=False):
    """Execute command on remote server via SSH"""
    if use_sudo:
        command = f"echo '{PASSWORD}' | sudo -S {command}"
    
    ssh_cmd = [
        "ssh", 
        "-o", "StrictHostKeyChecking=no",
        "-o", "UserKnownHostsFile=/dev/null",
        f"{USER}@{SERVER}",
        command
    ]
    
    try:
        # Create expect script for password
        expect_script = f"""#!/usr/bin/expect -f
set timeout 30
spawn {' '.join(ssh_cmd)}
expect {{
    "*password*" {{
        send "{PASSWORD}\\r"
        exp_continue
    }}
    eof
}}
"""
        
        # Write expect script to temp file
        with open("/tmp/ssh_cmd.exp", "w") as f:
            f.write(expect_script)
        
        os.chmod("/tmp/ssh_cmd.exp", 0o755)
        
        # Execute via expect
        result = subprocess.run(["/tmp/ssh_cmd.exp"], 
                              capture_output=True, text=True, timeout=60)
        
        return result.returncode == 0, result.stdout + result.stderr
        
    except Exception as e:
        print(f"Error executing SSH command: {e}")
        return False, str(e)

def upload_file(local_path, remote_path):
    """Upload file to remote server via SCP"""
    expect_script = f"""#!/usr/bin/expect -f
set timeout 60
spawn scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null {local_path} {USER}@{SERVER}:{remote_path}
expect {{
    "*password*" {{
        send "{PASSWORD}\\r"
        expect eof
    }}
    eof
}}
"""
    
    try:
        with open("/tmp/scp_upload.exp", "w") as f:
            f.write(expect_script)
        
        os.chmod("/tmp/scp_upload.exp", 0o755)
        
        result = subprocess.run(["/tmp/scp_upload.exp"], 
                              capture_output=True, text=True, timeout=120)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"Error uploading file: {e}")
        return False

def create_deployment_package():
    """Create deployment package"""
    print("🔄 Creating deployment package...")
    
    # List of files to include
    files_to_include = []
    
    # Add Python files
    for file in os.listdir("."):
        if file.endswith(".py"):
            files_to_include.append(file)
    
    # Add directories
    for dir_name in ["templates", "static", "services", "docs"]:
        if os.path.exists(dir_name):
            files_to_include.append(dir_name)
    
    # Add other files
    for file in ["LICENSE", "README.md", ".replit"]:
        if os.path.exists(file):
            files_to_include.append(file)
    
    # Create tar archive
    archive_name = "ai-translator-v2.2.4.tar.gz"
    
    with tarfile.open(archive_name, "w:gz") as tar:
        for item in files_to_include:
            if os.path.exists(item):
                tar.add(item, arcname=item)
    
    print(f"✓ Package created: {archive_name}")
    return archive_name

def main():
    """Main deployment function"""
    print("=== AI Translator v2.2.4 Remote Deployment ===")
    print(f"Target: {USER}@{SERVER}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Check if expect is available
    if not os.path.exists("/usr/bin/expect"):
        print("Installing expect...")
        os.system("sudo apt update && sudo apt install -y expect")
    
    # Step 1: System cleanup
    print("🔄 Step 1: System cleanup...")
    
    cleanup_commands = [
        "systemctl stop ai-translator 2>/dev/null",
        "systemctl stop nginx 2>/dev/null", 
        "systemctl disable ai-translator 2>/dev/null",
        "rm -rf /root/ai-translator",
        "rm -rf /opt/ai-translator-venv",
        "rm -f /etc/systemd/system/ai-translator.service",
        "pkill -f 'gunicorn.*ai-translator' 2>/dev/null",
        "pkill -f 'python.*app.py' 2>/dev/null"
    ]
    
    for cmd in cleanup_commands:
        success, output = run_ssh_command(cmd, use_sudo=True)
        if "ai-translator" in cmd:
            print(f"  Cleaned: {cmd.split()[1] if len(cmd.split()) > 1 else cmd}")
    
    print("✓ System cleanup completed")
    
    # Step 2: Create and upload package
    print("🔄 Step 2: Creating and uploading package...")
    
    package_name = create_deployment_package()
    
    if upload_file(package_name, "/tmp/"):
        print("✓ Package uploaded successfully")
    else:
        print("✗ Failed to upload package")
        return False
    
    # Step 3: Installation
    print("🔄 Step 3: Installing AI Translator...")
    
    installation_script = """
# Create installation directory
mkdir -p /root/ai-translator
cd /root/ai-translator

# Extract package
tar -xzf /tmp/ai-translator-v2.2.4.tar.gz

# Update system
apt update
apt install -y python3 python3-pip python3-venv postgresql postgresql-contrib nginx

# Setup PostgreSQL
systemctl start postgresql
systemctl enable postgresql

# Create database user
sudo -u postgres createdb ai_translator 2>/dev/null || true
sudo -u postgres psql -c "CREATE USER ai_translator WITH PASSWORD 'ai_translator_pass2024';" 2>/dev/null || true
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE ai_translator TO ai_translator;" 2>/dev/null || true

# Create Python environment
python3 -m venv venv
./venv/bin/pip install --upgrade pip
./venv/bin/pip install flask flask-sqlalchemy gunicorn psycopg2-binary psutil requests pynvml werkzeug

# Initialize database
DATABASE_URL='postgresql://ai_translator:ai_translator_pass2024@localhost/ai_translator' ./venv/bin/python database_setup.py

# Create systemd service
cat > /etc/systemd/system/ai-translator.service << 'EOF'
[Unit]
Description=AI Translator v2.2.4
After=network.target postgresql.service

[Service]
Type=notify
User=root
WorkingDirectory=/root/ai-translator
Environment=DATABASE_URL=postgresql://ai_translator:ai_translator_pass2024@localhost/ai_translator
Environment=SESSION_SECRET=ai-translator-secret-$(date +%s)
ExecStart=/root/ai-translator/venv/bin/gunicorn --bind 0.0.0.0:5000 --workers 2 --timeout 300 main:app
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# Configure Nginx
cat > /etc/nginx/sites-available/ai-translator << 'EOF'
server {
    listen 80 default_server;
    server_name _;
    
    client_max_body_size 100M;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 300;
        proxy_connect_timeout 300;
        proxy_send_timeout 300;
    }
}
EOF

# Enable services
rm -f /etc/nginx/sites-enabled/default
ln -sf /etc/nginx/sites-available/ai-translator /etc/nginx/sites-enabled/
nginx -t

systemctl daemon-reload
systemctl enable ai-translator
systemctl start ai-translator
systemctl restart nginx

echo "AI Translator v2.2.4 installation completed!"
"""
    
    # Write installation script to remote server
    script_cmd = f"cat > /tmp/install.sh << 'SCRIPT_EOF'\n{installation_script}\nSCRIPT_EOF"
    
    success, output = run_ssh_command(script_cmd)
    if success:
        print("✓ Installation script uploaded")
    else:
        print("✗ Failed to upload installation script")
        return False
    
    # Execute installation
    success, output = run_ssh_command("bash /tmp/install.sh", use_sudo=True)
    if success:
        print("✓ Installation completed")
    else:
        print("✗ Installation failed")
        print(output)
        return False
    
    # Step 4: Verification
    print("🔄 Step 4: Verification...")
    
    time.sleep(10)  # Wait for services to start
    
    # Check service status
    success, output = run_ssh_command("systemctl status ai-translator --no-pager", use_sudo=True)
    if "active (running)" in output:
        print("✓ AI Translator service is running")
    else:
        print("⚠ AI Translator service status unclear")
    
    # Test HTTP connection
    success, output = run_ssh_command("curl -I http://localhost/ 2>/dev/null")
    if "200 OK" in output or "302" in output:
        print("✓ HTTP service responding")
    else:
        print("⚠ HTTP service not responding yet (may need more time)")
    
    # Cleanup
    if os.path.exists(package_name):
        os.remove(package_name)
    
    for temp_file in ["/tmp/ssh_cmd.exp", "/tmp/scp_upload.exp"]:
        if os.path.exists(temp_file):
            os.remove(temp_file)
    
    print()
    print("🎉 AI Translator v2.2.4 Deployment Completed!")
    print()
    print("📋 Access Information:")
    print(f"   🌐 URL: http://{SERVER}")
    print("   👤 Username: admin")
    print("   🔑 Password: your_strong_password")
    print()
    print("📋 Management Commands (on server):")
    print("   sudo systemctl start ai-translator")
    print("   sudo systemctl stop ai-translator")
    print("   sudo systemctl status ai-translator")
    print("   sudo journalctl -u ai-translator -f")
    print()
    print("✅ Deployment Complete!")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⚠ Deployment interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Deployment failed: {e}")
        sys.exit(1)