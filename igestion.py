import os

from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Pinecone
from langchain.document_loaders import UnstructuredMarkdownLoader
from dotenv import load_dotenv
import os
import fnmatch
import pinecone
from langchain.document_loaders import GitLoader

load_dotenv()

pinecone.init(
    api_key=os.environ["PINECONE_API_KEY"],
    environment=os.environ["PINECONE_ENVIRONMENT_REGION"],
)
INDEX_NAME = "langchain-doc-index"


def find_md_files(root_dir):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in fnmatch.filter(filenames, "*.md"):
            yield os.path.join(dirpath, filename)


def ingest_docs():
    # root_directory = "content"
    # for md_file in find_md_files(root_directory):
    #     print(f"Loading {md_file} to vectorestore")
    loader = GitLoader(repo_path="Polly", branch="main")
    data = loader.load()
    print(len(data))

    # loader = UnstructuredMarkdownLoader(file_path=md_file)
    raw_documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=100, separators=["\n\n", "\n", " ", ""]
    )
    documents = text_splitter.split_documents(raw_documents)
    # for doc in documents:
    #     new_url = doc.metadata["source"]
    #     new_url = new_url.replace("langchain-docs", "https:/")
    #     doc.metadata.update({"source": new_url})

    embeddings = OpenAIEmbeddings()
    print(f"Going to add {len(documents)} to Pinecone")
    Pinecone.from_documents(documents, embeddings, index_name=INDEX_NAME)
    print("***Loading to vectorestore done ***")


if __name__ == "__main__":
    ingest_docs()
