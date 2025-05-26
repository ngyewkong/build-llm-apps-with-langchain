from langchain_pinecone import PineconeVectorStore
from langchain_ollama import OllamaEmbeddings
from langchain_community.document_loaders import ReadTheDocsLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from ollama import embeddings

load_dotenv()


embeddings = OllamaEmbeddings(model="mxbai-embed-large")


def ingest_docs():
    loader = ReadTheDocsLoader(
        "proj-doc-asst/langchain-docs/api.python.langchain.com/en/latest"
    )
    raw_docs = loader.load()
    print(f"Loaded {len(raw_docs)} documents...")

    # text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=600, chunk_overlap=50
    )

    documents = text_splitter.split_documents(raw_docs)

    # update doc metdata to actual url
    for doc in documents:
        new_url = doc.metadata["source"]
        new_url = new_url.replace("projec-doc-asst/langchain-docs", "https:/")
        doc.metadata.update({"source": new_url})

    print(f"Going to add {len(documents)} to Pinecone...")

    # # convert to vectors in Pinecone
    # PineconeVectorStore.from_documents(
    #     documents=documents, embedding=embeddings, index_name="langchain-doc-index"
    # )
    vectorstore = PineconeVectorStore(
        embedding=embeddings,
        index_name="langchain-doc-index"
    )

    # message length too large (handle by batching)
    batch_size = 100

    for i in range(0, len(documents), batch_size):
        batch = documents[i: i+batch_size]
        vectorstore.add_documents(batch)
        print(f"Uploaded batch {i} with {len(documents)}")

    print(f"***** Upload to Pinecone Completed *****")


if __name__ == "__main__":
    ingest_docs()
