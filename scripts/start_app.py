#!/usr/bin/env python3
"""
Startup script for LexiLocal Streamlit app with proper environment configuration.
"""

import os
import sys
import subprocess

def set_environment():
    """Set environment variables for optimal Streamlit operation."""
    # Disable Streamlit file watcher to prevent torch conflicts
    os.environ["STREAMLIT_SERVER_FILE_WATCHER_TYPE"] = "none"
    os.environ["STREAMLIT_GLOBAL_DEVELOPMENT_MODE"] = "false"
    os.environ["STREAMLIT_LOGGER_LEVEL"] = "error"
    
    # Disable usage statistics
    os.environ["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"
    
    # Set server configuration
    os.environ["STREAMLIT_SERVER_HEADLESS"] = "true"
    os.environ["STREAMLIT_SERVER_PORT"] = "8501"
    os.environ["STREAMLIT_SERVER_ADDRESS"] = "0.0.0.0"

def main():
    """Start the LexiLocal application."""
    print("🚀 Starting LexiLocal...")
    print("📋 Setting up environment...")
    
    set_environment()
    
    # Add src to Python path
    src_path = os.path.join(os.path.dirname(__file__), '..', 'src')
    sys.path.insert(0, os.path.abspath(src_path))
    
    print("🌐 Starting Streamlit server...")
    print("📍 Access the app at: http://localhost:8501")
    print("🛑 Press Ctrl+C to stop")
    
    try:
        # Start Streamlit
        app_path = os.path.join(os.path.dirname(__file__), '..', 'app.py')
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", app_path,
            "--server.headless", "true",
            "--server.fileWatcherType", "none",
            "--logger.level", "error"
        ])
    except KeyboardInterrupt:
        print("\n🛑 Shutting down LexiLocal...")
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()