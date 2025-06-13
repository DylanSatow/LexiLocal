# LexiLocal API Documentation

## Core Classes

### DocumentProcessor

The `DocumentProcessor` class handles document chunking, embedding generation, and vector search functionality.

#### Constructor

```python
DocumentProcessor(
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
)
```

**Parameters:**
- `chunk_size`: Maximum size of text chunks
- `chunk_overlap`: Overlap between consecutive chunks
- `embedding_model`: HuggingFace model identifier for embeddings

#### Methods

##### process_documents()
```python
def process_documents(documents: List[Dict[str, Any]]) -> None
```
Process a list of documents by chunking and creating embeddings.

**Parameters:**
- `documents`: List of document dictionaries with 'document', 'title', etc.

##### search_similar_chunks()
```python
def search_similar_chunks(query: str, k: int = 5) -> List[Dict[str, Any]]
```
Search for similar document chunks using semantic similarity.

**Parameters:**
- `query`: Search query string
- `k`: Number of results to return

**Returns:**
List of chunk metadata with similarity scores.

##### save_index() / load_index()
```python
def save_index(filepath: str) -> None
def load_index(filepath: str) -> None
```
Persist or load the vector index and metadata.

### LegalRAGSystem

The `LegalRAGSystem` class orchestrates the complete RAG pipeline for legal document analysis.

#### Constructor

```python
LegalRAGSystem(
    model_name: str = "llama3.2:1b",
    chunk_size: int = 1000,
    chunk_overlap: int = 200
)
```

**Parameters:**
- `model_name`: Ollama model identifier
- `chunk_size`: Text chunk size for processing
- `chunk_overlap`: Overlap between chunks

#### Methods

##### ask_question()
```python
def ask_question(question: str, k: int = 3) -> Dict[str, Any]
```
Answer a question using retrieval-augmented generation.

**Parameters:**
- `question`: Natural language question
- `k`: Number of context chunks to retrieve

**Returns:**
```python
{
    "answer": str,           # Generated answer
    "sources": List[Dict],   # Source documents with metadata
    "context_used": List[Dict]  # Retrieved chunks used for context
}
```

##### summarize_document()
```python
def summarize_document(document_text: str) -> str
```
Generate a summary of a legal document.

**Parameters:**
- `document_text`: Full text of the document

**Returns:**
Structured summary string.

##### summarize_by_title()
```python
def summarize_by_title(title: str) -> Dict[str, Any]
```
Find and summarize a document by its title.

**Parameters:**
- `title`: Document title to search for

**Returns:**
```python
{
    "summary": str,          # Generated summary
    "source": Dict           # Source document metadata
}
```

### DatasetLoader

Utility class for loading documents from various sources.

#### Methods

##### load_huggingface_dataset()
```python
def load_huggingface_dataset(
    dataset_name: str,
    config: str = "default",
    split: str = "train",
    num_samples: Optional[int] = None
) -> List[Dict[str, Any]]
```
Load dataset from HuggingFace Hub.

##### load_local_files()
```python
def load_local_files(file_paths: List[str]) -> List[Dict[str, Any]]
```
Load documents from local files.

##### validate_documents()
```python
def validate_documents(documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]
```
Validate and clean document data.

### PerformanceMetrics

Performance monitoring and metrics collection.

#### Methods

##### measure_time()
```python
@contextmanager
def measure_time(metric_name: str)
```
Context manager for measuring execution time.

**Usage:**
```python
metrics = PerformanceMetrics()
with metrics.measure_time('qa_response_times'):
    result = rag.ask_question("What is the main issue?")
```

##### get_summary()
```python
def get_summary() -> Dict[str, Any]
```
Get statistical summary of all collected metrics.

##### export_metrics()
```python
def export_metrics(filepath: str) -> None
```
Export metrics to JSON file.

## Configuration

### Settings Module

The `config.settings` module provides centralized configuration:

```python
from lexilocal.config import get_config

config = get_config()

# Access different configuration sections
model_config = config['model']
processing_config = config['processing']
ui_config = config['ui']
```

### Available Settings

#### Model Configuration
```python
{
    'default': 'llama3.2:1b',
    'available': ['llama3.2:1b', 'llama3:8b', 'mistral:7b', 'gemma:7b']
}
```

#### Processing Configuration
```python
{
    'chunk_size': 1000,
    'chunk_overlap': 200,
    'embedding_model': 'sentence-transformers/all-MiniLM-L6-v2',
    'batch_size': 32,
    'max_sequence_length': 512
}
```

## Error Handling

### Custom Exceptions

```python
class LexiLocalError(Exception):
    """Base exception for LexiLocal."""
    pass

class DocumentProcessingError(LexiLocalError):
    """Raised when document processing fails."""
    pass

class ModelLoadError(LexiLocalError):
    """Raised when model loading fails."""
    pass

class SearchError(LexiLocalError):
    """Raised when search operations fail."""
    pass
```

### Error Response Format

API methods return consistent error information:

```python
{
    "error": True,
    "error_type": "DocumentProcessingError",
    "message": "Failed to process document: invalid format",
    "details": {...}  # Additional error context
}
```

## Usage Examples

### Basic RAG Pipeline

```python
from lexilocal import LegalRAGSystem, get_mock_dataset

# Initialize system
rag = LegalRAGSystem(model_name="llama3.2:1b")

# Load documents
documents = get_mock_dataset()
rag.load_documents(documents)

# Ask questions
result = rag.ask_question("What was the court's decision?")
print(f"Answer: {result['answer']}")
print(f"Sources: {len(result['sources'])}")

# Generate summary
summary = rag.summarize_by_title("Johnson v. Smith")
print(f"Summary: {summary['summary']}")
```

### Custom Document Processing

```python
from lexilocal.core import DocumentProcessor

# Initialize with custom settings
processor = DocumentProcessor(
    chunk_size=500,
    chunk_overlap=100,
    embedding_model="all-mpnet-base-v2"
)

# Process documents
processor.process_documents(my_documents)

# Search for relevant content
results = processor.search_similar_chunks("contract breach", k=5)

# Save for later use
processor.save_index("my_legal_docs")
```

### Performance Monitoring

```python
from lexilocal.utils import PerformanceMetrics

metrics = PerformanceMetrics()

# Time different operations
with metrics.measure_time('document_loading'):
    rag.load_documents(documents)

with metrics.measure_time('qa_processing'):
    result = rag.ask_question("Legal question")

# Get performance summary
summary = metrics.get_summary()
print(f"Average Q&A time: {summary['qa_processing']['mean']:.2f}s")

# Export for analysis
metrics.export_metrics("performance_report.json")
```

### Custom Data Loading

```python
from lexilocal.data import DatasetLoader

loader = DatasetLoader()

# Load from HuggingFace
hf_docs = loader.load_huggingface_dataset(
    "HFforLegal/case-law",
    config="default",
    num_samples=100
)

# Load local files
local_docs = loader.load_local_files([
    "/path/to/case1.txt",
    "/path/to/case2.txt"
])

# Combine and validate
all_docs = hf_docs + local_docs
validated_docs = loader.validate_documents(all_docs)
```

## Integration Patterns

### Streamlit Integration

```python
import streamlit as st
from lexilocal import LegalRAGSystem

@st.cache_resource
def load_rag_system():
    return LegalRAGSystem()

rag = load_rag_system()

# Chat interface
if question := st.chat_input("Ask a legal question"):
    with st.spinner("Processing..."):
        result = rag.ask_question(question)
    st.write(result['answer'])
```

### Command Line Integration

```python
import argparse
from lexilocal import LegalRAGSystem, get_mock_dataset

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--question", required=True)
    parser.add_argument("--model", default="llama3.2:1b")
    args = parser.parse_args()
    
    rag = LegalRAGSystem(model_name=args.model)
    rag.load_documents(get_mock_dataset())
    
    result = rag.ask_question(args.question)
    print(result['answer'])

if __name__ == "__main__":
    main()
```