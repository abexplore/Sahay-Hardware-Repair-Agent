import os
import streamlit as st
from PIL import Image
from google import genai
from google.genai import types

# 1. Setup Page and API Key
st.set_page_config(page_title="Sahay: Hardware Agent", layout="wide")
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.error("API Key missing! Add GEMINI_API_KEY to your Secrets.")
    st.stop()

client = genai.Client(api_key=api_key)

# 2. UI for File Upload
st.title("SAHAY: Electronics Repair Agent")
uploaded_file = st.file_uploader("Upload a photo of the PCB or component", type=["jpg", "png", "jpeg"])

if uploaded_file:
    # Display the image for the user
    img = Image.open(uploaded_file)
    st.image(img, caption="Target Hardware", width=400)

    if st.button("Analyze & Diagnose"):
        # 3. Model Configuration (Keeping your Thinking setup)
        model_id = "gemini-2.0-flash" # Use stable name for API
        
        tools = [types.Tool(googleSearch=types.GoogleSearch())]
        
        generate_content_config = types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(
                include_thoughts=True, # Shows the AI's reasoning process
            ),
            tools=tools,
        )

        # 4. Preparing Multimodal Content
        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text="Analyze this PCB. Identify components, check for damage, and suggest repair steps using engineering math."),
                    img # The PIL Image object is passed directly here
                ],
            ),
        ]

        with st.spinner("Sahay is reasoning..."):
            try:
                # 5. Generate Response (Streaming for real-time thoughts)
                response_container = st.empty()
                full_text = ""
                
                for chunk in client.models.generate_content_stream(
                    model=model_id,
                    contents=contents,
                    config=generate_content_config,
                ):
                    for part in chunk.candidates[0].content.parts:
                        if part.thought:
                            st.info(f"AI Thinking: {part.text}")
                        elif part.text:
                            full_text += part.text
                            response_container.markdown(full_text)
                            
            except Exception as e:
                st.error(f"Analysis failed: {e}")
