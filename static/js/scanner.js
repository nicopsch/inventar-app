let html5QrcodeScanner = null;
let scannerAktiv = false;

// Scanner starten
function starteScanner() {
    if (scannerAktiv) {
        stoppeScanner();
        return;
    }
    
    const scannerContainer = document.getElementById('scanner-container');
    scannerContainer.innerHTML = ''; // Zurücksetzen
    
    html5QrcodeScanner = new Html5QrcodeScanner(
        "scanner-container",
        { 
            fps: 10,
            qrbox: { width: 300, height: 150 },
            aspectRatio: 1.777778,
            // WICHTIG: Barcode-Formate explizit angeben
            formatsToSupport: [
                Html5QrcodeSupportedFormats.EAN_13,
                Html5QrcodeSupportedFormats.EAN_8,
                Html5QrcodeSupportedFormats.UPC_A,
                Html5QrcodeSupportedFormats.UPC_E,
                Html5QrcodeSupportedFormats.CODE_128,
                Html5QrcodeSupportedFormats.CODE_39,
                Html5QrcodeSupportedFormats.QR_CODE
            ],
            // Kamera-Einstellungen
            videoConstraints: {
                facingMode: "environment" // Rückkamera als Vorschlag
            }
        }
    );
    
    html5QrcodeScanner.render(onScanSuccess, onScanError);
    scannerAktiv = true;
    
    // Button-Text ändern
    document.getElementById('scanner-button').textContent = 'Scanner stoppen';
}

// Bei erfolgreichem Scan
function onScanSuccess(decodedText, decodedResult) {
    console.log(`Barcode gefunden: ${decodedText}`);
    
    // Scanner stoppen
    stoppeScanner();
    
    // Barcode ins Eingabefeld
    document.getElementById('barcode-input').value = decodedText;
    
    // Automatisch suchen
    sucheBarcode();
}

// Bei Scan-Fehler (normal, passiert ständig)
function onScanError(errorMessage) {
    // Nichts tun - zu viele Fehlermeldungen sonst
}

// Scanner stoppen
function stoppeScanner() {
    if (html5QrcodeScanner) {
        html5QrcodeScanner.clear();
        html5QrcodeScanner = null;
        scannerAktiv = false;
        
        // Button-Text zurücksetzen
        document.getElementById('scanner-button').textContent = 'Kamera-Scanner starten';
        
        // Container zurücksetzen
        const scannerContainer = document.getElementById('scanner-container');
        scannerContainer.innerHTML = '<p style="color: #999;">Klicke auf "Kamera-Scanner starten"</p>';
    }
}