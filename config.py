import os

class Config:
    # Geheimer Schlüssel für Sessions (später ändern!)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-bitte-aendern'
    
    # Datenbank
    SQLALCHEMY_DATABASE_URI = 'sqlite:///inventar.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False