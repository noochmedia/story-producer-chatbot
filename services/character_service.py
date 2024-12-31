import os
import json
from utils.logger import logger
from services.transcript_service import TranscriptService
from services.chat_service import ChatService
from services.prompt_manager import PromptManager

class CharacterService:
    def __init__(self):
        self.chat_service = ChatService()
        self.transcript_service = TranscriptService()
        self.prompt_manager = PromptManager()
        self.characters_file = 'characters.json'

    def generate_character_brief(self, character_name, transcripts):
        """Generate a detailed brief about a character using the character_brief prompt"""
        try:
            # Collect all mentions of the character from transcripts
            character_mentions = []
            for transcript in transcripts:
                # Find sections where character is mentioned
                mentions = self._find_character_mentions(transcript, character_name)
                if mentions:
                    character_mentions.extend(mentions)

            if not character_mentions:
                return f"No information found about {character_name} in the transcripts."

            # Construct the context for the AI
            context = "\n".join([
                f"Transcript excerpt {i+1}:",
                mention,
                "---"
            ] for i, mention in enumerate(character_mentions))

            # Get the character brief prompt from prompt manager
            brief_prompt = self.prompt_manager.get_prompt('character_brief')
            if not brief_prompt:
                raise Exception("Character brief prompt not found")
                
            # Create the full prompt
            full_prompt = f"{brief_prompt}\n\nCharacter Name: {character_name}\n\nContext:\n{context}"

            # Get the AI response
            response = self.chat_service.get_chat_response(full_prompt)
            return response

        except Exception as e:
            logger.error(f"Error generating character brief: {str(e)}")
            raise

    def _extract_characters_from_transcript(self, transcript_path):
        """Extract character names from transcript filename"""
        try:
            from utils.name_checker import NameChecker
            name_checker = NameChecker()
            
            # Get filename without extension
            filename = os.path.basename(transcript_path)
            name_part = os.path.splitext(filename)[0]
            
            # Remove any date or identifier patterns
            import re
            clean_name = re.sub(r'_?\d{4}-\d{2}-\d{2}.*$', '', name_part)
            clean_name = re.sub(r'_?\d+$', '', clean_name)
            
            # Replace separators with spaces and clean up
            clean_name = clean_name.replace('_', ' ').replace('-', ' ')
            
            # Extract names using the name checker
            names = name_checker.extract_names(clean_name)
            return names if names else []
            
        except Exception as e:
            logger.error(f"Error extracting characters from transcript: {str(e)}")
            return []

    def _find_character_mentions(self, transcript, character_name):
        """Find relevant mentions of a character in a transcript"""
        mentions = []
        
        # Split into paragraphs and look for name mentions
        paragraphs = transcript.split('\n\n')
        for para in paragraphs:
            if character_name.lower() in para.lower():
                # Get surrounding context
                mentions.append(para)

        return mentions

    def get_all_characters(self, refresh=False):
        """Get list of all characters. If refresh=True, re-scan all transcripts"""
        try:
            if refresh:
                characters = set()
                # Get all transcripts
                transcripts = self.transcript_service.get_transcript_list()
                for transcript_id in transcripts:
                    path = os.path.join(self.transcript_service.transcripts_dir, transcript_id)
                    chars = self._extract_characters_from_transcript(path)
                    characters.update(chars)
                # Save and return the updated list
                character_list = list(characters)
                self._save_characters(character_list)
                return character_list
            else:
                return self.transcript_service.get_characters()
        except Exception as e:
            logger.error(f"Error getting characters: {str(e)}")
            return []

    def add_character(self, name):
        """Add a new character"""
        try:
            characters = self.get_all_characters()
            if name not in characters:
                characters.append(name)
                self._save_characters(characters)
            return characters
        except Exception as e:
            logger.error(f"Error adding character: {str(e)}")
            raise

    def delete_character(self, name):
        """Delete a character"""
        try:
            characters = self.get_all_characters()
            if name in characters:
                characters.remove(name)
                self._save_characters(characters)
            return characters
        except Exception as e:
            logger.error(f"Error deleting character: {str(e)}")
            raise

    def _save_characters(self, characters):
        """Save characters to file"""
        try:
            with open(self.characters_file, 'w') as f:
                json.dump(characters, f)
        except Exception as e:
            logger.error(f"Error saving characters: {str(e)}")
            raise