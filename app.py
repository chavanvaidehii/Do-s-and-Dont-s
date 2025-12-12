from dotenv import load_dotenv
load_dotenv()  # Loads .env from same folder

import streamlit as st
import os
import google.generativeai as genai

# Configure API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Gemini model
model_name = "models/gemini-2.5-pro"
model = genai.GenerativeModel(model_name)

# Predefined fallback advice
advice_dict = {
    "normal": [
        "✅ Maintain a balanced diet and regular exercise",
        "✅ Get enough sleep (7–8 hours daily)",
        "✅ Practice good hygiene",
        "⚠️ Even if normal, consult a doctor for routine checkups"
    ],
    "viral pneumonia": [
        "✅ Rest adequately and stay hydrated",
        "✅ Eat light, nutritious meals",
        "✅ Maintain hygiene to avoid infections",
        "⚠️ Consult a doctor if symptoms worsen"
    ],
    "bacterial pneumonia": [
        "✅ Get adequate rest and nutrition",
        "✅ Avoid smoking and polluted air",
        "✅ Keep hands and environment clean",
        "⚠️ Seek medical advice promptly"
    ],
    "obstructive pulmonary disorder": [
        "✅ Avoid smoking and pollutants",
        "✅ Practice breathing exercises",
        "✅ Stay active but rest when needed",
        "⚠️ Consult a pulmonologist for proper management"
    ],
    "tuberculosis": [
        "✅ Follow a nutritious, high-protein diet",
        "✅ Avoid crowded places and wear masks",
        "✅ Ensure regular rest and exercise cautiously",
        "⚠️ Always follow medical supervision and treatment"
    ]
}

# Streamlit UI
st.set_page_config(page_title="Gemini Health Advisor")
st.header("🩺 Health Advisor")

disease_name = st.text_input(
    "Enter the disease predicted from X-ray (e.g., Viral Pneumonia, Tuberculosis, Normal, etc):"
)

if st.button("Generate DOs and DON'Ts"):
    disease_clean = disease_name.lower().strip()

    if not disease_clean:
        st.warning("⚠️ Please enter a disease name.")
        st.stop()

    # ⭐ CASE 1: If disease is NORMAL → No API call
    if disease_clean == "normal":
        st.subheader("🧾 Recommendations (Normal Case):")
        for line in advice_dict["normal"]:
            st.write(line)
        st.info("ℹ️ API not used for 'Normal'. Showing predefined safe advice.")
        st.stop()

    # Build prompt for API
    prompt = f"""
You are a responsible AI health assistant.
Provide exactly 3 short, clear, medically appropriate Do’s and Don'ts for {disease_name}:
- Plain-language bullet points (<=20 words each)
- Focus on lifestyle, hygiene, rest, diet, prevention
- Avoid medicine names or treatments
- Include one short safety note to consult a qualified doctor
"""

    # ⭐ CASE 2: Try API → cache only success
    try:
        if "cache" not in st.session_state:
            st.session_state.cache = {}

        # If AI result previously cached
        if disease_clean in st.session_state.cache:
            st.subheader("🧾 AI Recommendations (via Gemini API):")
            st.write(st.session_state.cache[disease_clean])
            st.stop()

        # Fresh API call
        response = model.generate_content(prompt)

        # Store ONLY success in cache
        st.session_state.cache[disease_clean] = response.text

        st.subheader("🧾 AI Recommendations (via Gemini API):")
        st.write(response.text)

    except Exception:
        # ⭐ CASE 3: API FAILURE → Fallback WITHOUT caching
        st.warning("⚠️ API error occurred. Showing fallback advice.")

        # Remove old cached value (if any)
        if disease_clean in st.session_state.cache:
            st.session_state.cache.pop(disease_clean, None)

        if disease_clean in advice_dict:
            st.subheader("🧾 Recommendations (Fallback):")
            for line in advice_dict[disease_clean]:
                st.write(line)
        else:
            st.error("No predefined advice available. Please consult a doctor.")
