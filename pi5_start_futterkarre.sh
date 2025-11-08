#!/bin/bash

# 🚀 EINFACH: Futterkarre GUI starten
# Ausführen: cd ~/Futterkarre && ./pi5_start_futterkarre.sh

echo "🚀 Futterkarre GUI starten..."

# Aktueller Ordner (sollte ~/Futterkarre sein)
echo "📍 Aktueller Ordner: $(pwd)"

# Updates holen
echo "📥 Updates holen..."  
git pull origin main

# GUI starten
echo "🖥️ GUI starten..."
python3 main.py

echo "👋 Futterkarre beendet."