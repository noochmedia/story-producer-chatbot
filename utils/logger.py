import logging

def setup_logger():
    """Configure and return logger instance"""
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('flask.log')
        ]
    )
    return logging.getLogger(__name__)

logger = setup_logger()