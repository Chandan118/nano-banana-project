import pytest
from src.nano_banana import BananaFeatures, NanoBananaModel

@pytest.fixture
def base_model():
    """Return a default NanoBananaModel instance."""
    return NanoBananaModel(threshold=0.5)

@pytest.fixture
def ripe_banana():
    """Return features for a typical ripe banana."""
    return BananaFeatures(
        length_cm=18.0,
        diameter_cm=3.5,
        color_score=0.5,
        weight_grams=118.0,
        firmness=3.0,
        temperature_celsius=20.0
    )

@pytest.fixture
def unripe_banana():
    """Return features for a typical unripe banana."""
    return BananaFeatures(
        length_cm=15.0,
        diameter_cm=3.0,
        color_score=0.1,
        weight_grams=110.0,
        firmness=8.0,
        temperature_celsius=20.0
    )

@pytest.fixture
def overripe_banana():
    """Return features for a typical overripe banana."""
    return BananaFeatures(
        length_cm=19.0,
        diameter_cm=3.6,
        color_score=0.9,
        weight_grams=125.0,
        firmness=1.5,
        temperature_celsius=20.0
    )
