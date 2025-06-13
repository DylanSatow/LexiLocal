#!/usr/bin/env python3
"""
Setup script for LexiLocal package.
"""

from setuptools import setup, find_packages
import os

# Read README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="lexilocal",
    version="1.0.0",
    author="Dylan Satow",
    author_email="your.email@example.com",
    description="AI-Powered Legal Document Summarization and Q&A with Local LLM Optimization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DylanSatow/LexiLocal",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Legal Industry",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Text Processing :: Linguistic",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0",
            "black>=23.0",
            "isort>=5.0",
            "mypy>=1.0",
            "flake8>=6.0",
            "pytest-cov>=4.0",
        ],
        "gpu": [
            "torch[gpu]",
            "faiss-gpu",
        ],
    },
    entry_points={
        "console_scripts": [
            "lexilocal=lexilocal.ui.streamlit_app:main",
            "lexilocal-test=scripts.run_performance_test:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)