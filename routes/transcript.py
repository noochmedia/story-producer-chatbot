import os
import re
from flask import Blueprint, request, jsonify
from services import FileProcessor
from utils.logger import logger

# Create blueprint
transcript_bp = Blueprint('transcript', __name__)

# Initialize storage and character set
from services.storage import TranscriptStorage
storage = TranscriptStorage()
transcripts = storage.get_all_transcripts()  # Load existing transcripts
characters = set()

def extract_name_from_filename(filename):
    """Extracts proper names from a file name"""
    base_name = re.sub(r'\.[a-zA-Z0-9]+$', '', filename)  # Remove file extension
    words = base_name.split(' ')  # Split by space
    if len(words) >= 2:
        return f"{words[0].capitalize()} {words[1].capitalize()}"
    return None

@transcript_bp.route('/upload_transcript', methods=['POST', 'OPTIONS'])
def upload_transcript():
    """Upload a transcript and extract character names"""
    try:
        logger.info("=== Upload Transcript Request Started ===")
        logger.info(f"Request Method: {request.method}")
        logger.info(f"Request Headers: {dict(request.headers)}")
        logger.info(f"Request URL: {request.url}")
        logger.info(f"Request Remote Addr: {request.remote_addr}")
        
        # Handle OPTIONS request for CORS
        if request.method == 'OPTIONS':
            logger.info("Handling OPTIONS request")
            response = jsonify({'status': 'ok'})
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
            return response, 200
            
        if not request.is_json:
            logger.error("Request is not JSON")
            logger.error(f"Content-Type: {request.content_type}")
            logger.error(f"Raw Data: {request.get_data(as_text=True)[:1000]}")  # Log first 1000 chars
            return jsonify({'error': 'Request must be JSON'}), 400

        data = request.json
        transcript_id = data.get('id')
        content = data.get('content', '')
        file_type = data.get('fileType', 'txt').lower()

        if not transcript_id or not content:
            return jsonify({'error': 'Missing transcript ID or content'}), 400

        # Process transcript content
        processed_content = FileProcessor.process_file_content(content, file_type)
        # Save to file system and update in-memory cache
        storage.save_transcript(transcript_id, processed_content)
        transcripts[transcript_id] = processed_content

        # Extract name from file name
        character_name = extract_name_from_filename(transcript_id)

        # Add the name if valid
        if character_name and " " in character_name:  # Ensure at least "First Last"
            characters.add(character_name)
        else:
            logger.warning(f"Invalid or incomplete name from file: {transcript_id}")

        return jsonify({
            'message': f'Transcript {transcript_id} uploaded successfully',
            'current_transcripts': list(transcripts.keys()),
            'characters': sorted(list(characters)),
            'char_preview': processed_content[:500],
            'char_count': len(processed_content)
        })

    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        logger.error(f"Error processing transcript: {str(e)}")
        logger.error(f"Traceback: {error_details}")
        return jsonify({
            'error': str(e),
            'details': error_details if os.getenv('FLASK_ENV') != 'production' else 'Check server logs for details'
        }), 500

@transcript_bp.route('/characters', methods=['GET'])
def get_characters():
    """Retrieve the current list of characters"""
    try:
        return jsonify({
            'message': 'Characters retrieved successfully',
            'characters': sorted(list(characters))
        })
    except Exception as e:
        logger.error(f"Error retrieving characters: {str(e)}")
        return jsonify({'error': str(e)}), 500

@transcript_bp.route('/characters', methods=['POST'])
def add_character():
    """Add a new character"""
    try:
        if not request.is_json:
            return jsonify({'error': 'Request must be JSON'}), 400

        data = request.json
        new_character = data.get('name', '').strip()

        if " " not in new_character:  # Require first and last name
            return jsonify({'error': 'Character must include both first and last name'}), 400

        characters.add(new_character)
        return jsonify({
            'message': f'Character {new_character} added successfully',
            'characters': sorted(list(characters))
        })
    except Exception as e:
        logger.error(f"Error adding character: {str(e)}")
        return jsonify({'error': str(e)}), 500

@transcript_bp.route('/characters/<character_name>', methods=['DELETE'])
def delete_character(character_name):
    """Delete a character"""
    try:
        # Keep names case-insensitive while preserving original format
        name = character_name.strip()
        matching_characters = [char for char in characters if char.lower() == name.lower()]
        if matching_characters:
            characters.remove(matching_characters[0])
            logger.debug(f"Deleted character: {name}")
            return jsonify({
                'message': f'Character {name} deleted successfully',
                'characters': sorted(list(characters))
            })
        else:
            return jsonify({'error': 'Character not found'}), 404
    except Exception as e:
        logger.error(f"Error deleting character: {str(e)}")
        return jsonify({'error': str(e)}), 500

@transcript_bp.route('/list_transcripts', methods=['GET'])
def list_transcripts():
    """List all available transcripts"""
    try:
        return jsonify({
            'transcripts': list(transcripts.keys()),
            'count': len(transcripts)
        })
    except Exception as e:
        logger.error(f"Error listing transcripts: {str(e)}")
        return jsonify({'error': str(e)}), 500

@transcript_bp.route('/transcript/<transcript_id>', methods=['GET'])
def get_transcript(transcript_id):
    """Retrieve a transcript by its ID"""
    try:
        transcript_id = transcript_id.strip()
        if transcript_id in transcripts:
            logger.debug(f"Retrieved transcript: {transcript_id}")
            return jsonify({
                'transcript_id': transcript_id,
                'content': transcripts[transcript_id]
            })
        else:
            logger.error(f"Transcript {transcript_id} not found")
            return jsonify({'error': 'Transcript not found'}), 404
    except Exception as e:
        logger.error(f"Error retrieving transcript: {str(e)}")
        return jsonify({'error': str(e)}), 500
