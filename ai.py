import streamlit as st
import PyPDF2
import requests
import time

# ---- Gemini API function ----
def gemini_generate_content(prompt, api_key, retries=3, delay=10):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": api_key
    }
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }
    for attempt in range(retries):
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            result = response.json()
            try:
                ai_text = result["candidates"][0]["content"]["parts"][0]["text"]
                return ai_text
            except Exception:
                st.error("Unexpected response format from Gemini API.")
                return None
        elif response.status_code == 429:
            st.warning(f"Rate limit reached. Retrying in {delay} seconds... (Attempt {attempt+1} of {retries})")
            time.sleep(delay)
        else:
            st.error(f"Gemini API Error: {response.status_code}\n{response.text}")
            return None
    st.error("Failed after several retries due to rate limit (429 Too Many Requests). Try again later or check your quota.")
    return None

# ---- PDF text extraction ----
def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
    return text

# ---- Streamlit UI ----
st.set_page_config(page_title="PDF MCQ Generator with Gemini AI", page_icon="📄")
st.title("📄 PDF to MCQ Generator (Gemini AI)")

API_KEY = "AIzaSyC8WOWCnT4_WFAZhrtEFmeN01fx4WWofBo"  # <-- put your Gemini API key here

uploaded_pdf = st.file_uploader("Upload your PDF", type=["pdf"])
if uploaded_pdf:
    with st.spinner("Extracting PDF text..."):
        pdf_text = extract_text_from_pdf(uploaded_pdf)
        if not pdf_text:
            st.warning("Could not extract any text from the PDF.")
        else:
            st.success("Text extracted from PDF!")

    st.markdown("### PDF Content Preview")
    st.write(pdf_text[:800] + "..." if len(pdf_text) > 800 else pdf_text)

    num_mcqs = st.number_input("Number of MCQs to generate", 1, 10, 3)
    if st.button("Generate MCQs (Gemini AI)"):
        with st.spinner("Generating MCQs with Gemini..."):
            prompt = f"Generate {num_mcqs} multiple-choice questions with 4 options each (A, B, C, D), provide the correct answer, and cover key ideas from the following passage:\n\n{pdf_text[:3000]}"
            mcqs = gemini_generate_content(prompt, API_KEY)
            if mcqs:
                st.markdown("## Generated MCQs")
                st.text(mcqs)

st.markdown("---")
st.caption("Powered by Google Gemini and Streamlit.")
