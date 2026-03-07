import streamlit as st
import requests
import time


BACKEND_URL = "http://localhost:8000"


st.title("AI Resume Analyzer")


uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])


prompt = st.text_area(
   "What would you like the AI to extract?",
   "Extract name, skills, years of experience and education from this resume."
)


if st.button("Analyze Resume"):


    # Progress UI
   progress = st.progress(0)
   status = st.empty()
  
   if uploaded_file is None:
       st.warning("Please upload a PDF first")
       st.stop()


   start_time = time.time()


   # -------------------------
   # Step 1: Send file to /extract
   # -------------------------
   files = {"file": uploaded_file}


   extract_response = requests.post(
       f"{BACKEND_URL}/extract",
       files=files
   )


   if extract_response.status_code != 200:
       st.error("Failed to extract PDF")
       st.stop()


   pdf_text = extract_response.json()["content"]


   # -------------------------
   # Step 2: Create prompt for LLM
   # -------------------------


   final_prompt = f"""
   Resume Content:


   {pdf_text}


   Task:
   {prompt}
   """


   # -------------------------
   # Step 3: Call LLM API
   # -------------------------


   llm_response = requests.get(
       f"{BACKEND_URL}/ask",
       params={"question": final_prompt}
   )


   if llm_response.status_code != 200:
       st.error("LLM request failed")
       st.stop()


   result = llm_response.json()


   end_time = time.time()
   total_time = round(end_time - start_time, 2)


   # -------------------------
   # Step 4: Show results
   # -------------------------


   st.subheader("AI Analysis")


   st.write(result["answer"])


   st.divider()


   st.caption(f"⏱ End-to-end response time: {total_time} seconds")