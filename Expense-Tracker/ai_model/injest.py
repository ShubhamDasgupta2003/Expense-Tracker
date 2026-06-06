from langchain_community.document_loaders import CSVLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from flask import jsonify,Flask,request,Response
from flask_cors import CORS
import pprint
import os
import tempfile
import pandas as pd
import math
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER,exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

data_embeddings = None
file_chosen = None

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
    global file_chosen

    if('file' not in request.files):
        return jsonify({"error":"No file selected"}),400

    file = request.files['file']

    file_name = secure_filename(file.filename)
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
    file.save(save_path)
    file_chosen = save_path

    # with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as temp_file:
    #     file.save(temp_file.name) # Save the uploaded data to the temp path
    #     temp_path = temp_file.name
    
    try:
        # Pass the valid file path string to the embedding function
        new_vector_store = create_vector_embeddings(file_chosen)
        data_embeddings = new_vector_store
        message = f"File {file.filename} uploaded and new vector store created successfully."

    finally:
        # Ensure the temporary file is deleted after processing is complete
        # os.remove(temp_path)
        print(f"Cleaned up temporary file")

    return jsonify({"message": message})


@app.route('/api/ask',methods=['POST'])
def rag_query_handler():
    #user_query="Find the category where overspending is observed except the necessary expenses and suggest some tips to save money considering the cost of living in Hyderabad."
    user_query = request.json.get('query')
    retriever = data_embeddings.as_retriever(search_kwargs={"k":3})
    
    llm = Ollama(model="llama3")


    system_prompt = (
        """Role: You are a Professional Financial Assistant specializing in precise question-answering for Indian financial contexts.

        Context: Use only the provided retrieved context to answer user queries. You may incorporate external market data or general knowledge for searching latest market trends and property available for rent with in a area

        Operational Constraints:
        1.Currency: Treat all numerical financial amounts as Indian Rupee (INR) unless specified otherwise [User Request].
        2.Date Format: All dates must be formatted as DD/MM/YYYY [User Request].
        3.Language Style: Maintain a formal, neutral, and fact-based tone.

        Safety & Integrity Guidelines:
        1.Groundedness: If the answer is not contained within the retrieved context, state clearly: "I do not have enough information in the provided context to answer this question.".
        2.Anti-Hallucination: Do not attempt to fabricate figures, dates, or financial projections not found in the source material.
        3.Disclaimer: Remind users that this information is for informational purposes and they should consult a certified financial advisor for critical decisions.
        
        Output Format:
        1.Provide a concise answer followed by the specific source or section from the context used.
        2.Use bullet points for lists of financial figures or dates for better scannability
        3.Use unicode bullet points (•) for lists, never asterisks (*)
"""   "{context}"
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


@app.route('/api/getmetrics',methods=['GET','POST'])
def getMetrics():

    data = request.get_json(silent=True)
    if(not data):
        return jsonify({"error": "Missing JSON or incorrect Content-Type"}), 400
    salary = data.get("salary_slider")


    df = pd.read_csv(file_chosen)
    
    essential_cats = ['FOOD','GROC','MEDICINES','TRAVEL','MOBRCHG','RENT']
    discretion_cats = ['SHOPPING','SUBSCRIPTION','DINEOUT','TRIP','MISC']
    json_data = df.to_json(orient='records')
    grouped_df = df.groupby('cat_code',as_index=False).agg({
        'amount':'sum',
        'exp_id':'count'
    }).rename(columns={
        'amount':'name'
    })

    desc_sorted = grouped_df.sort_values(by="exp_id",ascending=False).to_dict(orient='records')

    grouped_data = grouped_df.to_dict(orient='records')

    filtered_essential_df = df[df['cat_code'].isin(essential_cats)]
    essential_total = float(filtered_essential_df['amount'].sum())

    filtered_discretion_df = df[df['cat_code'].isin(discretion_cats)]
    discretion_total = float(filtered_discretion_df['amount'].sum())

    piechart_data = [{"amount":round((essential_total/salary)*100,2),"name":"Essential","color":"#0392ff"},{"amount":round((discretion_total/salary)*100,2),"name":"Discreation","color":"#ff5203"},
    {"amount":round((salary-(essential_total+discretion_total))/salary*100,2),"name":"Savings","color":"#89d102"}]

    data = {"total":float(df['amount'].sum()),"group":grouped_data,"essential":essential_total, "desc_sort":desc_sorted,"pie_chart":piechart_data,"salary":salary,"savings":salary-float(df['amount'].sum())}
    # return Response(json_data, mimetype='application/json')
    return jsonify(data)

if __name__ == '__main__':
    app.run(port=5000, debug=True)