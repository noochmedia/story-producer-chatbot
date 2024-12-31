import os
import json
from utils.logger import logger

class TranscriptService:
    def __init__(self):
        self.transcripts_dir = 'transcripts'
        self.characters_file = 'characters.json'

    def delete_transcript(self, transcript_id):
        """Delete a transcript and update character list"""
        try:
            # Construct the full path
            transcript_path = os.path.join(self.transcripts_dir, transcript_id)
            
            if not os.path.exists(transcript_path):
                raise ValueError(f"Transcript {transcript_id} not found")

            # Get characters from this transcript before deletion
            chars_in_transcript = self._extract_characters_from_transcript(transcript_path)
            
            # Delete the transcript file
            os.remove(transcript_path)
            
            # After deletion, check which characters appear in remaining transcripts
            remaining_chars = set()
            for transcript in self.get_transcript_list():
                path = os.path.join(self.transcripts_dir, transcript)
                transcript_chars = self._extract_characters_from_transcript(path)
                remaining_chars.update(transcript_chars)
            
            # Update character list to only include those still present
            self._save_characters(list(remaining_chars))
            
            return True

        except Exception as e:
            logger.error(f"Error deleting transcript: {str(e)}")
            raise

    def _extract_characters_from_transcript(self, transcript_path):
        """Extract character names from a transcript"""
        try:
            # Get characters that appear in this transcript
            current_transcript_characters = set()
            
            # Read the transcript content
            with open(transcript_path, 'r') as f:
                content = f.read()
            
            # Get all current characters
            all_characters = self.get_characters()
            
            # Check which characters appear in this transcript
            for character in all_characters:
                if character.lower() in content.lower():
                    current_transcript_characters.add(character)
            
            return list(current_transcript_characters)
            
        except Exception as e:
            logger.error(f"Error extracting characters: {str(e)}")
            return []

    def _update_character_list(self, removed_characters):
        """Update character list after removing characters"""
        try:
            current_characters = self.get_characters()
            
            # Only keep characters that aren't in the removed list
            remaining_characters = [c for c in current_characters if c not in removed_characters]
            
            # Save updated character list
            self._save_characters(remaining_characters)
            
            return remaining_characters
        except Exception as e:
            logger.error(f"Error updating character list: {str(e)}")
            raise

    def get_characters(self):
        """Get list of all characters"""
        try:
            if os.path.exists(self.characters_file):
                with open(self.characters_file, 'r') as f:
                    return json.load(f)
            return []
        except Exception as e:
            logger.error(f"Error reading characters: {str(e)}")
            return []

    def _save_characters(self, characters):
        """Save character list to file"""
        try:
            with open(self.characters_file, 'w') as f:
                json.dump(characters, f)
        except Exception as e:
            logger.error(f"Error saving characters: {str(e)}")
            raise

    def get_transcript_list(self):
        """Get list of all transcripts"""
        try:
            if not os.path.exists(self.transcripts_dir):
                return []
            return [f for f in os.listdir(self.transcripts_dir) 
                   if os.path.isfile(os.path.join(self.transcripts_dir, f))]
        except Exception as e:
            logger.error(f"Error getting transcript list: {str(e)}")
            return []

    def get_all_transcripts(self):
        """Get contents of all transcripts"""
        transcripts = []
        try:
            for transcript_id in self.get_transcript_list():
                path = os.path.join(self.transcripts_dir, transcript_id)
                with open(path, 'r') as f:
                    transcripts.append(f.read())
            return transcripts
        except Exception as e:
            logger.error(f"Error reading transcripts: {str(e)}")
            return []