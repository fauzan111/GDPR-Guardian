from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_italian_fiscal_code_redaction():
    # A fake but valid-format Italian Fiscal Code
    # RSSMRA80A01H501U -> Rossi Mario, Born 1980 in Rome
    payload = {
        "text": "Il cliente Mario Rossi ha il codice fiscale RSSMRA80A01H501U.",
        "language": "it"
    }
    
    response = client.post("/anonymize", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    
    # Check if the name was redacted
    assert "Mario Rossi" not in data["anonymized_text"]
    assert "<PERSON>" in data["anonymized_text"]
    
    # Check if the Fiscal Code was redacted
    assert "RSSMRA80A01H501U" not in data["anonymized_text"]
    assert "<IT_FISCAL_CODE>" in data["anonymized_text"]

def test_email_redaction():
    payload = {"text": "Scrivimi a mario.rossi@email.it", "language": "it"}
    response = client.post("/anonymize", json=payload)
    assert "mario.rossi@email.it" not in response.json()["anonymized_text"]
    assert "<EMAIL_ADDRESS>" in response.json()["anonymized_text"]