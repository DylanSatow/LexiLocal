#!/usr/bin/env python3

from typing import List, Dict, Any
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama
from langchain_core.runnables import RunnablePassthrough
from document_processor import DocumentProcessor
from mock_data import get_mock_dataset

class LegalRAGSystem:
    def __init__(self, 
                 model_name: str = "llama3.2:1b",
                 chunk_size: int = 1000,
                 chunk_overlap: int = 200):
        """Initialize the Legal RAG system"""
        self.model_name = model_name
        
        # Initialize the LLM
        print(f"Initializing LLM: {model_name}")
        self.llm = Ollama(model=model_name, temperature=0.1)
        
        # Initialize document processor
        print("Initializing document processor...")
        self.doc_processor = DocumentProcessor(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        
        # Initialize prompts
        self._setup_prompts()
        
        # Initialize chains
        self._setup_chains()
        
    def _setup_prompts(self):
        """Set up prompt templates for different tasks"""
        
        # Q&A prompt
        self.qa_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a legal AI assistant specializing in analyzing legal documents. 
You will be provided with relevant excerpts from legal case documents and a question.

Your task is to:
1. Answer the question based ONLY on the provided context
2. Be precise and accurate in your legal analysis
3. Cite specific parts of the documents when relevant
4. If the context doesn't contain enough information to answer the question, clearly state this
5. Use clear, professional legal language

Context from legal documents:
{context}

Remember: Only use information from the provided context. Do not make assumptions or use external legal knowledge not present in the context."""),
            ("human", "Question: {question}")
        ])
        
        # Summarization prompt
        self.summary_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a legal AI assistant that creates concise summaries of legal documents.

Your task is to:
1. Provide a clear, structured summary of the legal document
2. Include key facts, legal issues, holdings, and reasoning
3. Maintain accuracy and legal precision
4. Use appropriate legal terminology
5. Structure the summary with clear sections (Facts, Issues, Holding, Reasoning)

Document to summarize:
{document}"""),
            ("human", "Please provide a comprehensive summary of this legal document.")
        ])
        
    def _setup_chains(self):
        """Set up LangChain chains for different tasks"""
        
        # Q&A chain
        self.qa_chain = (
            {
                "context": lambda x: self._format_context(x["context"]),
                "question": RunnablePassthrough()
            }
            | self.qa_prompt
            | self.llm
            | StrOutputParser()
        )
        
        # Summary chain
        self.summary_chain = (
            {"document": RunnablePassthrough()}
            | self.summary_prompt
            | self.llm
            | StrOutputParser()
        )
        
    def _format_context(self, context_chunks: List[Dict[str, Any]]) -> str:
        """Format retrieved context chunks for the prompt"""
        formatted_chunks = []
        
        for i, chunk in enumerate(context_chunks, 1):
            chunk_text = f"""
--- Document {i}: {chunk['title']} ---
Citation: {chunk['citation']}
Content: {chunk['text']}
"""
            formatted_chunks.append(chunk_text)
        
        return "\n".join(formatted_chunks)
    
    def load_documents(self, documents: List[Dict[str, Any]]) -> None:
        """Load and process documents for RAG"""
        print("Loading documents into RAG system...")
        self.doc_processor.process_documents(documents)
        print("Documents loaded successfully!")
    
    def load_index(self, filepath: str) -> None:
        """Load pre-built index"""
        print(f"Loading index from {filepath}...")
        self.doc_processor.load_index(filepath)
        print("Index loaded successfully!")
    
    def save_index(self, filepath: str) -> None:
        """Save current index"""
        self.doc_processor.save_index(filepath)
    
    def ask_question(self, question: str, k: int = 3) -> Dict[str, Any]:
        """Answer a question using RAG"""
        print(f"Processing question: {question}")
        
        # Retrieve relevant chunks
        relevant_chunks = self.doc_processor.search_similar_chunks(question, k=k)
        
        if not relevant_chunks:
            return {
                "answer": "I couldn't find relevant information in the legal documents to answer your question.",
                "sources": [],
                "context_used": []
            }
        
        # Generate answer using RAG chain
        answer = self.qa_chain.invoke({
            "context": relevant_chunks,
            "question": question
        })
        
        # Prepare source information
        sources = []
        for chunk in relevant_chunks:
            sources.append({
                "title": chunk['title'],
                "citation": chunk['citation'],
                "similarity_score": chunk['similarity_score']
            })
        
        return {
            "answer": answer,
            "sources": sources,
            "context_used": relevant_chunks
        }
    
    def summarize_document(self, document_text: str) -> str:
        """Summarize a legal document"""
        print("Generating document summary...")
        
        # Use summary chain
        summary = self.summary_chain.invoke(document_text)
        
        return summary
    
    def summarize_by_title(self, title: str) -> Dict[str, Any]:
        """Summarize a document by finding it by title"""
        # Search for the document
        search_results = self.doc_processor.search_similar_chunks(title, k=1)
        
        if not search_results:
            return {
                "summary": f"Document with title '{title}' not found.",
                "source": None
            }
        
        # Get the full document text (combine all chunks from the same document)
        doc_id = search_results[0]['doc_id']
        doc_chunks = [chunk for chunk in self.doc_processor.chunk_metadata 
                     if chunk['doc_id'] == doc_id]
        
        # Sort chunks by index
        doc_chunks.sort(key=lambda x: x['chunk_index'])
        
        # Combine all chunks
        full_text = "\n".join([chunk['text'] for chunk in doc_chunks])
        
        # Generate summary
        summary = self.summarize_document(full_text)
        
        return {
            "summary": summary,
            "source": {
                "title": doc_chunks[0]['title'],
                "citation": doc_chunks[0]['citation'],
                "total_chunks": len(doc_chunks)
            }
        }

def main():
    """Test the RAG system"""
    print("Testing Legal RAG System...")
    
    # Initialize RAG system
    rag = LegalRAGSystem()
    
    # Load mock documents
    mock_docs = get_mock_dataset()
    rag.load_documents(mock_docs)
    
    # Test questions
    test_questions = [
        "What was the outcome of Johnson v. Smith?",
        "What constitutional amendment was violated in Brown v. City of Los Angeles?",
        "What type of injunction was granted in the Tech Corp case?",
        "What are the requirements for a preliminary injunction?",
        "What happens when time is of the essence in a contract?"
    ]
    
    print("\n" + "="*60)
    print("TESTING Q&A FUNCTIONALITY")
    print("="*60)
    
    for question in test_questions:
        print(f"\n🔍 Question: {question}")
        print("-" * 50)
        
        result = rag.ask_question(question)
        
        print(f"Answer: {result['answer']}")
        print(f"\nSources used:")
        for i, source in enumerate(result['sources'], 1):
            print(f"  {i}. {source['title']} (similarity: {source['similarity_score']:.3f})")
    
    print("\n" + "="*60)
    print("TESTING SUMMARIZATION FUNCTIONALITY")
    print("="*60)
    
    # Test document summarization
    for doc in mock_docs:
        print(f"\n📄 Summarizing: {doc['title']}")
        print("-" * 50)
        
        result = rag.summarize_by_title(doc['title'])
        print(f"Summary: {result['summary']}")
        print(f"Source: {result['source']['citation']}")
    
    # Save the index for future use
    rag.save_index("legal_rag_index")
    print("\n✅ RAG system test completed!")

if __name__ == "__main__":
    main()