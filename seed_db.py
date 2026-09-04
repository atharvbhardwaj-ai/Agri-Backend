import chromadb

# 1. Initialize persistent storage
client = chromadb.PersistentClient(path="./chroma_db")

# 2. Get or create collection
collection = client.get_or_create_collection(name="agri_knowledge")

# 3. Complete Dataset: All 15 Native Crops + 7 Central Schemes
documents = [
    # --- 15 NATIVE CROPS ---
    (
        "Rice (Paddy) Cultivation & Soil: Requires deep, fertile clayey, clay-loam, or silty soils "
        "capable of holding water. Optimal soil pH is 5.5 to 6.5. Best grown in warm, humid climates with "
        "standing water during early vegetative stages. Recommended NPK fertilizer ratio is 120:60:40 kg/ha. "
        "Sowing season: Kharif (June-July). Critical irrigation stages: Panicle initiation and flowering. "
        "Common pests: Yellow stem borer and blast disease (managed with Tricyclazole 75% WP)."
    ),
    (
        "Wheat (Gehun) Crop Cultivation, Agronomy & Soil: Specific guide for growing wheat crop. Prefers well-drained, fertile loamy and clay-loam soils with neutral pH (6.0 to 7.5). "
        "Grown as a Rabi crop sown in October to December and harvested in March-April. Requires cool temperatures during "
        "vegetative growth and warm weather during ripening. Recommended NPK ratio is 120:60:40 kg/ha. "
        "Critical irrigation at Crown Root Initiation (CRI) stage (20-25 days after sowing) is mandatory. "
        "Susceptible to Yellow rust and Karnal bunt."
    ),
    (
        "Mustard Cultivation & Soil: Requires light to heavy loam soils with good drainage; tolerates slight alkalinity (pH 6.5 to 8.0). "
        "Major Rabi oilseed crop sown in September-October. Recommended NPK: 80:40:40 kg/ha along with 20-30 kg/ha elemental Sulphur "
        "for higher oil content. Major pest: Mustard aphid (Lipaphis erysimi); managed using Dimethoate 30% EC or Thiamethoxam 25% WG."
    ),
    (
        "Cotton Cultivation & Soil: Best suited for deep black soils (Regur soils) and well-drained alluvial soils "
        "with good moisture retention. Optimal pH range is 6.0 to 8.0. Requires long frost-free periods and warm climate. "
        "Recommended NPK: 100:50:50 kg/ha with Zinc Sulfate application. Kharif crop sown in April-May (North) or June-July (Central/South). "
        "Common pests: Pink bollworm and sucking pests (aphids, jassids, whiteflies; managed via IPM and Neem-based sprays)."
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
        "Potato Cultivation & Soil: Requires well-drained, loose, friable sandy loam or silt loam soils rich in organic matter. "
        "Optimal soil pH is 5.2 to 6.4 (slightly acidic helps prevent potato scab). Sown in Rabi season (October-November). "
        "Recommended NPK ratio is 150:100:120 kg/ha (high potash demand for tuber bulking). Sensitive to waterlogging; "
        "furrow or drip irrigation preferred. Common diseases: Late Blight (Phytophthora infestans) managed via Mancozeb or Metalaxyl."
    ),
    (
        "Soybean Cultivation & Soil: Prefers fertile, well-drained loamy soils rich in calcium and organic matter, pH 6.0 to 7.5. "
        "Requires seed inoculation with Rhizobium japonicum culture. Recommended NPK: 30:60:40 kg/ha (legume fixes atmospheric nitrogen). "
        "Sown in Kharif (June-July). Sensitive to moisture stress during flowering and pod-filling stages."
    ),
    (
        "Chickpea (Gram/Pulses) Cultivation & Soil: Grown predominantly in well-drained medium-heavy black soils and alluvial loams with pH 6.0 to 7.5. "
        "Strictly cannot tolerate poorly drained or waterlogged soils, which trigger Fusarium wilt. Recommended NPK: 20:50:20 kg/ha. "
        "Sown in October-November (Rabi). Major pest: Gram pod borer (Helicoverpa armigera), controlled via pheromone traps and Chlorantraniliprole."
    ),
    (
        "Tomato Cultivation & Soil: Thrives in well-drained sandy loam or clay loam soils rich in organic matter. "
        "Optimal pH is 6.0 to 7.0. Very sensitive to waterlogging. Recommended NPK ratio is 150:100:100 kg/ha. "
        "Major diseases: Early Blight (Alternaria solani) and Late Blight. Recommended management includes Mancozeb 75% WP "
        "(600g in 200L water per acre) or Copper Oxychloride sprays."
    ),
    (
        "Onion Cultivation & Soil: Requires deep, well-drained, loose friable sandy loam to clay loam soils with high organic matter. "
        "Optimal pH range is 6.0 to 7.0; highly sensitive to high salinity and waterlogging. Sown in Kharif (May-June) or Late Kharif/Rabi (October-November). "
        "Recommended NPK ratio is 100:50:50 kg/ha with 15 kg/ha Sulphur. Major pest: Onion thrips (Thrips tabaci) managed with Fipronil or Profenofos."
    ),
    (
        "Garlic Cultivation & Soil: Requires fertile, well-drained rich loamy to sandy loam soil with good moisture retention and pH 6.0 to 7.0. "
        "Heavy clay soils lead to deformed cloves and poor bulb development. Rabi crop planted in September to November. "
        "Recommended NPK: 100:50:50 kg/ha with 20 kg/ha elemental Sulphur. Critical irrigation at bulb development stage."
    ),
    (
        "Millet (Bajra/Pearl Millet & Jowar/Sorghum) Cultivation & Soil: Extremely drought-hardy. Grows well in shallow to deep sandy loam, "
        "loamy, or light black soils with pH 6.5 to 8.0. Highly drought-tolerant; ideal for semi-arid rainfed regions. "
        "Recommended NPK: 80:40:20 kg/ha for Bajra, 80:40:40 kg/ha for Sorghum. Sown in Kharif (June-July). "
        "Major disease: Downy mildew / Green ear in Bajra, managed with Metalaxyl seed treatment."
    ),
    (
        "Groundnut (Peanut) Cultivation & Soil: Requires well-drained, loose, friable sandy loam or light loamy soil rich in calcium and organic matter. "
        "Optimal pH is 6.0 to 6.8. Loose soil is essential for easy penetration of pegs into the soil. Recommended NPK: 25:50:40 kg/ha "
        "with Gypsum application (400-500 kg/ha) at flowering/pegging for healthy pod development. Sown in Kharif (June-July) or Rabi/Summer."
    ),
    (
        "Barley Cultivation & Soil: Thrives in well-drained loamy to sandy loam soils. Remarkable for its high tolerance to saline and alkaline conditions "
        "compared to other cereals; grows well in pH 7.0 to 8.5. Sown in October-November (Rabi). Recommended NPK ratio is 60:30:20 kg/ha for rainfed "
        "and 80:40:30 kg/ha for irrigated crop. Critical irrigation stages: Active tillering and heading."
    ),

    # --- 7 GOVERNMENT SCHEMES ---
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
    # Crops (15)
    {"source": "ICAR_Package_of_Practices_Rice.pdf", "category": "crop_agronomy"},
    {"source": "ICAR_Package_of_Practices_Wheat.pdf", "category": "crop_agronomy"},
    {"source": "ICAR_Package_of_Practices_Mustard.pdf", "category": "crop_agronomy"},
    {"source": "ICAR_Package_of_Practices_Cotton.pdf", "category": "crop_agronomy"},
    {"source": "ICAR_Package_of_Practices_Sugarcane.pdf", "category": "crop_agronomy"},
    {"source": "ICAR_Package_of_Practices_Maize.pdf", "category": "crop_agronomy"},
    {"source": "ICAR_Package_of_Practices_Potato.pdf", "category": "crop_agronomy"},
    {"source": "ICAR_Package_of_Practices_Soybean.pdf", "category": "crop_agronomy"},
    {"source": "ICAR_Package_of_Practices_Chickpea.pdf", "category": "crop_agronomy"},
    {"source": "ICAR_Package_of_Practices_Tomato.pdf", "category": "crop_agronomy"},
    {"source": "ICAR_Package_of_Practices_Onion.pdf", "category": "crop_agronomy"},
    {"source": "ICAR_Package_of_Practices_Garlic.pdf", "category": "crop_agronomy"},
    {"source": "ICAR_Package_of_Practices_Millet.pdf", "category": "crop_agronomy"},
    {"source": "ICAR_Package_of_Practices_Groundnut.pdf", "category": "crop_agronomy"},
    {"source": "ICAR_Package_of_Practices_Barley.pdf", "category": "crop_agronomy"},
    # Schemes (7)
    {"source": "PM_Kisan_Guidelines.pdf", "category": "scheme_income"},
    {"source": "PMFBY_Operational_Guidelines.pdf", "category": "scheme_insurance"},
    {"source": "KCC_Scheme_Details.pdf", "category": "scheme_credit"},
    {"source": "Soil_Health_Card_Manual.pdf", "category": "scheme_soil"},
    {"source": "PMKSY_Guidelines.pdf", "category": "scheme_irrigation"},
    {"source": "SMAM_Mechanization_Guidelines.pdf", "category": "scheme_machinery"},
    {"source": "PKVY_Organic_Farming_Rules.pdf", "category": "scheme_organic"}
]

ids = [
    "crop_rice", "crop_wheat", "crop_mustard", "crop_cotton", "crop_sugarcane",
    "crop_maize", "crop_potato", "crop_soybean", "crop_chickpea", "crop_tomato",
    "crop_onion", "crop_garlic", "crop_millet", "crop_groundnut", "crop_barley",
    "scheme_pm_kisan", "scheme_pmfby", "scheme_kcc", "scheme_soil_health",
    "scheme_pmksy", "scheme_smam", "scheme_pkvy"
]

# Upsert all entries
collection.upsert(documents=documents, metadatas=metadatas, ids=ids)
print(f"✅ ChromaDB successfully seeded with {len(documents)} total records.")

# --- DIAGNOSTIC VERIFICATION ---
print("\n🔍 Running diagnostic retrieval verification on native crops...")
all_native_crops = [
    "Wheat", "Rice", "Mustard", "Cotton", "Sugarcane", "Maize", "Potato",
    "Soybean", "Chickpea", "Tomato", "Onion", "Garlic", "Millet", "Groundnut", "Barley"
]

for crop in all_native_crops:
    res = collection.query(query_texts=[f"Best soil, pH, and fertilizer for {crop}"], n_results=1)
    retrieved_id = res["ids"][0][0] if res["ids"] and res["ids"][0] else "NONE"
    expected_id = f"crop_{crop.lower()}"
    status = "✅ PASS" if retrieved_id == expected_id else f"⚠️ RETRIEVED ({retrieved_id})"
    print(f"  • {crop.ljust(10)} -> {status}")

print("\n🚀 Database verification complete. Ready for deployment!")