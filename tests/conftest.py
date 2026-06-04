import pytest
import pandas as pd
import cv2

@pytest.fixture
def blank_frame():
    # plain white frame - no response from scanner
    import numpy as np
    return np.ones((480, 640, 3), dtype="uint8") * 255

@pytest.fixture
def sample_cache_df():
    # sample dataframe like filtered_barcodes.csv
    return pd.DataFrame({
        "code": [
            "5000193034559",  # Coca-Cola can - valid, aluminium
            "5054267007123",  # Lucozade 1L - valid, pet bottle
            "5010251484851",  # Morrisons water 500ml - valid, pet bottle
            None,             # invalid - missing barcode
            "123",            # invalid - barcode too short
        ],
        "product_name_en": [
            "Coca-Cola",
            "Lucozade Wild Cherry",
            "Sparkling Lemon Lime Water",
            "Unknown Product",
            "Invalid Product",
        ],
        "packaging_tags": [
            "en:aluminium",
            "en:mixed-plastic-bottle",
            "en:pet-bottle",
            "en:pet-bottle",
            "en:pet-bottle",
        ],
        "categories_tags": [
            "en:beverages,en:sweetened-beverages",
            "en:beverages,en:energy-drinks",
            "en:beverages,en:waters",
            "en:beverages",
            "en:beverages",
        ]
    })