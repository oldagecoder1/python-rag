# PDF RAG System

A Retrieval-Augmented Generation (RAG) system for answering questions about PDF documents, including password-protected PDFs.

## Features

- Extract text from PDF documents (including password-protected PDFs)
- Process and chunk text for efficient retrieval
- Create and persist vector embeddings using OpenAI embeddings
- Answer questions about the PDF content using a retrieval-based approach
- Interactive chat interface

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd rag_practive
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your OpenAI API key:
```bash
# Create a .env file
cp .env.example .env
# Edit the .env file to add your OpenAI API key
```

## Usage

### Process a PDF and Answer Questions

```bash
python -m pdf_rag.main --pdf path/to/your/pdf --password your-password --process --persist_dir ./data/vectorstore --question "Your question about the PDF"
```

### Interactive Chat Interface

```bash
python -m pdf_rag.chat --pdf path/to/your/pdf --password your-password --persist_dir ./data/vectorstore
```

### Web Interface

```bash
streamlit run app.py
```

### Command-line Arguments

- `--pdf`: Path to the PDF file (required)
- `--password`: Password for the PDF file (if protected)
- `--process`: Process the PDF and create a vector store
- `--persist_dir`: Directory to persist the vector store
- `--question`: Question to ask about the PDF (for main.py)

## Example

```bash
# Process a PDF and create a vector store
python -m pdf_rag.main --pdf ./data/document.pdf --password HIMA1010 --process --persist_dir ./data/vectorstore

# Ask a question about the PDF
python -m pdf_rag.main --pdf ./data/document.pdf --password HIMA1010 --persist_dir ./data/vectorstore --question "What is this document about?"

# Start an interactive chat session
python -m pdf_rag.chat --pdf ./data/document.pdf --password HIMA1010 --persist_dir ./data/vectorstore
```

## How It Works

1. **PDF Text Extraction**: The system extracts text from the PDF document, handling password protection if necessary.

2. **Text Chunking**: The extracted text is split into manageable chunks with some overlap to maintain context.

3. **Vector Embedding**: Each text chunk is converted into a vector embedding using OpenAI's embedding model.

4. **Vector Storage**: The embeddings are stored in a Chroma vector database for efficient retrieval.

5. **Question Answering**: When a question is asked, the system:
   - Converts the question into an embedding
   - Retrieves the most relevant text chunks from the vector store
   - Sends the question and relevant context to a language model (GPT-4)
   - Returns the generated answer

## Requirements

- Python 3.8+
- OpenAI API key
- Dependencies listed in requirements.txt