from openai import OpenAI
import os

from utils.key import API_KEY

MODEL = os.environ.get('MODEL')

client = OpenAI(
  api_key=API_KEY
)

# hier unsere client konfiguration einbauen mit allen wichtigen konfigurationen