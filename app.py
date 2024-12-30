from flask import Flask
from flask_cors import CORS
import os

from config import Config
from routes.main import main_bp
from routes.transcript import transcript_bp
from routes.chat import chat_bp
from utils.logger import logger
from services.backup import BackupService

def create_automatic_backup():
    """Create a backup before starting the application"""
    try:
        backup_service = BackupService(
            backup_dir=Config.BACKUP_DIR,
            max_backups=Config.MAX_BACKUPS
        )
        source_dir = os.path.dirname(os.path.abspath(__file__))
        success = backup_service.create_backup(source_dir)
        if success:
            logger.info("Automatic backup created successfully before startup")
        else:
            logger.warning("Failed to create automatic backup before startup")
    except Exception as e:
        logger.error(f"Error creating automatic backup: {str(e)}")

def create_app(config_class=Config):
    """Application factory function"""
    # Create backup before initializing the app
    create_automatic_backup()
    
    app = Flask(__name__)
    
    # Initialize CORS
    CORS(app)
    
    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(transcript_bp)
    app.register_blueprint(chat_bp)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG
    )