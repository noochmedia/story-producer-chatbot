import json
from utils.logger import logger

class ContextAnalyzer:
    def __init__(self, prompt_manager):
        self.prompt_manager = prompt_manager

    def analyze_context(self, current_message, conversation_history, current_context):
        """Analyze the current context and conversation history"""
        try:
            # Get the context check prompt
            context_check_prompt = self.prompt_manager.get_prompt('context_check')
            if not context_check_prompt:
                return None

            # Prepare the context information
            context_info = {
                'current_message': current_message,
                'history': conversation_history[-5:] if conversation_history else [],  # Last 5 messages
                'context': current_context
            }

            # Format the prompt with context information
            formatted_prompt = f"{context_check_prompt}\n\nCONTEXT INFORMATION:\n{json.dumps(context_info, indent=2)}"

            return formatted_prompt

        except Exception as e:
            logger.error(f"Error in context analysis: {str(e)}")
            return None

    def extract_entities(self, text):
        """Extract character names and key topics from text"""
        try:
            # Basic entity extraction (to be enhanced)
            entities = {
                'characters': set(),
                'topics': set(),
                'references': set()
            }

            # Extract potential character names (basic implementation)
            words = text.split()
            for i in range(len(words)):
                word = words[i].strip('.,!?()[]{}""\'')
                # Check for capitalized words that might be names
                if word and word[0].isupper():
                    # Single capitalized word
                    if len(word) > 1:
                        entities['characters'].add(word)
                    # Check for full names (two capitalized words)
                    if i < len(words) - 1 and words[i+1][0].isupper():
                        entities['characters'].add(f"{word} {words[i+1]}")

            # Extract potential topics (basic implementation)
            # Look for repeated meaningful words
            word_count = {}
            for word in text.lower().split():
                word = word.strip('.,!?()[]{}""\'')
                if len(word) > 5:  # Arbitrary length to filter common words
                    word_count[word] = word_count.get(word, 0) + 1

            # Add words that appear multiple times as topics
            for word, count in word_count.items():
                if count > 1:
                    entities['topics'].add(word)

            return entities

        except Exception as e:
            logger.error(f"Error extracting entities: {str(e)}")
            return {
                'characters': set(),
                'topics': set(),
                'references': set()
            }

    def merge_contexts(self, current_context, new_context):
        """Merge current context with new context information"""
        try:
            merged = current_context.copy() if current_context else {}

            if not new_context:
                return merged

            # Merge sets
            for key in ['characters', 'topics', 'references']:
                if key in new_context:
                    if key not in merged:
                        merged[key] = set()
                    if isinstance(new_context[key], (set, list)):
                        merged[key].update(new_context[key])

            # Update simple values
            for key in ['current_transcript', 'last_action', 'current_character']:
                if key in new_context:
                    merged[key] = new_context[key]

            return merged

        except Exception as e:
            logger.error(f"Error merging contexts: {str(e)}")
            return current_context or {}

    def should_switch_context(self, current_context, message_analysis):
        """Determine if context switch is needed based on message analysis"""
        try:
            if not current_context or not message_analysis:
                return False

            # Check for explicit context switches
            if 'switch_context' in message_analysis:
                return True

            # Check for new character focus
            current_character = current_context.get('current_character')
            new_characters = message_analysis.get('characters', set())
            if new_characters and current_character not in new_characters:
                return True

            # Check for topic shift
            current_topics = set(current_context.get('topics', []))
            new_topics = set(message_analysis.get('topics', []))
            topic_overlap = current_topics & new_topics
            if not topic_overlap and new_topics:
                return True

            return False

        except Exception as e:
            logger.error(f"Error checking context switch: {str(e)}")
            return False