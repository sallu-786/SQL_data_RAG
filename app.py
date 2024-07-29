from flask import Flask, request, jsonify, render_template, send_from_directory, Response
from openai import AzureOpenAI
import os
from dotenv import load_dotenv
import sqlite3
import pandas as pd
from datetime import datetime
from embeddings import create_embeddings
from prompt import get_prompt

load_dotenv()
app = Flask(__name__)

#-----------------------------------------------Chat--------------------------------------------------

endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
api_key = os.getenv("AZURE_OPENAI_API_KEY")

client = AzureOpenAI(api_version="2023-03-15-preview")
model = "azure_openai_app"
embed_model = "kant_embed_3"

# Initial system message
system_msg = get_prompt()
chat_history = []
xlsx_log_file = "chat_log/chat_log.xlsx"

vectordb = create_embeddings()

def update_embeddings():
    global vectordb
    vectordb = create_embeddings()


def save_chat_log(user_msg, assistant_msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    chat_data = pd.DataFrame([[timestamp, user_msg, assistant_msg]], columns=["Timestamp", "Question", "Answer"])
    if os.path.exists(xlsx_log_file):
        existing_data = pd.read_excel(xlsx_log_file)
        chat_data = pd.concat([existing_data, chat_data], ignore_index=True)
    chat_data.to_excel(xlsx_log_file, index=False)

@app.route('/chat', methods=['POST'])
def chat():
    global chat_history
    global vectordb

    user_input = request.json.get('message')
    if not user_input:
        return jsonify({'error': 'No input message'}), 400

    messages = [{"role": "assistant", "content": system_msg}]

    for chat in chat_history[-3:]:
        messages.append({"role": chat["role"], "content": chat["content"]})

    messages.append({"role": "user", "content": user_input})

    try:
        doc_text = vectordb.similarity_search_with_score(query=user_input, k=1)
        doc_texts = [{"content": doc.page_content, "metadata": doc.metadata} for doc, score in doc_text]
        for doc in doc_texts:
            messages.append({"role": "user", "content": f"Document snippet:\n{doc['content']}"})

        response = client.chat.completions.create(model=model, messages=messages, temperature=0)
        answer = response.choices[0].message.content

        # Append user message and bot answer to chat history
        chat_history.append({"role": "user", "content": user_input})
        chat_history.append({"role": "assistant", "content": answer})
        save_chat_log(user_input, answer)
        return jsonify({"answer": answer})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download')
def download_file():
    return send_from_directory(directory='chat_log', path='chat_log.xlsx', as_attachment=True)

@app.route('/data')
def get_data():
    if not request.authorization or not check_auth(request.authorization.username, request.authorization.password):
        return authenticate()

    df = pd.read_excel('chat_log/chat_log.xlsx')
    data = df.to_dict(orient='records')
    return jsonify(data)

#--------------------------------Database----------------------------------------------------------

def get_db_connection():
    conn = sqlite3.connect('input_data/miibo_data.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS miibo_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    Keyword TEXT NOT NULL,
                    Description TEXT NOT NULL
                )''')
    conn.commit()
    conn.close()

create_table()

@app.route('/api/data', methods=['GET'])
def get_all_data():
    conn = get_db_connection()
    data = conn.execute('SELECT * FROM miibo_data').fetchall()
    conn.close()
    return jsonify([dict(row) for row in data])

@app.route('/api/data', methods=['POST'])
def add_data():
    new_data = request.json
    conn = get_db_connection()
    conn.execute('INSERT INTO miibo_data (Keyword, Description) VALUES (?, ?)',
                 (new_data['Keyword'], new_data['Description']))
    conn.commit()
    conn.close()
    update_embeddings()
    return jsonify({'status': 'success'})

@app.route('/api/data/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handle_data(id):
    conn = get_db_connection()
    if request.method == 'GET':
        data = conn.execute('SELECT * FROM miibo_data WHERE id = ?', (id,)).fetchone()
        conn.close()
        if data is None:
            return jsonify({'error': 'Data not found'}), 404
        
        return jsonify(dict(data))

    elif request.method == 'PUT':
        updated_data = request.json
        conn.execute('UPDATE miibo_data SET Keyword = ?, Description = ? WHERE id = ?',
                     (updated_data['Keyword'], updated_data['Description'], id))
        conn.commit()
        conn.close()
        update_embeddings()
        return jsonify({'status': 'success'})
    elif request.method == 'DELETE':
        conn.execute('DELETE FROM miibo_data WHERE id = ?', (id,))
        conn.commit()
        conn.close()
        update_embeddings()
        return jsonify({'status': 'success'})
    else:
        return jsonify({'error': 'Method not allowed'}), 405

#----------------------------------------Web Pages----------------------------------------------

def check_auth(username, password):
    """Check if a username/password combination is valid."""
    return username == 'admin' and password == 'admin'

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials.\n Refresh page and try again', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"',
         'Cache-Control': 'no-cache, no-store, must-revalidate',
         'Pragma': 'no-cache',
         'Expires': '0'})

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/admin')
def admin():
    if not request.authorization or not check_auth(request.authorization.username, request.authorization.password):
        return authenticate()
    return render_template('admin.html')

@app.route('/log')
def log():
    if not request.authorization or not check_auth(request.authorization.username, request.authorization.password):
        return authenticate()
    return render_template('log.html')

if __name__ == '__main__':
    app.run(debug=True)


