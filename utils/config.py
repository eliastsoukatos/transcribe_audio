import os
from dotenv import load_dotenv

def load_config():
    load_dotenv()
    return {
        'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY')
    }