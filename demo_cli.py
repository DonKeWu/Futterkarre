#!/usr/bin/env python3
"""
Command-line demo of Futterkarre-2 functionality
Demonstrates the core features without GUI (no PyQt5 required)
"""
import sys
import os
from datetime import datetime, timedelta
import time

# Add src to path
sys.path.insert(0, os.path.dirname(__file__))

from src.models import Horse, FeedRecord, DataManager
from src.hardware import SimulatedScale
import config.settings as settings


def print_header(title):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def demo_models():
    """Demonstrate model functionality"""
    print_header("DEMO: Data Models")
    
    # Create horses
    print("\n1. Creating horses...")
    horse1 = Horse(1, "Apollo", "Hannoveraner", 8, 550.0, "Leistungssportler")
    horse2 = Horse(2, "Luna", "Haflinger", 5, 480.0, "Freizeitpferd")
    horse3 = Horse(3, "Thunder", "Araber", 12, 450.0)
    
    print(f"   - {horse1}")
    print(f"   - {horse2}")
    print(f"   - {horse3}")
    
    # Create feed records
    print("\n2. Creating feed records...")
    record1 = FeedRecord(1, 1, "Heu", 5.50, datetime.now(), "Morgenfütterung")
    record2 = FeedRecord(2, 1, "Pellets", 2.00, datetime.now())
    record3 = FeedRecord(3, 2, "Heulage", 6.20, datetime.now())
    
    print(f"   - {record1}")
    print(f"   - {record2}")
    print(f"   - {record3}")


def demo_data_manager():
    """Demonstrate data manager functionality"""
    print_header("DEMO: Data Manager (CSV Persistence)")
    
    dm = DataManager()
    
    # Add horses
    print("\n1. Adding horses to database...")
    horses = [
        Horse(1, "Apollo", "Hannoveraner", 8, 550.0),
        Horse(2, "Luna", "Haflinger", 5, 480.0),
        Horse(3, "Thunder", "Araber", 12, 450.0),
    ]
    
    for horse in horses:
        dm.add_horse(horse)
        print(f"   ✓ Added: {horse.name}")
    
    # List all horses
    print("\n2. Listing all horses...")
    all_horses = dm.get_all_horses()
    for horse in all_horses:
        print(f"   - ID {horse.horse_id}: {horse.name} ({horse.breed}, {horse.age} Jahre)")
    
    # Add feed records
    print("\n3. Adding feed records...")
    records = [
        FeedRecord(None, 1, "Heu", 5.50, datetime.now(), "Morgenfütterung"),
        FeedRecord(None, 1, "Pellets", 2.00, datetime.now()),
        FeedRecord(None, 2, "Heulage", 6.20, datetime.now()),
        FeedRecord(None, 3, "Heu", 4.80, datetime.now()),
    ]
    
    for record in records:
        dm.add_feed_record(record)
        horse = dm.get_horse_by_id(record.horse_id)
        print(f"   ✓ Recorded: {record.weight:.2f}kg {record.feed_type} for {horse.name}")
    
    # Show statistics
    print("\n4. Feed statistics...")
    all_records = dm.get_all_feed_records()
    total_weight = sum(r.weight for r in all_records)
    print(f"   - Total feedings: {len(all_records)}")
    print(f"   - Total weight: {total_weight:.2f} kg")
    
    # Show records per horse
    for horse in all_horses:
        horse_records = dm.get_all_feed_records(horse_id=horse.horse_id)
        horse_total = sum(r.weight for r in horse_records)
        print(f"   - {horse.name}: {len(horse_records)} feedings, {horse_total:.2f} kg")


def demo_scale():
    """Demonstrate scale functionality"""
    print_header("DEMO: Simulated Scale")
    
    scale = SimulatedScale()
    
    print("\n1. Initializing scale...")
    if scale.initialize():
        print("   ✓ Scale initialized successfully")
    
    print("\n2. Checking scale status...")
    print(f"   - Scale ready: {scale.is_ready()}")
    
    print("\n3. Initial weight reading...")
    weight = scale.get_weight()
    print(f"   - Current weight: {weight:.2f} kg")
    
    print("\n4. Taring scale...")
    scale.tare()
    weight = scale.get_weight()
    print(f"   - Weight after tare: {weight:.2f} kg")
    
    print("\n5. Simulating weight placement...")
    print("   - Placing 5.5 kg on scale...")
    scale.set_weight(5.5)
    time.sleep(0.2)
    
    # Take multiple readings
    print("   - Taking 5 weight readings:")
    for i in range(5):
        weight = scale.get_weight()
        print(f"     Reading {i+1}: {weight:.2f} kg")
        time.sleep(0.1)
    
    print("\n6. Adding more weight...")
    print("   - Adding 2.0 kg...")
    scale.add_weight(2.0)
    weight = scale.get_weight()
    print(f"   - New weight: {weight:.2f} kg")
    
    print("\n7. Removing weight...")
    print("   - Removing 3.0 kg...")
    scale.remove_weight(3.0)
    weight = scale.get_weight()
    print(f"   - Final weight: {weight:.2f} kg")
    
    print("\n8. Cleaning up...")
    scale.cleanup()
    print("   ✓ Scale cleaned up")


def demo_complete_workflow():
    """Demonstrate a complete feeding workflow"""
    print_header("DEMO: Complete Feeding Workflow")
    
    # Initialize components
    print("\n1. Initializing system...")
    dm = DataManager()
    scale = SimulatedScale()
    scale.initialize()
    print("   ✓ System initialized")
    
    # Check for horses
    print("\n2. Checking horse database...")
    horses = dm.get_all_horses()
    if not horses:
        print("   ℹ No horses in database, adding sample horses...")
        sample_horses = [
            Horse(1, "Apollo", "Hannoveraner", 8, 550.0),
            Horse(2, "Luna", "Haflinger", 5, 480.0),
        ]
        for horse in sample_horses:
            dm.add_horse(horse)
        horses = dm.get_all_horses()
    
    print(f"   - Found {len(horses)} horses")
    for horse in horses:
        print(f"     • {horse.name}")
    
    # Simulate feeding Apollo
    print("\n3. Feeding Apollo...")
    apollo = horses[0]
    
    print("   a) Taring scale...")
    scale.tare()
    print(f"      Weight: {scale.get_weight():.2f} kg")
    
    print("   b) Placing hay on scale...")
    scale.set_weight(5.5)
    time.sleep(0.2)
    measured_weight = scale.get_weight()
    print(f"      Measured: {measured_weight:.2f} kg")
    
    print("   c) Recording feeding...")
    record = FeedRecord(
        record_id=None,
        horse_id=apollo.horse_id,
        feed_type="Heu",
        weight=measured_weight,
        timestamp=datetime.now(),
        notes="Automated feeding demo"
    )
    dm.add_feed_record(record)
    print(f"      ✓ Recorded: {measured_weight:.2f}kg Heu for {apollo.name}")
    
    # Show today's feeding summary
    print("\n4. Today's feeding summary...")
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = datetime.now()
    today_records = dm.get_feed_records_by_date_range(today_start, today_end)
    
    print(f"   - Total feedings today: {len(today_records)}")
    for rec in today_records:
        horse = dm.get_horse_by_id(rec.horse_id)
        print(f"     • {horse.name}: {rec.weight:.2f}kg {rec.feed_type} at {rec.timestamp.strftime('%H:%M')}")
    
    # Cleanup
    scale.cleanup()
    print("\n   ✓ Workflow complete!")


def main():
    """Main demo function"""
    print("\n" + "=" * 60)
    print("  🚜 Futterkarre-2 - Command-Line Demo")
    print("  Intelligente Futterwaage für Pferde")
    print("=" * 60)
    
    # Run all demos
    demo_models()
    demo_scale()
    demo_data_manager()
    demo_complete_workflow()
    
    print_header("Demo Complete")
    print("\n✓ All demos completed successfully!")
    print("\nTo run the full GUI application:")
    print("  python3 main.py")
    print("\nNote: GUI requires PyQt5 and works best on Raspberry Pi with touchscreen")
    print()


if __name__ == "__main__":
    main()
