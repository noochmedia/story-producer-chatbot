import os

# Server socket
port = os.getenv('PORT', '8000')
bind = f"0.0.0.0:{port}"

# Worker processes
workers = 1  # Reducing to 1 worker for debugging
worker_class = 'sync'
timeout = 30  # Reduced timeout
keepalive = 2

# Logging
accesslog = '-'
errorlog = '-'
loglevel = 'debug'  # Increased log level for debugging
capture_output = True
enable_stdio_inheritance = True

# Startup logging
spew = False
check_config = True

# Reload
reload = False

# Development
reload_engine = 'auto'
reload_extra_files = []

def on_starting(server):
    print("Gunicorn is starting up...")

def on_reload(server):
    print("Gunicorn is reloading...")

def when_ready(server):
    print(f"Gunicorn is ready. Listening on port {port}")

def on_exit(server):
    print("Gunicorn is shutting down...")