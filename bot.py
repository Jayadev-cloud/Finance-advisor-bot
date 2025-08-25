# pip install streamlit google-generativeai python-dotenv

import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("API_KEY")

# Configure Gemini
genai.configure(api_key=API_KEY)
MODEL_NAME = "gemini-1.5-flash"

# Title
st.set_page_config(page_title="Personal Finance Advisor", page_icon="💰")
st.title("💰 Personal Finance Advisor Chatbot")

# Hidden instruction (NOT stored in UI history)
FINANCE_ONLY_INSTRUCTION = """
You are a financial advisor bot. 
You should only answer questions related to personal finance, budgeting, savings, investments, debt management, retirement, or related money matters. 
If the user asks about anything unrelated (like coding, sports, movies, etc.), respond with:
"Sorry, I can only help with financial topics."
"""

# Initialize chat history (only real conversation here)
if "history" not in st.session_state:
    st.session_state.history = [
        {
            "role": "model",
            "parts": [{"text": "Hello! I'm your personal finance advisor. Tell me about your financial situation or problems, and I’ll suggest solutions."}]
        }
    ]

# Display visible chat history
for msg in st.session_state.history:
    if msg["role"] == "user":
        st.chat_message("user").markdown(msg["parts"][0]["text"])
    elif msg["role"] == "model":
        st.chat_message("assistant").markdown(msg["parts"][0]["text"])

# Chat input
if user_input := st.chat_input("Enter your financial problem..."):
    # Append visible user message
    st.session_state.history.append({"role": "user", "parts": [{"text": user_input}]})
    st.chat_message("user").markdown(user_input)

    # Create model with hidden instruction + history
    model = genai.GenerativeModel(MODEL_NAME)
    chat = model.start_chat(
        history=[{"role": "user", "parts": [{"text": FINANCE_ONLY_INSTRUCTION}]}] + st.session_state.history
    )
    response = chat.send_message(user_input)

    # Append bot reply
    bot_reply = response.text
    st.session_state.history.append({"role": "model", "parts": [{"text": bot_reply}]})

    # Display bot reply
    st.chat_message("assistant").markdown(bot_reply)
