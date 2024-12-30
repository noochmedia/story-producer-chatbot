from app import create_app

# Create the application instance
app = create_app()

# Make the application available to gunicorn
application = app

if __name__ == "__main__":
    app.run()
