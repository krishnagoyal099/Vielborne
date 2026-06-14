# SHADOWSELF 🌑

SHADOWSELF is an AI-powered narrative card game built with Gradio and Hugging Face's OpenBMB models. Face your inner shadow in a battle of cards, dialogue, and psychological reflections.

## 🛠️ Prerequisites

Before setting up, ensure you have the following installed:
- [Python 3.10+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/)
- A [Hugging Face account](https://huggingface.co/) (to get a free API token)

## 🚀 Setup Instructions

Follow these steps to get the game running on your local machine:

### 1. Clone the Repository
```bash
git clone https://github.com/krishnagoyal099/Vielborne.git
cd Vielborne
```
*(If you already have the code locally, just navigate to the project directory).*

### 2. Create a Virtual Environment
It is highly recommended to use a virtual environment to manage dependencies to avoid conflicts.
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
Install all required Python packages (`gradio`, `huggingface-hub`, `rembg`, etc.).
```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables
The game relies on Hugging Face API, so you need to provide your API token.
1. Get your free access token at: [Hugging Face Settings -> Access Tokens](https://huggingface.co/settings/tokens) (Create a token with `READ` permissions).
2. Copy the `.env.example` file to create a new file named `.env`.
   ```bash
   cp .env.example .env
   # On Windows Command Prompt: copy .env.example .env
   ```
3. Open the `.env` file and replace `hf_your_token_here` with your actual token.

```env
# Example of what your .env should look like:
HF_TOKEN=hf_abc123yourtokenhere
HF_MODEL=openbmb/MiniCPM3-4B
```

### 5. Run the Application
Start the game by running the Gradio app script:
```bash
python app.py
```
Once it starts, you will see a local URL in the console (typically `http://127.0.0.1:7860/`). Open this link in your web browser to start playing!

## 📦 Deployment (Hugging Face Spaces)
If you wish to deploy this game online:
1. Push the code to a new Hugging Face Space as-is.
2. Go to your Space's **Settings** and add `HF_TOKEN` under **Variables and secrets** as a secret.
