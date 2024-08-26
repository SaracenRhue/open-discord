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
    env['SD_URL'] = os.getenv('SD_URL')
    env['SD_MODEL'] = os.getenv('SD_MODEL')

TOKEN = env['DISCORD_TOKEN']
ADMIN_ID = env['ADMIN_ID']
OLLAMA_URL = env['OLLAMA_URL']
MODEL = env['MODEL']

SD_URL = env['SD_URL']
SD_MODEL = env['SD_MODEL']
SD_RATIO = [1024, 1024]
SD_STEPS = 20
SD_CFG_SCALE = 7.5
SD_BATCH_COUNT = 2
SD_BATCH_SIZE = 1