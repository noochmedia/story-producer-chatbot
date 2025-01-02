import os
import requests
from utils.logger import logger
from services.prompt_manager import PromptManager
from services.conversation_manager import ConversationManager
from services.transcript_service import TranscriptService
from prompts.base_system import BASE_SYSTEM_PROMPT

class ChatService:
    def __init__(self):
        self.api_url = os.getenv('MISTRAL_API_URL')
        self.api_key = os.getenv('MISTRAL_API_KEY')
        if not self.api_url:
            raise ValueError("Missing required environment variable: MISTRAL_API_URL")
        
        self.prompt_manager = PromptManager()
        self.conversation_manager = ConversationManager()
        self.transcript_service = TranscriptService()
        self.base_prompt = self._get_system_prompt()

    def _get_system_prompt(self):
        """Get system prompt with full transcript content"""
        try:
            transcript_files = self.transcript_service.get_transcript_list()
            
            if not transcript_files:
                return BASE_SYSTEM_PROMPT.format(
                    available_transcripts="No transcripts currently loaded."
                )
            
            # Format transcript list with basic info and collect full content
            transcript_list = []
            full_content = ""
            
            for transcript_id in transcript_files:
                try:
                    path = os.path.join('transcripts', transcript_id)
                    with open(path, 'r') as f:
                        content = f.read()
                        word_count = len(content.split())
                        transcript_list.append(f"- {transcript_id} ({word_count} words)")
                        full_content += f"\n\n### {transcript_id} ###\n{content}"
                except Exception as e:
                    logger.error(f"Error reading transcript {transcript_id}: {str(e)}")
                    continue
            
            # Format the available transcripts section
            transcripts_info = "\n".join(transcript_list)
            
            if not transcripts_info:
                transcripts_info = "Error: Unable to read transcript contents."
            
            # Create complete system prompt with all content
            system_prompt = BASE_SYSTEM_PROMPT.format(
                available_transcripts=transcripts_info
            )
            
            return system_prompt + "\n\nFULL TRANSCRIPT CONTENTS:\n" + full_content
            
        except Exception as e:
            logger.error(f"Error preparing system prompt: {str(e)}")
            return BASE_SYSTEM_PROMPT.format(
                available_transcripts="Error loading transcript information"
            )

    def get_chat_response(self, prompt, session_id='default'):
        """Get a response from our self-hosted model"""
        try:
            # Get conversation history
            conversation_history = self.conversation_manager.get_formatted_messages(session_id)
            
            # Start with system message containing full transcript content
            messages = [{
                'role': 'system',
                'content': self._get_system_prompt()
            }]
            
            # Add conversation history
            if conversation_history:
                messages.extend(conversation_history)
            
            # Add the new user message
            messages.append({
                'role': 'user',
                'content': prompt
            })
            
            # Log the request details
            request_url = f"{self.api_url}/v1/chat/completions"
            logger.info(f"Making request to: {request_url}")
            
            # Prepare headers and data
            headers = {
                'Content-Type': 'application/json'
            }
            if self.api_key:
                headers['Authorization'] = f'Bearer {self.api_key}'
            
            data = {
                'messages': messages,
                'temperature': 0.7
            }
            
            try:
                # Make API call to our self-hosted model
                response = requests.post(
                    request_url,
                    headers=headers,
                    json=data,
                    verify=False,
                    timeout=60  # Increased timeout for larger content
                )
                
                # Log the response status
                logger.info(f"Response status: {response.status_code}")
                
                if response.status_code == 200:
                    result = response.json()
                    response_content = result['choices'][0]['message']['content']
                    
                    # Store messages in conversation history
                    self.conversation_manager.add_message(session_id, 'user', prompt)
                    self.conversation_manager.add_message(session_id, 'assistant', response_content)
                    
                    return {
                        'response': response_content,
                        'success': True
                    }
                else:
                    error_msg = f"API request failed with status {response.status_code}: {response.text}"
                    raise Exception(error_msg)
                    
            except requests.exceptions.ConnectionError:
                error_msg = f"Failed to connect to model at {self.api_url}. Please verify the server is running."
                logger.error(error_msg)
                raise Exception(error_msg)
            except requests.exceptions.Timeout:
                error_msg = "Request to model timed out. The server might be overloaded."
                logger.error(error_msg)
                raise Exception(error_msg)
            except requests.exceptions.RequestException as e:
                error_msg = f"Error communicating with model: {str(e)}"
                logger.error(error_msg)
                raise Exception(error_msg)
                
        except Exception as e:
            logger.error(f"Error in chat response: {str(e)}")
            raise