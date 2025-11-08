#!/usr/bin/env python3
"""
WeightManager - Zentrale Gewichtsverwaltung (Hardware-Only)
Singleton Pattern für einheitliche Gewichts-Datenquelle

Version: 1.5.0 (Hardware-Ready)
- Simulation komplett entfernt
- Direkte HX711-Hardware Integration
- Resource-optimiert für Pi5
"""

import logging
import threading
import time
from abc import ABC, abstractmethod
from typing import Optional, Dict, Callable, Any
from dataclasses import dataclass, field
from datetime import datetime
from threading import Lock

logger = logging.getLogger(__name__)


class WeightSensorInterface(ABC):
    """Abstract Interface für Gewichtssensoren"""
    @abstractmethod
    def read_weight(self) -> float:
        pass

@dataclass
class WeightState:
    """Hardware-Gewichtszustand"""
    current_weight: float = 0.0
    last_update: float = field(default_factory=time.time)
    hardware_available: bool = False
    error_count: int = 0
    last_error: Optional[str] = None

class WeightManager:
    """
    Singleton für Hardware-Gewichtsverwaltung
    
    Nur für echte HX711 Hardware (4 Wägezellen)
    - Keine Simulation mehr
    - Direkte Hardware-Integration
    """
    
    _instance: Optional['WeightManager'] = None
    _lock = Lock()
    
    def __new__(cls) -> 'WeightManager':
        """Singleton Pattern"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        # Verhindere Mehrfach-Initialisierung
        if hasattr(self, '_initialized'):
            return
            
        self._initialized = True
        self.state = WeightState()
        self._observers: Dict[str, Callable[[float], None]] = {}
        
        # Hardware-Verfügbarkeit prüfen
        self._detect_hardware()
        
        logger.info(f"WeightManager initialisiert - Hardware verfügbar: {self.state.hardware_available}")
    
    def _detect_hardware(self):
        """Prüft Hardware-Verfügbarkeit und initialisiert entsprechend"""
        try:
            from hardware.hx711_real import lese_gewicht_hx711, hx_sensors
            if hx_sensors:  # Hardware erfolgreich initialisiert
                self.state.hardware_available = True
                logger.info("✅ HX711 Hardware erkannt und initialisiert")
            else:
                logger.error("❌ HX711-Sensoren nicht verfügbar")
                self.state.hardware_available = False
                
        except ImportError as e:
            logger.error(f"❌ Hardware-Module nicht importierbar: {e}")
            self.state.hardware_available = False
        except Exception as e:
            logger.error(f"❌ Hardware-Erkennung fehlgeschlagen: {e}")
            self.state.hardware_available = False
    
    def read_weight(self, use_cache: bool = True) -> float:
        """
        Liest aktuelles Gewicht von der Hardware
        
        Args:
            use_cache: Verwende zwischengespeicherten Wert wenn verfügbar
            
        Returns:
            Gewicht in kg
        """
        if not self.state.hardware_available:
            logger.warning("Hardware nicht verfügbar - gebe 0.0 zurück")
            return 0.0
            
        current_time = time.time()
        
        # Cache-Logik: Nur alle 100ms neu lesen (Performance)
        if use_cache and (current_time - self.state.last_update) < 0.1:
            return self.state.current_weight
        
        try:
            from hardware.hx711_real import lese_gewicht_hx711
            weight = lese_gewicht_hx711()
            
            # State aktualisieren
            self.state.current_weight = max(0.0, weight)  # Negative Gewichte verhindern
            self.state.last_update = current_time
            self.state.error_count = 0
            self.state.last_error = None
            
            # Observer benachrichtigen
            self._notify_observers(self.state.current_weight)
            
            return self.state.current_weight
            
        except Exception as e:
            self.state.error_count += 1
            self.state.last_error = str(e)
            logger.error(f"Gewichtslesung fehlgeschlagen: {e}")
            
            return self.state.current_weight  # Letzten gültigen Wert zurückgeben
    
    def read_individual_cells(self) -> list[float]:
        """
        Liest die 4 Wägezellen einzeln (für Kalibrierung/Debugging)
        
        Returns:
            Liste mit 4 Gewichtswerten [VL, VR, HL, HR]
        """
        if not self.state.hardware_available:
            return [0.0, 0.0, 0.0, 0.0]
            
        try:
            from hardware.hx711_real import lese_einzelzellwerte_hx711
            return lese_einzelzellwerte_hx711()
                
        except Exception as e:
            logger.error(f"Einzelzellwerte nicht lesbar: {e}")
            return [0.0, 0.0, 0.0, 0.0]
    
    def register_observer(self, name: str, callback: Callable[[float], None]):
        """
        Registriert einen Observer für Gewichtsupdates
        
        Args:
            name: Eindeutige ID des Observers
            callback: Funktion die bei Gewichtsänderung aufgerufen wird
        """
        self._observers[name] = callback
        logger.debug(f"Observer '{name}' registriert")
    
    def unregister_observer(self, name: str):
        """Entfernt einen Observer"""
        if name in self._observers:
            del self._observers[name]
            logger.debug(f"Observer '{name}' entfernt")
    
    def _notify_observers(self, weight: float):
        """Benachrichtigt alle Observer über Gewichtsänderung"""
        for name, callback in self._observers.items():
            try:
                callback(weight)
            except Exception as e:
                logger.error(f"Observer '{name}' Fehler: {e}")
    
    def get_status(self) -> Dict[str, Any]:
        """
        Gibt aktuellen Status zurück
        
        Returns:
            Status-Dictionary mit Hardware-Details
        """
        return {
            'hardware_available': self.state.hardware_available,
            'current_weight': self.state.current_weight,
            'last_update': self.state.last_update,
            'error_count': self.state.error_count,
            'last_error': self.state.last_error
        }
    
    def tare_scale(self):
        """Nullt die Waage (Tara-Funktion)"""
        if not self.state.hardware_available:
            logger.warning("Tara nicht möglich - Hardware nicht verfügbar")
            return False
            
        try:
            from hardware.hx711_real import nullpunkt_setzen_alle
            nullpunkt_setzen_alle()
            logger.info("Waage genullt (Tara)")
            return True
            
        except Exception as e:
            logger.error(f"Tara fehlgeschlagen: {e}")
            return False
    
    def cleanup(self):
        """Aufräumen beim Programm-Ende"""
        logger.info("WeightManager Cleanup...")
        
        # Observer entfernen
        self._observers.clear()
        
        logger.info("WeightManager Cleanup abgeschlossen")

# Globale Instanz - späte Initialisierung
_weight_manager_instance: Optional[WeightManager] = None

def get_weight_manager() -> WeightManager:
    """Gibt die globale WeightManager-Instanz zurück (Lazy Loading)"""
    global _weight_manager_instance
    if _weight_manager_instance is None:
        _weight_manager_instance = WeightManager()
    return _weight_manager_instance