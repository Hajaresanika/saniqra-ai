
import streamlit as st
import requests
import json
from pathlib import Path
APP_DIR = Path(__file__).parent
HISTORY_FILE = APP_DIR / "chat_history.json"

MODEL = "qwen2.5:0.5b"
API_URL = "http://localhost:11434/api/chat"

st.set_page_config(
    page_title="SANIQRA AI",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- CUSTOM PROFESSIONAL DESIGN ----------------

st.markdown("""
<style>
.stApp {
    background: #0b1020;
    color: #f1f5f9;
}

[data-testid="stSidebar"] {
    background: #11182b;
    border-right: 1px solid #303b58;
}

[data-testid="stSidebar"] * {
    color: #e2e8f0;
}

.main .block-container {
    max-width: 1050px;
    padding-top: 2rem;
    padding-bottom: 5rem;
}

.brand-title {
    font-size: 34px;
    font-weight: 800;
    letter-spacing: 2px;
    color: #f8fafc;
}

.brand-title span {
    color: #a78bfa;
}

.tagline {
    color: #a5b4cc;
    font-size: 13px;
    letter-spacing: 2px;
    margin-top: 5px;
}

.logo-wrap {
    display: flex;
    align-items: center;
    gap: 15px;
}

.welcome {
    text-align: center;
    padding: 95px 10px 45px 10px;
}

.welcome h1 {
    color: #f8fafc;
    font-size: 38px;
    font-weight: 750;
}

.welcome p {
    color: #a5b4cc;
    font-size: 16px;
}

[data-testid="stChatMessage"] {
    background: #151f35;
    border: 1px solid #303e5c;
    border-radius: 18px;
    padding: 16px;
    margin-bottom: 14px;
}

[data-testid="stChatInput"] {
    background: #f8fafc !important;
    border: 2px solid #8b5cf6 !important;
    border-radius: 16px !important;
}

[data-testid="stChatInput"] textarea {
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
    caret-color: #7c3aed !important;
    background: transparent !important;
    opacity: 1 !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #64748b !important;
    -webkit-text-fill-color: #64748b !important;
    opacity: 1 !important;
}

.stButton button {
    background: linear-gradient(90deg, #7c3aed, #9333ea);
    color: white;
    border: none;
    border-radius: 12px;
    font-weight: 600;
    padding: 10px;
}

.stButton button:hover {
    background: #6d28d9;
    color: white;
    border: 1px solid #c4b5fd;
}
/* AI ANSWER VISIBILITY */
[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li,
[data-testid="stChatMessage"] div,
.stMarkdown p {
    color: #f8fafc !important;
}

/* Chat message readable background */
[data-testid="stChatMessage"] {
    background: #151f35 !important;
    color: #ffffff !important;
}
hr {
    border-color: #303b58;
}

</style>
""", unsafe_allow_html=True)


# ---------------- S + LOTUS LOGO ----------------

logo = """
<svg width="76" height="76" viewBox="0 0 100 100"
xmlns="http://www.w3.org/2000/svg">
<defs>
  <linearGradient id="silver" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#ffffff"/>
    <stop offset="50%" stop-color="#c4b5fd"/>
    <stop offset="100%" stop-color="#8b5cf6"/>
  </linearGradient>
</defs>

<!-- Lotus petals -->
<path d="M50 8 C35 22 35 36 50 45 C65 36 65 22 50 8Z"
fill="url(#silver)" stroke="#c4b5fd" stroke-width="1"/>

<path d="M48 42 C24 23 12 36 29 52 C37 57 44 53 48 42Z"
fill="#8b5cf6" stroke="#c4b5fd" stroke-width="1"/>

<path d="M52 42 C76 23 88 36 71 52 C63 57 56 53 52 42Z"
fill="#8b5cf6" stroke="#c4b5fd" stroke-width="1"/>

<path d="M30 53 Q50 72 70 53 Q64 75 50 80 Q36 75 30 53Z"
fill="#6d28d9" stroke="#c4b5fd" stroke-width="1"/>

<!-- S symbol -->
<text x="50" y="66" text-anchor="middle"
font-family="Georgia,serif" font-size="39"
font-weight="bold" fill="#ffffff">S</text>
</svg>
"""

# ---------------- PERMANENT CHAT MEMORY ----------------

def load_history():
    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)

            messages = []

            if not isinstance(data, list):
                return []

            for item in data:
                if not isinstance(item, dict):
                    continue

                # Old format: question and answer
                if "question" in item and "answer" in item:
                    messages.append({
                        "role": "user",
                        "content": item["question"]
                    })
                    messages.append({
                        "role": "assistant",
                        "content": item["answer"]
                    })

                # New format: role and content
                elif "role" in item and "content" in item:
                    messages.append(item)

            return messages

        except (json.JSONDecodeError, OSError):
            return []

    return []


def save_history():
    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(
            st.session_state.messages,
            file,
            indent=4,
            ensure_ascii=False
        )


if "messages" not in st.session_state:
    st.session_state.messages = load_history()

# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.markdown("## ✦ SANIQRA AI")
    st.caption("Intelligence Beyond Limits")

    st.divider()

    if st.button("＋ New Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown("### Chat History")

    if not st.session_state.messages:
        st.caption("Your conversations will appear here.")
    else:
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.caption("👤 " + msg["content"][:40])

    st.divider()

    st.caption("PERSONAL AI ASSISTANT")
    st.caption("Powered by Ollama")
    st.caption("Model: qwen2.5:0.5b")
    st.caption("Version 1.0")


# ---------------- MAIN HEADER ----------------

# ---------------- MAIN HEADER ----------------


# ---------------- MAIN HEADER ----------------


# ---------------- MAIN HEADER ----------------

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.image("app/saniqra_logo.png", width=180)
    st.divider()




# ---------------- WELCOME SCREEN ----------------

if not st.session_state.messages:

    st.markdown("""
    <div class="welcome">
        <h1>Welcome to SANIQRA AI ✨</h1>
        <p>Your personal intelligent assistant is ready.</p>
        <p>Ask anything. Learn anything. Create anything.</p>
    </div>
    """, unsafe_allow_html=True)


# ---------------- DISPLAY MESSAGES ----------------

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# ---------------- CHAT INPUT ----------------

question = st.chat_input("Message SANIQRA AI...")

if question:

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })
    save_history()

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):

        with st.spinner("SANIQRA is thinking..."):

            try:

                response = requests.post(
                    API_URL,
                    json={
                        "model": MODEL,
                        "messages": [
    {
        "role": "system",
        "content": """
You are SANIQRA AI, a personal AI assistant created by Sanika Hajare.

Your identity:
- Your name is SANIQRA AI.
- Your creator is Sanika Hajare.
- You are powered by the Qwen2.5 AI model developed by Alibaba Cloud.
- Never claim that your assistant name is Qwen.
- If asked about your underlying model, answer honestly that you use Qwen2.5.

Help users with education, coding, technology and daily tasks.
Use simple, friendly language.
"""
    }
] + st.session_state.messages,
                        "stream": False
                    },
                    timeout=180
                )

                response.raise_for_status()

                answer = response.json()["message"]["content"]

            except requests.exceptions.RequestException:

                answer = (
                    "Ollama connection nahi ho raha. "
                    "Please check if Ollama is running."
                )

            except (KeyError, ValueError):

                answer = "Sorry, response read karne mein problem hui."

            st.markdown(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })
    save_history()
