from enum import Enum


class SearchConfig(Enum):
    TOP = 3
    QUERY_TYPE = "full"
    SELECT_FIELDS = ["title", "fullplot", "countries"]
    VECTOR_KIND = "vector"
    K_NEAREST_NEIGHBORS = 3
    VECTOR_FIELD = "vector"
