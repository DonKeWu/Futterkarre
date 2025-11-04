"""
Unit tests for data models
"""
import unittest
import sys
import os
from datetime import datetime
import tempfile
import shutil

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models import Horse, FeedRecord, DataManager


class TestHorse(unittest.TestCase):
    """Test Horse model"""
    
    def test_horse_creation(self):
        """Test creating a horse"""
        horse = Horse(
            horse_id=1,
            name="Apollo",
            breed="Hannoveraner",
            age=8,
            weight=550.0,
            notes="Test horse"
        )
        self.assertEqual(horse.horse_id, 1)
        self.assertEqual(horse.name, "Apollo")
        self.assertEqual(horse.breed, "Hannoveraner")
    
    def test_horse_to_dict(self):
        """Test converting horse to dictionary"""
        horse = Horse(horse_id=1, name="Luna", breed="Haflinger", age=5)
        data = horse.to_dict()
        self.assertEqual(data['horse_id'], 1)
        self.assertEqual(data['name'], "Luna")
        self.assertEqual(data['breed'], "Haflinger")
    
    def test_horse_from_dict(self):
        """Test creating horse from dictionary"""
        data = {
            'horse_id': '2',
            'name': 'Thunder',
            'breed': 'Araber',
            'age': '12',
            'weight': '450.0',
            'notes': 'Test'
        }
        horse = Horse.from_dict(data)
        self.assertEqual(horse.horse_id, 2)
        self.assertEqual(horse.name, "Thunder")
        self.assertEqual(horse.age, 12)
        self.assertEqual(horse.weight, 450.0)


class TestFeedRecord(unittest.TestCase):
    """Test FeedRecord model"""
    
    def test_feed_record_creation(self):
        """Test creating a feed record"""
        timestamp = datetime.now()
        record = FeedRecord(
            record_id=1,
            horse_id=1,
            feed_type="Heu",
            weight=5.5,
            timestamp=timestamp,
            notes="Morning feeding"
        )
        self.assertEqual(record.record_id, 1)
        self.assertEqual(record.horse_id, 1)
        self.assertEqual(record.feed_type, "Heu")
        self.assertEqual(record.weight, 5.5)
    
    def test_feed_record_to_dict(self):
        """Test converting feed record to dictionary"""
        timestamp = datetime.now()
        record = FeedRecord(
            record_id=1,
            horse_id=1,
            feed_type="Pellets",
            weight=2.0,
            timestamp=timestamp
        )
        data = record.to_dict()
        self.assertEqual(data['record_id'], 1)
        self.assertEqual(data['feed_type'], "Pellets")
        self.assertEqual(data['weight'], "2.00")
    
    def test_feed_record_from_dict(self):
        """Test creating feed record from dictionary"""
        timestamp_str = "2024-11-04T07:30:00"
        data = {
            'record_id': '1',
            'horse_id': '1',
            'feed_type': 'Heulage',
            'weight': '6.2',
            'timestamp': timestamp_str,
            'notes': 'Test'
        }
        record = FeedRecord.from_dict(data)
        self.assertEqual(record.record_id, 1)
        self.assertEqual(record.horse_id, 1)
        self.assertEqual(record.feed_type, "Heulage")
        self.assertEqual(record.weight, 6.2)


class TestDataManager(unittest.TestCase):
    """Test DataManager"""
    
    def setUp(self):
        """Set up test environment"""
        # Create temporary directory for test data
        self.test_dir = tempfile.mkdtemp()
        
        # Override settings for testing
        import config.settings as settings
        self.original_data_dir = settings.DATA_DIR
        self.original_horses_csv = settings.HORSES_CSV
        self.original_feed_csv = settings.FEED_RECORDS_CSV
        
        settings.DATA_DIR = self.test_dir
        settings.HORSES_CSV = os.path.join(self.test_dir, "horses.csv")
        settings.FEED_RECORDS_CSV = os.path.join(self.test_dir, "feed_records.csv")
        
        self.data_manager = DataManager()
    
    def tearDown(self):
        """Clean up test environment"""
        # Restore original settings
        import config.settings as settings
        settings.DATA_DIR = self.original_data_dir
        settings.HORSES_CSV = self.original_horses_csv
        settings.FEED_RECORDS_CSV = self.original_feed_csv
        
        # Remove temporary directory
        shutil.rmtree(self.test_dir)
    
    def test_add_horse(self):
        """Test adding a horse"""
        horse = Horse(horse_id=1, name="TestHorse", breed="TestBreed")
        result = self.data_manager.add_horse(horse)
        self.assertTrue(result)
        
        # Verify horse was added
        horses = self.data_manager.get_all_horses()
        self.assertEqual(len(horses), 1)
        self.assertEqual(horses[0].name, "TestHorse")
    
    def test_get_horse_by_id(self):
        """Test retrieving a horse by ID"""
        horse = Horse(horse_id=1, name="Apollo")
        self.data_manager.add_horse(horse)
        
        retrieved = self.data_manager.get_horse_by_id(1)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.name, "Apollo")
    
    def test_update_horse(self):
        """Test updating a horse"""
        horse = Horse(horse_id=1, name="Original", breed="OldBreed")
        self.data_manager.add_horse(horse)
        
        # Update horse
        horse.name = "Updated"
        horse.breed = "NewBreed"
        result = self.data_manager.update_horse(horse)
        self.assertTrue(result)
        
        # Verify update
        updated = self.data_manager.get_horse_by_id(1)
        self.assertEqual(updated.name, "Updated")
        self.assertEqual(updated.breed, "NewBreed")
    
    def test_delete_horse(self):
        """Test deleting a horse"""
        horse = Horse(horse_id=1, name="ToDelete")
        self.data_manager.add_horse(horse)
        
        result = self.data_manager.delete_horse(1)
        self.assertTrue(result)
        
        # Verify deletion
        horses = self.data_manager.get_all_horses()
        self.assertEqual(len(horses), 0)
    
    def test_add_feed_record(self):
        """Test adding a feed record"""
        record = FeedRecord(
            record_id=None,
            horse_id=1,
            feed_type="Heu",
            weight=5.0,
            timestamp=datetime.now()
        )
        result = self.data_manager.add_feed_record(record)
        self.assertTrue(result)
        
        # Verify record was added
        records = self.data_manager.get_all_feed_records()
        self.assertEqual(len(records), 1)
    
    def test_get_feed_records_by_horse(self):
        """Test filtering feed records by horse"""
        # Add records for different horses
        record1 = FeedRecord(None, 1, "Heu", 5.0, datetime.now())
        record2 = FeedRecord(None, 2, "Pellets", 2.0, datetime.now())
        record3 = FeedRecord(None, 1, "Heulage", 6.0, datetime.now())
        
        self.data_manager.add_feed_record(record1)
        self.data_manager.add_feed_record(record2)
        self.data_manager.add_feed_record(record3)
        
        # Get records for horse 1
        records = self.data_manager.get_all_feed_records(horse_id=1)
        self.assertEqual(len(records), 2)


if __name__ == '__main__':
    unittest.main()
