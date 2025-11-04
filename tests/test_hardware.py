"""
Unit tests for hardware abstraction layer
"""
import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.hardware import SimulatedScale


class TestSimulatedScale(unittest.TestCase):
    """Test simulated scale implementation"""
    
    def setUp(self):
        """Set up test scale"""
        self.scale = SimulatedScale()
    
    def tearDown(self):
        """Clean up"""
        if self.scale:
            self.scale.cleanup()
    
    def test_initialization(self):
        """Test scale initialization"""
        result = self.scale.initialize()
        self.assertTrue(result)
        self.assertTrue(self.scale.is_ready())
    
    def test_tare(self):
        """Test taring the scale"""
        self.scale.initialize()
        result = self.scale.tare()
        self.assertTrue(result)
        
        # Weight should be close to zero after tare
        weight = self.scale.get_weight()
        self.assertIsNotNone(weight)
        self.assertAlmostEqual(weight, 0.0, delta=0.1)
    
    def test_get_weight(self):
        """Test getting weight"""
        self.scale.initialize()
        self.scale.tare()
        
        # Set a specific weight
        self.scale.set_weight(5.5)
        weight = self.scale.get_weight()
        
        self.assertIsNotNone(weight)
        # Allow for small variation due to simulated noise
        self.assertAlmostEqual(weight, 5.5, delta=0.1)
    
    def test_add_weight(self):
        """Test adding weight to scale"""
        self.scale.initialize()
        self.scale.tare()
        
        initial = self.scale.get_weight()
        self.scale.add_weight(3.0)
        final = self.scale.get_weight()
        
        self.assertGreater(final, initial)
    
    def test_calibrate(self):
        """Test calibration (simulated)"""
        self.scale.initialize()
        result = self.scale.calibrate(10.0)
        self.assertTrue(result)
    
    def test_not_ready_before_init(self):
        """Test that scale is not ready before initialization"""
        scale = SimulatedScale()
        self.assertFalse(scale.is_ready())
        self.assertIsNone(scale.get_weight())


if __name__ == '__main__':
    unittest.main()
