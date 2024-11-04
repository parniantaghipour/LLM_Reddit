from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

app = FastAPI()

# Allow CORS for your Svelte frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust to your frontend URL in production
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the model sentiment data
@app.get("/model_sentiment")
async def get_model_sentiment():
    try:
        # Load the model sentiment ranking CSV
        df = pd.read_csv("model_sentiment_ranking.csv")
        data = df.to_dict(orient="records")
        return {"status": "success", "data": data}
    except FileNotFoundError:
        return {"status": "error", "message": "Data not found."}

# Run with: uvicorn app:app --reload
