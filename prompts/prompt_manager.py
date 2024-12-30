from . import (
    story_summary,
    character_brief,
    find_soundbites,
    create_soundbites
)

class PromptManager:
    @staticmethod
    def get_prompt(prompt_type):
        """Get the appropriate prompt based on the type requested"""
        prompts = {
            'story_summary': story_summary.get_prompt(),
            'character_brief': character_brief.get_prompt(),
            'find_soundbites': find_soundbites.get_prompt(),
            'create_soundbites': create_soundbites.get_prompt(),
        }
        return prompts.get(prompt_type, None)

    @staticmethod
    def detect_prompt_type(message):
        """Detect which type of prompt to use based on the message content"""
        message_lower = message.lower()
        
        # Character-related queries
        if any(word in message_lower for word in ['who', 'character', 'person', 'people']):
            return 'character_brief'
        
        # Soundbite-related queries
        if 'soundbite' in message_lower or 'sound bite' in message_lower:
            if 'create' in message_lower or 'sequence' in message_lower:
                return 'create_soundbites'
            return 'find_soundbites'
        
        # Story summary queries
        if any(word in message_lower for word in ['summary', 'summarize', 'overview']):
            return 'story_summary'
        
        return None  # No specific prompt detected