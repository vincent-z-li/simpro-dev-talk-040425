import os
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from api.core.config import settings
from api.core.logging import logger

def get_vector_store():
    try:
        embeddings = OpenAIEmbeddings()

        if os.path.exists(settings.VECTOR_STORE_PATH):
            vector_store = FAISS.load_local(
                settings.VECTOR_STORE_PATH, 
                embeddings,
                allow_dangerous_deserialization=True
            )
            return vector_store
        else:
            logger.warning("Created empty vector store - no documents indexed yet")
            return FAISS.from_documents([], embeddings)  
    except Exception as e:
        logger.error(f"Error getting vector store: {str(e)}")
        raise