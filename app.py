from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, Nutzer, Haushalt, Produkt
from config import Config
import requests
import string
import random

app = Flask(__name__)
app.config.from_object(Config)

# Initialisierung
db.init_app(app)
CORS(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Bitte logge dich ein, um fortzufahren.'

@login_manager.user_loader
def load_user(user_id):
    return Nutzer.query.get(int(user_id))

# Datenbank erstellen (beim ersten Start)
with app.app_context():
    db.create_all()

# Hilfsfunktion
def generiere_einladungscode(laenge=8):
    """Generiert einen zufälligen Einladungscode"""
    zeichen = string.ascii_uppercase + string.digits
    return ''.join(random.choice(zeichen) for _ in range(laenge))

# ===== ROUTES =====

@app.route('/')
@login_required
def index():
    """Startseite"""
    return render_template('index.html')

@app.route('/api/barcode/<barcode>')
@login_required
def suche_barcode(barcode):
    """Sucht ein Produkt in der Open Food Facts Datenbank"""
    try:
        # Open Food Facts API
        url = f'https://world.openfoodfacts.org/api/v0/product/{barcode}.json'
        response = requests.get(url)
        data = response.json()
        
        if data['status'] == 1:
            product = data['product']
            return jsonify({
                'success': True,
                'produkt': {
                    'barcode': barcode,
                    'name': product.get('product_name', 'Unbekannt'),
                    'marke': product.get('brands', ''),
                    'kategorie': product.get('categories', ''),
                    'bild_url': product.get('image_url', '')
                }
            })
        else:
            return jsonify({'success': False, 'message': 'Produkt nicht gefunden'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/inventar')
@login_required
def get_inventar():
    """Gibt alle Produkte des aktuellen Haushalts zurück"""
    haushalt_id = request.args.get('haushalt_id', type=int)
    
    if not haushalt_id:
        return jsonify([])
    
    # Prüfen ob Nutzer Mitglied ist
    haushalt = Haushalt.query.get(haushalt_id)
    if not haushalt or current_user not in haushalt.mitglieder:
        return jsonify({'success': False, 'message': 'Keine Berechtigung'}), 403
    
    from datetime import date, timedelta
    heute = date.today()
    bald_ablauf = heute + timedelta(days=7)  # 7 Tage Warnung
    
    produkte = Produkt.query.filter_by(haushalt_id=haushalt_id).all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'marke': p.marke,
        'menge': p.menge,
        'barcode': p.barcode,
        'bild_url': p.bild_url,
        'mindesthaltbarkeit': p.mindesthaltbarkeit.isoformat() if p.mindesthaltbarkeit else None,
        'abgelaufen': p.mindesthaltbarkeit < heute if p.mindesthaltbarkeit else False,
        'bald_ablauf': heute <= p.mindesthaltbarkeit <= bald_ablauf if p.mindesthaltbarkeit else False
    } for p in produkte])

@app.route('/api/produkt', methods=['POST'])
@login_required
def add_produkt():
    """Fügt ein Produkt zum Inventar hinzu"""
    data = request.json
    haushalt_id = data.get('haushalt_id')
    
    if not haushalt_id:
        return jsonify({'success': False, 'message': 'Haushalt erforderlich'}), 400
    
    # Prüfen ob Nutzer Mitglied ist
    haushalt = Haushalt.query.get(haushalt_id)
    if not haushalt or current_user not in haushalt.mitglieder:
        return jsonify({'success': False, 'message': 'Keine Berechtigung'}), 403
    
    # MHD konvertieren (falls vorhanden)
    from datetime import datetime
    mhd = None
    if data.get('mindesthaltbarkeit'):
        try:
            mhd = datetime.strptime(data.get('mindesthaltbarkeit'), '%Y-%m-%d').date()
        except:
            pass
    
    neues_produkt = Produkt(
        barcode=data['barcode'],
        name=data['name'],
        marke=data.get('marke', ''),
        kategorie=data.get('kategorie', ''),
        menge=data.get('menge', 1),
        bild_url=data.get('bild_url', ''),
        mindesthaltbarkeit=mhd,
        haushalt_id=haushalt_id
    )
    
    db.session.add(neues_produkt)
    db.session.commit()
    
    return jsonify({'success': True, 'id': neues_produkt.id})
# ===== LOGIN / REGISTRIERUNG =====

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login-Seite"""
    if request.method == 'POST':
        data = request.json
        username = data.get('username')
        passwort = data.get('passwort')
        
        nutzer = Nutzer.query.filter_by(username=username).first()
        
        if nutzer and nutzer.pruefe_passwort(passwort):
            login_user(nutzer)
            return jsonify({'success': True, 'message': 'Login erfolgreich'})
        else:
            return jsonify({'success': False, 'message': 'Falscher Benutzername oder Passwort'})
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registrierungs-Seite"""
    if request.method == 'POST':
        data = request.json
        username = data.get('username')
        email = data.get('email')
        passwort = data.get('passwort')
        
        # Prüfen ob Username schon existiert
        if Nutzer.query.filter_by(username=username).first():
            return jsonify({'success': False, 'message': 'Username bereits vergeben'})
        
        # Prüfen ob Email schon existiert
        if Nutzer.query.filter_by(email=email).first():
            return jsonify({'success': False, 'message': 'Email bereits registriert'})
        
        # Neuen Nutzer erstellen
        neuer_nutzer = Nutzer(username=username, email=email)
        neuer_nutzer.setze_passwort(passwort)
        
        db.session.add(neuer_nutzer)
        db.session.commit()
        
        login_user(neuer_nutzer)
        return jsonify({'success': True, 'message': 'Registrierung erfolgreich'})
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    """Logout"""
    logout_user()
    return jsonify({'success': True, 'message': 'Logout erfolgreich'})

@app.route('/api/current-user')
def current_user_info():
    """Gibt Info über aktuellen Nutzer zurück"""
    if current_user.is_authenticated:
        return jsonify({
            'logged_in': True,
            'username': current_user.username,
            'email': current_user.email
        })
    return jsonify({'logged_in': False})

@app.route('/static/manifest.json')
def manifest():
    """Liefert das PWA Manifest"""
    return app.send_static_file('manifest.json')

# ===== HAUSHALTE =====

@app.route('/haushalt')
@login_required
def haushalt_page():
    """Haushalt-Verwaltungsseite"""
    return render_template('haushalt.html')

@app.route('/api/haushalt/erstellen', methods=['POST'])
@login_required
def haushalt_erstellen():
    """Erstellt einen neuen Haushalt"""
    data = request.json
    name = data.get('name')
    
    if not name:
        return jsonify({'success': False, 'message': 'Name erforderlich'})
    
    # Neuen Haushalt erstellen
    neuer_haushalt = Haushalt(
        name=name,
        einladungscode=generiere_einladungscode()
    )
    
    # Aktuellen Nutzer hinzufügen
    neuer_haushalt.mitglieder.append(current_user)
    
    db.session.add(neuer_haushalt)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'haushalt': {
            'id': neuer_haushalt.id,
            'name': neuer_haushalt.name,
            'einladungscode': neuer_haushalt.einladungscode
        }
    })

@app.route('/api/haushalt/beitreten', methods=['POST'])
@login_required
def haushalt_beitreten():
    """Tritt einem Haushalt bei (via Einladungscode)"""
    data = request.json
    code = data.get('code')
    
    if not code:
        return jsonify({'success': False, 'message': 'Code erforderlich'})
    
    # Haushalt finden
    haushalt = Haushalt.query.filter_by(einladungscode=code).first()
    
    if not haushalt:
        return jsonify({'success': False, 'message': 'Ungültiger Code'})
    
    # Prüfen ob bereits Mitglied
    if current_user in haushalt.mitglieder:
        return jsonify({'success': False, 'message': 'Du bist bereits Mitglied'})
    
    # Nutzer hinzufügen
    haushalt.mitglieder.append(current_user)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'haushalt': {
            'id': haushalt.id,
            'name': haushalt.name
        }
    })

@app.route('/api/haushalte')
@login_required
def meine_haushalte():
    """Gibt alle Haushalte des aktuellen Nutzers zurück"""
    haushalte = [{
        'id': h.id,
        'name': h.name,
        'einladungscode': h.einladungscode,
        'mitglieder_anzahl': h.mitglieder.count(),
        'produkte_anzahl': len(h.produkte)
    } for h in current_user.haushalte]
    
    return jsonify(haushalte)

@app.route('/api/haushalt/<int:haushalt_id>/mitglieder')
@login_required
def haushalt_mitglieder(haushalt_id):
    """Gibt alle Mitglieder eines Haushalts zurück"""
    haushalt = Haushalt.query.get_or_404(haushalt_id)
    
    # Prüfen ob Nutzer Mitglied ist
    if current_user not in haushalt.mitglieder:
        return jsonify({'success': False, 'message': 'Keine Berechtigung'}), 403
    
    mitglieder = [{
        'id': m.id,
        'username': m.username
    } for m in haushalt.mitglieder]
    
    return jsonify(mitglieder)

# ===== PRODUKT-VERWALTUNG =====

@app.route('/api/produkt/<int:produkt_id>', methods=['DELETE'])
@login_required
def delete_produkt(produkt_id):
    """Löscht ein Produkt"""
    produkt = Produkt.query.get_or_404(produkt_id)
    
    # Prüfen ob Nutzer Mitglied des Haushalts ist
    if current_user not in produkt.haushalt.mitglieder:
        return jsonify({'success': False, 'message': 'Keine Berechtigung'}), 403
    
    db.session.delete(produkt)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Produkt gelöscht'})

@app.route('/api/produkt/<int:produkt_id>/menge', methods=['PATCH'])
@login_required
def update_menge(produkt_id):
    """Ändert die Menge eines Produkts"""
    produkt = Produkt.query.get_or_404(produkt_id)
    
    # Prüfen ob Nutzer Mitglied des Haushalts ist
    if current_user not in produkt.haushalt.mitglieder:
        return jsonify({'success': False, 'message': 'Keine Berechtigung'}), 403
    
    data = request.json
    neue_menge = data.get('menge')
    
    if neue_menge is None or neue_menge < 0:
        return jsonify({'success': False, 'message': 'Ungültige Menge'}), 400
    
    # Wenn Menge 0, Produkt löschen
    if neue_menge == 0:
        db.session.delete(produkt)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Produkt gelöscht', 'deleted': True})
    
    produkt.menge = neue_menge
    db.session.commit()
    
    return jsonify({'success': True, 'menge': produkt.menge})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, 
            ssl_context=('cert.pem', 'key.pem'))