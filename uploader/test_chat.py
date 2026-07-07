import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
STORE_NAME = os.environ["FILE_SEARCH_STORE_NAME"]

SYSTEM_PROMPT = """You are OptiBot, the customer-support bot for OptiSigns.com.
- Tone: helpful, factual, concise.
- Only answer using the uploaded docs.
- Max 5 bullet points; else link to the doc.
- Cite up to 3 "Article URL:" lines per reply."""


def ask(question):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=question,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            tools=[
                types.Tool(
                    file_search=types.FileSearch(file_search_store_names=[STORE_NAME])
                )
            ],
        ),
    )
    print("ANSWER")
    print(response.text)

    if response.candidates and response.candidates[0].grounding_metadata:
        print("\nSOURCES")
        chunks = response.candidates[0].grounding_metadata.grounding_chunks or []
        for c in chunks:
            if hasattr(c, "retrieved_context") and c.retrieved_context:
                print(f"- {c.retrieved_context.title}")


if __name__ == "__main__":
    ask("How do I add a YouTube video?")
