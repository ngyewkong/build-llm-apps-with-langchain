from dotenv import load_dotenv
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain import hub
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_pinecone import PineconeVectorStore
from ollama import embeddings
from typing import List, Dict, Any
from langchain.chains.history_aware_retriever import create_history_aware_retriever

load_dotenv()

INDEX_NAME = "langchain-doc-index"


def run_llm(query: str, chat_history: List[Dict[str, Any]] = []):
    embeddings = OllamaEmbeddings(model="mxbai-embed-large")
    docsearch = PineconeVectorStore(
        index_name=INDEX_NAME, embedding=embeddings)

    chat = ChatOllama(model="deepseek-r1")

    retrieval_qa_prompt = hub.pull("langchain-ai/retrieval-qa-chat")

    stuff_documents_chain = create_stuff_documents_chain(
        chat, retrieval_qa_prompt)

    # chat_history is to add memory to the llm
    # need a rephrase prompt (follow up)
    rephrase_prompt = hub.pull("langchain-ai/chat-langchain-rephrase")

    # use the history_aware_retriever (built-in with langchain)
    history_aware_retriever = create_history_aware_retriever(
        llm=chat, retriever=docsearch.as_retriever(), prompt=rephrase_prompt
    )

    qa_chain = create_retrieval_chain(
        retriever=history_aware_retriever,
        combine_docs_chain=stuff_documents_chain
    )

    result = qa_chain.invoke(
        input={"input": query, "chat_history": chat_history}
    )

    # to match streamlit
    new_result = {
        "query": result["input"],
        "result": result["answer"],
        "source_documents": result["context"]
    }
    return new_result


if __name__ == "__main__":
    res = run_llm(query="What is a LangChain Chain")
    print(res["source_documents"])
    print("************")
    print(res["result"])
