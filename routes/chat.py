from flask import Blueprint, request, jsonify
from services.chat_service import ChatService
from utils.logger import logger

chat_bp = Blueprint('chat', __name__)
chat_service = ChatService()

@chat_bp.route('/chat', methods=['POST'])
def chat():
    """Process chat messages"""
    try:
        if not request.is_json:
            return jsonify({'error': 'Request must be JSON'}), 400
            
        data = request.json
        message = data.get('message')
        
        if not message:
            return jsonify({
                'error': 'Message is required',
                'success': False
            }), 400
        
        # Get session ID from request
        session_id = request.cookies.get('session_id', 'default')
        
        # Get response from chat service
        response = chat_service.get_chat_response(message, session_id)
        
        return jsonify({
            'success': True,
            'response': response['response']
        })
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        return jsonify({
            'error': str(e),
            'success': False
        }), 500

@chat_bp.route('/test_mistral', methods=['GET'])
def test_mistral():
    """Test Mistral API connection"""
    try:
        test_message = "Please respond with 'Mistral connection successful!' if you receive this message."
        response = chat_service.get_chat_response(test_message)
        return jsonify({
            'status': 'success',
            'response': response['response'],
            'message': 'Mistral API test completed successfully'
        })
    except Exception as e:
        logger.error(f"Mistral API test failed: {str(e)}")
        return jsonify({
            'status': 'error',
            'error': str(e),
            'message': 'Mistral API test failed'
        }), 500