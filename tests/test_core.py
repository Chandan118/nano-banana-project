import pytest
import numpy as np
from src.nano_banana import BananaStatus, BananaFeatures, NanoBananaModel

def test_model_initialization(base_model):
    """Test that the model initializes correctly."""
    assert base_model.threshold == 0.5
    assert base_model.version == "1.0.0"

def test_feature_vectorization(ripe_banana):
    """Test that features are correctly converted to a numpy vector."""
    vector = ripe_banana.to_vector()
    assert isinstance(vector, np.ndarray)
    assert len(vector) == 6
    assert vector[2] == 0.5  # Color score

def test_banana_classification_unripe(base_model, unripe_banana):
    """Test classification of unripe bananas."""
    status, confidence = base_model.classify(unripe_banana)
    assert status == BananaStatus.UNRIPE
    assert confidence > 0.8

def test_banana_classification_ripe(base_model, ripe_banana):
    """Test classification of ripe bananas."""
    status, confidence = base_model.classify(ripe_banana)
    assert status == BananaStatus.RIPE
    assert confidence >= 0.7

def test_banana_classification_overripe(base_model, overripe_banana):
    """Test classification of overripe bananas."""
    status, confidence = base_model.classify(overripe_banana)
    assert status == BananaStatus.OVERRIPE
    assert confidence > 0.8

def test_volume_estimation(base_model, ripe_banana):
    """Test volume estimation calculation (pi * r^2 * h)."""
    # radius = 3.5 / 2 = 1.75
    # expected_volume = pi * (1.75)^2 * 18.0 = 173.18
    volume = base_model._estimate_volume(ripe_banana)
    expected_volume = np.pi * (1.75 ** 2) * 18.0
    assert pytest.approx(volume, 0.01) == expected_volume

def test_full_analysis(base_model, ripe_banana):
    """Test the full analysis pipeline."""
    result = base_model.analyze(ripe_banana)
    
    assert "status" in result
    assert "confidence" in result
    assert "volume_cm3" in result
    assert "density_g_per_cm3" in result
    assert "features" in result
    
    assert result["status"] == "ripe"
    assert result["density_g_per_cm3"] > 0

def test_batch_analyze(base_model, unripe_banana, ripe_banana, overripe_banana):
    """Test analyzing multiple bananas at once."""
    batch = [unripe_banana, ripe_banana, overripe_banana]
    results = base_model.batch_analyze(batch)
    
    assert len(results) == 3
    assert results[0]["status"] == "unripe"
    assert results[1]["status"] == "ripe"
    assert results[2]["status"] == "overripe"
