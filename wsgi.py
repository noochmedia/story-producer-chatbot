import os
from flask import Flask

def create_minimal_app():
    app = Flask(__name__)
    
    @app.route('/health')
    def health_check():
        return {'status': 'healthy'}, 200
    
    return app

# Create the application instance
application = create_minimal_app()

if __name__ == "__main__":
    port = int(os.getenv('PORT', 8000))
    application.run(host='0.0.0.0', port=port)