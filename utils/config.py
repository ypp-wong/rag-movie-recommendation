from enum import Enum
from azure.search.documents.models import SearchMode


class SearchConfig(Enum):
    TOP = 3
    SEARCH_MODE = SearchMode.ANY
    QUERY_TYPE = "full"
    SELECT_FIELDS = ["title", "fullplot", "countries"]
    VECTOR_KIND = "vector"
    K_NEAREST_NEIGHBORS = 3
    VECTOR_FIELD = "vector"
