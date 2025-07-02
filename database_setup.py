#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Database Setup for AI Translator
Initialize all database tables and default settings
"""

import os
import sys
from datetime import datetime
from app import app, db
from models import Settings, MediaFile, Log, TranslationJob, Notification, UserSession, PasswordReset, TranslationHistory, DatabaseStats, TranslationLog

def create_database():
    """Create all database tables"""
    with app.app_context():
        try:
            # Drop all tables and recreate (for fresh setup)
            db.drop_all()
            db.create_all()
            print("✓ All database tables created successfully")
            return True
        except Exception as e:
            print(f"✗ Error creating database: {e}")
            return False

def initialize_default_settings():
    """Initialize default settings in database"""
    with app.app_context():
        try:
            # Check if settings already exist
            if Settings.query.count() > 0:
                print("✓ Settings already exist, skipping initialization")
                return True
            
            default_settings = [
                # Authentication Settings
                Settings(key='admin_username', value='admin', section='AUTH', type='string', description='Administrator username'),
                Settings(key='admin_password', value='your_strong_password', section='AUTH', type='password', description='Administrator password'),
                
                # Language and Theme Settings
                Settings(key='default_language', value='ar', section='UI', type='select', options='ar:العربية,en:English', description='Default interface language'),
                Settings(key='default_theme', value='dark', section='UI', type='select', options='dark:داكن,light:فاتح,system:النظام', description='Default theme'),
                Settings(key='items_per_page', value='24', section='UI', type='select', options='12:12,24:24,48:48,96:96', description='Items per page'),
                
                # AI Models Settings
                Settings(key='whisper_model', value='medium.en', section='AI', type='select', options='tiny:tiny,base:base,small:small,medium:medium,medium.en:medium.en,large:large', description='Whisper model for speech recognition'),
                Settings(key='ollama_model', value='llama3', section='AI', type='string', description='Ollama model for translation'),
                Settings(key='whisper_model_gpu', value='auto', section='AI', type='select', options='auto:تلقائي,cpu:المعالج فقط', description='GPU allocation for Whisper'),
                Settings(key='ollama_model_gpu', value='auto', section='AI', type='select', options='auto:تلقائي,cpu:المعالج فقط', description='GPU allocation for Ollama'),
                
                # API Settings
                Settings(key='sonarr_url', value='http://localhost:8989', section='API', type='string', description='Sonarr API URL'),
                Settings(key='sonarr_api_key', value='', section='API', type='password', description='Sonarr API Key'),
                Settings(key='radarr_url', value='http://localhost:7878', section='API', type='string', description='Radarr API URL'),
                Settings(key='radarr_api_key', value='', section='API', type='password', description='Radarr API Key'),
                Settings(key='ollama_url', value='http://localhost:11434', section='API', type='string', description='Ollama API URL'),
                
                # Media Services Settings
                Settings(key='plex_enabled', value='false', section='MEDIA_SERVICES', type='select', options='true:نعم,false:لا', description='Enable Plex integration'),
                Settings(key='jellyfin_enabled', value='false', section='MEDIA_SERVICES', type='select', options='true:نعم,false:لا', description='Enable Jellyfin integration'),
                Settings(key='emby_enabled', value='false', section='MEDIA_SERVICES', type='select', options='true:نعم,false:لا', description='Enable Emby integration'),
                Settings(key='kodi_enabled', value='false', section='MEDIA_SERVICES', type='select', options='true:نعم,false:لا', description='Enable Kodi integration'),
                Settings(key='radarr_enabled', value='true', section='MEDIA_SERVICES', type='select', options='true:نعم,false:لا', description='Enable Radarr integration'),
                Settings(key='sonarr_enabled', value='true', section='MEDIA_SERVICES', type='select', options='true:نعم,false:لا', description='Enable Sonarr integration'),
                
                # Path Settings
                Settings(key='remote_movies_path', value='/volume1/movies', section='PATHS', type='string', description='Remote movies path on NAS'),
                Settings(key='remote_series_path', value='/volume1/tv', section='PATHS', type='string', description='Remote TV series path on NAS'),
                Settings(key='local_movies_mount', value='/mnt/movies', section='PATHS', type='string', description='Local movies mount point'),
                Settings(key='local_series_mount', value='/mnt/series', section='PATHS', type='string', description='Local series mount point'),
                
                # Processing Settings
                Settings(key='auto_correct_filenames', value='true', section='PROCESSING', type='select', options='true:نعم,false:لا', description='Auto-correct subtitle filenames'),
                Settings(key='max_concurrent_jobs', value='2', section='PROCESSING', type='select', options='1:1,2:2,4:4,8:8', description='Maximum concurrent translation jobs'),
                Settings(key='translation_prompt', value='Translate the following English text to Arabic. Keep technical terms and names unchanged:', section='PROCESSING', type='textarea', description='Translation prompt for AI'),
                
                # System Settings
                Settings(key='server_host', value='0.0.0.0', section='SYSTEM', type='string', description='Server host IP'),
                Settings(key='server_port', value='5000', section='SYSTEM', type='string', description='Server port'),
                Settings(key='debug_mode', value='false', section='SYSTEM', type='select', options='true:نعم,false:لا', description='Enable debug mode'),
                Settings(key='log_level', value='INFO', section='SYSTEM', type='select', options='DEBUG:DEBUG,INFO:INFO,WARNING:WARNING,ERROR:ERROR', description='Logging level'),
                
                # Development Settings
                Settings(key='enable_testing_features', value='false', section='DEVELOPMENT', type='select', options='true:نعم,false:لا', description='Enable testing features'),
                Settings(key='sample_data_enabled', value='false', section='DEVELOPMENT', type='select', options='true:نعم,false:لا', description='Enable sample data generation'),
            ]
            
            for setting in default_settings:
                db.session.add(setting)
            
            db.session.commit()
            print(f"✓ Initialized {len(default_settings)} default settings")
            return True
            
        except Exception as e:
            print(f"✗ Error initializing settings: {e}")
            db.session.rollback()
            return False

def main():
    """Main setup function"""
    print("=== AI Translator Database Setup ===")
    
    # Create database tables
    if not create_database():
        sys.exit(1)
    
    # Initialize default settings
    if not initialize_default_settings():
        sys.exit(1)
    
    print("✓ Database setup completed successfully!")
    print("✓ You can now start the application with: python main.py")

if __name__ == "__main__":
    main()