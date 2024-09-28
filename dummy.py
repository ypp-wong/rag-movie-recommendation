# Set up the query for generating responses
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import SearchMode, VectorizedQuery
from openai import AzureOpenAI

credential = AzureKeyCredential("MIwNtZsgbVVN7TmhEDhDGPcEvQOONB0ShUMtVgmefMAzSeCKg99U")
# openai_client = AzureOpenAI(
#     api_version="2024-02-15-preview",
#     azure_endpoint="https://open-ai-for-scaling.openai.azure.com/",
#     api_key="82446626c4644fda89a49f04d8c71f7d"
# )

search_client = SearchClient(
    endpoint="https://ai-search-4-scaling.search.windows.net",
    index_name="movie-indexer",
    credential=credential
)

# Define the query parameters (for example, retrieve all documents)
query = "I want to search for some Hong Kong movies"

search_options = {
    "top": 3,  # Retrieve top 10 results (Top K)
    "search_mode": SearchMode.ANY,  # Use 'ALL' to match all search terms, or 'ANY' to match any search term
    "query_type": "full",  # Use 'simple' or 'full' depending on your need for structured queries
    "vector_queries": VectorizedQuery()
}


# Search the index
results = search_client.search(search_text=query, **search_options)

# Iterate through the results and display the data
for result in results:
    print(f"Document: {result}")
