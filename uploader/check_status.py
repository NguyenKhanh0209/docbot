import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
STORE_NAME = os.environ["FILE_SEARCH_STORE_NAME"]

store = client.file_search_stores.get(name=STORE_NAME)
print(f"Store: {store.name}")
print(f"Display name: {store.display_name}")

docs = list(client.file_search_stores.documents.list(parent=STORE_NAME))
print(f"Total documents indexed: {len(docs)}")

for d in docs[:5]:
    print(f"  - {d.display_name}")
