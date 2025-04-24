"""
Example script to demonstrate how to use the PDF RAG system with a specific PDF file.
"""

import os
from pdf_rag.pdf_processor import PDFProcessor

# Path to your PDF file
PDF_PATH = "/Users/himanshu/Downloads/4854XXXXXXXXXX09_19-04-2025.PDF"
# Password for your PDF file
PDF_PASSWORD = "HIMA1010"
# Directory to persist the vector store
PERSIST_DIR = "./data/vectorstore"

def main():
    # Create the data directory if it doesn't exist
    os.makedirs(PERSIST_DIR, exist_ok=True)
    
    # Create PDF processor
    processor = PDFProcessor(PDF_PATH, PDF_PASSWORD)
    
    # Process the PDF and create a vector store
    print(f"Processing PDF: {PDF_PATH}")
    processor.process_pdf(PERSIST_DIR)
    
    # Example questions to ask
    questions = [
        "What is the document type?",
        "What is the date of this document?",
        "What bank issued this document?",
        "What are the main sections in this document?"
    ]
    
    # Answer each question
    for question in questions:
        print(f"\nQuestion: {question}")
        result = processor.answer_question(question)
        
        print("Answer:")
        print(result["result"])
        print("-" * 50)

if __name__ == "__main__":
    main()