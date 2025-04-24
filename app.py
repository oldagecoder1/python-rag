"""
Streamlit web application for the PDF RAG system.
"""

import os
import streamlit as st
from pdf_rag.pdf_processor import PDFProcessor

def main():
    st.set_page_config(
        page_title="PDF Question Answering",
        page_icon="📄",
        layout="wide"
    )
    
    st.title("📄 PDF Question Answering System")
    st.write("Upload a PDF file and ask questions about its content.")
    
    # Sidebar for PDF upload and processing
    with st.sidebar:
        st.header("Upload PDF")
        uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
        
        pdf_password = st.text_input("PDF Password (if protected)", type="password")
        
        process_button = st.button("Process PDF")
        
        st.divider()
        st.write("Made with ❤️ using LangChain and OpenAI")
    
    # Main content area
    if uploaded_file is not None:
        # Save the uploaded file temporarily
        pdf_path = os.path.join("./data", uploaded_file.name)
        os.makedirs("./data", exist_ok=True)
        
        with open(pdf_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Create a session state to store the processor
        if "processor" not in st.session_state or process_button:
            with st.spinner("Processing PDF..."):
                st.session_state.processor = PDFProcessor(pdf_path, pdf_password if pdf_password else None)
                st.session_state.processor.process_pdf()
                st.success("PDF processed successfully!")
        
        # Question answering
        st.header("Ask a Question")
        question = st.text_input("Enter your question about the PDF")
        
        if question and st.button("Get Answer"):
            with st.spinner("Generating answer..."):
                result = st.session_state.processor.answer_question(question)
                
                st.header("Answer")
                st.write(result["result"])
                
                with st.expander("View Sources"):
                    for i, doc in enumerate(result["source_documents"]):
                        st.markdown(f"**Source {i+1}:**")
                        st.text(doc.page_content[:500] + "..." if len(doc.page_content) > 500 else doc.page_content)
    else:
        st.info("Please upload a PDF file to get started.")
        
        # Example questions
        st.header("Example Questions You Can Ask")
        st.write("- What is this document about?")
        st.write("- What are the key sections in this document?")
        st.write("- What is the date of this document?")
        st.write("- Who issued this document?")

if __name__ == "__main__":
    main()