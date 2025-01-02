import subprocess

try:
    subprocess.run(['ping', 'api.deepseek.ai'], timeout=5)
except subprocess.TimeoutExpired:
    print("Could not reach the domain")
