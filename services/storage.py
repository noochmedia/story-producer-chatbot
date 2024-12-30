import os
import json
from datetime import datetime
from utils.logger import logger

class TranscriptStorage:
    def __init__(self):
        self.base_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'transcripts')
        self.metadata_file = os.path.join(self.base_dir, 'metadata.json')
        self._ensure_directory_exists()
        self._load_metadata()
    
    def _ensure_directory_exists(self):
        """Ensure the transcripts directory exists"""
        os.makedirs(self.base_dir, exist_ok=True)
    
    def _load_metadata(self):
        """Load or create metadata file"""
        if os.path.exists(self.metadata_file):
            try:
                with open(self.metadata_file, 'r') as f:
                    self.metadata = json.load(f)
            except Exception as e:
                logger.error(f"Error loading metadata: {e}")
                self.metadata = {}
        else:
            self.metadata = {}
    
    def _save_metadata(self):
        """Save metadata to file"""
        try:
            with open(self.metadata_file, 'w') as f:
                json.dump(self.metadata, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving metadata: {e}")
    
    def save_transcript(self, transcript_id, content):
        """Save a transcript to file"""
        try:
            # Create a safe filename
            safe_filename = transcript_id.replace(' ', '_').replace('/', '_')
            file_path = os.path.join(self.base_dir, f"{safe_filename}.txt")
            
            # Save the transcript content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Update metadata
            self.metadata[transcript_id] = {
                'filename': f"{safe_filename}.txt",
                'upload_date': datetime.now().isoformat(),
                'size': len(content),
                'word_count': len(content.split())
            }
            
            # Save metadata
            self._save_metadata()
            
            logger.info(f"Saved transcript: {transcript_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving transcript {transcript_id}: {e}")
            raise
    
    def get_transcript(self, transcript_id):
        """Retrieve a transcript by ID"""
        try:
            if transcript_id not in self.metadata:
                logger.warning(f"Transcript not found: {transcript_id}")
                return None
            
            filename = self.metadata[transcript_id]['filename']
            file_path = os.path.join(self.base_dir, filename)
            
            if not os.path.exists(file_path):
                logger.error(f"Transcript file missing: {file_path}")
                return None
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return content
            
        except Exception as e:
            logger.error(f"Error retrieving transcript {transcript_id}: {e}")
            return None
    
    def get_all_transcripts(self):
        """Get all transcripts and their metadata"""
        transcripts = {}
        for transcript_id in self.metadata:
            content = self.get_transcript(transcript_id)
            if content is not None:
                transcripts[transcript_id] = content
        return transcripts
    
    def delete_transcript(self, transcript_id):
        """Delete a transcript"""
        try:
            if transcript_id not in self.metadata:
                return False
            
            filename = self.metadata[transcript_id]['filename']
            file_path = os.path.join(self.base_dir, filename)
            
            # Delete the file if it exists
            if os.path.exists(file_path):
                os.remove(file_path)
            
            # Remove from metadata
            del self.metadata[transcript_id]
            self._save_metadata()
            
            logger.info(f"Deleted transcript: {transcript_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting transcript {transcript_id}: {e}")
            return False