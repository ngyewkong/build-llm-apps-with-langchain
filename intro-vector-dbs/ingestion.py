import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_ollama import OllamaEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_text_splitters import CharacterTextSplitter
from ollama import embeddings

load_dotenv()

if __name__ == "__main__":
    print("Ingesting...")
    loader = TextLoader(
        "/Users/ngyewkong/build-llm-apps-with-langchain/intro-vector-dbs/medium-blog.txt")
    document = loader.load()

    print("Splitting...")
    text_splitter = CharacterTextSplitter(
        chunk_size=1000, chunk_overlap=0)  # no overlap between chunks

    chunks = text_splitter.split_documents(document)

    print(f"Created {len(chunks)} chunks")

    embeddings = OllamaEmbeddings(
        model="mxbai-embed-large")  # dimension default 1024

    print("ingesting the chunks...")
    PineconeVectorStore.from_documents(
        chunks, embeddings, index_name=os.environ["INDEX_NAME"])
    print("Finish Ingestion...")
