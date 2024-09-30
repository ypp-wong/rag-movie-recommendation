from fastapi import FastAPI
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import SearchMode, VectorizedQuery
from openai import AzureOpenAI
from pydantic import BaseModel
import os

# storage = os.environ.get("STORAGE_ACCOUNT_NAME")

credential = AzureKeyCredential("MIwNtZsgbVVN7TmhEDhDGPcEvQOONB0ShUMtVgmefMAzSeCKg99U")

openai_client = AzureOpenAI(
    api_version="2024-02-15-preview",
    azure_endpoint="https://open-ai-for-scaling.openai.azure.com/",
    api_key="82446626c4644fda89a49f04d8c71f7d"
)

search_client = SearchClient(
    endpoint="https://ai-search-4-scaling.search.windows.net",
    index_name="movie-indexer",
    credential=credential
)


def generate_embedding(text):
    response = openai_client.embeddings.create(
        input=text,
        model="ada002-for-scaling"
    )
    return response.data[0].embedding

class QueryRequest(BaseModel):
    query: str


app = FastAPI()

GROUNDED_PROMPT = """
You are an assisstent that provides personalized movie recommendations and generates detailed synopses based on user preferences and query inputs.
You will be using the data here:
{data}

This is a json format, just make sure to go through each json array and extract information.

The output format should be as follow:

I would recommend the movie named 'title_1', this movie is from 'country_1'. This movie is about 'fullplot_1'.
Furthermore, I would also recommend the movie named 'title_2' which is from 'country_2' and it is about 'fullplot_2'.


Here are the instructions:

1. If there's more than one recommendation, please use the above format to give the second, third recommendation etc. 
2. Please use all the data available and don't miss anything. As mentioned, the data is of json format, make sure to go through each json array and extract information.
3. You must give 3 recommendations if the data contains 3 json arrays and etc.
4. Don't just copy from the data, but also try to elaborate and paraphrase a little.
Query: {query}
"""


@app.get('/')
def read_root():
    return {"message": "Hello, welcome to your personal movie recommendation assistant!"}


@app.post('/rag')
async def rag(request: QueryRequest):
    search_options = {
        "top": 3,
        "search_mode": SearchMode.ANY,
        "query_type": "full",
        "select": ["title", "fullplot", "countries"],
        "vector_queries": [
            VectorizedQuery(vector=generate_embedding(text=request.query), kind="vector", k_nearest_neighbors=3,
                            fields="vector")]
    }
    results = search_client.search(**search_options)
    retrieved_documents = []
    for result in results:
        retrieved_documents.append(result)
    response = openai_client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": GROUNDED_PROMPT.format(query=request.query, data=retrieved_documents)
            }
        ],
        model="gpt4o-for-scaling"
    )
    return {"answer": response.choices[0].message.content}
