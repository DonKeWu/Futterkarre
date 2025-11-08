#!/bin/bash

# 🔧 EINFACH: Komplette Futterkarre neu laden
# Ausführen: cd ~/Futterkarre && ./pi5_git_fix.sh

echo "🔧 Futterkarre komplett neu laden..."

# Ins Home-Verzeichnis
cd ~

# Alles löschen und neu
echo "�️ Alten Futterkarre-Ordner löschen..."
rm -rf Futterkarre

# Frisch klonen  
echo "📥 Frisch von GitHub laden..."
git clone https://github.com/DonKeWu/Futterkarre.git

echo "✅ Fertig! Futterkarre ist sauber!"
echo "💡 Jetzt: cd ~/Futterkarre && ./pi5_start_futterkarre.sh"