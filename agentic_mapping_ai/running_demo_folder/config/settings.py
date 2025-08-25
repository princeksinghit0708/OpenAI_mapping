"""
Configuration settings for Agentic Mapping AI Platform
"""

import os
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import Field
from pathlib import Path


class DatabaseSettings(BaseSettings):
    """Database configuration"""
    url: str = Field(default="postgresql://localhost:5432/agentic_mapping")
    echo: bool = Field(default=False)
    pool_size: int = Field(default=10)
    max_overflow: int = Field(default=20)
    
    class Config:
        env_prefix = "DATABASE_"


class VectorDBSettings(BaseSettings):
    """Vector database configuration"""
    type: str = Field(default="chroma")  # chroma, pinecone, faiss
    chroma_persist_directory: str = Field(default="./data/chroma_db")
    pinecone_api_key: Optional[str] = None
    pinecone_environment: Optional[str] = None
    embedding_model: str = Field(default="sentence-transformers/all-MiniLM-L6-v2")
    
    class Config:
        env_prefix = "VECTOR_DB_"


class LLMSettings(BaseSettings):
    """LLM configuration - Now using token-based authentication"""
    # API keys are no longer required - using token-based auth
    default_model: str = Field(default="claude-3-7-sonnet@20250219")  # Updated to use actual default model
    temperature: float = Field(default=0.1)
    max_tokens: int = Field(default=2000)
    default_provider: str = Field(default="claude")  # Updated to use claude as default provider
    
    class Config:
        env_prefix = "LLM_"


class AgentSettings(BaseSettings):
    """Agent configuration"""
    max_iterations: int = Field(default=5)
    timeout: int = Field(default=300)
    enable_memory: bool = Field(default=True)
    memory_type: str = Field(default="buffer")  # buffer, summary, entity
    
    class Config:
        env_prefix = "AGENT_"


class RAGSettings(BaseSettings):
    """RAG configuration"""
    max_retrieval_results: int = Field(default=10)
    similarity_threshold: float = Field(default=0.7)
    chunk_size: int = Field(default=1000)
    chunk_overlap: int = Field(default=200)
    
    class Config:
        env_prefix = "RAG_"


class CodeGenSettings(BaseSettings):
    """Code generation configuration"""
    default_spark_version: str = Field(default="3.5.0")
    code_output_dir: str = Field(default="./output/code")
    test_output_dir: str = Field(default="./output/tests")
    templates_dir: str = Field(default="./templates")
    
    class Config:
        env_prefix = "CODEGEN_"


class APISettings(BaseSettings):
    """API configuration"""
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8000)
    reload: bool = Field(default=True)
    cors_origins: List[str] = Field(default=["*"])
    
    class Config:
        env_prefix = "API_"


class UISettings(BaseSettings):
    """UI configuration"""
    streamlit_port: int = Field(default=8501)
    streamlit_host: str = Field(default="localhost")
    
    class Config:
        env_prefix = "UI_"


class MonitoringSettings(BaseSettings):
    """Monitoring configuration"""
    enable_metrics: bool = Field(default=True)
    metrics_port: int = Field(default=9090)
    log_level: str = Field(default="INFO")
    
    class Config:
        env_prefix = "MONITORING_"


class AppSettings(BaseSettings):
    """Main application settings"""
    name: str = Field(default="Agentic Mapping AI")
    version: str = Field(default="1.0.0")
    debug: bool = Field(default=False)
    
    # Sub-configurations
    database: DatabaseSettings = DatabaseSettings()
    vector_db: VectorDBSettings = VectorDBSettings()
    llm: LLMSettings = LLMSettings()
    agents: AgentSettings = AgentSettings()
    rag: RAGSettings = RAGSettings()
    codegen: CodeGenSettings = CodeGenSettings()
    api: APISettings = APISettings()
    ui: UISettings = UISettings()
    monitoring: MonitoringSettings = MonitoringSettings()
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = AppSettings()


def get_project_root() -> Path:
    """Get the project root directory"""
    return Path(__file__).parent.parent


def ensure_directories():
    """Ensure all required directories exist"""
    directories = [
        settings.codegen.code_output_dir,
        settings.codegen.test_output_dir,
        settings.vector_db.chroma_persist_directory,
        "./data/input",
        "./data/processed", 
        "./data/embeddings",
        "./output/reports",
        "./logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)


# Initialize directories on import
ensure_directories()