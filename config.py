import os

class Config:
    # Geheimer Schlüssel für Sessions
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-bitte-aendern'
    
    # Datenbank - nutzt PostgreSQL wenn verfügbar, sonst SQLite
    DATABASE_URL = os.environ.get('DATABASE_URL')
    
    # Für PostgreSQL: Konvertiere zu psycopg (Version 3) statt psycopg2
    if DATABASE_URL:
        # Render nutzt "postgres://" aber SQLAlchemy braucht "postgresql://"
        if DATABASE_URL.startswith('postgres://'):
            DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
        
        # Nutze psycopg3 Treiber statt psycopg2
        if DATABASE_URL.startswith('postgresql://'):
            # Füge +psycopg hinzu um explizit psycopg3 zu nutzen
            DATABASE_URL = DATABASE_URL.replace('postgresql://', 'postgresql+psycopg://', 1)
    
    SQLALCHEMY_DATABASE_URI = DATABASE_URL or 'sqlite:///inventar.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False