from fastapi import FastAPI
from azure.identity import DefaultAzureCredential
from azure.identity import get_bearer_token_provider
from azure.search.documents import SearchClient
from openai import AzureOpenAI
import os

# storage = os.environ.get("STORAGE_ACCOUNT_NAME")

credential = DefaultAzureCredential()
token_provider = get_bearer_token_provider(credential, "https://cognitiveservices.azure.com/.default")
openai_client = AzureOpenAI(
    api_version="2024-02-15-preview",
    azure_endpoint="https://open-ai-for-scaling.openai.azure.com/",
    api_key="82446626c4644fda89a49f04d8c71f7d"
)

# search_client = SearchClient(
#     endpoint="https://ai-search-4-scaling.search.windows.net",
#     index_name="movie-indexer",
#     credential=credential
# )

app = FastAPI()

GROUNDED_PROMPT = """
You are a friendly assistant that recommends hotels based on activities and amenities.
Answer the query using only the sources provided below in a friendly and concise bulleted manner.
Answer ONLY with the facts listed in the list of sources below.
If there isn't enough information below, say you don't know.
Do not generate answers that don't use the sources below.
Query: {query}
"""


@app.post('/rag')
async def rag(query):
    response = openai_client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": GROUNDED_PROMPT.format(query=query)
            }
        ],
        model="gpt4o-for-scaling"
    )
    return {"answer": response.choices[0].message.content}
