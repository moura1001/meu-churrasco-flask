"Central configuration"
import os
from dotenv import load_dotenv

load_dotenv()

FLASK_SECRET = os.environ['FLASK_SECRET']
