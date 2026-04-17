"""
Unit tests for Nano Banana Model.

Author: Chandan Kumar
Email: chandan@bit.edu.cn
"""

import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from nano_banana import (
    NanoBananaModel,
    BananaFeatures,
    BananaStatus,
    __version__,
    __author__,
    __email__
)


class TestBananaFeatures(unittest.TestCase):
    """Test cases for BananaFeatures dataclass."""

    def test_create_features(self):
        """Test creating banana features."""
        banana = BananaFeatures(
            length_cm=15.0,
            diameter_cm=3.0,
            color_score=0.5,
            weight_grams=100.0,
            firmness=5.0,
            temperature_celsius=20.0
        )
        self.assertEqual(banana.length_cm, 15.0)
        self.assertEqual(banana.diameter_cm, 3.0)

    def test_to_vector(self):
        """Test conversion to numpy array."""
        banana = BananaFeatures(
            length_cm=10.0,
            diameter_cm=2.0,
            color_score=0.3,
            weight_grams=80.0,
            firmness=6.0,
            temperature_celsius=18.0
        )
        vector = banana.to_vector()
        self.assertEqual(len(vector), 6)
        self.assertEqual(vector[0], 10.0)


class TestNanoBananaModel(unittest.TestCase):
    """Test cases for NanoBananaModel."""

    def setUp(self):
        """Set up test fixtures."""
        self.model = NanoBananaModel(threshold=0.5)

    def test_model_initialization(self):
        """Test model initialization."""
        self.assertEqual(self.model.threshold, 0.5)
        self.assertEqual(self.model.version, __version__)

    def test_classify_unripe(self):
        """Test classification of unripe banana."""
        banana = BananaFeatures(
            length_cm=12.0,
            diameter_cm=2.5,
            color_score=0.2,  # Greenish
            weight_grams=90.0,
            firmness=7.0,
            temperature_celsius=20.0
        )
        status, confidence = self.model.classify(banana)
        self.assertEqual(status, BananaStatus.UNRIPE)
        self.assertGreater(confidence, 0.5)

    def test_classify_ripe(self):
        """Test classification of ripe banana."""
        banana = BananaFeatures(
            length_cm=15.0,
            diameter_cm=3.0,
            color_score=0.5,  # Yellow
            weight_grams=120.0,
            firmness=4.0,
            temperature_celsius=22.0
        )
        status, confidence = self.model.classify(banana)
        self.assertEqual(status, BananaStatus.RIPE)
        self.assertGreater(confidence, 0.5)

    def test_classify_overripe(self):
        """Test classification of overripe banana."""
        banana = BananaFeatures(
            length_cm=18.0,
            diameter_cm=3.5,
            color_score=0.9,  # Brown spots
            weight_grams=150.0,
            firmness=2.0,
            temperature_celsius=25.0
        )
        status, confidence = self.model.classify(banana)
        self.assertEqual(status, BananaStatus.OVERRIPE)
        self.assertGreater(confidence, 0.5)

    def test_analyze(self):
        """Test full analysis pipeline."""
        banana = BananaFeatures(
            length_cm=14.0,
            diameter_cm=2.8,
            color_score=0.6,
            weight_grams=110.0,
            firmness=4.2,
            temperature_celsius=21.0
        )
        result = self.model.analyze(banana)

        self.assertIn("status", result)
        self.assertIn("confidence", result)
        self.assertIn("volume_cm3", result)
        self.assertIn("density_g_per_cm3", result)
        self.assertIn("features", result)
        self.assertIsInstance(result["confidence"], float)

    def test_batch_analyze(self):
        """Test batch processing."""
        bananas = [
            BananaFeatures(12, 2.5, 0.2, 90, 7, 20),
            BananaFeatures(15, 3.0, 0.5, 120, 4, 22),
            BananaFeatures(18, 3.5, 0.9, 150, 2, 25)
        ]
        results = self.model.batch_analyze(bananas)
        self.assertEqual(len(results), 3)
        for result in results:
            self.assertIn("status", result)


class TestVolumeCalculation(unittest.TestCase):
    """Test volume estimation."""

    def test_volume_estimation(self):
        """Test volume calculation for cylindrical banana."""
        banana = BananaFeatures(
            length_cm=10.0,
            diameter_cm=2.0,
            color_score=0.5,
            weight_grams=100.0,
            firmness=5.0,
            temperature_celsius=20.0
        )
        model = NanoBananaModel()
        volume = model._estimate_volume(banana)

        # Expected: π * (1)^2 * 10 = 31.4159...
        expected = 3.14159 * 10
        self.assertAlmostEqual(volume, expected, places=1)


def run_tests():
    """Run all unit tests."""
    print("=" * 60)
    print("Nano Banana Model - Test Suite")
    print(f"Author: {__author__}")
    print(f"Email: {__email__}")
    print("=" * 60)

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestBananaFeatures))
    suite.addTests(loader.loadTestsFromTestCase(TestNanoBananaModel))
    suite.addTests(loader.loadTestsFromTestCase(TestVolumeCalculation))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("\n" + "=" * 60)
    if result.wasSuccessful():
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed.")
    print("=" * 60)

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
