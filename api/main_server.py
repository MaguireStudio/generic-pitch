from fastapi import FastAPI, Request
import requests
import os

app = FastAPI()
SHEET_API_URL = os.environ.get("SHEET_API_URL")

@app.post("/api/leads")
async def add_lead(request: Request):
    data = await request.json()
    if not SHEET_API_URL:
        return {"error": "API URL not configured"}
    
    # Generic payload for any business
    payload = {
        "name": data.get('name', 'N/A'),
        "phone": data.get('phone', 'N/A'),
        "interest": data.get('interest', 'General Inquiry'),
        "status": "NEW"
    }
    response = requests.post(SHEET_API_URL, json=payload)
    return response.json()

@app.get("/api/leads")
async def get_leads():
    if not SHEET_API_URL:
        return {"error": "API URL not configured"}
    response = requests.get(SHEET_API_URL)
    return response.json()
