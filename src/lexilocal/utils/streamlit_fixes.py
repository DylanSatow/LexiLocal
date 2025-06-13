#!/usr/bin/env python3
"""
Workarounds for Streamlit compatibility issues.
"""

import os
import sys
import warnings

def apply_torch_streamlit_fix():
    """
    Apply fix for Streamlit + PyTorch compatibility issue.
    
    This addresses the RuntimeError: Tried to instantiate class '__path__._path'
    that occurs with newer versions of PyTorch and Streamlit.
    """
    # Set environment variables to disable problematic features
    os.environ["STREAMLIT_LOGGER_LEVEL"] = "error"
    os.environ["STREAMLIT_CLIENT_CACHING"] = "false"
    os.environ["STREAMLIT_CLIENT_DISPLAY_ENABLED"] = "false"
    
    try:
        # Disable torch's custom class system if problematic
        import torch
        if hasattr(torch, '_C') and hasattr(torch._C, '_get_custom_class_python_wrapper'):
            # Store original function
            original_wrapper = torch._C._get_custom_class_python_wrapper
            
            def safe_wrapper(class_name, attr_name):
                try:
                    return original_wrapper(class_name, attr_name)
                except RuntimeError as e:
                    if '__path__._path' in str(e):
                        # Return None for problematic path queries
                        return None
                    raise e
            
            torch._C._get_custom_class_python_wrapper = safe_wrapper
            
    except ImportError:
        # torch not available, skip fix
        pass
    except Exception as e:
        # Log warning but don't fail
        warnings.warn(f"Could not apply torch-streamlit compatibility fix: {e}")

def suppress_warnings():
    """Suppress common warnings that don't affect functionality."""
    warnings.filterwarnings("ignore", category=UserWarning, module="transformers")
    warnings.filterwarnings("ignore", category=UserWarning, module="torch")
    warnings.filterwarnings("ignore", category=FutureWarning, module="transformers")
    warnings.filterwarnings("ignore", category=RuntimeWarning, module="streamlit")
    warnings.filterwarnings("ignore", message=".*resume_download.*")
    warnings.filterwarnings("ignore", message=".*clean_up_tokenization_spaces.*")
    warnings.filterwarnings("ignore", message=".*local_sources_watcher.*")

def disable_streamlit_watcher():
    """Disable Streamlit's file watcher that causes the torch issue."""
    # Set environment variable to disable file watcher
    os.environ["STREAMLIT_SERVER_FILE_WATCHER_TYPE"] = "none"
    os.environ["STREAMLIT_GLOBAL_DEVELOPMENT_MODE"] = "false"

def init_streamlit_compatibility():
    """Initialize all Streamlit compatibility fixes."""
    disable_streamlit_watcher()
    suppress_warnings()
    apply_torch_streamlit_fix()