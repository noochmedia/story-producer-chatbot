from flask import Flask

# Create the Flask application
app = Flask(__name__)

# Basic routes
@app.route('/')
def home():
    return 'App is running!'

@app.route('/health')
def health():
    return {'status': 'healthy'}, 200

# Get the application object
application = app

if __name__ == "__main__":
    # For local development
    app.run(host='0.0.0.0', port=8000)
