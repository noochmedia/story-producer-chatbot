from flask import Blueprint, jsonify
from services.character_service import CharacterService
from services.transcript_service import TranscriptService
from utils.logger import logger

character_bp = Blueprint('character', __name__)

@character_bp.route('/characters', methods=['GET'])
def get_characters():
    """Get all characters"""
    try:
        character_service = CharacterService()
        characters = character_service.get_all_characters()
        return jsonify({
            'characters': characters,
            'success': True
        })
    except Exception as e:
        logger.error(f"Error getting characters: {str(e)}")
        return jsonify({
            'error': str(e),
            'success': False
        }), 400

@character_bp.route('/refresh_characters', methods=['POST'])
def refresh_characters():
    try:
        character_service = CharacterService()
        characters = character_service.get_all_characters(refresh=True)
        return jsonify({
            'characters': characters,
            'success': True
        })
    except Exception as e:
        logger.error(f"Error refreshing characters: {str(e)}")
        return jsonify({
            'error': str(e),
            'success': False
        }), 400

@character_bp.route('/character_brief/<character_name>', methods=['GET'])
def get_character_brief(character_name):
    try:
        character_service = CharacterService()
        transcript_service = TranscriptService()
        
        # Get all transcripts
        transcripts = transcript_service.get_all_transcripts()
        if not transcripts:
            return jsonify({
                'error': 'No transcripts available',
                'success': False
            }), 400
            
        # Generate character brief
        brief = character_service.generate_character_brief(character_name, transcripts)
        
        return jsonify({
            'brief': brief,
            'success': True
        })
    except Exception as e:
        logger.error(f"Error generating character brief: {str(e)}")
        return jsonify({
            'error': str(e),
            'success': False
        }), 400

@character_bp.route('/delete_source/<source_id>', methods=['DELETE'])
def delete_source(source_id):
    try:
        transcript_service = TranscriptService()
        character_service = CharacterService()
        
        # Delete the source and get updated lists
        transcript_service.delete_transcript(source_id)
        remaining_sources = transcript_service.get_transcript_list()
        remaining_characters = character_service.get_all_characters()
        
        return jsonify({
            'message': f'Successfully deleted {source_id}',
            'sources': remaining_sources,
            'characters': remaining_characters,
            'success': True
        })
    except Exception as e:
        logger.error(f"Error deleting source: {str(e)}")
        return jsonify({
            'error': str(e),
            'success': False
        }), 400