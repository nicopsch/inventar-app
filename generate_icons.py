from PIL import Image, ImageDraw, ImageFont

def create_icon(size, filename):
    # Erstelle ein Bild mit Farbverlauf
    img = Image.new('RGB', (size, size), color='#667eea')
    draw = ImageDraw.Draw(img)
    
    # Zeichne einen Kreis
    margin = size // 10
    draw.ellipse([margin, margin, size-margin, size-margin], fill='#764ba2')
    
    # Füge Text hinzu (Emoji)
    try:
        font_size = size // 2
        # Versuche einen Font zu laden
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
    except:
        font = ImageFont.load_default()
    
    text = "🏠"
    # Zentriere Text
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    position = ((size - text_width) // 2, (size - text_height) // 2 - size // 10)
    
    draw.text(position, text, fill='white', font=font)
    
    img.save(filename)
    print(f"Icon erstellt: {filename}")

# Icons generieren
create_icon(192, 'static/icons/icon-192.png')
create_icon(512, 'static/icons/icon-512.png')