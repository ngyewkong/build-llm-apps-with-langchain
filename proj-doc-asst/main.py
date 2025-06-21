import streamlit as st
import time
from backend.core import run_llm

# LangChain color theme (based on docs)
PRIMARY_COLOR = "#3b5fc1"
SECONDARY_COLOR = "#f7fafc"
ACCENT_COLOR = "#f9c846"
DARK_BG = "#222831"
DARK_TEXT = "#f7fafc"

st.set_page_config(
    page_title="LangChain Document Helper",
    page_icon="🦜",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Detect dark mode using Streamlit theme
theme = st.get_option("theme.base")
is_dark = theme == "dark"

sidebar_bg = DARK_BG if is_dark else SECONDARY_COLOR
sidebar_text = DARK_TEXT if is_dark else PRIMARY_COLOR

with st.sidebar:
    st.markdown(
        f"""
        <div style="text-align:center;background-color:{sidebar_bg};padding:1.5rem 0 1rem 0;border-radius:10px;">
            <img src="https://randomuser.me/api/portraits/men/32.jpg" alt="Profile" style="border-radius:50%;width:100px;height:100px;border:4px solid {ACCENT_COLOR};margin-bottom:1rem;">
            <h3 style="color:{ACCENT_COLOR};margin-bottom:0.2rem;">John Doe</h3>
            <p style="color:{DARK_TEXT if is_dark else '#444'};margin-top:0;font-size:0.95rem;">johndoe@email.com</p>
        </div>
        <hr style="border:1px solid {ACCENT_COLOR};margin:1.5rem 0;">
        <div style="color:{sidebar_text};">
            <b>Instructions:</b>
            <ul>
                <li>Enter your prompt in the main window.</li>
                <li>Get answers with sources from your documents.</li>
            </ul>
        </div>
        <span style="color:{ACCENT_COLOR};font-size:0.9rem;">Powered by LangChain & Streamlit</span>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    f"<h1 style='color:{PRIMARY_COLOR if not is_dark else ACCENT_COLOR};margin-bottom:0.5rem;'>LangChain Document Helper using RAG</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    f"<p style='color:{PRIMARY_COLOR if not is_dark else DARK_TEXT};font-size:1.1rem;'>Ask questions about your documents and get answers with sources.</p>",
    unsafe_allow_html=True,
)

prompt = st.text_input("Prompt", placeholder="Enter your prompt here...")

if (
    "chat_answers_history" not in st.session_state
    and "user_prompt_history" not in st.session_state
    and "chat_history" not in st.session_state
):
    st.session_state["chat_answers_history"] = []
    st.session_state["user_prompt_history"] = []
    st.session_state["chat_history"] = []


def create_sources_string(source_urls: set[str]) -> str:
    if not source_urls:
        return ""
    sources_list = list(source_urls)
    sources_list.sort()
    sources_string = "sources:\n"
    for i, source in enumerate(sources_list):
        sources_string += f"- {source}\n"
    return sources_string


if prompt:
    with st.spinner("Generating response..."):
        generated_res = run_llm(
            query=prompt, chat_history=st.session_state["chat_history"]
        )
        sources = set(
            [doc.metadata["source"]
                for doc in generated_res["source_documents"]]
        )
        formatted_res = (
            f"{generated_res['result']} \n\n {create_sources_string(sources)}"
        )
        st.session_state["user_prompt_history"].append(prompt)
        st.session_state["chat_answers_history"].append(formatted_res)
        st.session_state["chat_history"].append(("human", prompt))
        st.session_state["chat_history"].append(
            ("ai", generated_res["result"]))

if st.session_state["chat_answers_history"]:
    for generated_res, user_query in zip(
        st.session_state["chat_answers_history"],
        st.session_state["user_prompt_history"],
    ):
        st.chat_message("user").write(user_query)
        st.chat_message("assistant").write(
            f"<div style='background-color:{SECONDARY_COLOR if not is_dark else DARK_BG};padding:1rem;border-radius:8px;color:{'#222' if not is_dark else DARK_TEXT};'>{generated_res}</div>",
            unsafe_allow_html=True,
        )
