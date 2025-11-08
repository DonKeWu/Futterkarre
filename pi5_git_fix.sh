#!/bin/bash

# 🔧 Pi5 Git Repository Reparatur
# Einfach antippen am Desktop!

echo "🔧 Git Repository reparieren..."

cd /home/daniel

# Korruptes Repository sichern
if [ -d "Futterkarre" ]; then
    echo "📦 Backup von korruptem Repository..."
    mv Futterkarre Futterkarre_corrupt_$(date +%H%M)
fi

# Frisch klonen
echo "📥 Frisches Repository klonen..."
git clone https://github.com/DonKeWu/Futterkarre.git

echo "✅ Repository repariert!"
echo "💡 Jetzt 'Futterkarre Starten' antippen!"

# 3 Sekunden warten damit man es lesen kann
sleep 3