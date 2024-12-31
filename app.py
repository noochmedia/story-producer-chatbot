from flask import Flask
from flask_cors import CORS
import os
import sys

from config import Config
from config_validator import ConfigValidator
from routes.main import main_bp
from routes.transcript import transcript_bp
from routes.chat import chat_bp
from utils.logger import logger
from services.backup import BackupService

def create_automatic_backup():
    """Create a backup before starting the application"""
    # Skip backup in production
    if os.getenv('FLASK_ENV') == 'production':
        logger.info("Skipping automatic backup in production environment")
        return

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
    # Validate environment variables
    if not ConfigValidator.check_configuration():
        logger.error("Missing required environment variables. Application cannot start.")
        sys.exit(1)
    app = Flask(__name__)
    
    # Initialize CORS with specific settings
    CORS(app, resources={
        r"/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # Load configuration
    app.config.from_object(config_class)
    
    # Create backup only in development
    if os.getenv('FLASK_ENV') != 'production':
        create_automatic_backup()
    
    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(transcript_bp)
    app.register_blueprint(chat_bp)
    
    @app.route('/health')
    def health_check():
        return {'status': 'healthy'}, 200
    
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.getenv('PORT', 8000))
    app.run(
        host='0.0.0.0',
        port=port,
        debug=os.getenv('FLASK_ENV') == 'development'
    )