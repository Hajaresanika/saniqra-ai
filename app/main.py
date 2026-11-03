
import requests
import json
import os
print("=" * 45)
print("          WELCOME TO SANIQRA AI")
print("=" * 45)

print("Hello! I am SANIQRA AI.")
print("Your Personal AI Assistant")
print("Intelligence Beyond Limits.")
print("=" * 45)

MODEL = "qwen2.5:0.5b"
HISTORY_FILE = os.path.join(
    os.path.dirname(__file__),
    "chat_history.json"
)


if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "r", encoding="utf-8") as file:
        chat_history = json.load(file)
else:
    chat_history = []


def save_chat(question, answer):
    chat_history.append({
        "question": question,
        "answer": answer
    })

    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(chat_history, file, indent=4, ensure_ascii=False)


while True:
    question = input("\nYou: ").strip()

    if not question:
        print("SANIQRA: Please enter a question.")
        continue

    if question.lower() in ["exit", "quit", "bye"]:
        print("\nSANIQRA: Goodbye! See you again.")
        break

    # SANIQRA AI identity control
    identity_questions = [
        "who are you",
        "your name",
        "what is your name",
        "tum kaun ho",
        "aap kaun ho",
        "who created you"
    ]

    if any(word in question.lower() for word in identity_questions):
        print(
            "\nSANIQRA: I am SANIQRA AI, "
            "your personal AI assistant created by Sanika Hajare."
        )
        continue

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": MODEL,
                "system": """
You are SANIQRA AI, a helpful personal AI assistant.
Your creator is Sanika Hajare.
Help with coding, education, technology and daily tasks.
Use simple and friendly language.
""",
                "prompt": question,
                "stream": False
            },
            timeout=120
        )

        response.raise_for_status()

        answer = response.json().get(
            "response",
            "Sorry, I could not generate an answer."
        )

        print("\nSANIQRA:", answer)
        save_chat(question, answer)
    except requests.exceptions.ConnectionError:
        print("\nSANIQRA: Ollama is not running. Please start Ollama.")

    except requests.exceptions.Timeout:
        print("\nSANIQRA: Response is taking too long. Try again.")

    except requests.exceptions.RequestException as error:
        print("\nSANIQRA: Something went wrong:", error)
