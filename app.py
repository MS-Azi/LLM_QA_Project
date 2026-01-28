# app.py
from flask import Flask, render_template, request
import google.generativeai as genai
import re
import os
import sys

app = Flask(__name__)

# --- CONFIGURATION ---
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("❌ CRITICAL ERROR: GEMINI_API_KEY is MISSING.", file=sys.stderr)
else:
    genai.configure(api_key=api_key)

# --- AUTO-DETECT MODEL FUNCTION ---
def get_working_model():
    """
    Asks Google which models are available and picks the first one 
    that supports text generation.
    """
    try:
        print("🔍 Checking available models...", file=sys.stderr)
        for m in genai.list_models():
            # We look for models that support 'generateContent'
            if 'generateContent' in m.supported_generation_methods:
                print(f"✅ Found valid model: {m.name}", file=sys.stderr)
                # Return the model name (clean it up just in case)
                return m.name
    except Exception as e:
        print(f"⚠️ Error listing models: {e}", file=sys.stderr)
    
    # Fallback if auto-detection fails
    return "gemini-1.5-flash"

# Global variable to store the best model name
CURRENT_MODEL_NAME = get_working_model()
print(f"🚀 APP STARTED using model: {CURRENT_MODEL_NAME}", file=sys.stderr)
# ----------------------------------

def preprocess(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    tokens = text.split()
    return " ".join(tokens)

def call_llm(prompt):
    try:
        # Use the auto-detected model name
        model = genai.GenerativeModel(CURRENT_MODEL_NAME)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"❌ GENERATION ERROR with {CURRENT_MODEL_NAME}: {e}", file=sys.stderr)
        return "Error calling AI. Please check server logs."

@app.route("/", methods=["GET", "POST"])
def index():
    processed = None
    answer = None

    if request.method == "POST":
        question = request.form["question"]
        processed = preprocess(question)
        final_prompt = f"Answer this question clearly: {processed}"
        answer = call_llm(final_prompt)

        return render_template(
            "index.html",
            question=question,
            processed=processed,
            answer=answer
        )

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
