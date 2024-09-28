from fastapi import FastAPI
from azure.identity import DefaultAzureCredential
from azure.identity import get_bearer_token_provider
from azure.search.documents import SearchClient
from openai import AzureOpenAI
from pydantic import BaseModel
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

class QueryRequest(BaseModel):
    query: str


app = FastAPI()

GROUNDED_PROMPT = """
You are a friendly assistant that can tell jokes, please generate some jokes based on the input. Please be as funny
as possible.
Query: {query}
"""


@app.get('/')
def read_root():
    return {"message": "Hello, welcome to your personal joke generation assistant!"}


@app.post('/rag')
async def rag(request: QueryRequest):
    response = openai_client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": GROUNDED_PROMPT.format(query=request.query)
            }
        ],
        model="gpt4o-for-scaling"
    )
    return {"answer": response.choices[0].message.content}
