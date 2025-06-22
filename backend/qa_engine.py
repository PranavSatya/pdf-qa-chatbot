import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Directories for storing uploaded PDFs and vector indices
UPLOAD_DIR = "uploads"
VECTOR_DB_DIR = "faiss_index"

# Load Together API key from .env
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")  # Ensure this is set in .env

# ---------------------------------------------
# Function 1: Extract text and create FAISS index
# ---------------------------------------------
def extract_text_and_create_index(file_path: str, filename: str):
    print(f"🛠️ Starting FAISS indexing for: {filename}")
    try:
        # Load PDF using PyMuPDF
        loader = PyMuPDFLoader(file_path)
        documents = loader.load()
        print(f"📄 Loaded {len(documents)} documents")

        # Split documents into chunks
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        docs = splitter.split_documents(documents)
        print(f"✂️ Split into {len(docs)} chunks")

        # Generate embeddings using HuggingFace model
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

        # Create FAISS vector store from document chunks
        db = FAISS.from_documents(docs, embeddings)

        # Save the vector store locally under the filename
        save_path = os.path.join(VECTOR_DB_DIR, filename)
        os.makedirs(save_path, exist_ok=True)
        db.save_local(save_path)
        print(f"✅ FAISS index saved at {save_path}")

    except Exception as e:
        print(f"❌ Indexing failed: {e}")

# ---------------------------------------------
# Function 2: Answer questions from the indexed file
# ---------------------------------------------
def answer_question(filename: str, question: str) -> str:
    print(f"📥 Received question: {question} for file: {filename}")

    # Construct the path to the FAISS index
    index_path = os.path.join(VECTOR_DB_DIR, filename)

    # Check if the FAISS index exists
    if not os.path.exists(index_path):
        return "❌ FAISS index not found for this file."

    # Reload the FAISS index and create a retriever
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
    retriever = db.as_retriever()

    # Set up the LLM from Together.ai
    llm = ChatOpenAI(
        openai_api_key=TOGETHER_API_KEY,
        base_url="https://api.together.xyz/v1",
        model_name="mistralai/Mistral-7B-Instruct-v0.2"
    )

    # Create a RetrievalQA chain using the LLM and retriever
    qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

    # Run the QA chain on the given question
    result = qa.run(question)
    return result
