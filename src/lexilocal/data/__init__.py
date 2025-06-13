"""Data handling modules for LexiLocal."""

from .mock_data import get_mock_dataset
from .dataset_loader import DatasetLoader

__all__ = ["get_mock_dataset", "DatasetLoader"]