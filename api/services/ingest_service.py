import os
import shutil
from dotenv import load_dotenv
from langchain.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from api.utils.pdf_utils import load_pdf
from api.core.config import settings
from api.core.logging import logger

load_dotenv()

def ingest_documents(directory_path: str = "./data/guides"):
    """Ingest documents from a directory into the vector store."""
    try:
        if os.path.exists(settings.VECTOR_STORE_PATH):
            shutil.rmtree(settings.VECTOR_STORE_PATH)
            logger.info(f"Removed existing vector store at {settings.VECTOR_STORE_PATH}")        
        os.makedirs(os.path.dirname(settings.VECTOR_STORE_PATH), exist_ok=True)
        

        all_chunks = []
        for filename in os.listdir(directory_path):
            if filename.endswith(".pdf"):
                file_path = os.path.join(directory_path, filename)
                chunks = load_pdf(file_path)
                all_chunks.extend(chunks)
        
        if not all_chunks:
            logger.warning(f"No documents found in {directory_path}")
            return False
        
        # create embeddings and vector store, and save it locally
        # in Production, this should be stored in s3 or similar
        embeddings = OpenAIEmbeddings()
        vector_store = FAISS.from_documents(all_chunks, embeddings)
        vector_store.save_local(settings.VECTOR_STORE_PATH)
        
        logger.info(f"Ingested {len(all_chunks)} chunks from {directory_path}")
        return True
    except Exception as e:
        logger.error(f"Error ingesting documents: {str(e)}")
        raise
    
    