from dotenv import load_dotenv
import sqlite3
import pandas as pd
import os 
from openai import AzureOpenAI
from langchain_openai import AzureOpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter

load_dotenv()

endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
api_key = os.getenv("AZURE_OPENAI_API_KEY")

client = AzureOpenAI(api_version="2023-03-15-preview")
embed_model = "kant_embed"

# Function to pre-process the default file and generate embeddings
def pre_process_db():
    db_path = 'input_data/database.db' 
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM miibo_data", conn) #name of the table is miibo_data
    conn.close()
    df.drop(columns=['id'], inplace=True)
    rows = []
    for index, row in df.iterrows():
        row_text = " ".join(str(cell) for cell in row)  
        rows.append((row_text,index + 1)) 
    return rows

def get_text_chunks(pages):  # divide text of file into chunks
    text_splitter = CharacterTextSplitter(separator="\n", chunk_size=1500, chunk_overlap=0)
    chunks = []
    for text, page_number in pages:
        for chunk in text_splitter.split_text(text):
            chunks.append({"text": chunk, "page_number": page_number})
    return chunks


class DocumentChunk:                   #create a class to store text chunk with metadata (page number)
    def __init__(self, page_content, metadata):
        self.page_content = page_content
        self.metadata = metadata

def create_embeddings():
    text = pre_process_db()
    text_chunks=get_text_chunks(text)
    # embeddings = HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-large")
    embeddings = AzureOpenAIEmbeddings(azure_deployment=embed_model, openai_api_version="2023-05-15")
    documents = [DocumentChunk(page_content=chunk['text'], metadata={'page': chunk['page_number']}) 
                 for chunk in text_chunks]
    vector_store = FAISS.from_documents(documents, embeddings)
    vector_store.save_local("embeddings/faiss_index_ai")
    # retriever = vector_store.as_retriever(search_kwargs={'k': 1}, search_type="similarity")
    return vector_store

