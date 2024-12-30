import os
import multiprocessing

# Server socket
port = os.getenv('PORT', '8000')
bind = f"0.0.0.0:{port}"

# Worker processes
workers = 1  # For the basic-xxs instance
worker_class = 'sync'
timeout = 120
keepalive = 2

# Logging
accesslog = '-'  # Log to stdout
errorlog = '-'   # Log to stderr
loglevel = 'info'
capture_output = True
enable_stdio_inheritance = True

# Process naming
proc_name = 'story-producer-chatbot'

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# SSL
keyfile = None
certfile = None

def on_starting(server):
    print(f"Starting Gunicorn on port {port}")

def when_ready(server):
    print("Gunicorn is ready for connections")

def on_exit(server):
    print("Shutting down Gunicorn")
