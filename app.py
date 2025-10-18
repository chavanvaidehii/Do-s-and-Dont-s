from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
import google.generativeai as genai

# Configure API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Choose a Gemini text-generation model
model_name = "models/gemini-2.5-pro"  # or "models/gemini-pro-latest"
model = genai.GenerativeModel(model_name)

# Streamlit UI
st.set_page_config(page_title="Gemini Health Advisor")
st.header("🩺 Health Advisor")

# Input disease name
disease_name = st.text_input(
    "Enter the disease predicted from X-ray (e.g., Viral Pneumonia, Tuberculosis, Normal):"
)

if st.button("Generate DOs and DON'Ts"):
    if not disease_name.strip():
        st.warning("⚠️ Please enter a disease name.")
    else:
        # Build prompt including the disease name
        prompt = f"""
You are a responsible AI health assistant.
Provide exactly 3 short, clear, medically appropriate *Do’s* and *Don’ts*:
- Use plain-language bullet points (<=20 words each)
- Focus on lifestyle, hygiene, rest, diet, prevention
- Avoid medicine names or treatments
- Include one short safety note to consult a qualified doctor
"""

        try:
            response = model.generate_content(prompt)
            st.subheader("🧾 AI Recommendations:")
            st.write(response.text)
        except Exception as e:
            st.error(f"Failed to generate response: {e}")
