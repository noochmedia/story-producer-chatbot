from .initial_routing import INITIAL_ROUTING_PROMPT
from .character_brief import CHARACTER_BRIEF_PROMPT
from .story_summary import STORY_SUMMARY_PROMPT
from .find_soundbites import FIND_SOUNDBITES_PROMPT
from .create_soundbites import CREATE_SOUNDBITES_PROMPT
from .quick_reference import QUICK_REFERENCE_PROMPT
from .context_check import CONTEXT_CHECK_PROMPT
from .extract_characters import EXTRACT_CHARACTERS_PROMPT

class PromptManager:
    def __init__(self):
        self.prompts = {
            'initial_routing': INITIAL_ROUTING_PROMPT,
            'character_brief': CHARACTER_BRIEF_PROMPT,
            'story_summary': STORY_SUMMARY_PROMPT,
            'find_soundbites': FIND_SOUNDBITES_PROMPT,
            'create_soundbites': CREATE_SOUNDBITES_PROMPT,
            'quick_reference': QUICK_REFERENCE_PROMPT,
            'context_check': CONTEXT_CHECK_PROMPT,
            'extract_characters': EXTRACT_CHARACTERS_PROMPT
        }

    def get_prompt(self, prompt_name):
        return self.prompts.get(prompt_name, None)

    def list_available_prompts(self):
        return list(self.prompts.keys())
