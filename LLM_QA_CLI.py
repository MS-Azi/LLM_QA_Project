# LLM_QA_CLI.py
import re
import google.generativeai as genai

import os
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def preprocess(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    tokens = text.split()
    return " ".join(tokens)

def ask_llm(prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text

print("=== NLP Question-and-Answering CLI (Gemini) ===")
print("Type 'exit' to quit.\n")

while True:
    question = input("Enter your question: ").strip()
    if question.lower() == "exit":
        break

    processed = preprocess(question)
    print(f"\nProcessed Question: {processed}")

    final_prompt = f"Answer this question clearly: {processed}"
    answer = ask_llm(final_prompt)

    print(f"\nGemini Answer: {answer}\n")

