import os

# Server socket
bind = "0.0.0.0:8000"  # Hard-coded for testing

# Worker processes
workers = 1
worker_class = 'sync'
timeout = 120
keepalive = 2

# Logging
accesslog = None
errorlog = None
loglevel = 'debug'
capture_output = True
enable_stdio_inheritance = True

# Startup logging
spew = False
check_config = True

# Reload
reload = False

def on_starting(server):
    print("Gunicorn is starting up...")

def when_ready(server):
    print("Gunicorn is ready. Listening on port 8000")

def on_exit(server):
    print("Gunicorn is shutting down...")
