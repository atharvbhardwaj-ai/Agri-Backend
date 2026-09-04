import os
import time
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

# 1. Initialize ChromaDB client and Gemini Client
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
    # Step A: Vector retrieval from ChromaDB
    search_results = collection.query(query_texts=[data.query], n_results=3)

    docs = search_results["documents"][0] if search_results.get("documents") and search_results["documents"] else []
    metadatas = search_results["metadatas"][0] if search_results.get("metadatas") and search_results["metadatas"] else []

    context = "\n---\n".join(docs) if docs else "No specific institutional documents indexed for this exact topic."
    source_name = metadatas[0]["source"] if metadatas else "General Agronomy Practice / KVK Advisory"

    # Step B: Grounded prompt with intelligent fallback
    prompt = f"""You are an agricultural advisor helping Indian farmers.

VERIFIED CONTEXT FROM LOCAL DATABASE:
{context}

FARMER'S QUESTION:
{data.query}

INSTRUCTIONS:
1. If the VERIFIED CONTEXT directly answers the question, base your response strictly on those facts, figures, and rules to provide a clear, accurate, and practical recommendation in 2-3 sentences.
2. If the VERIFIED CONTEXT does not cover the question, use your general agronomic knowledge to provide a clear, accurate, and practical recommendation in 2-3 sentences.
3. Keep the response direct, actionable, and encouraging for a farmer."""

    # Step C: Dedicated call to gemini-3.5-flash-lite with graceful error handling
    response_text = None
    for attempt in range(2):
        try:
            response = ai.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt
            )
            if response and response.text:
                response_text = response.text.strip()
                break
        except Exception as err:
            print(f"[Warning] Attempt {attempt + 1} encountered an issue: {err}")
            time.sleep(1.0)  # Brief pause in case of a temporary network/demand spike

    if not response_text:
        return {
            "answer": "Our advisory servers are currently experiencing high demand. Please try asking your question again in a moment.",
            "source_document": "System Advisory"
        }

    return {
        "answer": response_text,
        "source_document": source_name
    }