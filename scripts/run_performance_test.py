#!/usr/bin/env python3
"""
Performance testing script for LexiLocal.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from lexilocal.core.rag_system import LegalRAGSystem
from lexilocal.data.mock_data import get_mock_dataset
from lexilocal.utils.performance_metrics import PerformanceMetrics
from lexilocal.utils.logging_config import setup_logging

def main():
    """Run comprehensive performance tests."""
    setup_logging(level="INFO")
    
    metrics = PerformanceMetrics()
    
    print("🔍 LexiLocal Performance Testing")
    print("=" * 50)
    
    # Initialize system
    with metrics.measure_time('initialization_time'):
        rag = LegalRAGSystem(model_name="llama3.2:1b")
    
    # Load documents
    with metrics.measure_time('document_loading_time'):
        mock_docs = get_mock_dataset()
        rag.load_documents(mock_docs)
    
    # Test Q&A performance
    test_questions = [
        "What was the outcome of Johnson v. Smith?",
        "What constitutional amendment was violated?",
        "What type of injunction was granted?",
        "What are the requirements for a preliminary injunction?",
        "What happens when time is of the essence?"
    ]
    
    print("\n🤖 Testing Q&A Performance...")
    for question in test_questions:
        with metrics.measure_time('qa_response_times'):
            result = rag.ask_question(question)
            print(f"  ✅ Question processed: {len(result['sources'])} sources")
    
    # Test summarization
    print("\n📄 Testing Summarization Performance...")
    for doc in mock_docs:
        with metrics.measure_time('summarization_times'):
            result = rag.summarize_by_title(doc['title'])
            print(f"  ✅ Summary generated: {len(result['summary'])} chars")
    
    # Test search
    print("\n🔍 Testing Search Performance...")
    search_queries = ["contract breach", "Fourth Amendment", "patent infringement"]
    for query in search_queries:
        with metrics.measure_time('search_times'):
            results = rag.doc_processor.search_similar_chunks(query, k=5)
            print(f"  ✅ Search '{query}': {len(results)} results")
    
    # Print and export results
    metrics.print_summary()
    metrics.export_metrics('performance_metrics.json')
    
    print("\n✅ Performance testing completed!")

if __name__ == "__main__":
    main()