from fastapi import FastAPI, File, UploadFile
import pytesseract
from PIL import Image
import re, io

app = FastAPI(title="महाराज का नौकर API")

@app.post("/scan-doc/")
async def parse_document(file: UploadFile = File(...)):
    img = Image.open(io.BytesIO(await file.read()))
    text = pytesseract.image_to_string(img)
    
    exam_date = re.search(r'\b\d{2}[/-]\d{2}[/-]\d{4}\b', text)
    roll_no = re.search(r'(?:Roll|Application)\s*(?:No[.:]?|Number)?\s*[:\s]*(\w+)', text, re.IGNORECASE)
    fee_paid = re.search(r'(?:Fee|Amount|Paid)[^\d]*([\d,]+(?:\.\d{2})?)', text, re.IGNORECASE)
    
    return {
        "status": "महाराज, आपका विवरण दर्ज कर लिया गया है!",
        "roll_number": roll_no.group(1) if roll_no else "उपलब्ध नहीं",
        "exam_date": exam_date.group(0) if exam_date else "उपलब्ध नहीं",
        "fee_amount": fee_paid.group(1) if fee_paid else "उपलब्ध नहीं"
  }
  
