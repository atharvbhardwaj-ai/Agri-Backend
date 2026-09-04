import chromadb

client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(name="agri_knowledge")

# Comprehensive Seed Data (Crops, Soil, Fertilizer, Schemes)
documents = [
    # --- CROP & AGRONOMY PRACTICES ---
    (
        "Rice (Paddy) Cultivation & Soil: Requires deep, fertile clayey, clay-loam, or silty soils "
        "capable of holding water. Optimal soil pH is 5.5 to 6.5. Best grown in warm, humid climates with "
        "standing water during early vegetative stages. Recommended NPK fertilizer ratio is 120:60:40 kg/ha. "
        "Sowing season: Kharif (June-July). Critical irrigation stages: Panicle initiation and flowering. "
        "Common pests: Yellow stem borer and blast disease (managed with Tricyclazole 75% WP)."
    ),
    (
        "Wheat Cultivation & Soil: Prefers well-drained, fertile loamy and clay-loam soils with neutral pH (6.0 to 7.5). "
        "Grown as a Rabi crop sown in October to December and harvested in March-April. Requires cool temperatures during "
        "vegetative growth and warm weather during ripening. Recommended NPK ratio is 120:60:40 kg/ha. "
        "Critical irrigation at Crown Root Initiation (CRI) stage (20-25 days after sowing) is mandatory. "
        "Susceptible to Yellow rust and Karnal bunt."
    ),
    (
        "Cotton Cultivation & Soil: Best suited for deep black soils (Regur soils) and well-drained alluvial soils "
        "with good moisture retention. Optimal pH range is 6.0 to 8.0. Requires long frost-free periods and warm climate. "
        "Recommended NPK: 100:50:50 kg/ha with Zinc Sulfate application. Kharif crop sown in April-May (North) or June-July (Central/South). "
        "Common pests: Pink bollworm and sucking pests (aphids, jassids, whiteflies; managed via IPM and Neem-based sprays)."
    ),
    (
        "Tomato Cultivation & Soil: Thrives in well-drained sandy loam or clay loam soils rich in organic matter. "
        "Optimal pH is 6.0 to 7.0. Very sensitive to waterlogging. Recommended NPK ratio is 150:100:100 kg/ha. "
        "Major diseases: Early Blight (Alternaria solani) and Late Blight. Recommended management includes Mancozeb 75% WP "
        "(600g in 200L water per acre) or Copper Oxychloride sprays."
    ),
    (
        "Sugarcane Cultivation & Soil: Requires deep, well-drained loamy or clayey soils rich in organic matter with pH 6.5 to 7.5. "
        "High water requirement (1500-2500 mm). High nutrient demand: NPK 250:115:115 kg/ha applied in split doses. "
        "Key pests include Early shoot borer and Top borer. Critical irrigation needed during formative tillering phase."
    ),
    (
        "Maize (Corn) Cultivation & Soil: Grows best in well-drained sandy loam to silty loam soils with pH 5.8 to 7.5. "
        "Cannot tolerate waterlogging or saline conditions. Recommended NPK is 120:60:40 kg/ha. "
        "Major pest: Fall Armyworm (Spodoptera frugiperda). Integrated Pest Management requires pheromone traps, "
        "Neem formulation (Azadirachtin 1500 ppm), or Emamectin Benzoate 5% SG application."
    ),
    (
        "Mustard Cultivation & Soil: Requires light to heavy loam soils with good drainage; tolerates slight alkalinity (pH 6.5 to 8.0). "
        "Major Rabi oilseed crop. Recommended NPK: 80:40:40 kg/ha with 20-30 kg/ha Sulphur for higher oil content. "
        "Major pest: Mustard aphid (Lipaphis erysimi); managed using Dimethoate 30% EC or Thiamethoxam 25% WG."
    ),
    (
        "Soybean Cultivation & Soil: Prefers fertile, well-drained loamy soils rich in calcium and organic matter, pH 6.0 to 7.5. "
        "Requires seed inoculation with Rhizobium culture. Recommended NPK: 30:60:40 kg/ha (legume requires less nitrogen). "
        "Sown in Kharif (June-July). Sensitive to moisture stress at flowering and pod filling."
    ),
    (
        "Pulses (Gram/Chickpea) Cultivation & Soil: Grown predominantly in light to medium-heavy black soils and alluvial loams. "
        "Requires well-drained soil; waterlogged soils cause wilt disease (Fusarium oxysporum). Recommended NPK: 20:50:20 kg/ha. "
        "Pod borer (Helicoverpa armigera) is controlled using pheromone traps and Chlorantraniliprole."
    ),

    # --- GOVERNMENT SCHEMES ---
    (
        "PM-Kisan Samman Nidhi: Provides ₹6,000 per year directly into the bank accounts of all landholding farmer families "
        "in three equal installments of ₹2,000 every four months. Eligibility requires land ownership records verified on the state "
        "revenue portal and active bank accounts with completed e-KYC."
    ),
    (
        "Pradhan Mantri Fasal Bima Yojana (PMFBY): Comprehensive crop insurance covering yield loss due to non-preventable natural risks "
        "including floods, drought, unseasonal rain, landslides, cyclones, and widespread pest attacks. Uniform low premium: 2% for Kharif, "
        "1.5% for Rabi food grains and oilseeds, and 5% for annual commercial/horticultural crops."
    ),
    (
        "Kisan Credit Card (KCC): Offers short-term crop loans and working capital up to ₹3,00,000 at a concessional interest rate of 4% per annum "
        "(with 3% prompt repayment incentive). Provides collateral-free agricultural loans up to ₹1,60,000. Extended to animal husbandry, dairy, and fisheries."
    ),
    (
        "Soil Health Card Scheme: Issues periodic soil health cards to farmers detailing status across 12 parameters: macro-nutrients (N, P, K), "
        "secondary nutrients (S), micro-nutrients (Zn, Fe, Cu, Mn, Bo), and physical indices (pH, EC, Organic Carbon). Includes customized fertilizer recommendations."
    ),
    (
        "PM Krishi Sinchayee Yojana (PMKSY - Per Drop More Crop): Focuses on micro-irrigation systems (drip and sprinkler sets) to maximize water efficiency. "
        "Provides subsidies up to 55% for small and marginal farmers and 45% for other farmers."
    ),
    (
        "Sub-Mission on Agricultural Mechanization (SMAM): Financial assistance and subsidies ranging from 40% to 50% for purchasing farm machinery "
        "(tractors, power tillers, rotavators, drone sprayers) and setting up Custom Hiring Centres (CHCs) at the village/block level."
    ),
    (
        "Paramparagat Krishi Vikas Yojana (PKVY): Promotes organic farming and PGS (Participatory Guarantee System) certification. "
        "Financial assistance of ₹50,000 per hectare for 3 years is provided for organic inputs, certification, and packaging/marketing linkages."
    )
]

metadatas = [
    {"source": "ICAR_Package_of_Practices_Rice.pdf", "category": "crop_agronomy"},
    {"source": "ICAR_Package_of_Practices_Wheat.pdf", "category": "crop_agronomy"},
    {"source": "ICAR_Package_of_Practices_Cotton.pdf", "category": "crop_agronomy"},
    {"source": "ICAR_Package_of_Practices_Tomato.pdf", "category": "crop_agronomy"},
    {"source": "ICAR_Package_of_Practices_Sugarcane.pdf", "category": "crop_agronomy"},
    {"source": "ICAR_Package_of_Practices_Maize.pdf", "category": "crop_agronomy"},
    {"source": "ICAR_Package_of_Practices_Mustard.pdf", "category": "crop_agronomy"},
    {"source": "ICAR_Package_of_Practices_Soybean.pdf", "category": "crop_agronomy"},
    {"source": "ICAR_Package_of_Practices_Pulses.pdf", "category": "crop_agronomy"},
    {"source": "PM_Kisan_Guidelines.pdf", "category": "scheme_income"},
    {"source": "PMFBY_Operational_Guidelines.pdf", "category": "scheme_insurance"},
    {"source": "KCC_Scheme_Details.pdf", "category": "scheme_credit"},
    {"source": "Soil_Health_Card_Manual.pdf", "category": "scheme_soil"},
    {"source": "PMKSY_Guidelines.pdf", "category": "scheme_irrigation"},
    {"source": "SMAM_Mechanization_Guidelines.pdf", "category": "scheme_machinery"},
    {"source": "PKVY_Organic_Farming_Rules.pdf", "category": "scheme_organic"}
]

ids = [
    "crop_rice", "crop_wheat", "crop_cotton", "crop_tomato", "crop_sugarcane", 
    "crop_maize", "crop_mustard", "crop_soybean", "crop_pulses",
    "scheme_pm_kisan", "scheme_pmfby", "scheme_kcc", "scheme_soil_health", 
    "scheme_pmksy", "scheme_smam", "scheme_pkvy"
]

collection.upsert(documents=documents, metadatas=metadatas, ids=ids)
print(f"✅ Successfully seeded {len(documents)} agronomy and scheme documents into ChromaDB.")