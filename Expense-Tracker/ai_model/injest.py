from langchain_community.document_loaders import CSVLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from flask import jsonify,Flask,request
from flask_cors import CORS
import pprint
import os
import tempfile

app = Flask(__name__)
CORS(app)


data_embeddings = None

def create_vector_embeddings(csvfile_path):
    # 1. Load the csv file
    document = CSVLoader(file_path=csvfile_path).load()
    # 2. Load the embedding model
    embedding_model = OllamaEmbeddings(model="mxbai-embed-large")
    # 3. Storing the embeddings
    vector_store = FAISS.from_documents(document,embedding_model)

    print(vector_store)
    return vector_store


with app.app_context():
    print("App started. Please select file to generate embeddings")

    


@app.route('/api/upload',methods=['POST'])
def upload_file():
    global data_embeddings

    if('file' not in request.files):
        return jsonify({"error":"No file selected"}),400

    file = request.files['file']

    with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as temp_file:
        file.save(temp_file.name) # Save the uploaded data to the temp path
        temp_path = temp_file.name
    
    try:
        # Pass the valid file path string to the embedding function
        new_vector_store = create_vector_embeddings(temp_path)
        data_embeddings = new_vector_store
        message = f"File {file.filename} uploaded and new vector store created successfully."

    finally:
        # Ensure the temporary file is deleted after processing is complete
        os.remove(temp_path)
        print(f"Cleaned up temporary file: {temp_path}")

    return jsonify({"message": message})


@app.route('/api/ask',methods=['POST'])
def rag_query_handler():
    #user_query="Find the category where overspending is observed except the necessary expenses and suggest some tips to save money considering the cost of living in Hyderabad."
    user_query = request.json.get('query')
    retriever = data_embeddings.as_retriever(search_kwargs={"k":3})
    
    llm = Ollama(model="llama3")

    system_prompt = (
        "You are an financial assistant for question-answering tasks. Use the following pieces of retrieved context to answer.Consider all the amounts as INR and dates in format DD/MM/YYYY"
        "the question. If you don't know the answer, just say that you don't know, don't try to make up an answer.\n\n"
        "{context}"
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{input}"),
        ]
    )

    question_answer_chain = create_stuff_documents_chain(llm,prompt)

    rag_chain = create_retrieval_chain(retriever, question_answer_chain)

    response = rag_chain.invoke({"input": user_query})

    return jsonify({
        "answer": response["answer"],
        # Sources are automatically included in the 'context' part of the response object
        "sources": [doc.page_content for doc in response["context"]] 
    })

if __name__ == '__main__':
    app.run(port=5000, debug=True)