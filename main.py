from fastapi import FastAPI, UploadFile, File
import shutil
import os
from fastapi.middleware.cors import CORSMiddleware
from src.parser import extract_text_from_pdf, get_keywords
from src.scrapper import scrape_jobs # New Import
from src.sheets_sync import save_to_local

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

@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    # Save the uploaded file
    file_path = f"data/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Step 1: Extract keywords
    text = extract_text_from_pdf(file_path)
    keywords = get_keywords(text)
    
    return {
        "filename": file.filename,
        "extracted_keywords": list(keywords),
        "status": "Ready for Step 2 (Scraping)"
    }

@app.post("/process-and-search")
async def process_and_search(file: UploadFile = File(...)):
    # 1. Parse Resume
    file_path = f"data/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    text = extract_text_from_pdf(file_path)
    keywords = get_keywords(text)
    
    # 2. Extract a 'Job Title' from keywords 
    # (Simple logic: take the first 2 keywords for the search query)
    search_query = " ".join(list(keywords)[:2]) 
    
    # 3. Trigger Scraper
    job_results = scrape_jobs(search_query)
    
    return {
        "found_keywords": keywords,
        "search_used": search_query,
        "jobs": job_results
    }

@app.post("/run-full-cycle")
async def run_full_cycle(file: UploadFile = File(...)):
    # 1. Parse Resume
    file_path = f"data/{file.filename}"
    with open(file_path, "wb") as f:
        import shutil
        shutil.copyfileobj(file.file, f)
    list = []
    list.append("Software Engineer")
    list.append("Data Engineer")
    list.append("Java Full Stack")
    # keywords = get_keywords(extract_text_from_pdf(file_path))
    search_query = list[2] # Using top keyword for now
    
    # 2. Scrape Jobs
    jobs = scrape_jobs(search_query)
    
    # 3. Save to Google Sheets
    if jobs:
        success = save_to_local(jobs)
    
    return {
        "keywords_found": list,
        "jobs_scraped": len(jobs),
        "sheets_updated": success if jobs else False
    }
