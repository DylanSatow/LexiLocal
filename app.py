#!/usr/bin/env python3
"""
Main application entry point for LexiLocal.
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from lexilocal.ui.streamlit_app import main

if __name__ == "__main__":
    main()