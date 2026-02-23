import os
from fastapi import FastAPI, Form, File, UploadFile, Request
from fastapi.templating import Jinja2Templates
import dropbox
from groq import Groq

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Config for Remington Rebuilds (CA)
DIVISION_NAME = "Remington Rebuilds"
BID_FOLDER = "/RBbids"  # Your Dropbox folder for CA
ADMIN_EMAIL = "rebuilds@yourdomain.com" 

# Connections
dbx = dropbox.Dropbox(
    app_key=os.getenv("DBX_KEY"),
    app_secret=os.getenv("DBX_SECRET"),
    oauth2_refresh_token=os.getenv("DBX_REFRESH_TOKEN")
)
llama = Groq(api_key=os.getenv("GROQ_API_KEY"))

@app.get("/")
async def serve_bid_room(request: Request):
    # This renders your branded landing page
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "division": DIVISION_NAME,
        "primary_color": "#B22222" # Example: Construction Red
    })

@app.post("/upload")
async def handle_upload(
    contractor: str = Form(...),
    category: str = Form(...),
    file: UploadFile = File(...)
):
    # Save directly to the RBbids folder in Dropbox
    dropbox_path = f"{BID_FOLDER}/Submittals/{category}/{contractor}_{file.filename}"
    content = await file.read()
    dbx.files_upload(content, dropbox_path)
    
    # Trigger AI summary & Email (Logic added here)
    return {"message": "Bid submitted successfully to Remington Rebuilds"}
