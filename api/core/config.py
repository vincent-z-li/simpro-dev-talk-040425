from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Dev Talk Retrieval Augmented Generation(RAG) Demo"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "2025-04-04 Vince RAG with LangChain & monitor and trace with LangSmith"
    
    # LLM settings
    LLM_TEMPERATURE: float = 0.7 # [0,2] => [deterministic, creative]
    
    # Vector store settings
    VECTOR_STORE_PATH: str = "./data/vector_store"
    
    # LangSmith settings
    langsmith_tracing: bool = False
    langsmith_endpoint: str = None
    langsmith_api_key: str = None
    langsmith_project: str = None

    model_config = {
        "env_file": ".env",
        "extra": "ignore"
    }

settings = Settings()