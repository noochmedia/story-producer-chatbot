import os

port = os.getenv('PORT', '8000')
bind = f"0.0.0.0:{port}"
workers = 3
timeout = 120
keepalive = 5
worker_class = "sync"
errorlog = "-"  # Log to stdout for Digital Ocean logging
accesslog = "-"  # Log to stdout for Digital Ocean logging
loglevel = "info"