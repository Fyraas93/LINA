import streamlit as st
import httpx
from PIL import Image
import base64

# Load and encode the LINA logo as background
def get_base64_bg(file_path):
    with open(file_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

lina_bg = get_base64_bg("lina_logo.jpg")

FASTAPI_URL = "http://localhost:8000/query"

# --- Custom Styling ---
st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{lina_bg}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    .chat-box {{
        background-color: #f9f9f9cc;
        border-radius: 10px;
        padding: 1em;
        margin-bottom: 1em;
        width: fit-content;
        max-width: 80%;
        clear: both;
    }}
    .user {{
        float: right;
        background-color: #d4e3fc;
        color: #000;
    }}
    .bot {{
        float: left;
        background-color: #ffc480;
        color: #000;
    }}
    </style>
""", unsafe_allow_html=True)

# --- Title ---
st.markdown("<h1 style='text-align: center;'>🤖 LINA Assistant</h1>", unsafe_allow_html=True)
st.write("Ask LINA any question:")

# --- Initialize Chat History ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Input ---
query = st.text_input("Type your message...", key="user_input", label_visibility="collapsed", placeholder="e.g. Restart NGINX")
send = st.button("Send")

# --- Send Query ---
if send and query:
    st.session_state.chat_history.append({"role": "user", "message": query})

    try:
        with st.spinner("Thinking..."):
            response = httpx.post(
                FASTAPI_URL,
                json={"query": query},
                timeout=60.0
            )
            response.raise_for_status()
            data = response.json()
            answer = data.get("output", {})
    except Exception as e:
        answer = f"❌ Error: {str(e)}"

    st.session_state.chat_history.append({"role": "bot", "message": answer})

# --- Display Messages ---
for msg in st.session_state.chat_history:
    role_class = "user" if msg["role"] == "user" else "bot"
    st.markdown(f"""
        <div class="chat-box {role_class}">
            {msg["message"]}
        </div>
    """, unsafe_allow_html=True)
