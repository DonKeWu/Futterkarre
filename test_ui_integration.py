#!/usr/bin/env python3
"""
Test der UI-Integration von Pi5-Tests in Waagen-Kalibrierung
"""

import sys
import os

# Pfad für Imports
sys.path.append('/home/daniel/Dokumente/HOF/Futterwagen/Python/Futterkarre')

def test_ui_integration():
    """Testet die UI-Integration ohne PyQt5 GUI"""
    print("🧪 TESTE UI-INTEGRATION (ohne GUI)")
    print("=" * 50)
    
    try:
        # 1. Import Test
        from views.waagen_kalibrierung import WaagenKalibrierung, Pi5SystemTester
        print("✅ Import erfolgreich")
        
        # 2. Pi5SystemTester separat testen
        print("\n📋 Pi5SystemTester Test:")
        tester = Pi5SystemTester()
        print("✅ Pi5SystemTester erstellt")
        
        # Kurzer Test ohne GUI
        tester.test_python_environment()
        
        print("\n✅ UI-Integration Test erfolgreich!")
        return True
        
    except Exception as e:
        print(f"❌ UI-Integration Test fehlgeschlagen: {e}")
        import traceback
        print(traceback.format_exc())
        return False

def test_with_gui():
    """Testet mit PyQt5 GUI (falls verfügbar)"""
    print("\n🖥️ TESTE MIT GUI")
    print("=" * 50)
    
    try:
        from PyQt5.QtWidgets import QApplication
        from views.waagen_kalibrierung import WaagenKalibrierung
        
        app = QApplication(sys.argv)
        print("✅ QApplication erstellt")
        
        # WaagenKalibrierung erstellen
        window = WaagenKalibrierung()
        print("✅ WaagenKalibrierung erstellt")
        
        # UI-Komponenten prüfen
        if hasattr(window, 'test_output_area'):
            print("✅ Test-Output-Area vorhanden")
        else:
            print("⚠️ Test-Output-Area nicht gefunden")
            
        if hasattr(window, 'btn_quick_test'):
            print("✅ Quick-Test-Button vorhanden")
        else:
            print("⚠️ Quick-Test-Button nicht gefunden")
            
        if hasattr(window, 'btn_hardware_test'):
            print("✅ Hardware-Test-Button vorhanden")
        else:
            print("⚠️ Hardware-Test-Button nicht gefunden")
        
        # Kurz anzeigen für Test
        window.resize(1000, 800)
        window.show()
        
        print("✅ Fenster angezeigt - schließe es manuell")
        print("🎯 Teste die Pi5-Test-Buttons in der GUI!")
        
        # Event Loop für kurze Zeit
        import time
        for i in range(5):
            app.processEvents()
            time.sleep(1)
            if not window.isVisible():
                break
                
        print("✅ GUI Test abgeschlossen")
        return True
        
    except Exception as e:
        print(f"❌ GUI Test fehlgeschlagen: {e}")
        import traceback
        print(traceback.format_exc())
        return False

def main():
    print("🚀 TESTE WAAGEN-KALIBRIERUNG MIT PI5-TESTS")
    print("=" * 60)
    
    # Test 1: UI Integration (ohne GUI)
    ui_ok = test_ui_integration()
    
    # Test 2: Mit GUI (falls Display verfügbar)
    gui_ok = False
    if ui_ok:
        try:
            gui_ok = test_with_gui()
        except Exception as e:
            print(f"⚠️ GUI Test übersprungen: {e}")
    
    # Ergebnis
    print("\n📊 TEST-ERGEBNIS")
    print("=" * 30)
    print(f"UI Integration: {'✅ OK' if ui_ok else '❌ FEHLER'}")
    print(f"GUI Test: {'✅ OK' if gui_ok else '⚠️ Übersprungen/Fehler'}")
    
    if ui_ok:
        print("\n🎉 TESTS ERFOLGREICH!")
        print("Die Pi5-Tests sind in die Waagen-Kalibrierung integriert.")
    else:
        print("\n❌ TESTS FEHLGESCHLAGEN!")
        print("Prüfe die Fehler oben.")

if __name__ == "__main__":
    main()