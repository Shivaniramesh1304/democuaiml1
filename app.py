import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

api_key="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"
client=Groq(api_key=api_key)

st.set_page_config(
    page_title="groq AI chatbot",
    page_icon="",
    layout="wide"
)

st.title("groq AI chatbot")
st.write("powered by groq liama models")

st.sidebar.title("settings")
model=st.sidebar.selectbox(
    "choose model",
    [
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant"
    ]
)

temperature=st.sidebar.slider(
    "temperature",
    0.0,
    1.0,
    0.7
)

max_tokens=st.sidebar.slider(
    "max tokens",
    100,
    2048,
    1024
)
if st.sidebar.button("clear chat"):
    st.session_state.messages=[]
if "messages" not in st.session_state:
    st.session_state.messages=[]
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt=st.chat_input("ask anything...")
if prompt:
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("thinking..."):
            response=client.chat.completions.create(
                model=model,
                messages=st.session_state.messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            reply=response.choices[0].message.content
            st.markdown(reply)
    st.session_state.messages.append(
        {
            "role":"assistant",
            "content":reply
        }
    )