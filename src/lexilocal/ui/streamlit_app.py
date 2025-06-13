#!/usr/bin/env python3

import streamlit as st
import os
import tempfile
from typing import Dict, Any
from ..core.rag_system import LegalRAGSystem
from ..data.mock_data import get_mock_dataset
from datasets import load_dataset

# Page configuration
st.set_page_config(
    page_title="LexiLocal - Legal Document AI",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f4e79;
        text-align: center;
        margin-bottom: 2rem;
    }
    .subheader {
        font-size: 1.5rem;
        color: #2c3e50;
        margin-bottom: 1rem;
    }
    .info-box {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #007bff;
        margin: 1rem 0;
    }
    .source-box {
        background-color: #f1f3f4;
        padding: 0.8rem;
        border-radius: 0.3rem;
        margin: 0.5rem 0;
        border-left: 3px solid #28a745;
    }
    .error-box {
        background-color: #f8d7da;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #dc3545;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'rag_system' not in st.session_state:
        st.session_state.rag_system = None
    if 'documents_loaded' not in st.session_state:
        st.session_state.documents_loaded = False
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

@st.cache_resource
def load_rag_system(model_name: str):
    """Load and cache the RAG system"""
    try:
        with st.spinner(f"Initializing AI system with {model_name}..."):
            return LegalRAGSystem(model_name=model_name)
    except Exception as e:
        st.error(f"Failed to initialize AI system: {str(e)}")
        return None

@st.cache_data
def load_mock_data():
    """Load mock data"""
    return get_mock_dataset()

def display_sources(sources: list):
    """Display source information"""
    if sources:
        st.subheader("📚 Sources")
        for i, source in enumerate(sources, 1):
            st.markdown(f"""
            <div class="source-box">
                <strong>{i}. {source['title']}</strong><br>
                <em>Citation:</em> {source['citation']}<br>
                <em>Relevance Score:</em> {source['similarity_score']:.3f}
            </div>
            """, unsafe_allow_html=True)

def main():
    """Main application"""
    initialize_session_state()
    
    # Header
    st.markdown('<div class="main-header">⚖️ LexiLocal</div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align: center; font-size: 1.2rem; color: #6c757d; margin-bottom: 2rem;">AI-Powered Legal Document Analysis & Q&A</div>', unsafe_allow_html=True)
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Model selection
        model_name = st.selectbox(
            "Select AI Model",
            ["llama3.2:1b", "llama3:8b", "mistral:7b", "gemma:7b"],
            help="Choose the local LLM model for processing"
        )
        
        # Data source selection
        st.subheader("📂 Data Source")
        data_source = st.radio(
            "Choose data source:",
            ["Mock Legal Documents", "Upload Documents", "HuggingFace Dataset"],
            help="Select the source of legal documents to analyze"
        )
        
        # Load RAG system
        if st.button("🚀 Initialize AI System", type="primary"):
            st.session_state.rag_system = load_rag_system(model_name)
            if st.session_state.rag_system:
                st.success("AI system initialized successfully!")
            else:
                st.error("Failed to initialize AI system. Make sure Ollama is running and the model is available.")
        
        # Load documents
        if st.session_state.rag_system and not st.session_state.documents_loaded:
            if st.button("📚 Load Documents", type="secondary"):
                try:
                    with st.spinner("Loading documents..."):
                        if data_source == "Mock Legal Documents":
                            documents = load_mock_data()
                            st.session_state.rag_system.load_documents(documents)
                            st.session_state.documents_loaded = True
                            st.success(f"Loaded {len(documents)} mock legal documents!")
                        
                        elif data_source == "HuggingFace Dataset":
                            # Load a subset of the HuggingFace dataset
                            with st.spinner("Downloading HuggingFace dataset..."):
                                dataset = load_dataset("HFforLegal/case-law", "default", split="train[:10]")
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
                                st.session_state.rag_system.load_documents(documents)
                                st.session_state.documents_loaded = True
                                st.success(f"Loaded {len(documents)} documents from HuggingFace!")
                        
                        else:  # Upload Documents
                            st.info("Document upload feature coming soon!")
                            
                except Exception as e:
                    st.error(f"Error loading documents: {str(e)}")
        
        # System status
        st.subheader("📊 System Status")
        if st.session_state.rag_system:
            st.success("✅ AI System Ready")
        else:
            st.warning("⏳ AI System Not Initialized")
        
        if st.session_state.documents_loaded:
            st.success("✅ Documents Loaded")
        else:
            st.warning("⏳ No Documents Loaded")

    # Main content area
    if not st.session_state.rag_system:
        st.markdown("""
        <div class="info-box">
            <h3>Welcome to LexiLocal!</h3>
            <p>LexiLocal is an AI-powered legal document analysis system that uses local LLMs for:</p>
            <ul>
                <li><strong>Document Summarization:</strong> Get concise summaries of legal cases</li>
                <li><strong>Q&A:</strong> Ask natural language questions about legal documents</li>
                <li><strong>Retrieval-Augmented Generation:</strong> Accurate answers based on document content</li>
                <li><strong>Local Processing:</strong> All analysis happens locally for privacy</li>
            </ul>
            <p><strong>To get started:</strong> Use the sidebar to initialize the AI system and load documents.</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    if not st.session_state.documents_loaded:
        st.markdown("""
        <div class="info-box">
            <h3>AI System Ready!</h3>
            <p>The AI system is initialized and ready. Please load documents using the sidebar to start analyzing legal content.</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Tabs for different functionalities
    tab1, tab2, tab3 = st.tabs(["💬 Q&A Chat", "📄 Document Summary", "🔍 Document Search"])
    
    with tab1:
        st.header("💬 Legal Q&A Chat")
        
        # Display chat history
        for message in st.session_state.chat_history:
            if message['role'] == 'user':
                st.chat_message("user").write(message['content'])
            else:
                with st.chat_message("assistant"):
                    st.write(message['content'])
                    if 'sources' in message:
                        display_sources(message['sources'])
        
        # Chat input
        if question := st.chat_input("Ask a legal question..."):
            # Add user message to chat history
            st.session_state.chat_history.append({'role': 'user', 'content': question})
            st.chat_message("user").write(question)
            
            # Generate response
            with st.chat_message("assistant"):
                with st.spinner("Analyzing documents and generating response..."):
                    try:
                        result = st.session_state.rag_system.ask_question(question)
                        st.write(result['answer'])
                        
                        # Add to chat history
                        st.session_state.chat_history.append({
                            'role': 'assistant', 
                            'content': result['answer'],
                            'sources': result['sources']
                        })
                        
                        # Display sources
                        display_sources(result['sources'])
                        
                    except Exception as e:
                        error_msg = f"Error generating response: {str(e)}"
                        st.error(error_msg)
                        st.session_state.chat_history.append({'role': 'assistant', 'content': error_msg})
    
    with tab2:
        st.header("📄 Document Summarization")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("Choose Document")
            
            # Get available documents
            if hasattr(st.session_state.rag_system.doc_processor, 'chunk_metadata'):
                available_docs = {}
                for chunk in st.session_state.rag_system.doc_processor.chunk_metadata:
                    doc_title = chunk['title']
                    if doc_title not in available_docs:
                        available_docs[doc_title] = chunk
                
                selected_doc = st.selectbox(
                    "Select document to summarize:",
                    list(available_docs.keys())
                )
                
                if st.button("📝 Generate Summary", type="primary"):
                    with st.spinner("Generating summary..."):
                        try:
                            result = st.session_state.rag_system.summarize_by_title(selected_doc)
                            
                            with col2:
                                st.subheader("Summary")
                                st.write(result['summary'])
                                
                                if result['source']:
                                    st.markdown(f"""
                                    <div class="source-box">
                                        <strong>Source:</strong> {result['source']['title']}<br>
                                        <strong>Citation:</strong> {result['source']['citation']}
                                    </div>
                                    """, unsafe_allow_html=True)
                        
                        except Exception as e:
                            st.error(f"Error generating summary: {str(e)}")
    
    with tab3:
        st.header("🔍 Document Search")
        
        search_query = st.text_input("Enter search terms:", placeholder="e.g., contract breach, constitutional rights, patent infringement")
        
        if search_query:
            try:
                results = st.session_state.rag_system.doc_processor.search_similar_chunks(search_query, k=5)
                
                if results:
                    st.subheader(f"Search Results for: '{search_query}'")
                    
                    for i, result in enumerate(results, 1):
                        with st.expander(f"{i}. {result['title']} (Score: {result['similarity_score']:.3f})"):
                            st.write(f"**Citation:** {result['citation']}")
                            st.write(f"**Content:** {result['text']}")
                            st.write(f"**Chunk {result['chunk_index'] + 1} of {result['total_chunks']}**")
                else:
                    st.info("No relevant documents found for your search query.")
                    
            except Exception as e:
                st.error(f"Search error: {str(e)}")

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #6c757d; font-size: 0.9rem;">
        <p>LexiLocal - AI-Powered Legal Document Analysis | Built with Streamlit, LangChain, and Ollama</p>
        <p>⚠️ This tool is for educational and research purposes. Always consult qualified legal professionals for legal advice.</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()