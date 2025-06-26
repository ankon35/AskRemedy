# import os
# from dotenv import load_dotenv
# from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
# from langchain_community.vectorstores import Chroma
# from langchain.chains import RetrievalQA

# load_dotenv()

# def query_vector_store(question: str):
#     embeddings = GoogleGenerativeAIEmbeddings(
#         model="models/embedding-001",
#         google_api_key=os.getenv("GEMINI_API_KEY")
#     )

#     vector_store = Chroma(
#         persist_directory="db",
#         embedding_function=embeddings
#     )

#     retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 3})

#     qa = RetrievalQA.from_chain_type(
#         llm=ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=os.getenv("GEMINI_API_KEY")),
#         chain_type="stuff",
#         retriever=retriever,
#         return_source_documents=False
#     )

#     return qa.invoke({"query": question})


# if __name__ == "__main__":
#     question = input("Enter your medical question: ")
#     answer = query_vector_store(question)
#     print("Answer:", answer)




import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

load_dotenv()

# Define custom prompt
custom_prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are a knowledgeable and professional medical assistant. Using the context below, provide a clear, descriptive, and user-friendly answer to the question.

- Structure your response with bullet points where appropriate.
- Use simple language that a general user can understand.
- Be polite and helpful.
- If the answer is not found in the context, respond with: "I'm sorry, I don't have enough information to answer that."
"

Context:
{context}

Question:
{question}

Helpful Answer:"""
)

def query_vector_store(question: str):
    # Load embeddings
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=os.getenv("GEMINI_API_KEY")
    )

    # Load vector store
    vector_store = Chroma(
        persist_directory="db",
        embedding_function=embeddings
    )

    # Create retriever
    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 3})

    # Load Gemini LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",  # You can use "gemini-2.5-flash" if needed
        temperature=0.2,
        google_api_key=os.getenv("GEMINI_API_KEY")
    )

    # Build RetrievalQA chain with custom prompt
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={"prompt": custom_prompt},
        return_source_documents=False
    )

    # Run QA
    return qa.invoke({"query": question})

if __name__ == "__main__":
    question = input("Enter your medical question: ")
    result = query_vector_store(question)

    print("\nAnswer:\n", result['result'] if 'result' in result else result)
