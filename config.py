import os

class Config:
    # Geheimer Schlüssel für Sessions
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-bitte-aendern'
    
    # Datenbank - nutzt PostgreSQL wenn verfügbar, sonst SQLite
    DATABASE_URL = os.environ.get('DATABASE_URL')
    
    # Render nutzt "postgres://" aber SQLAlchemy braucht "postgresql://"
    if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
    
    SQLALCHEMY_DATABASE_URI = DATABASE_URL or 'sqlite:///inventar.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False