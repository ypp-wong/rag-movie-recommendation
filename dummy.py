# Set up the query for generating responses
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import SearchMode, VectorizedQuery
from openai import AzureOpenAI

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

# Define the query parameters (for example, retrieve all documents)
query = "I want to search for some Hong Kong movies"


def generate_embedding(text):
    response = openai_client.embeddings.create(
        input=query,
        model="ada002-for-scaling"
    )
    return response.data[0].embedding


search_options = {
    "top": 3,  # Retrieve top 10 results (Top K)
    "search_mode": SearchMode.ANY,  # Use 'ALL' to match all search terms, or 'ANY' to match any search term
    "query_type": "full",  # Use 'simple' or 'full' depending on your need for structured queries
    "vector_queries": [
        VectorizedQuery(vector=generate_embedding(query), kind="vector", k_nearest_neighbors=3,
                        fields="vector")]
}

# Search the index
results = search_client.search(search_text=query, **search_options)

# Iterate through the results and display the data
for result in results:
    print(f"Document: {result}")
