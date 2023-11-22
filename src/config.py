"Central configuration"
import os
from dotenv import load_dotenv

load_dotenv()

FLASK_SECRET = os.environ['FLASK_SECRET']
CEP_ORIGEM = os.getenv('CEP_ORIGEM', "06194010")
