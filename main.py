import os
import json
import time
import chromadb
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
from google.genai import types
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

# Initialize ChromaDB client and Gemini Client
db = chromadb.PersistentClient(path="./chroma_db")
collection = db.get_or_create_collection(name="agri_knowledge")
ai = genai.Client()

class UserPrompt(BaseModel):
    query: str

@app.get("/")
def home():
    return {"status": "Agri-Advisor backend is live and ready"}

# -------------------------------------------------------------
# 1. AGRONOMY & SCHEME ADVISORY (RAG Pipeline)
# -------------------------------------------------------------
@app.post("/api/v1/ask")
def ask_advisor(data: UserPrompt):
    search_results = collection.query(query_texts=[data.query], n_results=3)

    docs = search_results["documents"][0] if search_results.get("documents") and search_results["documents"] else []
    metadatas = search_results["metadatas"][0] if search_results.get("metadatas") and search_results["metadatas"] else []

    context = "\n---\n".join(docs) if docs else "No specific institutional documents indexed for this exact topic."
    source_name = metadatas[0]["source"] if metadatas else "General Agronomy Practice / KVK Advisory"

    prompt = f"""You are an agricultural advisor helping Indian farmers.

VERIFIED CONTEXT FROM LOCAL DATABASE:
{context}

FARMER'S QUESTION:
{data.query}

INSTRUCTIONS:
1. If the VERIFIED CONTEXT directly answers the question, base your response strictly on those facts, figures, and rules to provide a clear, accurate, and practical recommendation in 2-3 sentences.
2. If the VERIFIED CONTEXT does not cover the question, use your general agronomic knowledge to provide a clear, accurate, and practical recommendation in 2-3 sentences.
3. Keep the response direct, actionable, and encouraging for a farmer."""

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
            print(f"[Warning] Advisory attempt {attempt + 1} encountered an issue: {err}")
            time.sleep(1.0)

    if not response_text:
        return {
            "answer": "Our advisory servers are currently experiencing high demand. Please try asking your question again in a moment.",
            "source_document": "System Advisory"
        }

    return {
        "answer": response_text,
        "source_document": source_name
    }

# -------------------------------------------------------------
# 2. PRODUCE QUALITY PRE-GRADING (Multimodal Vision)
# -------------------------------------------------------------
@app.post("/api/v1/grade-crop")
async def grade_crop(
    crop_name: str = Form(...),
    image: UploadFile = File(...)
):
    try:
        # Read the uploaded binary bytes directly from the request stream
        image_bytes = await image.read()
        mime_type = image.content_type or "image/jpeg"

        grading_prompt = f"""
You are an expert agricultural quality inspector evaluating a sample batch of raw, harvested {crop_name} according to Indian physical market standards.

CRITICAL FIRST CHECK (VALIDATION GATE):
Examine if this image shows REAL, RAW, HARVESTED {crop_name} produce suitable for mandi/wholesale appraisal.
- If the image contains cooked food, prepared dishes, processed goods, an entirely different crop/object, humans, or indoor furniture, it is INVALID.
- In this case, DO NOT grade the produce. Immediately return the failure JSON schema below.

If the image is VALID raw {crop_name}, inspect physical surface parameters:
1. Surface Blemishes & Defect Ratio (cuts, fungal spots, insect damage, rot)
2. Color Ripeness & Uniformity (harvest maturity vs underripe/decayed)
3. Shape & Size Uniformity (consistency across visible batch)

Grading Rubric:
- "Grade A (Premium / Retail)": < 5% defects, uniform shape and color.
- "Grade B (Standard / Processing)": 5% - 15% minor defects, slight irregularities.
- "Grade C (Distress / Rejection)": > 15% severe defects, visible rot, or major damage.

Return ONLY a valid, raw JSON object matching one of these exact schemas:

IF VALID RAW PRODUCE:
{{
    "is_valid_crop": true,
    "crop": "{crop_name}",
    "visual_grade": "Grade A" | "Grade B" | "Grade C",
    "blemish_percentage": float,
    "color_uniformity": "High" | "Medium" | "Low",
    "observations": "Brief 1-2 sentence physical description of produce.",
    "recommendation": "1-sentence note on best selling channel."
}}

IF INVALID (Cooked food, wrong object, not raw harvest):
{{
    "is_valid_crop": false,
    "crop": "{crop_name}",
    "visual_grade": "Invalid",
    "blemish_percentage": null,
    "color_uniformity": null,
    "observations": "Image does not depict raw, freshly harvested produce. Detected non-agricultural or processed item.",
    "recommendation": "Please capture a clear photo of raw, harvested crop samples in natural lighting."
}}
"""

        response = ai.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=[
                types.Part.from_bytes(data=image_bytes, mime_type=mime_type),
                grading_prompt
            ],
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )

        if not response or not response.text:
            raise HTTPException(status_code=500, detail="Failed to extract visual inspection from model.")

        return json.loads(response.text)

    except HTTPException:
        raise
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Visual grading pipeline error: {str(err)}")