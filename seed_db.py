import chromadb

# 1. Initialize persistent storage on your disk
client = chromadb.PersistentClient(path="./chroma_db")

# 2. Get or create the schemes collection
collection = client.get_or_create_collection(name="agri_schemes")

# 3. Seed data (Official Scheme Summaries)
documents = [
    (
        "PM-Kisan Samman Nidhi: Provides ₹6,000 per year in three equal"
        " installments of ₹2,000 to all landholding farmer families."
        " Beneficiaries require Aadhaar-seeded active bank accounts and land"
        " records verified on the state portal."
    ),
    (
        "Pradhan Mantri Fasal Bima Yojana (PMFBY): Crop insurance scheme"
        " providing financial support for crop loss or damage due to"
        " non-preventable natural risks (floods, drought, pests). Premium rates"
        " are capped at 2% for Kharif crops, 1.5% for Rabi crops, and 5% for"
        " commercial/horticultural crops."
    ),
    (
        "Soil Health Card Scheme: Issues soil health cards to farmers every 2"
        " years indicating the nutrient status of their soil (NPK, secondary,"
        " and micro-nutrients) along with customized fertilizer dosage"
        " recommendations to reduce input costs."
    ),
    (
        "Kisan Credit Card (KCC): Provides affordable institutional credit with"
        " an effective interest rate of 4% per annum (with prompt repayment"
        " incentive) up to a credit limit of ₹3,00,000 without collateral for"
        " loans up to ₹1,60,000."
    ),
    (
        "PM Krishi Sinchayee Yojana (PMKSY - Per Drop More Crop): Provides"
        " financial assistance of up to 55% for small and marginal farmers and"
        " 45% for other farmers to adopt micro-irrigation systems (drip and"
        " sprinkler)."
    ),
]

metadatas = [
    {"source": "PM_Kisan_Guidelines.pdf", "category": "income_support"},
    {"source": "PMFBY_Operational_Guidelines.pdf", "category": "insurance"},
    {"source": "Soil_Health_Card_Manual.pdf", "category": "soil_management"},
    {"source": "KCC_Scheme_Details.pdf", "category": "credit"},
    {"source": "PMKSY_Guidelines.pdf", "category": "irrigation"},
]

ids = ["pm_kisan", "pmfby", "soil_health", "kcc", "pmksy"]

# 4. Upsert (inserts or updates existing entries without duplicates)
collection.upsert(documents=documents, metadatas=metadatas, ids=ids)

print("✅ ChromaDB seeded successfully with 5 agricultural scheme documents.")