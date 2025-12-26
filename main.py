from fastapi import FastAPI, UploadFile, File
import shutil
import os
from fastapi.middleware.cors import CORSMiddleware
from src.parser import parse_resume

app = FastAPI(title="ATS Job Scraper AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Create data directory if it doesn't exist
os.makedirs("data", exist_ok=True)

@app.get("/")
def home():
    return {"message": "ATS Scraper API is running"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Save the uploaded file
    file_path = os.path.join("data", file.filename)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    
    # Parse the resume
    resume_data = parse_resume(file_path)
    
    # Return the parsed data
    return resume_data
