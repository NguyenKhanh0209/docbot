import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
client.file_search_stores.delete(
    name=os.environ["FILE_SEARCH_STORE_NAME"], config={"force": True}
)
print("Deleted old store.")
