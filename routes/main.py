from flask import Blueprint, send_from_directory

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    """Route for root URL"""
    return send_from_directory('.', 'index.html')