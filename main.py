from fastapi import FastAPI, HTTPException
from utils.prompt import GROUNDED_PROMPT
from utils.rag import RAGService
from utils.model import QueryRequest, RAGResponse


app = FastAPI()
rag_service = RAGService()


@app.get('/')
def read_root():
    return {"message": "Hello, welcome to your personal movie recommendation assistant!"}


@app.post('/rag')
async def rag(request: QueryRequest):
    try:
        result = rag_service.orchestrate_rag(request.query, GROUNDED_PROMPT)
        return RAGResponse(response=result['response'])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
