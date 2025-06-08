# futter_sim.py
USE_SIMULATION = True

def setze_simulation(an):
    global USE_SIMULATION
    USE_SIMULATION = an

def berechne_naehrwerte(heu_daten, entnommene_menge_kg):
    """
    Berechnet die Nährwerte für eine bestimmte entnommene Menge Heu.
    heu_daten: dict mit Nährwerten pro 100g (aus CSV)
    entnommene_menge_kg: float, Menge in kg
    """
    faktor = entnommene_menge_kg * 10 # 1kg = 10*100g
    return {
        "Rohprotein": float(heu_daten.get("Rohprotein", 0)) * faktor,
        "Rohfaser": float(heu_daten.get("Rohfaser", 0)) * faktor,
        "Gesamtzucker": float(heu_daten.get("Gesamtzucker", 0)) * faktor,
        "Fruktan": float(heu_daten.get("Fruktan", 0)) * faktor,
        "ME-Pferd": float(heu_daten.get("ME-Pferd", 0)) * faktor,
        "pcv_XP": float(heu_daten.get("pcv_XP", 0)) * faktor,
    }

def simuliere_entnahme(aktueller_wert, entnahme_kg):
    """Simuliert die Entnahme von Futter (nur im Simulationsmodus)"""
    if not USE_SIMULATION:
        return aktueller_wert
    return max(0.0, aktueller_wert - entnahme_kg)
