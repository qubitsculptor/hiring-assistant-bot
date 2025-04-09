import requests
from prompts import build_prompt

def get_technical_questions(tech_stack):
    prompt = build_prompt(tech_stack)

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "llama2", "prompt": prompt, "stream": False}
        )
        text = response.json().get("response", "")
        lines = text.strip().split("\n")

        questions = []
        for line in lines:
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith("-")):
                q = line.lstrip("0123456789.- ").strip()
                if q:
                    questions.append(q)
        if not questions:
            raise ValueError("No valid questions parsed.")
        return questions[:5]

    except Exception as e:
        print("Error fetching questions:", e)
        return [
            "Explain how you would preprocess data for a machine learning model.",
            "What’s the difference between supervised and unsupervised learning?",
            "How do you prevent overfitting in deep learning models?",
            "Can you explain gradient descent in simple terms?",
            "How would you handle missing data in a dataset?"
        ]
