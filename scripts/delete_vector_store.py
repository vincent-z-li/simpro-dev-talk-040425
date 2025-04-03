import shutil
import os
from api.core.config import settings

if os.path.exists(settings.VECTOR_STORE_PATH):
    print(f"Deleting vector store at {settings.VECTOR_STORE_PATH}")
    shutil.rmtree(settings.VECTOR_STORE_PATH)
    print("Vector store deleted successfully")
else:
    print("Vector store doesn't exist")