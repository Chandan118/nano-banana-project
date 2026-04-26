"""
Nano Banana Model - Main Implementation
Author: Chandan Kumar (chandan@bit.edu.cn)
Description: A lightweight model for banana analysis and classification.
"""

__version__ = "1.0.0"
__author__ = "Chandan Kumar"
__email__ = "chandan@bit.edu.cn"

import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BananaStatus(Enum):
    """Enumeration of banana ripeness states."""
    UNRIPE = "unripe"
    RIPE = "ripe"
    OVERRIPE = "overripe"
    UNKNOWN = "unknown"


@dataclass
class BananaFeatures:
    """Data class for banana feature extraction."""
    length_cm: float
    diameter_cm: float
    color_score: float  # 0-1 scale (0=green, 1=yellow/brown)
    weight_grams: float
    firmness: float
    temperature_celsius: float

    def to_vector(self) -> np.ndarray:
        """Convert features to numpy array for model processing."""
        return np.array([
            self.length_cm,
            self.diameter_cm,
            self.color_score,
            self.weight_grams,
            self.firmness,
            self.temperature_celsius
        ])


class NanoBananaModel:
    """
    Nano-scale banana classification model.

    This model uses lightweight algorithms to classify bananas based on
    physical characteristics. Designed for efficiency and accuracy.
    """

    def __init__(self, threshold: float = 0.5):
        """
        Initialize the Nano Banana Model.

        Args:
            threshold: Classification threshold for confidence
        """
        self.threshold = threshold
        self.version = __version__
        logger.info(f"Initialized NanoBananaModel v{self.version}")

    def preprocess(self, features: BananaFeatures) -> np.ndarray:
        """
        Preprocess banana features for model input.

        Args:
            features: Raw banana features

        Returns:
            Normalized feature vector
        """
        vector = features.to_vector()

        # Simple normalization using fixed reasonable ranges for each feature
        # [length(0-30), diameter(0-10), color(0-1), weight(0-300), firmness(0-10), temp(0-40)]
        max_vals = np.array([30.0, 10.0, 1.0, 300.0, 10.0, 40.0])
        min_vals = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        
        normalized = (vector - min_vals) / (max_vals - min_vals + 1e-8)

        logger.debug("Preprocessing complete")
        return normalized

    def classify(self, features: BananaFeatures) -> Tuple[BananaStatus, float]:
        """
        Classify banana ripeness based on features.

        Args:
            features: Banana features to classify

        Returns:
            Tuple of (status, confidence_score)
        """
        # Preprocess input
        input_vector = self.preprocess(features)

        # Simple rule-based classification (placeholder)
        # Replace with actual ML model inference in production
        color_weight = input_vector[2]  # color score is most important

        if color_weight < 0.3:
            status = BananaStatus.UNRIPE
            confidence = 0.8 + (0.2 * (1 - color_weight))
        elif color_weight < 0.7:
            status = BananaStatus.RIPE
            confidence = 0.7 + (0.3 * (1 - abs(color_weight - 0.5)))
        else:
            status = BananaStatus.OVERRIPE
            confidence = 0.6 + (0.4 * color_weight)

        confidence = min(confidence, 0.99)

        logger.info(f"Classified as {status.value} with {confidence:.2%} confidence")
        return status, confidence

    def analyze(self, features: BananaFeatures) -> Dict:
        """
        Full analysis pipeline for a banana.

        Args:
            features: Banana features

        Returns:
            Dictionary containing analysis results
        """
        status, confidence = self.classify(features)

        # Calculate additional metrics
        volume = self._estimate_volume(features)
        density = features.weight_grams / volume if volume > 0 else 0

        result = {
            "status": status.value,
            "confidence": round(confidence, 4),
            "volume_cm3": round(volume, 2),
            "density_g_per_cm3": round(density, 2),
            "features": {
                "length_cm": features.length_cm,
                "diameter_cm": features.diameter_cm,
                "color_score": features.color_score,
                "weight_grams": features.weight_grams,
                "firmness": features.firmness,
                "temperature_celsius": features.temperature_celsius
            }
        }

        return result

    def _estimate_volume(self, features: BananaFeatures) -> float:
        """Estimate banana volume assuming cylindrical shape."""
        radius = features.diameter_cm / 2
        height = features.length_cm
        # Volume of cylinder: π * r² * h
        return np.pi * (radius ** 2) * height

    def batch_analyze(self, banana_list: List[BananaFeatures]) -> List[Dict]:
        """
        Analyze multiple bananas in batch.

        Args:
            banana_list: List of banana features

        Returns:
            List of analysis results
        """
        logger.info(f"Processing batch of {len(banana_list)} bananas")
        results = [self.analyze(banana) for banana in banana_list]
        return results


# Example usage and testing
def main():
    """Example usage of the Nano Banana Model."""
    print("=" * 60)
    print("Nano Banana Model - Demo")
    print(f"Author: {__author__}")
    print(f"Email: {__email__}")
    print("=" * 60)

    # Create model instance
    model = NanoBananaModel(threshold=0.6)

    # Example banana
    banana = BananaFeatures(
        length_cm=15.5,
        diameter_cm=3.2,
        color_score=0.65,  # Yellowish
        weight_grams=120.0,
        firmness=4.5,
        temperature_celsius=22.0
    )

    # Analyze
    result = model.analyze(banana)

    print("\nAnalysis Result:")
    print(f"  Status: {result['status'].upper()}")
    print(f"  Confidence: {result['confidence']:.1%}")
    print(f"  Volume: {result['volume_cm3']} cm³")
    print(f"  Density: {result['density_g_per_cm3']} g/cm³")

    print("\n" + "=" * 60)
    print("Analysis complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
