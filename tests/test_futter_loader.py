# tests/test_futter_loader.py
import unittest
from utils.futter_loader import lade_heu_aus_csv

class TestFutterLoader(unittest.TestCase):
    def test_lade_heu(self):
        heu = lade_heu_aus_csv("data/heu2024.csv")
        self.assertIsNotNone(heu)
