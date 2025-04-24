import os
import sys
from typing import List, Dict, Any

from pypdf import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class PDFProcessor:
    def __init__(self, pdf_path: str, password: str = None):
        """
        Initialize the PDF processor with a path to a PDF file and optional password.
        
        Args:
            pdf_path: Path to the PDF file
            password: Password to decrypt the PDF (if protected)
        """
        self.pdf_path = pdf_path
        self.password = password
        self.text_chunks = []
        self.vectorstore = None
        
        # Check if OpenAI API key is set
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY environment variable is not set")
    
    def extract_text(self) -> str:
        """
        Extract text from the PDF file.
        
        Returns:
            Extracted text from the PDF
        """
        try:
            reader = PdfReader(self.pdf_path)
            
            # If the PDF is encrypted and a password is provided
            if reader.is_encrypted and self.password:
                reader.decrypt(self.password)
            
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            
            return text
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
            return ""
    
    def chunk_text(self, text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[str]:
        """
        Split the extracted text into chunks.
        
        Args:
            text: Text to split into chunks
            chunk_size: Size of each chunk
            chunk_overlap: Overlap between chunks
            
        Returns:
            List of text chunks
        """
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len
        )
        
        self.text_chunks = text_splitter.split_text(text)
        return self.text_chunks
    
    def create_vectorstore(self, persist_directory: str = None) -> Chroma:
        """
        Create a vector store from the text chunks.
        
        Args:
            persist_directory: Directory to persist the vector store
            
        Returns:
            Chroma vector store
        """
        embeddings = OpenAIEmbeddings()
        
        if persist_directory:
            self.vectorstore = Chroma.from_texts(
                texts=self.text_chunks,
                embedding=embeddings,
                persist_directory=persist_directory
            )
            self.vectorstore.persist()
        else:
            self.vectorstore = Chroma.from_texts(
                texts=self.text_chunks,
                embedding=embeddings
            )
        
        return self.vectorstore
    
    def load_vectorstore(self, persist_directory: str) -> Chroma:
        """
        Load a vector store from a directory.
        
        Args:
            persist_directory: Directory where the vector store is persisted
            
        Returns:
            Chroma vector store
        """
        embeddings = OpenAIEmbeddings()
        self.vectorstore = Chroma(
            persist_directory=persist_directory,
            embedding_function=embeddings
        )
        return self.vectorstore
    
    def create_qa_chain(self, temperature: float = 0) -> RetrievalQA:
        """
        Create a question-answering chain.
        
        Args:
            temperature: Temperature for the language model
            
        Returns:
            RetrievalQA chain
        """
        if not self.vectorstore:
            raise ValueError("Vector store not created. Call create_vectorstore() first.")
        
        # Create a retriever from the vector store
        retriever = self.vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 4}
        )
        
        # Create a custom prompt template
        template = """
        You are an AI assistant specialized in analyzing PDF documents.
        Use the following pieces of context to answer the question at the end.
        If you don't know the answer, just say that you don't know, don't try to make up an answer.
        
        Context:
        {context}
        
        Question: {question}
        
        Answer:
        """
        
        prompt = PromptTemplate(
            template=template,
            input_variables=["context", "question"]
        )
        
        # Create the QA chain
        llm = ChatOpenAI(temperature=temperature, model_name="gpt-4")
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": prompt}
        )
        
        return qa_chain
    
    def process_pdf(self, persist_directory: str = None) -> None:
        """
        Process the PDF file: extract text, chunk it, and create a vector store.
        
        Args:
            persist_directory: Directory to persist the vector store
        """
        # Extract text from PDF
        text = self.extract_text()
        if not text:
            print("Failed to extract text from the PDF.")
            return
        
        # Chunk the text
        self.chunk_text(text)
        
        # Create vector store
        self.create_vectorstore(persist_directory)
        
        print(f"PDF processed successfully. Created {len(self.text_chunks)} chunks.")
    
    def answer_question(self, question: str) -> Dict[str, Any]:
        """
        Answer a question about the PDF.
        
        Args:
            question: Question to answer
            
        Returns:
            Dictionary with the answer and source documents
        """
        if not self.vectorstore:
            raise ValueError("Vector store not created. Process the PDF first.")
        
        qa_chain = self.create_qa_chain()
        result = qa_chain({"query": question})
        
        return result