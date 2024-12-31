from datetime import datetime
import json
from utils.logger import logger

class ConversationManager:
    def __init__(self, max_history=20):
        self.max_history = max_history
        self.conversations = {}
        self.current_context = {}

    def create_conversation(self, conversation_id):
        """Initialize a new conversation"""
        self.conversations[conversation_id] = {
            'messages': [],
            'created_at': datetime.now().isoformat(),
            'last_updated': datetime.now().isoformat(),
            'context': {
                'current_character': None,
                'current_transcript': None,
                'focused_topics': set(),
                'mentioned_characters': set()
            }
        }
        return self.conversations[conversation_id]

    def add_message(self, conversation_id, role, content):
        """Add a message to the conversation history"""
        if conversation_id not in self.conversations:
            self.create_conversation(conversation_id)

        conversation = self.conversations[conversation_id]
        message = {
            'role': role,
            'content': content,
            'timestamp': datetime.now().isoformat()
        }

        # Add message and trim history if needed
        conversation['messages'].append(message)
        if len(conversation['messages']) > self.max_history:
            conversation['messages'] = conversation['messages'][-self.max_history:]

        conversation['last_updated'] = datetime.now().isoformat()
        return message

    def get_conversation_messages(self, conversation_id):
        """Get all messages for a conversation"""
        if conversation_id not in self.conversations:
            return []
        return self.conversations[conversation_id]['messages']

    def update_context(self, conversation_id, updates):
        """Update conversation context"""
        if conversation_id not in self.conversations:
            self.create_conversation(conversation_id)

        context = self.conversations[conversation_id]['context']
        for key, value in updates.items():
            if isinstance(value, set):
                if isinstance(context.get(key), set):
                    context[key].update(value)
                else:
                    context[key] = value
            else:
                context[key] = value

    def get_context(self, conversation_id):
        """Get current context for a conversation"""
        if conversation_id not in self.conversations:
            return None
        return self.conversations[conversation_id]['context']

    def get_formatted_messages(self, conversation_id, include_context=True):
        """Get messages formatted for the Mistral API"""
        messages = []
        
        # Add context if available and requested
        if include_context and conversation_id in self.conversations:
            context = self.conversations[conversation_id]['context']
            if context.get('current_character'):
                messages.append({
                    'role': 'system',
                    'content': f"Current character in focus: {context['current_character']}"
                })
            if context.get('current_transcript'):
                messages.append({
                    'role': 'system',
                    'content': f"Working with transcript: {context['current_transcript']}"
                })

        # Add conversation history
        conv_messages = self.get_conversation_messages(conversation_id)
        for msg in conv_messages:
            messages.append({
                'role': msg['role'],
                'content': msg['content']
            })

        return messages

    def cleanup_old_conversations(self, max_age_hours=24):
        """Remove conversations older than max_age_hours"""
        now = datetime.now()
        to_remove = []
        
        for conv_id, conv in self.conversations.items():
            last_updated = datetime.fromisoformat(conv['last_updated'])
            age = (now - last_updated).total_seconds() / 3600
            
            if age > max_age_hours:
                to_remove.append(conv_id)
        
        for conv_id in to_remove:
            del self.conversations[conv_id]

        return len(to_remove)