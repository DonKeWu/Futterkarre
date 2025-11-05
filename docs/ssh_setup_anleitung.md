# SSH Setup für Raspberry Pi 5 - Futterkarre Projekt

## 🎯 Ziel
Fernzugriff vom Hauptrechner auf den Raspberry Pi 5 per SSH einrichten.

## 📋 Voraussetzungen

### Raspberry Pi 5 Seite:
- Raspberry Pi OS installiert
- WiFi/Ethernet-Verbindung aktiv
- SSH aktiviert

### Hauptrechner Seite:
- SSH-Client verfügbar (bei Linux standardmäßig vorhanden)
- Netzwerkverbindung zum RPi5

## 🛠 Schritt-für-Schritt Anleitung

### 1. SSH auf Raspberry Pi 5 aktivieren

**Option A: Bei der Ersteinrichtung (Raspberry Pi Imager)**
```bash
# Im Raspberry Pi Imager:
# 1. Erweiterte Optionen (Zahnrad-Symbol)
# 2. SSH aktivieren
# 3. Benutzername/Passwort setzen
# 4. WiFi konfigurieren
```

**Option B: Nachträglich aktivieren**
```bash
# Direkt am RPi5 (Tastatur/Monitor):
sudo systemctl enable ssh
sudo systemctl start ssh

# Oder über raspi-config:
sudo raspi-config
# → Interface Options → SSH → Enable
```

### 2. IP-Adresse des RPi5 herausfinden

**Auf dem RPi5:**
```bash
hostname -I
# oder
ip addr show wlan0  # für WiFi
ip addr show eth0   # für Ethernet
```

**Vom Hauptrechner aus (Netzwerk scannen):**
```bash
# Nmap installieren falls nicht vorhanden:
sudo apt install nmap  # Ubuntu/Debian
# oder
sudo dnf install nmap  # Fedora

# Netzwerk scannen:
nmap -sn 192.168.1.0/24  # Anpassen an Ihr Netzwerk
# oder
arp -a | grep -i raspberry
```

### 3. SSH-Verbindung herstellen

**Grundlegende Verbindung:**
```bash
# Format: ssh benutzername@ip-adresse
ssh pi@192.168.1.100  # Beispiel-IP, anpassen!

# Beim ersten Mal Fingerprint bestätigen:
# "Are you sure you want to continue connecting (yes/no/[fingerprint])?" → yes
```

**Mit Custom Port (falls geändert):**
```bash
ssh -p 2222 pi@192.168.1.100
```

### 4. SSH-Schlüssel für passwortlosen Zugang (empfohlen)

**SSH-Schlüssel generieren (auf Hauptrechner):**
```bash
ssh-keygen -t rsa -b 4096 -C "futterkarre@hauptrechner"
# Enter bei allen Prompts für Standardwerte
```

**Öffentlichen Schlüssel auf RPi5 kopieren:**
```bash
ssh-copy-id pi@192.168.1.100
# Passwort eingeben
```

**Test der schlüsselbasierten Anmeldung:**
```bash
ssh pi@192.168.1.100
# Sollte jetzt ohne Passwort funktionieren
```

### 5. SSH-Konfiguration optimieren

**SSH-Config erstellen/bearbeiten (auf Hauptrechner):**
```bash
nano ~/.ssh/config
```

**Konfiguration hinzufügen:**
```
Host futterkarre
    HostName 192.168.1.100
    User pi
    Port 22
    IdentityFile ~/.ssh/id_rsa
    ServerAliveInterval 60
    ServerAliveCountMax 3
```

**Vereinfachte Verbindung:**
```bash
ssh futterkarre
```

## 🔒 Sicherheitsmaßnahmen

### 1. Standard-Passwort ändern
```bash
# Auf dem RPi5:
passwd
```

### 2. SSH-Port ändern (optional)
```bash
# Auf dem RPi5:
sudo nano /etc/ssh/sshd_config

# Zeile ändern:
# Port 22
# zu:
Port 2222

# SSH-Dienst neu starten:
sudo systemctl restart ssh
```

### 3. Passwort-Authentifizierung deaktivieren (nach SSH-Schlüssel Setup)
```bash
# Auf dem RPi5:
sudo nano /etc/ssh/sshd_config

# Ändern:
PasswordAuthentication no
PubkeyAuthentication yes

# SSH-Dienst neu starten:
sudo systemctl restart ssh
```

## 📱 Praktische SSH-Befehle

### Dateien übertragen (SCP)
```bash
# Vom Hauptrechner zum RPi5:
scp /pfad/zur/datei.py pi@192.168.1.100:/home/pi/Futterkarre-2/

# Vom RPi5 zum Hauptrechner:
scp pi@192.168.1.100:/home/pi/logs/app.log ./

# Ganzen Ordner übertragen:
scp -r ./lokaler_ordner/ pi@192.168.1.100:/home/pi/
```

### Remote-Befehle ausführen
```bash
# Einzelner Befehl:
ssh pi@192.168.1.100 "cd /home/pi/Futterkarre-2 && python3 main.py"

# System-Status abfragen:
ssh pi@192.168.1.100 "uptime && df -h && free -h"
```

### Tunnel für GUI-Anwendungen (X11 Forwarding)
```bash
ssh -X pi@192.168.1.100
# Dann GUI-Anwendungen starten wie:
# python3 main.py  # Falls GUI verwendet wird
```

## 🚨 Troubleshooting

### Connection refused
```bash
# SSH-Status prüfen:
ssh pi@192.168.1.100 "sudo systemctl status ssh"

# Port prüfen:
ssh pi@192.168.1.100 "sudo netstat -tlnp | grep :22"
```

### Host key verification failed
```bash
# Bekannte Hosts zurücksetzen:
ssh-keygen -R 192.168.1.100
```

### Timeout-Probleme
```bash
# Ping-Test:
ping 192.168.1.100

# Router/Firewall prüfen
```

## 🔄 Integration in Entwicklungsworkflow

### VS Code Remote-SSH Extension
1. VS Code Extension "Remote - SSH" installieren
2. Ctrl+Shift+P → "Remote-SSH: Connect to Host"
3. "futterkarre" auswählen
4. Direktes Bearbeiten auf dem RPi5

### Automatische Synchronisation
```bash
# Script für automatisches Deployment:
#!/bin/bash
# deploy.sh
rsync -avz --exclude '.git' --exclude '__pycache__' \
  ./ pi@192.168.1.100:/home/pi/Futterkarre-2/

ssh pi@192.168.1.100 "cd /home/pi/Futterkarre-2 && python3 main.py"
```

## 📝 Nützliche Aliase (für ~/.bashrc)

```bash
# SSH-Aliase
alias fk-ssh='ssh futterkarre'
alias fk-logs='ssh futterkarre "tail -f /home/pi/Futterkarre-2/logs/*.log"'
alias fk-status='ssh futterkarre "cd /home/pi/Futterkarre-2 && python3 -c \"import main; print(\\\"System OK\\\")\""'
alias fk-sync='rsync -avz --exclude .git --exclude __pycache__ ./ futterkarre:/home/pi/Futterkarre-2/'
```

## 🎯 Nächste Schritte

1. [ ] SSH auf RPi5 aktivieren
2. [ ] IP-Adresse ermitteln
3. [ ] Erste SSH-Verbindung testen
4. [ ] SSH-Schlüssel einrichten
5. [ ] VS Code Remote-SSH konfigurieren
6. [ ] Deployment-Script erstellen

---

**Datum:** 5. November 2025  
**Projekt:** Futterkarre-2  
**Autor:** Entwicklungsteam