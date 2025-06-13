#!/usr/bin/env python3
"""
Dataset loading utilities for various data sources.
"""

import os
from typing import List, Dict, Any, Optional
from datasets import load_dataset
import logging

logger = logging.getLogger(__name__)

class DatasetLoader:
    """Unified interface for loading datasets from various sources."""
    
    def __init__(self):
        self.supported_sources = ["huggingface", "local", "mock"]
    
    def load_huggingface_dataset(
        self, 
        dataset_name: str, 
        config: str = "default",
        split: str = "train",
        num_samples: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Load dataset from HuggingFace Hub."""
        try:
            logger.info(f"Loading HuggingFace dataset: {dataset_name}")
            
            if num_samples:
                split = f"{split}[:{num_samples}]"
            
            dataset = load_dataset(dataset_name, config, split=split)
            
            documents = []
            for item in dataset:
                documents.append({
                    'id': item.get('id', ''),
                    'title': item.get('title', 'Untitled'),
                    'citation': item.get('citation', ''),
                    'state': item.get('state', ''),
                    'issuer': item.get('issuer', ''),
                    'document': item.get('document', '')
                })
            
            logger.info(f"Successfully loaded {len(documents)} documents")
            return documents
            
        except Exception as e:
            logger.error(f"Failed to load HuggingFace dataset: {str(e)}")
            raise
    
    def load_local_files(self, file_paths: List[str]) -> List[Dict[str, Any]]:
        """Load documents from local files."""
        documents = []
        
        for file_path in file_paths:
            if not os.path.exists(file_path):
                logger.warning(f"File not found: {file_path}")
                continue
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                documents.append({
                    'id': os.path.basename(file_path),
                    'title': os.path.splitext(os.path.basename(file_path))[0],
                    'citation': '',
                    'state': '',
                    'issuer': '',
                    'document': content
                })
                
            except Exception as e:
                logger.error(f"Failed to load file {file_path}: {str(e)}")
        
        logger.info(f"Loaded {len(documents)} local documents")
        return documents
    
    def validate_documents(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Validate and clean document data."""
        valid_documents = []
        
        for doc in documents:
            if not doc.get('document', '').strip():
                logger.warning(f"Skipping document with empty content: {doc.get('id', 'unknown')}")
                continue
            
            # Ensure all required fields exist
            doc.setdefault('id', '')
            doc.setdefault('title', 'Untitled')
            doc.setdefault('citation', '')
            doc.setdefault('state', '')
            doc.setdefault('issuer', '')
            
            valid_documents.append(doc)
        
        logger.info(f"Validated {len(valid_documents)}/{len(documents)} documents")
        return valid_documents