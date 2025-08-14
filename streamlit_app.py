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
        white-space: pre-wrap;
        font-family: 'Courier New', monospace;
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
    .chat-box pre {{
        white-space: pre-wrap;
        font-family: monospace;
        overflow-x: auto;
        background-color: rgba(0, 0, 0, 0.05);
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }}
    .input-container {{
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: rgba(255, 255, 255, 0.95);
        padding: 20px;
        border-top: 1px solid #ddd;
        z-index: 1000;
    }}
    .main-content {{
        margin-bottom: 150px;
    }}
    </style>
""", unsafe_allow_html=True)

# --- Title ---
st.markdown("<h1 style='text-align: center;'>🤖 LINA Assistant</h1>", unsafe_allow_html=True)

# --- Initialize Chat History ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Display Messages First ---
st.markdown('<div class="main-content">', unsafe_allow_html=True)
for msg in st.session_state.chat_history:
    role_class = "user" if msg["role"] == "user" else "bot"
    st.markdown(f"""
        <div class="chat-box {role_class}">
            {msg["message"]}
        </div>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- Input Section at Bottom ---
st.markdown('<div class="input-container">', unsafe_allow_html=True)
st.write("Ask LINA any question:")
query = st.text_input("Type your message...", key="user_input", label_visibility="collapsed", placeholder="e.g. Restart NGINX")
send = st.button("Send")
st.markdown('</div>', unsafe_allow_html=True)

# Function to format diagrams
def format_message(message):
    """Format message to handle diagrams and code blocks properly"""
    if isinstance(message, str):
        # Replace code block markers with proper HTML
        message = message.replace("```", "")
        return message
    return message

# --- Send Query ---
if send and query:
    st.session_state.chat_history.append({"role": "user", "message": query})

    try:
        with st.spinner("Thinking..."):
            response = httpx.post(
                FASTAPI_URL,
                json={"query": query},
                timeout=120.0
            )
            response.raise_for_status()
            data = response.json()
            answer = data.get("output", {})
    except Exception as e:
        answer = f"❌ Error: {str(e)}"

    # Format the answer to handle diagrams
    formatted_answer = format_message(answer)
    st.session_state.chat_history.append({"role": "bot", "message": formatted_answer})
    st.rerun()