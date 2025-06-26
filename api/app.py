from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

load_dotenv()

app = Flask(__name__)
CORS(app)

# Load the vector store
embedding = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001", google_api_key=os.getenv("GEMINI_API_KEY")
)

vector_store = Chroma(
    persist_directory="db",
    embedding_function=embedding,
)

retriever = vector_store.as_retriever()

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.3
)

# QA chain setup
qa = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True
)

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "")
    
    if not question:
        return jsonify({"error": "No question provided"}), 400

    response = qa.invoke({"query": question})
    
    return jsonify({
        "question": question,
        "answer": response["result"],
        "sources": [doc.metadata.get("source", "") for doc in response["source_documents"]]
    })

@app.route("/", methods=["GET"])
def root():
    return "✅ Medical Chatbot API is running."

if __name__ == "__main__":
    app.run(debug=True)
