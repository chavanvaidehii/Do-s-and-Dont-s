from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
import google.generativeai as genai

# Configure API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Gemini model
model_name = "models/gemini-2.5-pro"
model = genai.GenerativeModel(model_name)

# Predefined advice for fallback
advice_dict = {
    "normal": [
        "✅ Maintain a balanced diet and regular exercise",
        "✅ Get enough sleep (7-8 hours)",
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

# Input
disease_name = st.text_input(
    "Enter the disease predicted from X-ray (e.g., Viral Pneumonia, Tuberculosis, Normal,etc):"
)

if st.button("Generate DOs and DON'Ts"):
    disease_clean = disease_name.lower().strip()

    if not disease_clean:
        st.warning("⚠️ Please enter a disease name.")
    else:
        # Build prompt for API
        prompt = f"""
You are a responsible AI health assistant.
Provide exactly 3 short, clear, medically appropriate *Do’s* and *Don’ts* for {disease_name}:
- Plain-language bullet points (<=20 words each)
- Focus on lifestyle, hygiene, rest, diet, prevention
- Avoid medicine names or treatments
- Include one short safety note to consult a qualified doctor
"""
        try:
            # Initialize cache
            if 'cache' not in st.session_state:
                st.session_state.cache = {}

            # Use cached response if available
            if disease_clean not in st.session_state.cache:
                response = model.generate_content(prompt)
                st.session_state.cache[disease_clean] = response.text

            st.subheader("🧾 AI Recommendations (via Gemini API):")
            st.write(st.session_state.cache[disease_clean])

        except Exception:
            # API failed — fallback to predefined advice
            st.warning("⚠️ API quota exceeded or error occurred. Showing predefined advice.")
            if disease_clean in advice_dict:
                st.subheader("🧾 Recommendations (Fallback):")
                for line in advice_dict[disease_clean]:
                    st.write(line)
            else:
                st.error("No predefined advice available. Please consult a doctor.")
