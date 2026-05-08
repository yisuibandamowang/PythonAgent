from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

loader = TextLoader(
    file_path="./data/a.txt",
    encoding="utf-8",
)
docs = loader.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n\n", "\n", " ", "",".","!","?","。","！","？"],
    length_function=len
)

split_docs = splitter.split_documents(docs)
print(split_docs)
print(len(split_docs))
