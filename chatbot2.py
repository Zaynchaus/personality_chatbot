import os

import streamlit as st
from openai import OpenAI

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- Page Configuration ---
def chat_ui():
    st.set_page_config(
        page_title="AI Personality Chatbot",
        page_icon="🤖",
        layout="wide"
    )

    # --- Sidebar Configuration ---
    with st.sidebar:
        st.title(" Configuration")

        st.info("Using GROQ API (Environment variable: GROQ_API_KEY)")

        api_key = os.getenv("GROQ_API_KEY")
        if api_key:
            st.success("Groq API Key loaded from environment")
        else:
            st.error("Missing GROQ_API_KEY in environment. Please set it before running.")

        st.divider()

        personalities = {
            "Helpful Assistant": "You are a helpful, polite, and concise AI assistant.",
            "Pirate": "You are a salty pirate captain. Speak in pirate slang (Ahoy, Matey, Arrgh). Be adventurous and slightly rude but helpful.",
            "Sarcastic Tech Support": "You are a bored, sarcastic tech support agent. You help, but you complain about it and make snarky comments.",
            "Shakespearean Poet": "You speak in Shakespearean English, using thee, thou, and rhyming couplets where possible.",
            "Motivational Coach": "You are a high-energy motivational coach. Use lots of exclamation marks, emojis, and encouraging words. YOU CAN DO IT!"
        }

        selected_personality = st.selectbox(
            "Choose Personality",
            list(personalities.keys())
        )

        system_instruction = personalities[selected_personality]

        st.divider()

        if st.button("Clear Chat History"):
            st.session_state.messages = []
            st.rerun()

    # --- Main Chat UI ---
    st.title(f"🤖 Chat with: {selected_personality}")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Process user message
    if prompt := st.chat_input("What is on your mind?"):

        if not api_key:
            st.error("GROQ_API_KEY missing from environment.")
            st.stop()

        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            placeholder = st.empty()
            full_response = ""

            try:
                client = OpenAI(
                    api_key=api_key,
                    base_url="https://api.groq.com/openai/v1"
                )

                # Build Groq message list
                groq_messages = [{"role": "system", "content": system_instruction}]
                for msg in st.session_state.messages:
                    groq_messages.append(msg)

                # Stream Groq response
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=groq_messages,
                    stream=True
                )

                for chunk in response:
                    delta = chunk.choices[0].delta
                    if delta and delta.content:
                        full_response += delta.content
                        placeholder.markdown(full_response + "▌")

                placeholder.markdown(full_response)

                st.session_state.messages.append(
                    {"role": "assistant", "content": full_response}
                )

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

chat_ui()