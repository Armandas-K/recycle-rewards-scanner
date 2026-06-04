import pytest
import pandas as pd
import cv2

@pytest.fixture
def blank_frame():
    # plain white frame - no response from scanner
    import numpy as np
    return np.ones((480, 640, 3), dtype="uint8") * 255

@pytest.fixture
def sample_export_df():
    # sample Open Food Facts export, only contains products: sold in UK, category: en:beverages
    return pd.DataFrame({
        "code": [
            "5000193034559",  # Coca-Cola can - valid, aluminium
            "5054267007123",  # Lucozade - valid, mixed plastic bottle
            "5010251484851",  # Morrisons water 500ml — valid, pet bottle
            "4056489010104",  # Cola Freeway - french aluminium tag
            "5010017109714",  # invalid - glass bottle
        ],
        "product_name_en": [
            "Coca-Cola",
            "Lucozade Wild Cherry",
            "Sparkling Lemon Lime Water",
            "Cola – Freeway – 33 cl",
            "Lager Beer - Stella Artois",
        ],
        "packaging_tags": [
            "en:aluminium",
            "en:mixed-plastic-bottle",
            "en:pet-bottle",
            "fr:canette-aluminium", # should be handled with suffix matching
            "en:glass-bottle", # should be filtered out
        ],
        "categories_tags": [
            "en:beverages,en:sweetened-beverages",
            "en:beverages,en:energy-drinks",
            "en:beverages,en:waters",
            "en:beverages",
            "en:beverages,en:beers",
        ]
    })