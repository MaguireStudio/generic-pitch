from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import requests
import os
from pathlib import Path

app = FastAPI()
SHEET_API_URL = os.environ.get("SHEET_API_URL")

# Verify public folder exists
PUBLIC_DIR = Path("public")
if not PUBLIC_DIR.exists():
    raise RuntimeError(f"Public directory not found at {PUBLIC_DIR.absolute()}")

# This tells the Brain to look in the /public folder for your website files
app.mount("/static", StaticFiles(directory="public"), name="static")

@app.post("/api/leads")
async def add_lead(request: Request):
    try:
        data = await request.json()
        if not SHEET_API_URL:
            return {"error": "API URL not configured"}, 500
        
payload = {
            "name": data.get('name', 'N/A'),
            "phone": data.get('phone', 'N/A'),
            "interest": data.get('interest', 'General Inquiry'),
            "status": "NEW"
        }
        response = requests.post(SHEET_API_URL, json=payload, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"API request failed: {str(e)}"}, 500
    except Exception as e:
        return {"error": f"Failed to process lead: {str(e)}"}, 400

@app.get("/api/leads")
async def get_leads():
    try:
        if not SHEET_API_URL:
            return {"error": "API URL not configured"}, 500
        response = requests.get(SHEET_API_URL, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"API request failed: {str(e)}"}, 500
    except Exception as e:
        return {"error": f"Failed to fetch leads: {str(e)}"}, 400

# This makes sure the "Face" of the site shows up at the main URL
@app.get("/")
async def read_index():
    index_path = PUBLIC_DIR / "index.html"
    if not index_path.exists():
        return {"error": "index.html not found"}, 404
    return FileResponse(str(index_path))

@app.get("/dashboard")
async def read_dashboard():
    dashboard_path = PUBLIC_DIR / "dashboard.html"
    if not dashboard_path.exists():
        return {"error": "dashboard.html not found"}, 404
    return FileResponse(str(dashboard_path))