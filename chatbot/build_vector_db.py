import os
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load .env environment variables
load_dotenv()

# ✅ Absolute path to your medical encyclopedia PDF
pdf_path = "data/The_GALE_ENCYCLOPEDIA_of_MEDICINE_SECOND.pdf"

# Ensure the file exists
assert os.path.exists(pdf_path), f"PDF not found at {pdf_path}"

# Load PDF
loader = PyMuPDFLoader(pdf_path)
documents = loader.load()
print(f"✅ Loaded {len(documents)} pages from PDF.")

# Split into chunks for embeddings
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = splitter.split_documents(documents)
print(f"✅ Split into {len(chunks)} chunks.")

# Load Gemini embeddings
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=os.getenv("GEMINI_API_KEY")
)

# Create and persist Chroma vector store
vector_store = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="db"
)

print("✅ Vector store built and saved to /db.")
