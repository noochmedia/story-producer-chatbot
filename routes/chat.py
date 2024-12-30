from flask import Blueprint, request, jsonify
from services.mistral_service import MistralService
from utils.logger import logger
from routes.transcript import transcripts, storage  # Import transcripts and storage

chat_bp = Blueprint('chat', __name__)
mistral_service = MistralService()

@chat_bp.route('/test_mistral', methods=['GET'])
def test_mistral():
    """Test Mistral API connection"""
    try:
        test_message = "Please respond with 'Mistral connection successful!' if you receive this message."
        response = mistral_service.get_chat_response(test_message)
        return jsonify({
            'status': 'success',
            'response': response,
            'message': 'Mistral API test completed successfully'
        })
    except Exception as e:
        logger.error(f"Mistral API test failed: {str(e)}")
        return jsonify({
            'status': 'error',
            'error': str(e),
            'message': 'Mistral API test failed'
        }), 500

@chat_bp.route('/chat', methods=['POST'])
def chat():
    """Process chat messages with Mistral"""
    try:
        if not request.is_json:
            return jsonify({'error': 'Request must be JSON'}), 400
            
        data = request.json
        message = data.get('message')
        action = data.get('action')  # For button-triggered actions
        
        # If action is specified, modify message to trigger appropriate prompt
        if action:
            action_messages = {
                'story_summary': "Please provide a story summary.",
                'character_brief': "Who are the people or characters in this story?",
                'find_soundbites': "Please find potential soundbites from the transcripts.",
                'create_soundbites': "Please create soundbite sequences from the transcripts."
            }
            message = action_messages.get(action, message)
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400

        # Check if this is a basic greeting or system question
        basic_greetings = ['hello', 'hi', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening']
        is_basic_greeting = message.lower().strip() in basic_greetings

        if is_basic_greeting:
            # Handle basic greeting without loading transcripts
            greeting_context = """You are a friendly and professional story analysis assistant. 
            Respond warmly to the greeting and let the user know you're ready to help analyze their story content."""
            response = mistral_service.get_chat_response(message, greeting_context)
            return jsonify({
                'response': response,
                'has_context': False
            })

        # For all other queries, load and use full transcript context
        current_transcripts = storage.get_all_transcripts()
        
        # Get base context
        context = mistral_service.get_story_context(current_transcripts)
        
        # Add transcript content when available
        if current_transcripts:
            # Create a condensed version of transcripts
            transcript_text = "\n\nTranscript contents:\n"
            for transcript_id, content in current_transcripts.items():
                transcript_text += f"\n--- Begin Transcript: {transcript_id} ---\n"
                # Include first 1000 characters of each transcript for context
                transcript_text += content[:1000] + "...\n"
                transcript_text += f"--- End Transcript: {transcript_id} ---\n"
            
            context += transcript_text
            logger.debug(f"Added {len(current_transcripts)} transcript summaries to context. Total context length: {len(context)}")
        else:
            # No transcripts available
            context += "\n\nNote: No transcripts have been uploaded yet. Please upload transcripts for analysis."
        
        response = mistral_service.get_chat_response(
            message=message,
            context=context
        )
        
        return jsonify({
            'response': response,
            'has_context': len(transcripts) > 0
        })
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        return jsonify({'error': str(e)}), 500