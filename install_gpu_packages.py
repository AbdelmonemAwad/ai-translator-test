#!/usr/bin/env python3
"""
GPU Packages Installation Script for AI Translator
سكريبت تثبيت حزم كروت الشاشة للمترجم الآلي
"""

import os
import subprocess
import logging
import sys
import time

def run_command(command, timeout=300):
    """Run command safely with timeout"""
    try:
        result = subprocess.run(
            command if isinstance(command, list) else command.split(),
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"
    except Exception as e:
        return False, "", str(e)

def update_package_lists():
    """Update package lists"""
    print("📦 Updating package lists...")
    success, stdout, stderr = run_command("apt-get update", timeout=180)
    
    if success:
        print("✅ Package lists updated successfully")
        return True
    else:
        print(f"❌ Failed to update package lists: {stderr}")
        return False

def install_system_packages():
    """Install system packages for GPU detection"""
    packages = [
        # Basic GPU utilities
        'lshw',
        'pciutils',
        'mesa-utils',
        'glxinfo',
        
        # NVIDIA packages
        'nvidia-detect',
        'nvidia-smi',
        'nvidia-utils-535',
        'nvidia-utils-525',
        'nvidia-utils-515',
        
        # AMD packages
        'mesa-vdpau-drivers',
        'mesa-va-drivers',
        
        # Intel packages
        'intel-gpu-tools',
        'vainfo',
        
        # Python development packages
        'python3-dev',
        'python3-pip',
        'build-essential'
    ]
    
    print("🔧 Installing system packages...")
    
    for package in packages:
        print(f"📥 Installing {package}...")
        success, stdout, stderr = run_command(f"apt-get install -y {package}", timeout=120)
        
        if success:
            print(f"✅ {package} installed successfully")
        else:
            print(f"⚠️ Could not install {package}: {stderr[:100]}")
    
    return True

def install_python_packages():
    """Install Python packages for GPU management"""
    packages = [
        'pynvml',
        'gpustat',
        'psutil',
        'nvidia-ml-py3'
    ]
    
    print("🐍 Installing Python packages...")
    
    for package in packages:
        print(f"📦 Installing {package}...")
        success, stdout, stderr = run_command(f"pip3 install {package}", timeout=120)
        
        if success:
            print(f"✅ {package} installed successfully")
        else:
            print(f"⚠️ Could not install {package}: {stderr[:100]}")
    
    return True

def detect_gpus():
    """Detect available GPUs"""
    print("🔍 Detecting GPUs...")
    
    # Check lspci for GPUs
    success, stdout, stderr = run_command("lspci | grep -i vga")
    if success and stdout:
        print("🎮 Detected graphics cards:")
        for line in stdout.split('\n'):
            if line.strip():
                print(f"  • {line}")
    
    # Check for NVIDIA GPUs
    success, stdout, stderr = run_command("nvidia-smi")
    if success:
        print("🟢 NVIDIA GPU detected and nvidia-smi working")
        if stdout:
            print("NVIDIA GPU Details:")
            for line in stdout.split('\n')[:10]:  # First 10 lines
                if line.strip():
                    print(f"  {line}")
    else:
        print("❌ NVIDIA GPU not detected or nvidia-smi not working")
    
    # Check for AMD GPUs
    success, stdout, stderr = run_command("lspci | grep -i amd")
    if success and stdout:
        print("🔴 AMD GPU detected:")
        for line in stdout.split('\n'):
            if line.strip():
                print(f"  • {line}")
    else:
        print("❌ AMD GPU not detected")
    
    # Check for Intel GPUs
    success, stdout, stderr = run_command("lspci | grep -i intel.*graphics")
    if success and stdout:
        print("🔵 Intel GPU detected:")
        for line in stdout.split('\n'):
            if line.strip():
                print(f"  • {line}")
    else:
        print("❌ Intel GPU not detected")

def setup_nvidia_environment():
    """Setup NVIDIA environment variables"""
    print("⚙️ Setting up NVIDIA environment...")
    
    # Create NVIDIA environment script
    env_script = """#!/bin/bash
# NVIDIA Environment Setup for AI Translator

# Set CUDA paths if NVIDIA is available
if command -v nvidia-smi &> /dev/null; then
    export CUDA_VISIBLE_DEVICES="0,1,2,3"
    export NVIDIA_VISIBLE_DEVICES="0,1,2,3"
    export CUDA_DEVICE_ORDER="PCI_BUS_ID"
    
    # Add CUDA to PATH if available
    if [ -d "/usr/local/cuda/bin" ]; then
        export PATH="/usr/local/cuda/bin:$PATH"
        export LD_LIBRARY_PATH="/usr/local/cuda/lib64:$LD_LIBRARY_PATH"
    fi
    
    echo "✅ NVIDIA environment configured"
else
    echo "❌ NVIDIA not available"
fi
"""
    
    try:
        with open('/etc/environment.d/nvidia.conf', 'w') as f:
            f.write(env_script)
        
        os.chmod('/etc/environment.d/nvidia.conf', 0o755)
        print("✅ NVIDIA environment script created")
        return True
    except Exception as e:
        print(f"⚠️ Could not create NVIDIA environment script: {e}")
        return False

def test_gpu_detection():
    """Test GPU detection with Python"""
    print("🧪 Testing GPU detection with Python...")
    
    test_script = '''
import sys

# Test pynvml
try:
    import pynvml
    pynvml.nvmlInit()
    device_count = pynvml.nvmlDeviceGetCount()
    print(f"NVIDIA GPUs detected via pynvml: {device_count}")
    
    for i in range(device_count):
        handle = pynvml.nvmlDeviceGetHandleByIndex(i)
        name = pynvml.nvmlDeviceGetName(handle).decode('utf-8')
        print(f"  GPU {i}: {name}")
        
except Exception as e:
    print(f"pynvml test failed: {e}")

# Test psutil
try:
    import psutil
    print(f"CPU count: {psutil.cpu_count()}")
    print(f"Memory: {psutil.virtual_memory().total // (1024**3)} GB")
except Exception as e:
    print(f"psutil test failed: {e}")

print("GPU detection test completed")
'''
    
    try:
        # Write test script
        with open('/tmp/gpu_test.py', 'w') as f:
            f.write(test_script)
        
        # Run test script
        success, stdout, stderr = run_command("python3 /tmp/gpu_test.py")
        
        if success:
            print("✅ GPU detection test results:")
            print(stdout)
        else:
            print(f"❌ GPU detection test failed: {stderr}")
        
        # Cleanup
        os.remove('/tmp/gpu_test.py')
        
    except Exception as e:
        print(f"⚠️ Could not run GPU detection test: {e}")

def main():
    """Main installation process"""
    print("🚀 AI Translator GPU Packages Installation")
    print("=" * 50)
    
    # Check if running as root
    if os.geteuid() != 0:
        print("❌ This script must be run as root (use sudo)")
        sys.exit(1)
    
    try:
        # Step 1: Update package lists
        if not update_package_lists():
            print("❌ Failed to update package lists. Continuing anyway...")
        
        # Step 2: Install system packages
        install_system_packages()
        
        # Step 3: Install Python packages
        install_python_packages()
        
        # Step 4: Setup NVIDIA environment
        setup_nvidia_environment()
        
        # Step 5: Detect GPUs
        detect_gpus()
        
        # Step 6: Test GPU detection
        test_gpu_detection()
        
        print("\n" + "=" * 50)
        print("✅ GPU packages installation completed!")
        print("🔄 You may need to restart the AI Translator service:")
        print("   sudo systemctl restart ai-translator")
        print("\n💡 To test GPU detection in AI Translator:")
        print("   1. Go to Settings > AI Services")
        print("   2. Click 'Refresh GPU Detection'")
        print("   3. Check GPU options in dropdown menus")
        
    except KeyboardInterrupt:
        print("\n❌ Installation interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Installation failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()