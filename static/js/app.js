// Globale Variablen
let aktuellesProdukt = null;
let aktuellerHaushalt = null;

// Beim Laden der Seite
document.addEventListener('DOMContentLoaded', function() {
    ladeAktuellenHaushalt();
});

// Aktuellen Haushalt laden
function ladeAktuellenHaushalt() {
    const gespeichert = localStorage.getItem('aktuellerHaushalt');
    
    if (gespeichert) {
        aktuellerHaushalt = JSON.parse(gespeichert);
        document.getElementById('haushalt-name').textContent = aktuellerHaushalt.name;
        document.getElementById('hauptbereich').style.display = 'block';
        document.getElementById('kein-haushalt-hinweis').style.display = 'none';
        ladeInventar();
    } else {
        document.getElementById('hauptbereich').style.display = 'none';
        document.getElementById('kein-haushalt-hinweis').style.display = 'block';
    }
}

// Barcode suchen
async function sucheBarcode() {
    const barcode = document.getElementById('barcode-input').value;
    
    if (!barcode) {
        alert('Bitte Barcode eingeben');
        return;
    }
    
    try {
        const response = await fetch(`/api/barcode/${barcode}`);
        const data = await response.json();
        
        if (data.success) {
            zeigeProduktInfo(data.produkt);
        } else {
            alert('Produkt nicht gefunden');
        }
    } catch (error) {
        console.error('Fehler:', error);
        alert('Fehler bei der Suche');
    }
}

// Produktinfo anzeigen
function zeigeProduktInfo(produkt) {
    aktuellesProdukt = produkt;
    
    document.getElementById('product-info').style.display = 'block';
    document.getElementById('product-name').textContent = produkt.name;
    document.getElementById('product-brand').textContent = produkt.marke || 'Unbekannt';
    
    const img = document.getElementById('product-image');
    if (produkt.bild_url) {
        img.src = produkt.bild_url;
        img.style.display = 'block';
    } else {
        img.style.display = 'none';
    }
}

// Produkt zum Inventar hinzufügen
async function produktHinzufuegen() {
    if (!aktuellesProdukt || !aktuellerHaushalt) return;
    
    const menge = document.getElementById('product-quantity').value;
    const mhdInput = document.getElementById('product-mhd').value;
    
    const produktDaten = {
        barcode: aktuellesProdukt.barcode,
        name: aktuellesProdukt.name,
        marke: aktuellesProdukt.marke,
        kategorie: aktuellesProdukt.kategorie,
        menge: parseInt(menge),
        bild_url: aktuellesProdukt.bild_url,
        haushalt_id: aktuellerHaushalt.id
    };
    
    // MHD nur hinzufügen wenn ausgefüllt
    if (mhdInput) {
        produktDaten.mindesthaltbarkeit = mhdInput;
    }
    
    try {
        const response = await fetch('/api/produkt', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(produktDaten)
        });
        
        const data = await response.json();
        
        if (data.success) {
            alert('Produkt hinzugefügt!');
            document.getElementById('barcode-input').value = '';
            document.getElementById('product-mhd').value = '';
            document.getElementById('product-info').style.display = 'none';
            ladeInventar();
        } else {
            alert(data.message || 'Fehler beim Hinzufügen');
        }
    } catch (error) {
        console.error('Fehler:', error);
        alert('Fehler beim Hinzufügen');
    }
}

// Inventar laden und anzeigen
async function ladeInventar() {
    if (!aktuellerHaushalt) return;
    
    try {
        const response = await fetch(`/api/inventar?haushalt_id=${aktuellerHaushalt.id}`);
        const produkte = await response.json();
        
        // Alle Produkte global speichern für Suche
        alleProdukte = produkte;
        
        // Produkte anzeigen
        zeigeProdukte(produkte);
    } catch (error) {
        console.error('Fehler:', error);
    }
}

// Menge ändern
async function mengaendern(produktId, aenderung) {
    try {
        // Erst aktuelles Produkt holen
        const response = await fetch(`/api/inventar?haushalt_id=${aktuellerHaushalt.id}`);
        const produkte = await response.json();
        const produkt = produkte.find(p => p.id === produktId);
        
        if (!produkt) return;
        
        const neueMenge = produkt.menge + aenderung;
        
        if (neueMenge < 0) return;
        
        // Menge aktualisieren
        const updateResponse = await fetch(`/api/produkt/${produktId}/menge`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ menge: neueMenge })
        });
        
        const data = await updateResponse.json();
        
        if (data.success) {
            ladeInventar();
        } else {
            alert(data.message || 'Fehler beim Aktualisieren');
        }
    } catch (error) {
        console.error('Fehler:', error);
        alert('Fehler beim Aktualisieren');
    }
}

// Produkt löschen
async function produktLoeschen(produktId) {
    if (!confirm('Möchtest du dieses Produkt wirklich löschen?')) {
        return;
    }
    
    try {
        const response = await fetch(`/api/produkt/${produktId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        if (!response.ok) {
            console.error('HTTP-Fehler:', response.status);
            alert('Fehler beim Löschen: ' + response.status);
            return;
        }
        
        const data = await response.json();
        
        if (data.success) {
            console.log('Produkt erfolgreich gelöscht');
            ladeInventar();
        } else {
            alert(data.message || 'Fehler beim Löschen');
        }
    } catch (error) {
        console.error('Fehler:', error);
        alert('Fehler beim Löschen: ' + error.message);
    }
}

// Globale Variable für alle Produkte
let alleProdukte = [];

// Suche im Inventar
function sucheImInventar() {
    const suchbegriff = document.getElementById('search-input').value.toLowerCase();
    const clearButton = document.getElementById('clear-search');
    
    // Clear-Button anzeigen/verstecken
    if (suchbegriff) {
        clearButton.style.display = 'block';
    } else {
        clearButton.style.display = 'none';
    }
    
    // Filtern
    const gefilterteProdukte = alleProdukte.filter(produkt => {
        return produkt.name.toLowerCase().includes(suchbegriff) ||
               (produkt.marke && produkt.marke.toLowerCase().includes(suchbegriff)) ||
               (produkt.kategorie && produkt.kategorie.toLowerCase().includes(suchbegriff)) ||
               produkt.barcode.includes(suchbegriff);
    });
    
    zeigeProdukte(gefilterteProdukte);
}

// Suche löschen
function sucheLöschen() {
    document.getElementById('search-input').value = '';
    document.getElementById('clear-search').style.display = 'none';
    zeigeProdukte(alleProdukte);
}

// Produkte anzeigen (neue Hilfsfunktion)
function zeigeProdukte(produkte) {
    const liste = document.getElementById('inventory-list');
    
    if (produkte.length === 0) {
        const suchbegriff = document.getElementById('search-input').value;
        if (suchbegriff) {
            liste.innerHTML = '<p style="color: #666; text-align: center;">Keine Produkte gefunden für "' + suchbegriff + '"</p>';
        } else {
            liste.innerHTML = '<p style="color: #666; text-align: center;">Noch keine Produkte im Inventar</p>';
        }
        return;
    }
    
    liste.innerHTML = '';
    
    produkte.forEach(produkt => {
        const item = document.createElement('div');
        item.className = 'inventory-item';
        
        // MHD-Status hinzufügen
        if (produkt.abgelaufen) {
            item.classList.add('abgelaufen');
        } else if (produkt.bald_ablauf) {
            item.classList.add('bald-ablauf');
        }
        
        let html = '';
        
        if (produkt.bild_url) {
            html += `<img src="${produkt.bild_url}" style="width: 100%; border-radius: 5px; margin-bottom: 10px;">`;
        }
        
        html += `<h4>${produkt.name}</h4>`;
        
        // MHD-Warnung anzeigen
        if (produkt.abgelaufen) {
            html += `<p class="mhd-warnung abgelaufen-text">⚠️ Abgelaufen!</p>`;
        } else if (produkt.bald_ablauf) {
            html += `<p class="mhd-warnung bald-ablauf-text">⏰ Läuft bald ab</p>`;
        }
        
        html += `<p>Marke: ${produkt.marke || 'Unbekannt'}</p>`;
        
        // MHD anzeigen (wenn vorhanden)
        if (produkt.mindesthaltbarkeit) {
            const datum = new Date(produkt.mindesthaltbarkeit);
            const formatiert = datum.toLocaleDateString('de-DE');
            html += `<p>MHD: ${formatiert}</p>`;
        }
        
        html += `
            <div class="menge-controls">
                <button class="btn-small" onclick="mengaendern(${produkt.id}, -1)">−</button>
                <span class="menge-anzeige">${produkt.menge}</span>
                <button class="btn-small" onclick="mengaendern(${produkt.id}, 1)">+</button>
            </div>
            <p style="font-size: 12px; color: #999; margin-top: 10px;">Barcode: ${produkt.barcode}</p>
            <button class="btn-delete" onclick="produktLoeschen(${produkt.id})">🗑️ Löschen</button>
        `;
        
        item.innerHTML = html;
        liste.appendChild(item);
    });
}

// Enter-Taste im Barcode-Eingabefeld
document.getElementById('barcode-input').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        sucheBarcode();
    }
});