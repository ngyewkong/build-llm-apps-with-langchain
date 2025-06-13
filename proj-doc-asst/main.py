import streamlit as st
import time
from backend.core import run_llm

st.header("LangChain Document Helper using RAG")
prompt = st.text_input("Prompt", placeholder="Enter your prompt here..")

# session state in streamlit
# # initialise the streamlit session for history awareness
# if "user_prompt_history" not in st.session_state:
#     st.session_state["user_prompt_history"] = []

# if "chat_answers_history" not in st.session_state:
#     st.session_state["chat_answers_history"] = []

# impl chat assistant memory
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
    # spinner icon when executing
    with st.spinner("Generating response..."):
        generated_res = run_llm(
            query=prompt, chat_history=st.session_state["chat_history"]
        )
        sources = set(
            [doc.metadata["source"]
                for doc in generated_res["source_documents"]]
        )

        formatted_res = (
            f"{generated_res['result']} \n\n {create_sources_string(sources)}")

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
        # output to browser
        st.chat_message("user").write(user_query)
        st.chat_message("assistant").write(generated_res)
