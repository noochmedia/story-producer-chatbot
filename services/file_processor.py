import base64
from utils.logger import logger

class FileProcessor:
    @staticmethod
    def process_text_content(content):
        """Process plain text content"""
        try:
            logger.debug("Processing text content")
            if isinstance(content, str):
                if content.startswith('data:text/plain;base64,'):
                    logger.debug("Decoding base64 text content")
                    return base64.b64decode(content.split(',')[1]).decode('utf-8')
                logger.debug("Using plain text content as is")
                return content
            else:
                logger.error(f"Unexpected content type: {type(content)}")
                raise Exception("Invalid content type")
        except Exception as e:
            logger.error(f"Error processing text: {str(e)}")
            raise Exception(f"Error processing text: {str(e)}")

    @classmethod
    def process_file_content(cls, content, file_type):
        """Process content based on file type"""
        logger.debug(f"Processing file content of type: {file_type}")
        try:
            if file_type.lower() != 'txt':
                raise Exception("Only .txt files are currently supported")
            return cls.process_text_content(content)
        except Exception as e:
            logger.error(f"Error in process_file_content: {str(e)}")
            raise