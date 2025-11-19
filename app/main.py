from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from app.engine import anonymize_text

app = FastAPI(
    title="GDPR Guardian API",
    description="An API to anonymize Italian PII (Codice Fiscale, Names, etc.) for GDPR compliance.",
    version="1.0.0"
)

# Data Models
class AnonymizeRequest(BaseModel):
    text: str = Field(..., example="Il mio Codice Fiscale è RSSMRA80A01H501U.")
    language: str = Field("it", example="it")

class AnonymizeResponse(BaseModel):
    original_text: str
    anonymized_text: str

# Endpoints 
@app.get("/")
def root():
    return {"message": "GDPR Guardian is running. Send POST requests to /anonymize"}

@app.post("/anonymize", response_model=AnonymizeResponse)
def redact_pii(request: AnonymizeRequest):
    try:
        clean_text = anonymize_text(request.text, request.language)
        return {
            "original_text": request.text,
            "anonymized_text": clean_text
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
