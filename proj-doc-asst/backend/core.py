from dotenv import load_dotenv
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain import hub
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_pinecone import PineconeVectorStore
from ollama import embeddings

load_dotenv()

INDEX_NAME = "langchain-doc-index"


def run_llm(query: str):
    embeddings = OllamaEmbeddings(model="mxbai-embed-large")
    docsearch = PineconeVectorStore(
        index_name=INDEX_NAME, embedding=embeddings)

    chat = ChatOllama(model="mistral")

    retrieval_qa_prompt = hub.pull("langchain-ai/retrieval-qa-chat")

    stuff_documents_chain = create_stuff_documents_chain(
        chat, retrieval_qa_prompt)

    qa_chain = create_retrieval_chain(
        retriever=docsearch.as_retriever(),
        combine_docs_chain=stuff_documents_chain
    )

    result = qa_chain.invoke(input={"input": query})
    return result


if __name__ == "__main__":
    res = run_llm(query="What is a LangChain Chain")
    print(res["context"])
    print("************")
    print(res["answer"])
