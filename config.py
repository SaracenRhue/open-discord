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
    env['GITEA_URL'] = os.getenv('GITEA_URL')
    env['GITEA_TOKEN'] = os.getenv('GITEA_TOKEN')
    env['GITEA_USERNAME'] = os.getenv('GITEA_USERNAME')
    env['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
    env['ANTHROPIC_API_KEY'] = os.getenv('ANTHROPIC_API_KEY')

LM_PROVIDER = 'ollana'

TOKEN = env['DISCORD_TOKEN']
ADMIN_ID = env['ADMIN_ID']
OLLAMA_URL = env['OLLAMA_URL']
MODEL = env['MODEL']

SD_URL = env['SD_URL']
SD_PROMPT = ""
SD_RATIO = [1024, 1024]
SD_STEPS = 20
SD_CFG_SCALE = 7.5
SD_BATCH_COUNT = 1
SD_BATCH_SIZE = 1

GITEA_URL = env['GITEA_URL']
GITEA_TOKEN = env['GITEA_TOKEN']
GITEA_USERNAME = env['GITEA_USERNAME']

OPENAI_API_KEY = env['OPENAI_API_KEY']
GPT_MODEL = "gpt-4o-mini"

ANTHROPIC_API_KEY = env['ANTHROPIC_API_KEY']
CLAUDE_MODEL = "claude-3-5-sonnet-20240620"