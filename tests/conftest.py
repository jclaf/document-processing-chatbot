"""
Configuration des tests pytest.
"""

import pytest
import sys
import os

# Ajouter le chemin source aux tests
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))


@pytest.fixture
def sample_fixture():
    """Fixture exemple."""
    return {"test": "data"}
