# app.py
from flask import Flask, render_template, request
import google.generativeai as genai
import re

app = Flask(__name__)

# Configure Gemini
import os
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def preprocess(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    tokens = text.split()
    return " ".join(tokens)

def call_llm(prompt):
    model = genai.GenerativeModel("models/gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text

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


