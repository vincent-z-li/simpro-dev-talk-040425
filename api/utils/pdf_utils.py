import os
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from api.core.logging import logger

def load_pdf(file_path: str):
    if not os.path.exists(file_path):
        logger.error(f"PDF file not found: {file_path}")
        raise FileNotFoundError(f"File not found: {file_path}")
    
    try:
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        chunks = text_splitter.split_documents(documents)
        
        logger.info(f"Loaded PDF: {file_path}, created {len(chunks)} chunks")
        return chunks
    except Exception as e:
        logger.error(f"Error loading PDF {file_path}: {str(e)}")
        raise