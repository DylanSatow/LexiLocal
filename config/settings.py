#!/usr/bin/env python3
"""
Configuration settings for LexiLocal.
"""

import os
from typing import Dict, Any

# Model Configuration
DEFAULT_MODEL = "llama3.2:1b"
AVAILABLE_MODELS = [
    "llama3.2:1b",
    "llama3:8b", 
    "mistral:7b",
    "gemma:7b"
]

# Document Processing
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Search Configuration
DEFAULT_K_RESULTS = 3
MAX_K_RESULTS = 10

# Performance
BATCH_SIZE = 32
MAX_SEQUENCE_LENGTH = 512

# File Paths
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
CACHE_DIR = os.path.join(os.path.dirname(__file__), '..', 'cache')
LOGS_DIR = os.path.join(os.path.dirname(__file__), '..', 'logs')

# UI Configuration
STREAMLIT_CONFIG = {
    'page_title': 'LexiLocal - Legal Document AI',
    'page_icon': '⚖️',
    'layout': 'wide',
    'initial_sidebar_state': 'expanded'
}

# Logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

def get_config() -> Dict[str, Any]:
    """Get complete configuration dictionary."""
    return {
        'model': {
            'default': DEFAULT_MODEL,
            'available': AVAILABLE_MODELS
        },
        'processing': {
            'chunk_size': CHUNK_SIZE,
            'chunk_overlap': CHUNK_OVERLAP,
            'embedding_model': EMBEDDING_MODEL,
            'batch_size': BATCH_SIZE,
            'max_sequence_length': MAX_SEQUENCE_LENGTH
        },
        'search': {
            'default_k': DEFAULT_K_RESULTS,
            'max_k': MAX_K_RESULTS
        },
        'paths': {
            'data': DATA_DIR,
            'cache': CACHE_DIR,
            'logs': LOGS_DIR
        },
        'ui': STREAMLIT_CONFIG,
        'logging': {
            'level': LOG_LEVEL,
            'format': LOG_FORMAT
        }
    }