import os
import argparse
from pdf_processor import PDFProcessor

def main():
    parser = argparse.ArgumentParser(description="PDF Chat System")
    parser.add_argument("--pdf", type=str, help="Path to the PDF file", required=True)
    parser.add_argument("--password", type=str, help="Password for the PDF file (if protected)")
    parser.add_argument("--persist_dir", type=str, help="Directory to persist the vector store")
    
    args = parser.parse_args()
    
    # Create PDF processor
    processor = PDFProcessor(args.pdf, args.password)
    
    # Check if vector store exists
    if args.persist_dir and os.path.exists(args.persist_dir):
        print(f"Loading existing vector store from {args.persist_dir}")
        processor.load_vectorstore(args.persist_dir)
    else:
        print(f"Processing PDF: {args.pdf}")
        processor.process_pdf(args.persist_dir)
    
    print("\nPDF Chat System")
    print("Type 'exit' or 'quit' to end the conversation")
    
    while True:
        question = input("\nYou: ")
        
        if question.lower() in ["exit", "quit"]:
            break
        
        result = processor.answer_question(question)
        
        print("\nAI: " + result["result"])

if __name__ == "__main__":
    main()