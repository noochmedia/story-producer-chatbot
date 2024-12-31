import os
from utils.logger import logger

class PromptManager:
    def __init__(self):
        self.prompts_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'prompts')
        self.prompts = {}
        self._load_prompts()

    def _load_prompts(self):
        """Load all prompts from the prompts directory"""
        try:
            prompt_files = {
                'character_brief': 'character_brief.py',
                'story_summary': 'story_summary.py',
                'find_soundbites': 'find_soundbites.py',
                'create_soundbites': 'create_soundbites.py',
                'initial_routing': 'initial_routing.py',
                'context_check': 'context_check.py',
                'quick_reference': 'quick_reference.py'
            }

            for prompt_name, filename in prompt_files.items():
                filepath = os.path.join(self.prompts_dir, filename)
                if os.path.exists(filepath):
                    with open(filepath, 'r') as f:
                        content = f.read()
                        # Get the variable name from the filename
                        var_name = filename.replace('.py', '').upper() + '_PROMPT'
                        # Extract content between triple quotes
                        parts = content.split('"""')
                        if len(parts) >= 3:  # Make sure we have opening and closing quotes
                            prompt_content = parts[1].strip()
                            self.prompts[prompt_name] = prompt_content
                        else:
                            logger.warning(f"Invalid prompt format in {filename}")
                else:
                    logger.warning(f"Prompt file not found: {filepath}")

        except Exception as e:
            logger.error(f"Error loading prompts: {str(e)}")
            raise

    def get_prompt(self, prompt_name):
        """Get a specific prompt by name"""
        return self.prompts.get(prompt_name)

    def list_prompts(self):
        """List all available prompts"""
        return list(self.prompts.keys())