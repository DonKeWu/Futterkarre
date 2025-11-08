#!/bin/bash

# 🚀 Futterkarre GUI Starten 
# Einfach antippen am Desktop!

echo "🚀 Futterkarre wird gestartet..."

cd /home/daniel/Futterkarre

# Git pull (falls Repository OK ist)
echo "📥 Updates holen..."
git pull origin main 2>/dev/null || echo "⚠️ Git pull fehlgeschlagen - Repository OK?"

# PyQt5 GUI starten
echo "🖥️ GUI wird gestartet..."
python3 main.py

echo "👋 Futterkarre beendet."