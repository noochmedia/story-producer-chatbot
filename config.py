import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # Mistral Configuration
    MISTRAL_API_URL = "http://162.243.42.76"
    MISTRAL_API_KEY = "L2Nisrbtg4s+KBTgK5fgKRDW+bcI/lx4a8QZ7Odyv7PCO2LWA"
    
    # Flask Configuration
    PORT = 5002
    DEBUG = True
    HOST = '0.0.0.0'

    # File Processing Configuration
    ALLOWED_EXTENSIONS = {'txt'}  # Currently supporting only text files
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Backup Configuration
    BACKUP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backup')
    MAX_BACKUPS = 5  # Maximum number of backups to keep
    BACKUP_EXCLUDE_PATTERNS = ['__pycache__', '*.pyc', '*.pyo', '*.pyd', '.git', '.env', 'backup']