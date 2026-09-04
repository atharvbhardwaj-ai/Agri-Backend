import os
import chromadb
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Agri-Advisor API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. Initialize persistent ChromaDB and Gemini Client
db = chromadb.PersistentClient(path="./chroma_db")
collection = db.get_or_create_collection(name="agri_knowledge")
ai = genai.Client()

class UserPrompt(BaseModel):
    query: str

@app.get("/")
def home():
    return {"status": "Agri-Advisor backend is live and ready"}

@app.post("/api/v1/ask")
def ask_advisor(data: UserPrompt):
    # Step A: Retrieve top 3 relevant chunks
    search_results = collection.query(query_texts=[data.query], n_results=3)

    docs = search_results["documents"][0] if search_results["documents"] else []
    metadatas = search_results["metadatas"][0] if search_results["metadatas"] else []

    context = "\n---\n".join(docs)
    source_name = metadatas[0]["source"] if metadatas else "ICAR Agricultural Guidelines"

    # Step B: Grounded yet helpful prompt
    prompt = f"""You are an expert agricultural extension advisor assisting Indian farmers.
Here is the verified context from our agronomy and government scheme database:
{context}

Farmer's Question: {data.query}

Guidelines:
1. Prioritize facts, numbers, soil types, NPK dosages, and rules from the verified context.
2. If the context covers the question (e.g. soil for rice/wheat, scheme details), give a clear, direct, and actionable answer in 2 to 3 concise sentences.
3. Keep the tone helpful, encouraging, and tailored for practical farming."""

    response = ai.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return {
        "answer": response.text.strip(),
        "source_document": source_name
    }