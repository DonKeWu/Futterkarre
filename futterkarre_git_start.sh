#!/bin/bash
# Futterkarre Git-Update und Start Script
# Automatisches Git-Pull vor dem Start der Anwendung

# Farben für Terminal-Output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚜 Futterkarre - Git Update & Start${NC}"
echo "============================================"

# Wechsel zum Projektverzeichnis - ANPASSBAR!
PROJECT_DIR="/home/daniel/Projekte/Futterkarre-2"

# Prüfe ob Verzeichnis existiert, sonst alternative Pfade probieren
if [ ! -d "$PROJECT_DIR" ]; then
    echo -e "${RED}❌ Projektverzeichnis nicht gefunden: $PROJECT_DIR${NC}"
    echo -e "${BLUE}🔍 Suche nach alternativen Pfaden...${NC}"
    
    # Alternative Pfade probieren
    ALT_PATHS=(
        "/home/daniel/Dokumente/HOF/Futterwagen/Python/Futterkarre-2"
        "/home/daniel/Futterkarre-2"
        "/home/daniel/Desktop/Futterkarre-2"
        "$(pwd)"
    )
    
    for path in "${ALT_PATHS[@]}"; do
        if [ -d "$path" ] && [ -f "$path/main.py" ]; then
            PROJECT_DIR="$path"
            echo -e "${GREEN}✅ Projekt gefunden in: $PROJECT_DIR${NC}"
            break
        fi
    done
    
    if [ ! -f "$PROJECT_DIR/main.py" ]; then
        echo -e "${RED}❌ main.py nicht gefunden! Bitte Pfad manuell anpassen.${NC}"
        echo "Aktuelle Position: $(pwd)"
        exit 1
    fi
fi

cd "$PROJECT_DIR"

# Git Status prüfen
echo -e "${BLUE}📋 Git Status prüfen...${NC}"
git status --porcelain

# Unkommittierte Änderungen sichern (falls vorhanden)
if [[ -n $(git status --porcelain) ]]; then
    echo -e "${BLUE}💾 Lokale Änderungen gefunden - Sicherung erstellen...${NC}"
    git stash push -m "Auto-Stash vor Git-Pull $(date '+%Y-%m-%d %H:%M:%S')"
fi

# Git Pull ausführen
echo -e "${BLUE}⬇️  Git Pull von GitHub...${NC}"
git pull origin main

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Git Pull erfolgreich${NC}"
else
    echo -e "${RED}❌ Git Pull fehlgeschlagen${NC}"
    echo "Versuche trotzdem zu starten..."
fi

# 2 Sekunden warten für Benutzer-Feedback
sleep 2

# Python-Umgebung aktivieren (falls conda verwendet wird)
if command -v conda &> /dev/null; then
    echo -e "${BLUE}🐍 Conda-Umgebung aktivieren...${NC}"
    source /home/daniel/miniconda3/etc/profile.d/conda.sh
    conda activate futterkarre
fi

# Hauptanwendung starten
echo -e "${GREEN}🚀 Futterkarre wird gestartet...${NC}"
echo "============================================"

# Display-Variable setzen für GUI
export DISPLAY=:0

# Python-Anwendung starten
python3 main.py

# Exit-Code prüfen
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Anwendung normal beendet${NC}"
else
    echo -e "${RED}❌ Anwendung mit Fehler beendet (Exit-Code: $?)${NC}"
    echo "Drücke Enter zum Fortfahren..."
    read
fi