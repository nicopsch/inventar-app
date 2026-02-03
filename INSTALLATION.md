# 📦 Installations-Anleitung

## Voraussetzungen

- **Python 3.8+** - [Download hier](https://www.python.org/downloads/)
- **Git** - [Download hier](https://git-scm.com/downloads)
- **pip** - (normalerweise mit Python installiert)

## Schritt-für-Schritt Installation

### 1. Repository klonen

```bash
git clone https://github.com/DEIN-USERNAME/inventar-app.git
cd inventar-app
```

### 2. Virtuelle Umgebung erstellen

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Abhängigkeiten installieren

**Linux:**
```bash
pip install -r requirements.txt --break-system-packages
```

**Windows/Mac:**
```bash
pip install -r requirements.txt
```

### 4. SSL-Zertifikate generieren (für Kamera-Zugriff)

```bash
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
```

Bei den Fragen kannst du einfach Enter drücken oder beliebige Werte eingeben.

### 5. App Icons generieren (optional)

Falls du eigene Icons erstellen möchtest:

```bash
pip install Pillow --break-system-packages  # Linux
# oder
pip install Pillow  # Windows/Mac

python create_simple_icons.py
```

### 6. Konfiguration anpassen

Öffne `config.py` und ändere den `SECRET_KEY`:

```python
SECRET_KEY = 'dein-sicherer-zufälliger-schlüssel-hier'
```

### 7. App starten

```bash
python app.py
```

Die App läuft jetzt auf:
- **Lokal**: `https://localhost:5000`
- **Im Netzwerk**: `https://DEINE-IP:5000`

### 8. Erste Schritte

1. Öffne `https://localhost:5000` im Browser
2. Akzeptiere die Sicherheitswarnung (selbst-signiertes Zertifikat)
3. Registriere einen neuen Account
4. Erstelle einen Haushalt
5. Beginne mit dem Scannen! 📱

## Zugriff vom Smartphone

1. **Finde deine lokale IP-Adresse:**
   ```bash
   # Linux/Mac
   hostname -I
   
   # Windows
   ipconfig
   ```

2. **Öffne im Smartphone-Browser:**
   ```
   https://DEINE-IP:5000
   ```
   (z.B. `https://192.168.0.104:5000`)

3. **Akzeptiere die Sicherheitswarnung**
   - Chrome: "Erweitert" → "Trotzdem fortfahren"
   - Safari: "Details" → "Diese Website besuchen"

4. **Als PWA installieren**
   - Android: Menü → "App installieren"
   - iOS: Teilen → "Zum Home-Bildschirm"

## Troubleshooting

### Problem: "ModuleNotFoundError"
**Lösung:** Stelle sicher, dass die virtuelle Umgebung aktiviert ist:
```bash
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### Problem: "Address already in use"
**Lösung:** Port 5000 ist bereits belegt. Ändere in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Anderer Port
```

### Problem: Kamera funktioniert nicht
**Lösung:** 
- Stelle sicher, dass du HTTPS verwendest (nicht HTTP)
- Akzeptiere die Browser-Berechtigung für Kamera-Zugriff

### Problem: Icons werden nicht angezeigt
**Lösung:** 
- Überprüfe, ob die Icons existieren: `ls static/icons/`
- Führe `python create_simple_icons.py` aus

## Weitere Hilfe

Bei Problemen öffne bitte ein Issue auf GitHub: [Issues](https://github.com/DEIN-USERNAME/inventar-app/issues)
