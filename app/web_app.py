
import streamlit as st
import requests
from pathlib import Path

# ---------------- APP SETTINGS ----------------

APP_DIR = Path(__file__).parent
LOGO_FILE = APP_DIR / "saniqra_logo.png"

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama-3.3-70b-versatile"

st.set_page_config(
    page_title="SANIQRA AI",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- PROFESSIONAL DESIGN ----------------

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

[data-testid="stChatMessage"] {
    background: #151f35 !important;
    border: 1px solid #303e5c;
    border-radius: 18px;
    padding: 16px;
    margin-bottom: 14px;
}

[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li,
[data-testid="stChatMessage"] div {
    color: #f8fafc !important;
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
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #64748b !important;
    -webkit-text-fill-color: #64748b !important;
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

hr {
    border-color: #303b58;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION CHAT MEMORY ----------------

if "messages" not in st.session_state:
    st.session_state.messages = []

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
    st.caption("Powered by Groq Cloud")
    st.caption("Model: Llama 3.3 70B")
    st.caption("Version 2.1")

# ---------------- MAIN HEADER ----------------

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    if LOGO_FILE.exists():
        st.image(str(LOGO_FILE), width=180)
    else:
        st.markdown("# ✦ SANIQRA AI")

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

# ---------------- DISPLAY OLD MESSAGES ----------------

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

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):

        with st.spinner("SANIQRA is thinking..."):

            try:

                api_key = st.secrets["GROQ_API_KEY"]

                system_message = {
                    "role": "system",
                    "content": """
You are SANIQRA AI, a personal AI assistant created by Sanika Hajare.

Your identity:
- Your name is SANIQRA AI.
- Your creator is Sanika Hajare.
- You are powered by Groq Cloud AI.
- Your underlying model is Llama 3.3 70B.
- Never claim that your assistant name is Llama.

Your responsibilities:
- Help with education and exam preparation.
- Explain coding step by step.
- Help with AI, Machine Learning and technology.
- Assist with projects and daily tasks.
- Use simple, friendly language.
- Give beginner-friendly explanations.
- Support Hindi, Marathi and English.
"""
                }

                response = requests.post(
                    GROQ_API_URL,
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": GROQ_MODEL,
                        "messages": [
                            system_message
                        ] + st.session_state.messages,
                        "temperature": 0.7
                    },
                    timeout=60
                )

                response.raise_for_status()

                answer = response.json()["choices"][0]["message"]["content"]

            except KeyError:
                answer = (
                    "Groq API key missing. "
                    "Please check Streamlit Cloud Secrets."
                )

            except requests.exceptions.HTTPError:
                try:
                    error_details = response.json().get(
                        "error", {}
                    ).get("message", response.text)
                except ValueError:
                    error_details = response.text

                answer = (
                    f"Groq Error {response.status_code}: "
                    f"{error_details[:500]}"
                )

            except requests.exceptions.RequestException:
                answer = (
                    "Cloud AI connection problem. "
                    "Please try again."
                )

            except (ValueError, TypeError, IndexError):
                answer = "Sorry, response read karne mein problem hui."

            st.markdown(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })
