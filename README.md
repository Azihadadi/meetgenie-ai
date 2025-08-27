# meetgenie-ai

AI-powered Meeting Assistant that automatically transcribes meetings, adjusts financial product terminology, and generates structured meeting minutes along with actionable task lists.

![App Screenshot](sample_audio/app_execution.png)

---

## Features

- **Automatic Speech-to-Text:** Uses Whisper model to transcribe audio meetings.
- **Financial Term Correction:** Adjusts product-related terminology (e.g., "401k" → "401(k) retirement savings plan").
- **Meeting Minutes Generation:** Creates structured summaries of key discussion points and decisions.
- **Task List Extraction:** Identifies actionable items with assignees and deadlines.
- **Web Interface:** Built with Gradio for easy audio upload and output download.
- **LLM Powered:** Leverages IBM Watsonx AI and LangChain for intelligent processing.

---

## Installation

1. **Clone the repository**
```bash
git clone https://github.com/Azihadadi/meetgenie-ai.git
cd meetgenie-ai
```
2. **Create and activate a virtual environment**
```bash
python -m venv my_env
source my_env/bin/activate      # Linux/Mac
my_env\Scripts\activate         # Windows
```
3. **Install dependencies**
```bash
pip install -r requirements.txt
```
4. **Install system requirements**
```bash
sudo apt update
sudo apt install ffmpeg -y
```
---
## Setup
1. IBM Watsonx Credentials

- **Replace `<YOUR_API_KEY>`** in `app.py` with your actual IBM Watsonx API key.
- Alternatively, you can **configure credentials via environment variables** for safety. This avoids committing sensitive information to GitHub.

2. Prompts

- The default prompt is stored in `prompts/meeting_prompt.txt`.
- You can **customize the prompt** to change the meeting minutes format or task extraction behavior.
---
## Usage
Run the app with:

```bash
python app.py
```
- Gradio UI will launch at http://localhost:5000 by default.

- share=True in iface.launch() will provide a temporary public link.

### Steps:

1. Upload a meeting audio file (supported formats: WAV, MP3, etc.).

2. Wait for transcription and processing.

3. View meeting minutes in the text box.

4. Download structured meeting minutes and task list (outputs/meeting_minutes_and_tasks.txt).
