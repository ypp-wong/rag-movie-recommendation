from openai import AzureOpenAI
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from utils.setting import settings
from azure.search.documents.models import SearchMode, VectorizedQuery
from utils.config import SearchConfig


class RAGService:
    def __init__(self):
        self.search_client = SearchClient(
            endpoint=settings.AZURE_SEARCH_ENDPOINT,
            index_name=settings.AZURE_SEARCH_INDEX_NAME,
            credential=AzureKeyCredential(settings.AZURE_SEARCH_API_KEY)
        )
        self.openai_client = AzureOpenAI(
            api_version=settings.OPENAI_API_VERSION,
            azure_endpoint=settings.OPENAI_ENDPOINT,
            api_key=settings.OPENAI_API_KEY
        )

    def get_embeddings(self, query: str):
        response = self.openai_client.embeddings.create(
            model=settings.OPENAI_EMBEDDING_MODEL,
            input=query
        )
        return response.data[0].embedding

    def search_documents(self, query: str):
        search_options = {
            "top": SearchConfig.TOP.value,
            "search_mode": SearchMode.ANY,
            "query_type": SearchConfig.QUERY_TYPE.value,
            "select": SearchConfig.SELECT_FIELDS.value,
            "vector_queries": [
                VectorizedQuery(
                    vector=self.get_embeddings(query=query),
                    kind=SearchConfig.VECTOR_KIND.value,
                    k_nearest_neighbors=SearchConfig.K_NEAREST_NEIGHBORS.value,
                    fields=SearchConfig.VECTOR_FIELD.value
                )
            ]
        }
        results = self.search_client.search(**search_options)
        retrieved_documents = []
        for result in results:
            retrieved_documents.append(result)
        return retrieved_documents

    def generate_response(self, prompt: str):
        response = self.openai_client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }

            ],
            model=settings.OPENAI_LLM_MODEL
        )
        return response.choices[0].message.content

    def orchestrate_rag(self, user_query: str, grounded_prompt: str):
        relevant_data = self.search_documents(query=user_query)
        ragged_query = grounded_prompt.format(query=user_query, data=relevant_data)
        response = self.generate_response(ragged_query)
        return {"response": response}
