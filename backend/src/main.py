from fastapi import FastAPI
from app.controller.ServerController import read_root , health 

app = FastAPI(title="RAG API")

app.get("/api/")(read_root)
app.get("/api/health")(health)