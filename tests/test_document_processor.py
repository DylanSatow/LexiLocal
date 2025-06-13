#!/usr/bin/env python3
"""
Unit tests for DocumentProcessor.
"""

import unittest
import sys
import os
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from lexilocal.core.document_processor import DocumentProcessor
from lexilocal.data.mock_data import get_mock_dataset

class TestDocumentProcessor(unittest.TestCase):
    """Test cases for DocumentProcessor."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.processor = DocumentProcessor(chunk_size=500, chunk_overlap=100)
        self.mock_docs = get_mock_dataset()
    
    def test_initialization(self):
        """Test processor initialization."""
        self.assertEqual(self.processor.chunk_size, 500)
        self.assertEqual(self.processor.chunk_overlap, 100)
        self.assertIsNotNone(self.processor.embedding_model)
        self.assertIsNotNone(self.processor.text_splitter)
    
    def test_document_processing(self):
        """Test document processing pipeline."""
        self.processor.process_documents(self.mock_docs)
        
        # Check that chunks were created
        self.assertGreater(len(self.processor.chunks), 0)
        self.assertEqual(len(self.processor.chunks), len(self.processor.chunk_metadata))
        
        # Check FAISS index was created
        self.assertIsNotNone(self.processor.faiss_index)
        self.assertGreater(self.processor.faiss_index.ntotal, 0)
    
    def test_search_functionality(self):
        """Test semantic search."""
        self.processor.process_documents(self.mock_docs)
        
        # Test search
        results = self.processor.search_similar_chunks("contract breach", k=3)
        
        # Verify results
        self.assertLessEqual(len(results), 3)
        for result in results:
            self.assertIn('similarity_score', result)
            self.assertIn('text', result)
            self.assertIn('title', result)
    
    def test_save_load_index(self):
        """Test saving and loading index."""
        self.processor.process_documents(self.mock_docs)
        
        with tempfile.TemporaryDirectory() as temp_dir:
            index_path = os.path.join(temp_dir, "test_index")
            
            # Save index
            self.processor.save_index(index_path)
            
            # Create new processor and load
            new_processor = DocumentProcessor()
            new_processor.load_index(index_path)
            
            # Verify loaded data
            self.assertEqual(len(new_processor.chunks), len(self.processor.chunks))
            self.assertEqual(len(new_processor.chunk_metadata), len(self.processor.chunk_metadata))

if __name__ == '__main__':
    unittest.main()