import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter

from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_community.vectorstores import FAISS
from ollama import embeddings
from langchain import hub
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

load_dotenv()

if __name__ == "__main__":
    print("Test...")
    pdf_path = "/Users/ngyewkong/build-llm-apps-with-langchain/vector-dbs-in-mem/ReAct.pdf"

    loader = PyPDFLoader(file_path=pdf_path)
    documents = loader.load()
    text_splitter = CharacterTextSplitter(
        chunk_size=1000, chunk_overlap=30, separator="\n")
    docs = text_splitter.split_documents(documents=documents)

    embeddings = OllamaEmbeddings(model="mxbai-embed-large")
    vectorstore = FAISS.from_documents(docs, embedding=embeddings)
    # save local -> to save to local disk for persistence
    vectorstore.save_local("faiss_index_react")

    # to load from local storage (loading the pickle dump)
    new_vectorstore = FAISS.load_local(
        "faiss_index_react", embeddings=embeddings, allow_dangerous_deserialization=True)

    # setup the chains
    retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
    combine_docs_chain = create_stuff_documents_chain(
        ChatOllama(model="mistral"),
        retrieval_qa_chat_prompt
    )

    retrieval_chain = create_retrieval_chain(
        new_vectorstore.as_retriever(),
        combine_docs_chain
    )

    res = retrieval_chain.invoke(
        {"input": "Give me the gist of ReAct in 3 sentences"}
    )

    print(res["answer"])
