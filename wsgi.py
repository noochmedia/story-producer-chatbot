import sys
import os
print("Python version:", sys.version)
print("Current working directory:", os.getcwd())
print("PYTHONPATH:", os.environ.get('PYTHONPATH', 'Not set'))

from app import create_app

print("Successfully imported create_app")

# Create the application instance
try:
    app = create_app()
    print("Successfully created Flask application")
except Exception as e:
    print(f"Error creating application: {str(e)}")
    raise

# Make the application available to gunicorn
application = app
print("Application assigned to 'application' variable")

if __name__ == "__main__":
    app.run()
