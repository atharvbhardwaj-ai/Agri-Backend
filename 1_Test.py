from fastapi import FastAPI

app = FastAPI(title="SIH Agri-Advisor API")


@app.get("/")
def home():
  return {"status": "running", "service": "SIH Agri Backend"}


@app.get("/api/v1/crop-info/{crop_name}")
def get_crop_info(crop_name: str):
  sample_data = {
      "wheat": {
          "season": "Rabi",
          "ideal_ph": "6.0 - 7.0",
          "msp_2025_26": "₹2,425 per quintal",
      },
      "rice": {
          "season": "Kharif",
          "ideal_ph": "5.5 - 6.5",
          "msp_2025_26": "₹2,300 per quintal",
      },
  }
  return sample_data.get(
      crop_name.lower(),
      {
          "status": "not_found",
          "message": f"No data available for {crop_name}",
      },
  )