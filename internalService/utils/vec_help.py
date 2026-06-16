from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
def build_vector_store(text: str, job_id: str):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
    chunks = splitter.split_text(text)
    docs = [
        Document(
            page_content=chunk,
            metadata={
                "job": job_id,
                "chunk_id": idx
            }
        )
        for idx, chunk in enumerate(chunks)
    ]
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_store = FAISS.from_documents(docs, embedding_model)
    vector_store.save_local( f"vector_indexes/{job_id}")
    return vector_store
