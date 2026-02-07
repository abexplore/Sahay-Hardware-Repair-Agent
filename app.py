import streamlit as st
import os
import io
from PIL import Image
from google import genai
from google.genai import types

# 1. Page Configuration
st.set_page_config(page_title="Sahay: Hardware Repair Agent", layout="wide")
st.title("SAHAY: Electronics & Hardware Repair Agent")

# 2. Secure API Key Retrieval
# Ensure you have GEMINI_API_KEY in your Streamlit Secrets
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.error("API Key missing! Please add 'GEMINI_API_KEY' to your Streamlit Secrets.")
    st.stop()

# Initialize the Gemini Client
client = genai.Client(api_key=api_key)

# 3. Sidebar for Manuals (Knowledge Base)
st.sidebar.header("📚 Technical Knowledge")
manual_file = st.sidebar.file_uploader("Upload Component Datasheet (PDF)", type="pdf")

# 4. Main Interface for Diagnosis
st.header("📸 Hardware Diagnosis")
uploaded_image = st.file_uploader("Upload a clear photo of the PCB or component", type=["jpg", "png", "jpeg"])

if uploaded_image:
    # Display the uploaded image
    img = Image.open(uploaded_image)
    st.image(img, caption="Hardware to be analyzed", width=500)

    if st.button("Start AI Analysis"):
        with st.spinner("Sahay is examining the hardware..."):
            try:
                # --- PREPARE MULTIMODAL CONTENT ---
                parts = [
                    types.Part.from_text(text="""You are SAHAY, a hardware repair expert. 
                    1. Identify components in this image.
                    2. Diagnose potential faults (burnt traces, damage).
                    3. If a manual is provided, use it to give precise pinout/spec details.
                    4. Use LaTeX for all engineering math.""")
                ]

                # Process Image to Bytes
                img_byte_arr = io.BytesIO()
                img.save(img_byte_arr, format='JPEG')
                parts.append(types.Part.from_bytes(data=img_byte_arr.getvalue(), mime_type="image/jpeg"))

                # Process PDF Manual to Bytes if available
                if manual_file:
                    manual_bytes = manual_file.read()
                    parts.append(types.Part.from_bytes(data=manual_bytes, mime_type="application/pdf"))

                # --- GENERATE CONTENT ---
                # We use gemini-2.0-flash for high-speed multimodal reasoning
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=[types.Content(role="user", parts=parts)],
                    config=types.GenerateContentConfig(
                        thinking_config=types.ThinkingConfig(include_thoughts=True),
                        tools=[types.Tool(googleSearch=types.GoogleSearch())]
                    )
                )

                # --- DISPLAY RESULTS ---
                st.subheader("🛠️ Sahay's Diagnosis")
                st.markdown(response.text)

            except Exception as e:
                st.error(f"Analysis failed: {e}")
