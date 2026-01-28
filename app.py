# app.py
from flask import Flask, render_template, request
import google.generativeai as genai
import re
import os
import sys # New import for printing errors

app = Flask(__name__)

# --- DIAGNOSTIC PRINT ---
# This will print to your Render logs immediately when the app starts
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ CRITICAL ERROR: GEMINI_API_KEY is MISSING.", file=sys.stderr)
else:
    # We print the length to verify it's loaded, but hide the actual key for safety
    print(f"✅ SUCCESS: GEMINI_API_KEY found! Length: {len(api_key)} characters.", file=sys.stderr)
    
    # Check for accidental quotes (Common mistake)
    if api_key.startswith('"') or api_key.startswith("'"):
        print("⚠️ WARNING: Your API key starts with a quote mark. Please remove quotes in Render Environment variables.", file=sys.stderr)

    genai.configure(api_key=api_key)
# ------------------------

def preprocess(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    tokens = text.split()
    return " ".join(tokens)

def call_llm(prompt):
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # This prints the specific Google error to your Render logs
        print(f"❌ GEMINI API ERROR: {e}", file=sys.stderr)
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

