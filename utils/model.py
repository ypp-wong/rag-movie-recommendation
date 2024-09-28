from pydantic import BaseModel


class QueryRequest(BaseModel):
    query: str


class RAGResponse(BaseModel):
    response: str
