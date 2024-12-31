import os
import requests
from utils.logger import logger
from services.prompt_manager import PromptManager
from services.conversation_manager import ConversationManager
from prompts.base_system import BASE_SYSTEM_PROMPT

class ChatService:
    def __init__(self):
        self.api_url = os.getenv('MISTRAL_API_URL')
        self.api_key = os.getenv('MISTRAL_API_KEY')
        if not self.api_url or not self.api_key:
            raise ValueError("Missing required environment variables: MISTRAL_API_URL and MISTRAL_API_KEY")
        
        self.prompt_manager = PromptManager()
        self.conversation_manager = ConversationManager()
        self.base_prompt = BASE_SYSTEM_PROMPT

    def get_chat_response(self, prompt, session_id='default'):
        """Get a response from the chat API using conversation history"""
        try:
            # Start with the base system prompt
            messages = [{
                'role': 'system',
                'content': self.base_prompt
            }]
            
            # Get formatted conversation history including context
            conversation_history = self.conversation_manager.get_formatted_messages(session_id)
            if conversation_history:
                messages.extend(conversation_history)
            
            # Add the new user message
            messages.append({
                'role': 'user',
                'content': prompt
            })
            
            # Make API call
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.api_key}'
            }
            
            data = {
                'model': 'mistral-medium',
                'messages': messages,
                'temperature': 0.7,
                'max_tokens': 2000
            }
            
            response = requests.post(
                f"{self.api_url}/v1/chat/completions",
                headers=headers,
                json=data
            )
            
            if response.status_code == 200:
                result = response.json()
                response_content = result['choices'][0]['message']['content']
                
                # Store messages in conversation history
                self.conversation_manager.add_message(session_id, 'user', prompt)
                self.conversation_manager.add_message(session_id, 'assistant', response_content)
                
                # Clean up old conversations periodically
                self.conversation_manager.cleanup_old_conversations()
                
                return {
                    'response': response_content,
                    'success': True
                }
            else:
                error_msg = f"API request failed with status {response.status_code}: {response.text}"
                logger.error(error_msg)
                raise Exception(error_msg)

        except Exception as e:
            logger.error(f"Error getting chat response: {str(e)}")
            raise

    def _determine_prompt_type(self, user_prompt):
        """Determine which type of prompt to use based on user input"""
        try:
            # Use the routing prompt to determine type
            routing_prompt = self.prompt_manager.get_prompt('initial_routing')
            if not routing_prompt:
                return 'quick_reference'  # Default if routing prompt not found

            # Prepare routing request
            messages = [
                {
                    'role': 'system',
                    'content': routing_prompt
                },
                {
                    'role': 'user',
                    'content': user_prompt
                }
            ]

            # Make API call for routing
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.api_key}'
            }
            
            data = {
                'model': 'mistral-medium',
                'messages': messages,
                'temperature': 0.3,  # Lower temperature for more consistent routing
                'max_tokens': 50     # Short response needed
            }
            
            response = requests.post(
                f"{self.api_url}/v1/chat/completions",
                headers=headers,
                json=data
            )

            if response.status_code == 200:
                result = response.json()
                prompt_type = result['choices'][0]['message']['content'].strip().lower()
                
                # Validate prompt type exists
                if self.prompt_manager.get_prompt(prompt_type):
                    return prompt_type
                
            return 'quick_reference'  # Default fallback

        except Exception as e:
            logger.error(f"Error in prompt routing: {str(e)}")
            return 'quick_reference'  # Default fallback