# Set up the query for generating responses
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from openai import AzureOpenAI

# credential = AzureKeyCredential("MIwNtZsgbVVN7TmhEDhDGPcEvQOONB0ShUMtVgmefMAzSeCKg99U")
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

# This prompt provides instructions to the model
GROUNDED_PROMPT = """
You are a friendly assistant that recommends hotels based on activities and amenities.
Answer the query using only the sources provided below in a friendly and concise bulleted manner.
Answer ONLY with the facts listed in the list of sources below.
If there isn't enough information below, say you don't know.
Do not generate answers that don't use the sources below.
Query: {query}
"""

# Query is the question being asked. It's sent to the search engine and the LLM.
query = "Can you recommend a few hotels near the ocean with beach access and good views"

# Set up the search results and the chat thread.
# Retrieve the selected fields from the search index related to the question.
response = openai_client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": GROUNDED_PROMPT.format(query=query)
        }
    ],
    model="gpt4o-for-scaling"
)
print(response.choices[0].message.content)
