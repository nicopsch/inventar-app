from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

# Verbindungstabelle: Welcher Nutzer gehört zu welchem Haushalt?
haushalt_mitglieder = db.Table('haushalt_mitglieder',
    db.Column('nutzer_id', db.Integer, db.ForeignKey('nutzer.id'), primary_key=True),
    db.Column('haushalt_id', db.Integer, db.ForeignKey('haushalt.id'), primary_key=True)
)

class Nutzer(UserMixin, db.Model):
    """Ein Benutzer der App"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    passwort_hash = db.Column(db.String(200), nullable=False)
    erstellt_am = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Beziehungen
    haushalte = db.relationship('Haushalt', secondary=haushalt_mitglieder, 
                                backref=db.backref('mitglieder', lazy='dynamic'))
    
    # NEU: Methoden für Passwort-Handling
    def setze_passwort(self, passwort):
        """Hasht und speichert das Passwort"""
        self.passwort_hash = generate_password_hash(passwort)
    
    def pruefe_passwort(self, passwort):
        """Überprüft, ob das Passwort korrekt ist"""
        return check_password_hash(self.passwort_hash, passwort)

class Haushalt(db.Model):
    """Ein Haushalt (z.B. eine WG oder Familie)"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    erstellt_am = db.Column(db.DateTime, default=datetime.utcnow)
    einladungscode = db.Column(db.String(20), unique=True)
    
    # Beziehung zu Produkten
    produkte = db.relationship('Produkt', backref='haushalt', lazy=True, cascade='all, delete-orphan')

class Produkt(db.Model):
    """Ein Produkt im Inventar"""
    id = db.Column(db.Integer, primary_key=True)
    barcode = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    marke = db.Column(db.String(100))
    kategorie = db.Column(db.String(100))
    menge = db.Column(db.Integer, default=1)
    einheit = db.Column(db.String(20))  # z.B. "Stück", "kg", "l"
    mindesthaltbarkeit = db.Column(db.Date)
    bild_url = db.Column(db.String(500))
    hinzugefuegt_am = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Fremdschlüssel
    haushalt_id = db.Column(db.Integer, db.ForeignKey('haushalt.id'), nullable=False)