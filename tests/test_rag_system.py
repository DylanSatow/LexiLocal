#!/usr/bin/env python3
"""
Unit tests for RAG System.
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from lexilocal.core.rag_system import LegalRAGSystem
from lexilocal.data.mock_data import get_mock_dataset

class TestRAGSystem(unittest.TestCase):
    """Test cases for RAG System."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures for the class."""
        cls.rag = LegalRAGSystem(model_name="llama3.2:1b")
        cls.mock_docs = get_mock_dataset()
        cls.rag.load_documents(cls.mock_docs)
    
    def test_system_initialization(self):
        """Test system initialization."""
        self.assertIsNotNone(self.rag.llm)
        self.assertIsNotNone(self.rag.doc_processor)
        self.assertEqual(self.rag.model_name, "llama3.2:1b")
    
    def test_question_answering(self):
        """Test Q&A functionality."""
        question = "What was the outcome of Johnson v. Smith?"
        result = self.rag.ask_question(question)
        
        # Verify response structure
        self.assertIn('answer', result)
        self.assertIn('sources', result)
        self.assertIn('context_used', result)
        
        # Verify content
        self.assertIsInstance(result['answer'], str)
        self.assertGreater(len(result['answer']), 0)
        self.assertGreater(len(result['sources']), 0)
    
    def test_summarization(self):
        """Test document summarization."""
        title = "Johnson v. Smith"
        result = self.rag.summarize_by_title(title)
        
        # Verify response structure
        self.assertIn('summary', result)
        self.assertIn('source', result)
        
        # Verify content
        self.assertIsInstance(result['summary'], str)
        self.assertGreater(len(result['summary']), 0)
        self.assertIsNotNone(result['source'])
    
    def test_context_formatting(self):
        """Test context formatting for prompts."""
        mock_chunks = [
            {
                'title': 'Test Case',
                'citation': '123 F.3d 456',
                'text': 'This is test content.'
            }
        ]
        
        formatted = self.rag._format_context(mock_chunks)
        
        self.assertIn('Test Case', formatted)
        self.assertIn('123 F.3d 456', formatted)
        self.assertIn('This is test content.', formatted)

if __name__ == '__main__':
    unittest.main()