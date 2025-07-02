// GPU Management Functions for AI Translator
console.log('GPU Management JS loaded');

// Global GPU management functions
function refreshGPUOptions() {
    console.log('Refreshing GPU options...');
    showNotification('جاري تحديث خيارات كروت الشاشة...', 'info');
    
    fetch('/api/gpu/refresh')
    .then(response => response.json())
    .then(data => {
        console.log('GPU refresh response:', data);
        if (data.success) {
            showNotification('تم تحديث خيارات كروت الشاشة بنجاح', 'success');
            setTimeout(() => window.location.reload(), 1000);
        } else {
            showNotification('فشل في تحديث خيارات كروت الشاشة', 'error');
        }
    })
    .catch(error => {
        console.error('Error refreshing GPU options:', error);
        showNotification('خطأ في تحديث خيارات كروت الشاشة', 'error');
    });
}

function smartGPUAllocation() {
    console.log('Running smart GPU allocation...');
    showNotification('جاري تطبيق التوزيع الذكي لكروت الشاشة...', 'info');
    
    fetch('/api/gpu/smart-allocation', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log('Smart allocation response:', data);
        if (data.success) {
            showNotification('تم تطبيق التوزيع الذكي بنجاح', 'success');
            
            // Show allocation details
            let allocationText = '=== التوزيع الذكي المطبق ===\n\n';
            allocationText += `Whisper: ${data.allocation.whisper}\n`;
            allocationText += `Ollama: ${data.allocation.ollama}\n`;
            allocationText += `الاستراتيجية: ${data.allocation.strategy}\n\n`;
            allocationText += 'سيتم تحديث الصفحة لعرض الإعدادات الجديدة...';
            
            alert(allocationText);
            
            // Refresh the page to show new settings
            setTimeout(() => window.location.reload(), 2000);
        } else {
            showNotification('فشل في تطبيق التوزيع الذكي', 'error');
        }
    })
    .catch(error => {
        console.error('Error in smart GPU allocation:', error);
        showNotification('خطأ في التوزيع الذكي لكروت الشاشة', 'error');
    });
}

function showGPUDiagnosis() {
    console.log('Running GPU diagnosis...');
    
    fetch('/api/gpu/status')
    .then(response => response.json())
    .then(data => {
        console.log('GPU status response:', data);
        let diagnosisText = '=== تشخيص كروت الشاشة ===\n\n';
        
        if (data.nvidia_available) {
            diagnosisText += `✓ NVIDIA متاح: نعم\n`;
            diagnosisText += `✓ عدد كروت الشاشة: ${data.total_gpus}\n\n`;
            
            if (data.gpus && data.gpus.length > 0) {
                data.gpus.forEach((gpu, index) => {
                    diagnosisText += `--- كارت الشاشة ${index} ---\n`;
                    diagnosisText += `الاسم: ${gpu.name || 'غير معروف'}\n`;
                    diagnosisText += `الذاكرة: ${Math.round((gpu.memory_total || 0)/1024)}GB\n`;
                    diagnosisText += `الاستخدام: ${gpu.utilization || 0}%\n`;
                    diagnosisText += `درجة الحرارة: ${gpu.temperature || 0}°C\n\n`;
                });
            }
        } else {
            diagnosisText += `✗ NVIDIA متاح: لا\n`;
            diagnosisText += `✗ عدد كروت الشاشة: 0\n\n`;
            diagnosisText += `التوصيات:\n`;
            diagnosisText += `- تثبيت تعريفات NVIDIA\n`;
            diagnosisText += `- تثبيت CUDA toolkit\n`;
            diagnosisText += `- إعادة تشغيل النظام\n`;
        }
        
        alert(diagnosisText);
    })
    .catch(error => {
        console.error('Error in GPU diagnosis:', error);
        showNotification('خطأ في تشخيص كروت الشاشة', 'error');
    });
}

// Helper function to show notifications if not available in main page
if (typeof showNotification === 'undefined') {
    function showNotification(message, type) {
        console.log(`Notification [${type}]: ${message}`);
        
        // Create notification element
        var notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 20px;
            border-radius: 8px;
            color: white;
            font-weight: 500;
            z-index: 10000;
            max-width: 400px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        `;
        
        // Set background color based on type
        if (type === 'success') {
            notification.style.backgroundColor = '#28a745';
        } else if (type === 'error') {
            notification.style.backgroundColor = '#dc3545';
        } else if (type === 'warning') {
            notification.style.backgroundColor = '#ffc107';
            notification.style.color = '#212529';
        } else {
            notification.style.backgroundColor = '#17a2b8';
        }
        
        notification.textContent = message;
        document.body.appendChild(notification);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 5000);
    }
}

console.log('GPU management functions ready: refreshGPUOptions, smartGPUAllocation, showGPUDiagnosis');