from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pdfplumber
import io
import requests
import os
from dotenv import load_dotenv


load_dotenv()
app = FastAPI()


# Allow frontend apps like Streamlit to call the API
app.add_middleware(
   CORSMiddleware,
   allow_origins=["*"],
   allow_credentials=True,
   allow_methods=["*"],
   allow_headers=["*"],
)


# Load API key
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")








# ------------------------------
# Root Endpoint
# ------------------------------
@app.get("/")
def read_root():
   return {"message": "Resume Analyzer API Running"}




# ------------------------------
# Extract Text from PDF
# ------------------------------
@app.post("/extract")
async def extract_pdf(file: UploadFile = File(...)):


   if not file.filename.endswith(".pdf"):
       return {"error": "Please upload a PDF file"}


   text_content = ""


   pdf_bytes = await file.read()


   with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
       for page in pdf.pages:
           page_text = page.extract_text()
           if page_text:
               text_content += page_text + "\n"


   return {"content": text_content}




# ------------------------------
# Ask LLM
# ------------------------------
@app.get("/ask")
def ask(question: str):


   url = "https://openrouter.ai/api/v1/chat/completions"


   headers = {
       "Authorization": f"Bearer {OPENROUTER_API_KEY}",
       "Content-Type": "application/json"
   }


   payload = {
       "model": "stepfun/step-3.5-flash:free",
       "messages": [
           {"role": "user", "content": question}
       ]
   }


   response = requests.post(url, headers=headers, json=payload)


   if response.status_code != 200:
       return {"error": response.text}


   result = response.json()


   answer = result["choices"][0]["message"]["content"]


   return {
       "question": question,
       "answer": answer
   }
