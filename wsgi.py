import os
import sys
from flask import Flask

def create_minimal_app():
    print("Starting Flask application creation...", file=sys.stderr)
    app = Flask(__name__)
    
    @app.route('/')
    def home():
        return 'App is running!'
    
    @app.route('/health')
    def health_check():
        print("Health check endpoint called", file=sys.stderr)
        return {'status': 'healthy'}, 200
    
    print("Flask application created successfully", file=sys.stderr)
    return app

print("wsgi.py: Starting application creation...", file=sys.stderr)
application = create_minimal_app()
print("wsgi.py: Application created successfully", file=sys.stderr)

if __name__ == "__main__":
    port = int(os.getenv('PORT', 8000))
    application.run(host='0.0.0.0', port=port)