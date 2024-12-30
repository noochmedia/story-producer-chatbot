import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # Mistral Configuration
    MISTRAL_API_URL = os.getenv('MISTRAL_API_URL')
    MISTRAL_API_KEY = os.getenv('MISTRAL_API_KEY')
    
    # Flask Configuration
    PORT = int(os.getenv('PORT', 8000))
    DEBUG = os.getenv('FLASK_ENV', 'production') == 'development'
    HOST = '0.0.0.0'

    # File Processing Configuration
    ALLOWED_EXTENSIONS = {'txt'}  # Currently supporting only text files
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Backup Configuration
    BACKUP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backup')
    MAX_BACKUPS = 5  # Maximum number of backups to keep
    BACKUP_EXCLUDE_PATTERNS = ['__pycache__', '*.pyc', '*.pyo', '*.pyd', '.git', '.env', 'backup']