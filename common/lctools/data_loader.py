from langchain.document_loaders import UnstructuredHTMLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


def process_document(file: str):
    loader = UnstructuredHTMLLoader(file)
    return loader.load_and_split(RecursiveCharacterTextSplitter(chunk_size=2000))
