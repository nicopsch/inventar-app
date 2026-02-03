#!/bin/bash
# Render Start Script

# Datenbank initialisieren
python -c "from app import app, db; app.app_context().push(); db.create_all()"

# Gunicorn starten
gunicorn --bind 0.0.0.0:$PORT app:app