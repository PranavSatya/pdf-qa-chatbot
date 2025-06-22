# Import required modules from FastAPI
from fastapi import FastAPI, Form, UploadFile, File, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

# Import custom modules for processing
from qa_engine import extract_text_and_create_index, answer_question
from test_generator import generate_test_pdf

import os

# Initialize FastAPI app
app = FastAPI()

# Add middleware to handle CORS (Cross-Origin Resource Sharing)
# This allows the frontend to make requests to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all domains (can restrict in production)
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Endpoint to upload a PDF file
@app.post("/upload/")
async def upload_pdf(file: UploadFile = File(...), background_tasks: BackgroundTasks = BackgroundTasks()):
    # Save uploaded file to the 'uploads' directory
    file_location = f"uploads/{file.filename}"
    with open(file_location, "wb") as f:
        f.write(await file.read())
    
    # Start background indexing task (FAISS)
    background_tasks.add_task(extract_text_and_create_index, file_location, file.filename)

    # Return filename and status
    return {"filename": file.filename, "status": "Processing started"}

# Endpoint to ask a question about the uploaded PDF
@app.post("/ask/")
async def ask_question(filename: str = Form(...), question: str = Form(...)):
    # Use QA engine to generate an answer based on the indexed PDF
    answer = answer_question(filename, question)
    return {"answer": answer}

# Endpoint to generate a test PDF based on subject and difficulty
@app.post("/generate-test/")
async def generate_test(subject: str = Form(...), difficulty: str = Form(...), count: int = Form(10)):
    # Generate the test PDF using provided criteria
    filename, error = generate_test_pdf(subject, difficulty, count)
    
    # Return error if generation failed
    if error:
        return {"error": error}
    
    # Return URL to access generated PDF
    return {"pdf_url": f"http://localhost:8000/generated_pdfs/{filename}"}

# Endpoint to retrieve the generated test PDF by filename
@app.get("/generated_pdfs/{filename}")
async def get_pdf(filename: str):
    path = f"generated_pdfs/{filename}"
    return FileResponse(path, media_type="application/pdf", filename=filename)
