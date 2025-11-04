# 🐎 Ernährungsphysiologische Richtwerte für Pferde (Vereinfacht)

## 📊 **Nährstoffbedarf pro 100kg Körpergewicht/Tag (Die 3 Wichtigsten)**

### **🌾 Hauptnährstoffe (Pflichtbestandteile):**

| Nährstoff | Mindestbedarf | Optimaler Bereich | Obergrenze | Einheit | Farbe-Code |
|-----------|---------------|-------------------|------------|---------|------------|
| **Rohprotein (Eiweiß)** | 0.5 kg | 0.5 - 0.8 kg | 0.8 kg | g/100kg KG | 🟢 Grün: Optimal<br>🟠 Orange: Mangel<br>🔴 Rot: Überschuss |
| **Rohfaser** | 1.0 kg | 1.0 - 1.5 kg | 1.5 kg | g/100kg KG | 🟢 Grün: Optimal<br>🟠 Orange: Mangel<br>🔴 Rot: Überschuss |

### **⚠️ Kritischer Inhaltsstoff (Nur Obergrenze):**

| Nährstoff | Unbedenklich | Vorsicht | Gefährlich | Einheit | Risiko |
|-----------|--------------|----------|------------|---------|--------|
| **Fruktan** | < 0.035 kg | 0.035 - 0.05 kg | > 0.05 kg | g/100kg KG | **HUFREHE-RISIKO** |

---

## 🔍 **Beispielrechnung für 350kg Pferd:**

### **Täglicher Nährstoffbedarf:**
```python
pferd_gewicht = 350  # kg
gewicht_faktor = pferd_gewicht / 100.0  # = 3.5

# Mindestbedarf pro Tag:
rohprotein_min = 500 * 3.5 = 1750g  # = 1.75kg Eiweiß  
rohfaser_min = 1000 * 3.5 = 3500g   # = 3.5kg Rohfaser

# Kritische Obergrenze:
fruktan_max = 50 * 3.5 = 175g       # = 0.175kg Fruktan (HUFREHE!)
```

### **Fütterungs-Beispiel (4.5kg Heulage):**
```python
# Heulage Eigen 2025: Nährwerte pro kg
rohprotein_prozent = 12.1     # %
rohfaser_prozent = 29.6       # % (aus CSV korrigiert)
fruktan_prozent = 3.7         # %

# Bei 4.5kg gefüttert:
rohprotein_g = (12.1/100) * 4500 = 545g    # ✅ Grün (über Mindestbedarf)
rohfaser_g = (29.6/100) * 4500 = 1332g     # ⚠️ Orange (unter Mindestbedarf!) 
fruktan_g = (3.7/100) * 4500 = 167g        # ⚠️ Orange (knapp unter kritischer Grenze)
```

---

## 🎯 **Farb-Codierung im System:**

### **🟢 GRÜN (Optimal):**
- **Rohprotein:** 1.75 - 2.8kg für 350kg Pferd
- **Rohfaser:** 3.5 - 5.25kg für 350kg Pferd  
- **Fruktan:** unter 122g für 350kg Pferd
- **Bedeutung:** Pferd wird ernährungsphysiologisch korrekt versorgt

### **🟠 ORANGE (Vorsicht):**
- **Rohprotein/Rohfaser:** Mangel - mehr füttern empfohlen
- **Fruktan:** 122-175g - Obergrenze erreicht, vorsichtig sein
- **Bedeutung:** Fütterung anpassen oder ergänzen

### **🔴 ROT (Kritisch):**
- **Rohprotein/Rohfaser:** Deutlicher Mangel oder Überschuss
- **Fruktan:** über 175g - **AKUTE HUFREHE-GEFAHR!**
- **Bedeutung:** Sofortige Fütterungsanpassung erforderlich

---

## 📚 **Warum nur diese 3 Werte?**

### **❌ Weggelassen (vernachlässigbar bei Grundfutter):**
- **Rohfett:** Gras/Heu hat < 3% Fett, daher irrelevant
- **Gesamtzucker:** Bei Grobfutter meist im akzeptablen Bereich
- **Trockenmasse:** Rechnerische Größe, nicht ernährungsphysiologisch kritisch

### **✅ Die 3 Wichtigsten:**
1. **Rohprotein:** Grundbaustein für Muskulatur und Immunsystem
2. **Rohfaser:** Lebenswichtig für Pferdeverdauung (Wiederkäuer-ähnlich)
3. **Fruktan:** Einziger Wert mit akuter Lebensgefahr (Hufrehe)

---

## 🖥️ **UI-Design Optimierungen:**

### **Größere Anzeige (30pt statt 15pt):**
- Bessere Lesbarkeit auf Touch-Display
- Eindeutige Farberkennung auch bei Sonnenlicht
- Weniger Ablenkung durch unwichtige Werte

### **Fokussierung auf das Wesentliche:**
- **3 statt 8 Werte** reduziert kognitive Belastung
- **Sofortige Erkennung** kritischer Zustände
- **Praktikable Entscheidungshilfe** für Fütterung

---

## ⚖️ **Praktische Umsetzung:**

### **Echtzeit-Monitoring:**
1. **Kontinuierliche Berechnung** der 3 Kernwerte
2. **Sofortige Farbkodierung** zur visuellen Bewertung  
3. **Physiologische Anpassung** an individuelles Pferdegewicht
4. **Präventive Warnungen** vor Hufrehe-Risiko

### **Decision Support:**
- ✅ **Alle Grün:** Weiter füttern bis Sättigung
- ⚠️ **Orange bei Protein/Faser:** Mehr füttern oder ergänzen
- ⚠️ **Orange bei Fruktan:** Vorsichtig reduzieren
- 🛑 **Rot bei Fruktan:** SOFORT STOPPEN - Hufrehe-Gefahr!

---

**💡 Das vereinfachte 3-Werte-System bietet maximum Sicherheit bei optimaler Benutzerfreundlichkeit! 🐎**