import os
import argparse
from pdf_processor import PDFProcessor

def main():
    parser = argparse.ArgumentParser(description="PDF RAG System")
    parser.add_argument("--pdf", type=str, help="Path to the PDF file", required=True)
    parser.add_argument("--password", type=str, help="Password for the PDF file (if protected)")
    parser.add_argument("--process", action="store_true", help="Process the PDF and create a vector store")
    parser.add_argument("--persist_dir", type=str, help="Directory to persist the vector store")
    parser.add_argument("--question", type=str, help="Question to ask about the PDF")
    
    args = parser.parse_args()
    
    # Create PDF processor
    processor = PDFProcessor(args.pdf, args.password)
    
    # Process the PDF if requested
    if args.process:
        print(f"Processing PDF: {args.pdf}")
        processor.process_pdf(args.persist_dir)
    
    # If a persist directory is provided but not processing, load the vector store
    elif args.persist_dir and os.path.exists(args.persist_dir):
        processor.load_vectorstore(args.persist_dir)
    
    # Answer a question if provided
    if args.question:
        if not processor.vectorstore:
            print("Vector store not loaded. Use --process or provide a valid --persist_dir.")
            return
        
        print(f"\nQuestion: {args.question}")
        result = processor.answer_question(args.question)
        
        print("\nAnswer:")
        print(result["result"])
        
        print("\nSources:")
        for i, doc in enumerate(result["source_documents"]):
            print(f"Source {i+1}:")
            print(doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content)
            print()

if __name__ == "__main__":
    main()
