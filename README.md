# 🏠 Lebensmittel Inventar App

Eine moderne Progressive Web App (PWA) zur Verwaltung deines Lebensmittel-Inventars mit Barcode-Scanner und Mehrbenutzerfähigkeit.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📱 Features

### Kernfunktionen
- 🔐 **Benutzer-Authentifizierung** - Registrierung und Login-System
- 🏘️ **Haushalts-Verwaltung** - Erstelle Haushalte und lade andere per Einladungscode ein
- 👥 **Mehrbenutzerfähigkeit** - Mehrere Nutzer können gemeinsam ein Inventar verwalten
- 📸 **Barcode-Scanner** - Scanne Barcodes direkt mit der Smartphone-Kamera
- 🌐 **Automatische Produktsuche** - Integration mit Open Food Facts API
- 📦 **Inventar-Verwaltung** - Produkte hinzufügen, löschen und Mengen anpassen
- 🔍 **Live-Suche** - Finde Produkte schnell nach Name, Marke oder Barcode
- 📅 **Mindesthaltbarkeitsdatum** - Optionale MHD-Eingabe mit Ablauf-Warnungen
- ⚠️ **Smart Notifications** - Visuelle Warnungen für ablaufende/abgelaufene Produkte

### Progressive Web App (PWA)
- 📲 **Installierbar** - Auf dem Smartphone-Homescreen wie eine native App
- 🎨 **Eigenes App-Icon** - Professionelles Erscheinungsbild
- 📱 **Vollbild-Modus** - Ohne Browser-UI nutzbar
- 🔄 **Offline-fähig** - Grundlegende Funktionalität auch ohne Internet (Service Worker)

## 🚀 Schnellstart

### Voraussetzungen
- Python 3.8 oder höher
- pip (Python Package Manager)
- Git

### Installation

1. **Repository klonen**
   ```bash
   git clone https://github.com/DEIN-USERNAME/inventar-app.git
   cd inventar-app
   ```

2. **Virtuelle Umgebung erstellen**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Auf Windows: venv\Scripts\activate
   ```

3. **Abhängigkeiten installieren**
   ```bash
   pip install -r requirements.txt
   ```

4. **App starten**
   ```bash
   python app.py
   ```

5. **Im Browser öffnen**
   - Lokal: `http://localhost:5000`
   - Im Netzwerk: `https://DEINE-IP:5000` (für Smartphone-Zugriff)

## 📖 Verwendung

### Erste Schritte

1. **Account erstellen**
   - Öffne die App und registriere dich mit Benutzername, Email und Passwort

2. **Haushalt erstellen**
   - Gehe zu "Haushalte verwalten"
   - Erstelle einen neuen Haushalt (z.B. "Meine WG")
   - Notiere den Einladungscode

3. **Andere Nutzer einladen**
   - Teile den Einladungscode mit deinen Mitbewohnern
   - Sie können über "Einem Haushalt beitreten" dem Haushalt beitreten

4. **Produkte scannen**
   - Wähle deinen Haushalt aus
   - Klicke auf "Kamera-Scanner starten"
   - Scanne den Barcode eines Produkts
   - Optional: Gib das Mindesthaltbarkeitsdatum ein
   - Füge das Produkt zum Inventar hinzu

### Als PWA auf dem Smartphone installieren

**Android (Chrome):**
1. Öffne die App im Chrome-Browser
2. Tippe auf das Menü (⋮)
3. Wähle "App installieren" oder "Zum Startbildschirm hinzufügen"

**iOS (Safari):**
1. Öffne die App in Safari
2. Tippe auf das Teilen-Symbol
3. Wähle "Zum Home-Bildschirm"

## 🏗️ Technologie-Stack

### Backend
- **Flask** - Python Web-Framework
- **Flask-Login** - Benutzer-Authentifizierung
- **Flask-SQLAlchemy** - ORM für Datenbank
- **SQLite** - Datenbank
- **Werkzeug** - Passwort-Hashing

### Frontend
- **HTML5 / CSS3** - Struktur und Design
- **JavaScript (Vanilla)** - Interaktivität
- **html5-qrcode** - Barcode-Scanner Bibliothek

### PWA
- **Service Worker** - Offline-Funktionalität und Caching
- **Web App Manifest** - Installierbarkeit und Metadaten

### APIs
- **Open Food Facts API** - Produktdaten und Informationen

## 📁 Projektstruktur

```
inventar-app/
├── app.py                  # Haupt-Backend (Flask Server)
├── models.py              # Datenbank-Modelle
├── config.py              # Konfiguration
├── requirements.txt       # Python-Abhängigkeiten
├── static/
│   ├── css/
│   │   └── style.css     # Styling
│   ├── js/
│   │   ├── app.js        # Hauptlogik
│   │   └── scanner.js    # Barcode-Scanner
│   ├── icons/            # PWA Icons
│   ├── manifest.json     # PWA Manifest
│   └── service-worker.js # Service Worker
├── templates/
│   ├── index.html        # Hauptseite
│   ├── login.html        # Login-Seite
│   ├── register.html     # Registrierung
│   └── haushalt.html     # Haushalts-Verwaltung
└── inventar.db           # SQLite Datenbank (wird erstellt)
```

## 🔒 Sicherheit

- ✅ Passwörter werden mit Werkzeug gehasht (niemals im Klartext gespeichert)
- ✅ Flask-Login für Session-Management
- ✅ HTTPS für Kamera-Zugriff erforderlich
- ✅ Berechtigungsprüfung für alle Haushalts-Operationen
- ⚠️ **Wichtig**: Vor Production-Einsatz `SECRET_KEY` in `config.py` ändern!

## 🛠️ Entwicklung

### Lokale Entwicklung

```bash
# Virtuelle Umgebung aktivieren
source venv/bin/activate

# Server im Debug-Modus starten
python app.py

# Die App läuft auf Port 5000
```

### HTTPS-Zertifikat generieren (für Kamera-Zugriff)

```bash
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
```

### Neue Abhängigkeiten hinzufügen

```bash
pip install PAKET-NAME --break-system-packages
pip freeze > requirements.txt
```

## 🐛 Bekannte Einschränkungen

- Die App läuft aktuell im Development-Modus (nicht für Production optimiert)
- SQLite ist für kleine bis mittlere Nutzerzahlen geeignet
- Kamera-Scanner benötigt HTTPS (funktioniert nicht über unsicheres HTTP)
- Open Food Facts API hat manchmal unvollständige Produktdaten

## 🚀 Deployment

### Option 1: Raspberry Pi (zu Hause)
- App auf dem Raspberry Pi installieren
- Permanent laufen lassen
- Im lokalen Netzwerk erreichbar

### Option 2: Cloud-Server
- VPS bei Anbietern wie DigitalOcean, Hetzner, AWS
- Für Production: Gunicorn + Nginx nutzen
- PostgreSQL statt SQLite empfohlen

### Option 3: Kostenlose Hosting-Dienste
- PythonAnywhere (kostenloser Tier verfügbar)
- Render.com
- Fly.io

## 🤝 Mitwirken

Contributions sind willkommen! So kannst du beitragen:

1. Fork das Repository
2. Erstelle einen Feature-Branch (`git checkout -b feature/NeuesFeature`)
3. Commit deine Änderungen (`git commit -m 'Füge neues Feature hinzu'`)
4. Push zum Branch (`git push origin feature/NeuesFeature`)
5. Erstelle einen Pull Request

## 📝 Roadmap

### Geplante Features
- [ ] Sortierung (nach Name, MHD, Menge)
- [ ] Kategorien-Filter
- [ ] Einkaufsliste-Funktion
- [ ] Produkte nachträglich bearbeiten
- [ ] Export/Import (CSV, Excel)
- [ ] Statistiken und Analytics
- [ ] Push-Benachrichtigungen
- [ ] Dark Mode
- [ ] Mehrsprachigkeit

## 📄 Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert - siehe [LICENSE](LICENSE) Datei für Details.

## 👏 Danksagungen

- [Open Food Facts](https://world.openfoodfacts.org/) - Für die kostenlose Produktdatenbank
- [html5-qrcode](https://github.com/mebjas/html5-qrcode) - Für die Barcode-Scanner Bibliothek
- [Flask](https://flask.palletsprojects.com/) - Für das großartige Web-Framework

## 📧 Kontakt

Bei Fragen oder Feedback kannst du gerne ein Issue erstellen oder mich kontaktieren.

---

**Entwickelt mit ❤️ und Claude**
