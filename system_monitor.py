#!/usr/bin/env python3
"""
Simple System Monitor - Stable Version
"""

import psutil

class SystemMonitor:
    def __init__(self):
        pass
    
    def get_system_info(self):
        """Get basic system information"""
        try:
            return {
                'cpu': {
                    'percent': psutil.cpu_percent(),
                    'count': psutil.cpu_count()
                },
                'memory': {
                    'percent': psutil.virtual_memory().percent,
                    'total': psutil.virtual_memory().total,
                    'available': psutil.virtual_memory().available
                },
                'disk': {
                    'percent': psutil.disk_usage('/').percent,
                    'total': psutil.disk_usage('/').total,
                    'free': psutil.disk_usage('/').free
                }
            }
        except:
            return {
                'cpu': {'percent': 0, 'count': 1},
                'memory': {'percent': 0, 'total': 0, 'available': 0},
                'disk': {'percent': 0, 'total': 0, 'free': 0}
            }