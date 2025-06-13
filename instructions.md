# Project Specification: AI-Powered Legal Document Summarization and Q&A with Local LLM Optimization

## 1. Project Goal

Develop an application that can:
* Summarize legal case documents.
* Answer natural language questions based on the content of those documents.
* Prioritize efficient local inference using quantized Large Language Models (LLMs).

## 2. Skills Showcased

This project is designed to highlight the user's existing strengths and interests, including:
* **LLM Application Development:** Building a Retrieval-Augmented Generation (RAG) system for Q&A and implementing summarization functionalities. This directly leverages expertise in LangChain and LangGraph.
* **High-Performance Machine Learning & Optimization:** Implementing and evaluating LLM quantization techniques to optimize inference speed and reduce memory footprint on local hardware. This ties into coursework in High Performance Machine Learning, experience with GPU-accelerated kNN, and cuDNN.
* **Software Engineering & Production Readiness:** Developing a complete, end-to-end application, including data pipeline, LLM integration, and a user interface, with an emphasis on code quality, scalability, and efficiency. This aligns with experience from an AWS SDE internship and developing AI lab management software.
* **Research Acumen:** The project involves applying advanced techniques (quantization, RAG) and understanding their trade-offs, reflecting a strong research background.

## 3. Dataset

* **Name:** `HFforLegal/case-law`
* **Source:** Hugging Face Datasets
* **Split to Use:** "us" (for United States legal documents)
* **URL:** [HFforLegal/case-law Dataset](https://huggingface.co/datasets/HFforLegal/case-law)
* **Key Fields:** The dataset contains fields such as `id`, `title`, `citation`, `docket_number`, `state`, `issuer`, `document` (full text of the legal case), `hash`, and `timestamp`. The `document` field will be the primary source for summarization and Q&A.

## 4. Detailed Step-by-Step Implementation

### Phase 1: Project Setup and Data Preparation

1.  **Environment Setup:**
    * Create a new Python virtual environment.
    * Install core libraries: `transformers`, `torch` (ensure CUDA support if available, e.g., `pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121`), `langchain`, `langgraph`, `sentence-transformers`, `faiss-cpu`, `ollama` (for local LLM), `streamlit` (for UI).

2.  **Data Acquisition and Initial Exploration:**
    * Load the `HFforLegal/case-law` dataset using `datasets.load_dataset("HFforLegal/case-law", "us")`.
    * Inspect the dataset structure and sample entries, particularly the `document` field.

3.  **Document Chunking and Embedding:**
    * **Purpose:** Break down large legal documents into smaller, semantically meaningful chunks for the RAG system to efficiently retrieve relevant passages.
    * **Method:** Use `RecursiveCharacterTextSplitter` from `langchain.text_splitter` to chunk the `document` field. Experiment with different `chunk_size` and `chunk_overlap` values (e.g., `chunk_size=1000`, `chunk_overlap=200`).
    * **Embedding Model:** Choose a suitable open-source embedding model (e.g., `sentence-transformers/all-MiniLM-L6-v2`) to convert text chunks into vector embeddings.

### Phase 2: Local LLM Setup and Optimization

1.  **LLM Selection:**
    * Choose a powerful yet runnable-locally open-source LLM. Recommended options include:
        * `llama3` (Meta Llama 3)
        * `mistral` (Mistral AI models)
        * `gemma` (Google Gemma)
    * Prioritize models known for strong performance in summarization and Q&A tasks.

2.  **Local LLM Inference with Ollama:**
    * Install Ollama from their official website (https://ollama.com/).
    * Download the chosen LLM model using Ollama (e.g., `ollama pull llama3`).
    * Configure `langchain` to use the locally running Ollama model (e.g., `Ollama(model="llama3")`).
    * *Alternative (for advanced users leveraging CUDA skills):* Explore running the chosen LLM directly using `llama.cpp` for more fine-grained control over GPU usage and quantization. This would involve compiling `llama.cpp` with CUDA support and using its Python bindings or a compatible library.

3.  **LLM Quantization (Critical Optimization Step):**
    * **Purpose:** Reduce model size and accelerate inference by representing model weights with lower precision (e.g., 4-bit, 8-bit integers).
    * **Methods:**
        * **For models served by Ollama:** Ollama often provides quantized versions (e.g., `llama3:8b-instruct-q4_0`). Use these directly.
        * **Manual Quantization (more advanced):** If using Hugging Face models directly with `transformers` and `torch`, explore techniques like:
            * **bitsandbytes:** For 4-bit or 8-bit quantization during inference.
            * **GPTQ:** For post-training quantization.
            * **QLoRA:** For fine-tuning quantized models (might be a stretch goal for this project, but demonstrates advanced skills).
    * **Implementation:** Apply the chosen quantization method to the selected LLM. Measure the impact on model size, inference speed, and summarization/Q&A quality.
    * *Dylan's advantage:* His `cuDNN` and GPU acceleration experience will be highly beneficial here for troubleshooting and optimizing quantization.

### Phase 3: RAG and Application Logic

1.  **Vector Database Setup:**
    * **Method:** Use `FAISS` (Facebook AI Similarity Search) as the local vector store for simplicity and efficiency.
    * **Implementation:** Create a `FAISS` index from the embeddings of the legal document chunks. Persist the vector store for later use.

2.  **Retrieval-Augmented Generation (RAG) Pipeline:**
    * **Purpose:** Enhance LLM answers by retrieving relevant document chunks from the vector store before generating a response.
    * **Components:**
        * **Retriever:** Configure a retriever (e.g., `VectorStoreRetriever` from LangChain) to fetch top-k (e.g., k=3 to 5) most relevant chunks based on a user query.
        * **Prompt Engineering:** Craft a system prompt that instructs the LLM to answer questions *only* based on the provided retrieved context. Include instructions for summarization requests.
        * **LangChain/LangGraph Integration:** Use LangChain's `Runnable` interface or `LangGraph` for orchestrating the RAG chain (user query -> embed query -> retrieve chunks -> pass to LLM with prompt -> get answer).
        * *Dylan's advantage:* His LangGraph experience will be directly applicable for building sophisticated RAG agent workflows.

3.  **Summarization Module:**
    * **Method:** For summarization requests, pass the full legal document (or a significant portion) to the LLM with a specific summarization prompt (e.g., "Summarize the following legal document concisely: [document_text]").
    * **Evaluation (Qualitative):** Assess summary quality for conciseness, accuracy, and completeness.

4.  **Question Answering Module:**
    * **Method:** Integrate the RAG pipeline. When a user asks a question, retrieve relevant chunks from the legal document, combine them with the question and prompt, and send to the LLM.
    * **Evaluation (Qualitative):** Assess answer accuracy, relevance, and adherence to the provided context.

### Phase 4: User Interface and Deployment Considerations

1.  **User Interface (Streamlit/Gradio):**
    * **Framework:** Use `Streamlit` or `Gradio` to build a simple web interface.
    * **Features:**
        * Input area for legal case documents (e.g., paste text or upload a text file).
        * Input area for natural language questions.
        * Buttons for "Summarize Document" and "Ask Question."
        * Display area for generated summaries and answers.
        * Clear loading indicators during LLM inference.
    * *Dylan's advantage:* His software development experience will make this a straightforward task.

2.  **Local Deployment and Showcase:**
    * Provide clear instructions on how to run the application locally using `streamlit run app.py` (or `python app.py` if not using Streamlit).
    * Ensure the project's `README.md` file is comprehensive, explaining the architecture, setup instructions, how to run it, and key technical decisions (especially regarding quantization and RAG).

3.  **Future Production Deployment Considerations (Discussion in README):**
    * Discuss how this local prototype could be scaled for production:
        * **Cloud Deployment:** Containerization with Docker, deployment on AWS (EC2, ECS, or SageMaker Endpoints for LLM serving). This aligns with Dylan's AWS experience.
        * **Scalability:** Discuss load balancing, horizontal scaling of LLM inference, and distributed vector stores.
        * **Monitoring:** Model drift, data drift, LLM response quality.
        * **Data Security/Privacy:** Especially crucial for legal documents.
        * **API Exposure:** How the functionality could be exposed via a REST API.

## 5. Showcase and Documentation

* **GitHub Repository:** Create a well-structured GitHub repository for the project.
* **Comprehensive `README.md`:**
    * Project title and clear description.
    * Demonstration (GIF/video of the UI in action).
    * Motivation and problem solved.
    * Key features.
    * Technical architecture (diagram if possible, highlighting RAG, local LLM, quantization).
    * Detailed setup and run instructions.
    * Explanation of key technical decisions (LLM choice, quantization method, chunking strategy).
    * Results and observations (e.g., inference speed improvements due to quantization).
    * Future work/production considerations.
    * Clearly link to the `HFforLegal/case-law` dataset.
* **Code Quality:** Ensure clean, well-commented, modular code following Python best practices.
* **Quantified Results:** Whenever possible, quantify the impact of optimizations (e.g., "reduced model size by X%, increased inference speed by Y% on Z hardware").
