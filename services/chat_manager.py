import os
from utils.logger import logger
from services.mistral_service import MistralService
from prompts.prompt_manager import PromptManager

class ChatManager:
    def __init__(self):
        self.mistral_service = MistralService()
        self.prompt_manager = PromptManager()
        self.chat_history = []  # Store conversation history
        self.current_context = {}  # Store current session context
        
    def process_message(self, message, transcripts=None, action=None):
        """Process incoming chat messages with context and history"""
        try:
            # Initialize response structure
            response_data = {
                'response': '',
                'has_context': bool(transcripts),
                'success': True
            }
            
            # Handle specific actions (button clicks)
            if action:
                return self._handle_action(action, transcripts)
            
            # Check if it's a basic greeting
            if self._is_basic_greeting(message):
                response = self._handle_greeting()
                response_data['response'] = response
                return response_data
            
            # Get initial routing prompt
            routing_prompt = self.prompt_manager.get_prompt('initial_routing')
            if not routing_prompt:
                raise ValueError("Failed to load initial routing prompt")
                
            # Build context including transcripts and history
            context = self._build_context(transcripts)
            
            # Create the full prompt
            full_prompt = f"{routing_prompt}\n\nCurrent Context:\n{context}\n\nUser Message: {message}"
            
            # Get response from Mistral
            response = self.mistral_service.get_chat_response(
                message=full_prompt,
                context=self.chat_history[-5:] if self.chat_history else None  # Last 5 messages for history
            )
            
            # Update chat history
            self.chat_history.append({
                'role': 'user',
                'content': message
            })
            self.chat_history.append({
                'role': 'assistant',
                'content': response
            })
            
            response_data['response'] = response
            return response_data
            
        except Exception as e:
            logger.error(f"Error processing chat message: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'has_context': bool(transcripts)
            }
    
    def _handle_action(self, action, transcripts):
        """Handle specific button-triggered actions"""
        try:
            # Get appropriate prompt based on action
            action_prompts = {
                'story_summary': 'story_summary',
                'character_brief': 'character_brief',
                'find_soundbites': 'find_soundbites',
                'create_soundbites': 'create_soundbites'
            }
            
            prompt_name = action_prompts.get(action)
            if not prompt_name:
                raise ValueError(f"Unknown action: {action}")
                
            prompt = self.prompt_manager.get_prompt(prompt_name)
            if not prompt:
                raise ValueError(f"Failed to load prompt for action: {action}")
                
            # Build context with transcripts
            context = self._build_context(transcripts)
            
            # Get response using specific prompt
            response = self.mistral_service.get_chat_response(
                message=f"{prompt}\n\nContext:\n{context}",
                context=self.chat_history[-5:] if self.chat_history else None
            )
            
            return {
                'response': response,
                'has_context': bool(transcripts),
                'success': True,
                'action': action
            }
            
        except Exception as e:
            logger.error(f"Error handling action {action}: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'has_context': bool(transcripts)
            }
    
    def _is_basic_greeting(self, message):
        """Check if the message is a basic greeting"""
        basic_greetings = {'hello', 'hi', 'hey', 'greetings', 
                          'good morning', 'good afternoon', 'good evening'}
        return message.lower().strip() in basic_greetings
    
    def _handle_greeting(self):
        """Handle basic greetings"""
        return ("Hello! I'm your story analysis assistant. I can help you with:\n"
                "1. Creating character profiles\n"
                "2. Generating story summaries\n"
                "3. Finding relevant quotes\n"
                "4. Creating soundbite sequences\n\n"
                "How can I help you today?")
    
    def _build_context(self, transcripts):
        """Build context string from available transcripts"""
        if not transcripts:
            return "No transcripts available for analysis."
            
        context_parts = []
        for transcript_id, content in transcripts.items():
            # Include a summary/preview of each transcript
            preview = content[:500] + "..." if len(content) > 500 else content
            context_parts.append(f"Transcript {transcript_id}:\n{preview}\n")
            
        return "\n".join(context_parts)
    
    def clear_history(self):
        """Clear chat history"""
        self.chat_history = []
        self.current_context = {}