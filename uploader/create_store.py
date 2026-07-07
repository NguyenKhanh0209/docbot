import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

store = client.file_search_stores.create(config={"display_name": "optibot-kb"})
print(f"FILE_SEARCH_STORE_NAME={store.name}")
