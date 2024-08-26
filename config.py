import os

# Load environment variables from .env file if it exists
env = {}
if os.path.exists('.env'):
    with open('.env', 'r') as f:
        for line in f:
            key, value = line.strip().split('=')
            env[key] = value
else:
    env['DISCORD_TOKEN'] = os.getenv('DISCORD_TOKEN')
    env['ADMIN_ID'] = os.getenv('ADMIN_ID')
    env['OLLAMA_URL'] = os.getenv('OLLAMA_URL')
    env['MODEL'] = os.getenv('MODEL')

TOKEN = env['DISCORD_TOKEN']
ADMIN_ID = env['ADMIN_ID']
OLLAMA_URL = env['OLLAMA_URL']
MODEL = env['MODEL']