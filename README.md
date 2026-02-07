
# Sahay: The Multimodal Electronics Repair Agent

## 📖 Overview

Sahay is an intelligent **Hardware Repair Agent** designed to bridge the gap between complex engineering manuals and real-world troubleshooting. Using **Gemini 3’s multimodal reasoning**, it identifies electronic components from live video or photos and provides step-by-step repair guidance grounded in actual technical datasheets.

## ✨ Key Features

* **Multimodal Diagnosis**: Instantly identify ICs, resistors (including color codes), and common PCB faults via camera.
* **Agentic Tool-Use**: Autonomously searches for replacement parts on local Indian stores and calculates circuit parameters using built-in Python tools.
* **1.5M Context Awareness**: Leverages a massive context window to "read" and apply knowledge from high-resolution PDF manuals and engineering textbooks.
* **Live Safety Audits**: Real-time alerts for high-voltage hazards and proper PPE requirements before starting a repair.

## 🚀 Installation & Local Setup

To run Sahay locally on your machine:

1. **Clone the repository**:
```bash
git clone https://github.com/your-username/Sahay-Repair-Agent.git
cd Sahay-Repair-Agent

```


2. **Install dependencies**:
```bash
pip install -r requirements.txt

```


3. **Set your API Key**:
Create a `.env` file or export your key:
```bash
export GOOGLE_API_KEY="your_api_key_here"

```


4. **Run the app**:
```bash
streamlit run app.py

```



## 🛠️ Tech Stack

* **Language**: Python 3.9+
* **AI Model**: Google Gemini 3 Pro (Multimodal)
* **Framework**: Streamlit
* **Orchestration**: Google Antigravity (Agentic Workflows)
* **Libraries**: `google-genai`, `Pillow`, `NumPy`

## 🗂️ Repository Structure

* `app.py`: Main Streamlit application and agent logic.
* `requirements.txt`: List of required Python libraries.
* `manuals/`: PDF technical datasheets used for RAG (Retrieval-Augmented Generation).
* `assets/`: Demo images and project logo.

