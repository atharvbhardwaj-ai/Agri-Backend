import chromadb
from fastapi import FastAPI
from google import genai
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. Connect to local ChromaDB and Gemini
db = chromadb.PersistentClient(path="./chroma_db")
collection = db.get_or_create_collection(name="agri_schemes")
ai = genai.Client()


# 2. Define the incoming request body
class UserPrompt(BaseModel):
  query: str


@app.get("/")
def home():
  return {"status": "Agri-Advisor backend is live"}


@app.post("/api/v1/ask")
def ask_advisor(data: UserPrompt):
  # Step A: Pull the top 2 matching text chunks from ChromaDB
  search_results = collection.query(query_texts=[data.query], n_results=2)

  docs = search_results["documents"][0]
  sources = search_results["metadatas"][0]

  context = "\n".join(docs)

  # Step B: Pass context and question to Gemini
  prompt = f"""You are an agricultural advisor helping Indian farmers.
Answer the farmer's question using only this verified context:
{context}

Farmer's Question: {data.query}
Give a clear, practical answer in 2-3 sentences."""

  response = ai.models.generate_content(
      model="gemini-2.5-flash", contents=prompt
  )

  # Step C: Return plain dictionary (FastAPI converts this to JSON automatically)
  return {"answer": response.text, "source_document": sources[0]["source"]}