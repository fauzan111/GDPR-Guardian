import streamlit as st
import requests
import re

st.set_page_config(page_title="GDPR Guardian", layout="wide")

API_URL = "http://api:80/anonymize" 
def is_valid_fiscal_code_format(text):
    
    pattern = r"^[A-Z]{6}\d{2}[A-Z]\d{2}[A-Z]\d{3}[A-Z]$"
    # Search for the exact pattern match
    return re.fullmatch(pattern, text, re.IGNORECASE) is not None

st.title("GDPR Guardian: PII Anonymizer Demo")
st.markdown("A compliance microservice demonstrating **Privacy by Design**.")
st.markdown("---")
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("1. Enter Sensitive Data")
    with st.form("pii_form", clear_on_submit=False):
        name = st.text_input("Name (to be redacted as <PERSON>)", value="Giuseppe Verdi")
        fiscal_code = st.text_input(
            "Codice Fiscale (CF):", 
            value="JZEFZN99T24Z222G", 
            help="16 characters: 6 letters, 2 digits, 1 letter, 2 digits, 1 letter, 3 digits, 1 letter."
        )
        combined_text = f"The customer {name} has the Fiscal Code: {fiscal_code}."
        
        language = st.selectbox("Language of Text:", ["it", "en"], index=0)
        submitted = st.form_submit_button("🚀 Anonymize Data (Send to API)")
        
        if submitted:
            #  Client-Side Validation 
            if not fiscal_code:
                st.error("Error: Codice Fiscale field cannot be empty.")
            elif not is_valid_fiscal_code_format(fiscal_code):
                st.error("Error: Codice Fiscale format is incorrect (should be 16 alphanumeric characters in correct pattern).")
            else:
            
                with col2:
                    st.subheader("2. MLOps Output")
                    with st.spinner('Sending data to MLOps API...'):
                        
                        payload = {"text": combined_text, "language": language}
                        
                        try:
                            response = requests.post(API_URL, json=payload, timeout=10)
                            response.raise_for_status() 
                            result = response.json()
                            
                            st.success("Anonymization Complete!")
                            st.markdown("**Original Text Sent:**")
                            st.code(result.get("original_text"))
                            
                            st.markdown("**Anonymized Output:**")
                            st.code(result.get("anonymized_text"))
                            
                        except requests.exceptions.RequestException as e:
                            st.error(f"Error connecting to backend API. Is the 'api' service running? Error: {e}")
with col2:
    st.subheader("2. MLOps Output")
    st.info("Results will appear here after clicking the button.")
    st.markdown("---")
    st.caption("Frontend powered by Streamlit. Backend powered by FastAPI.")
