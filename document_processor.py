#!/usr/bin/env python3

import numpy as np
from typing import List, Dict, Any
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import faiss
import pickle
import os
from mock_data import get_mock_dataset

class DocumentProcessor:
    def __init__(self, 
                 chunk_size: int = 1000, 
                 chunk_overlap: int = 200,
                 embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """Initialize document processor with chunking and embedding capabilities"""
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        
        # Initialize embedding model
        print(f"Loading embedding model: {embedding_model}")
        self.embedding_model = SentenceTransformer(embedding_model)
        self.embedding_dim = self.embedding_model.get_sentence_embedding_dimension()
        
        # Storage for chunks and metadata
        self.chunks = []
        self.chunk_metadata = []
        self.faiss_index = None
        
    def process_documents(self, documents: List[Dict[str, Any]]) -> None:
        """Process documents by chunking and creating embeddings"""
        print(f"Processing {len(documents)} documents...")
        
        all_chunks = []
        all_metadata = []
        
        for doc_idx, doc in enumerate(documents):
            document_text = doc.get('document', '')
            if not document_text.strip():
                continue
                
            # Split document into chunks
            chunks = self.text_splitter.split_text(document_text)
            
            for chunk_idx, chunk in enumerate(chunks):
                all_chunks.append(chunk)
                all_metadata.append({
                    'doc_id': doc.get('id', f'doc_{doc_idx}'),
                    'chunk_id': f"{doc.get('id', f'doc_{doc_idx}')}_{chunk_idx}",
                    'title': doc.get('title', ''),
                    'citation': doc.get('citation', ''),
                    'state': doc.get('state', ''),
                    'issuer': doc.get('issuer', ''),
                    'chunk_index': chunk_idx,
                    'total_chunks': len(chunks),
                    'text': chunk
                })
        
        print(f"Created {len(all_chunks)} chunks from {len(documents)} documents")
        
        # Generate embeddings
        print("Generating embeddings...")
        embeddings = self.embedding_model.encode(all_chunks, show_progress_bar=True)
        
        # Store chunks and metadata
        self.chunks = all_chunks
        self.chunk_metadata = all_metadata
        
        # Create FAISS index
        self.create_faiss_index(embeddings)
        
    def create_faiss_index(self, embeddings: np.ndarray) -> None:
        """Create FAISS index from embeddings"""
        print("Creating FAISS index...")
        
        # Normalize embeddings for cosine similarity
        embeddings_normalized = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
        
        # Create FAISS index (using Inner Product for normalized vectors = cosine similarity)
        self.faiss_index = faiss.IndexFlatIP(self.embedding_dim)
        self.faiss_index.add(embeddings_normalized.astype('float32'))
        
        print(f"FAISS index created with {self.faiss_index.ntotal} vectors")
        
    def search_similar_chunks(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """Search for similar chunks given a query"""
        if self.faiss_index is None:
            raise ValueError("FAISS index not created. Call process_documents first.")
        
        # Encode query
        query_embedding = self.embedding_model.encode([query])
        query_embedding_normalized = query_embedding / np.linalg.norm(query_embedding, axis=1, keepdims=True)
        
        # Search FAISS index
        scores, indices = self.faiss_index.search(query_embedding_normalized.astype('float32'), k)
        
        # Return results with metadata
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx != -1:  # Valid index
                result = self.chunk_metadata[idx].copy()
                result['similarity_score'] = float(score)
                results.append(result)
        
        return results
    
    def save_index(self, filepath: str) -> None:
        """Save FAISS index and metadata to disk"""
        if self.faiss_index is None:
            raise ValueError("No index to save")
            
        # Save FAISS index
        faiss.write_index(self.faiss_index, f"{filepath}.faiss")
        
        # Save metadata and chunks
        with open(f"{filepath}_metadata.pkl", 'wb') as f:
            pickle.dump({
                'chunks': self.chunks,
                'chunk_metadata': self.chunk_metadata,
                'embedding_dim': self.embedding_dim,
                'chunk_size': self.chunk_size,
                'chunk_overlap': self.chunk_overlap
            }, f)
        
        print(f"Index and metadata saved to {filepath}")
    
    def load_index(self, filepath: str) -> None:
        """Load FAISS index and metadata from disk"""
        # Load FAISS index
        self.faiss_index = faiss.read_index(f"{filepath}.faiss")
        
        # Load metadata and chunks
        with open(f"{filepath}_metadata.pkl", 'rb') as f:
            data = pickle.load(f)
            self.chunks = data['chunks']
            self.chunk_metadata = data['chunk_metadata']
            self.embedding_dim = data['embedding_dim']
            self.chunk_size = data['chunk_size'] 
            self.chunk_overlap = data['chunk_overlap']
        
        print(f"Index and metadata loaded from {filepath}")

def main():
    """Test the document processor with mock data"""
    print("Testing DocumentProcessor with mock data...")
    
    # Initialize processor
    processor = DocumentProcessor()
    
    # Get mock data
    mock_docs = get_mock_dataset()
    
    # Process documents
    processor.process_documents(mock_docs)
    
    # Test search
    test_queries = [
        "contract breach and damages",
        "Fourth Amendment civil rights violation",
        "patent infringement preliminary injunction"
    ]
    
    for query in test_queries:
        print(f"\n{'='*50}")
        print(f"Query: {query}")
        print(f"{'='*50}")
        
        results = processor.search_similar_chunks(query, k=3)
        
        for i, result in enumerate(results, 1):
            print(f"\nResult {i} (similarity: {result['similarity_score']:.3f}):")
            print(f"Document: {result['title']}")
            print(f"Text preview: {result['text'][:200]}...")
    
    # Save index
    processor.save_index("legal_docs_index")
    print("\nIndex saved successfully!")

if __name__ == "__main__":
    main()