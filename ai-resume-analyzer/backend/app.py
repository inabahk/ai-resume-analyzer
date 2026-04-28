from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import os, re, io
from analyzer import analyze_resume

app = FastAPI(title="AI Resume Analyzer", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
async def root():
    with open("../frontend/index.html") as f:
        return f.read()

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    if not file.filename.endswith((".txt", ".pdf", ".doc", ".docx")):
        raise HTTPException(status_code=400, detail="Please upload a .txt, .pdf, .doc, or .docx file")
    content = await file.read()
    try:
        text = content.decode("utf-8", errors="ignore")
    except Exception:
        text = content.decode("latin-1", errors="ignore")
    if len(text.strip()) < 50:
        raise HTTPException(status_code=400, detail="File appears to be empty or unreadable")
    result = analyze_resume(text)
    return result

@app.post("/analyze-text")
async def analyze_text(payload: dict):
    text = payload.get("text", "")
    if len(text.strip()) < 50:
        raise HTTPException(status_code=400, detail="Please provide more resume text")
    result = analyze_resume(text)
    return result

@app.get("/health")
async def health():
    return {"status": "ok"}
