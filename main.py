from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
import requests
import os

app = FastAPI()
SHEET_API_URL = os.environ.get("SHEET_API_URL")

# This tells the Brain to look in the /public folder for your website files
app.mount("/static", StaticFiles(directory="public"), name="static")

@app.post("/api/leads")
async def add_lead(request: Request):
    data = await request.json()
    if not SHEET_API_URL:
        return {"error": "API URL not configured"}
    
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

# This makes sure the "Face" of the site shows up at the main URL
@app.get("/")
async def read_index():
    from fastapi.responses import FileResponse
    return FileResponse('public/index.html')

@app.get("/dashboard")
async def read_dashboard():
    from fastapi.responses import FileResponse
    return FileResponse('public/dashboard.html')
