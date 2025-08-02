
import os
from flask import Flask, request, jsonify, render_template
import openai
from chromadb import Client
from chromadb.utils import embedding_functions
import json

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize Chroma client
chroma_client = Client()
embedding_fn = embedding_functions.OpenAIEmbeddingFunction(api_key=openai.api_key)
collection = chroma_client.get_or_create_collection("scoutbot", embedding_function=embedding_fn)

# Load data (FAQ chunks)
data_path = os.path.join(os.path.dirname(__file__), 'data', 'faq_site_chunks.json')
if os.path.exists(data_path):
    with open(data_path, 'r', encoding='utf-8') as f:
        docs = json.load(f)
        # Add documents to Chroma
        for d in docs:
            collection.add(documents=[d['content']], metadatas=[{"source": d['source'], "url": d['url']}], ids=[d['id']])

@app.route("/")
def home():
    return render_template("widget.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_question = request.json.get("question")
    # Search vector DB
    results = collection.query(query_texts=[user_question], n_results=3)
    context = " ".join(results['documents'][0]) if results['documents'] else ""

    prompt = f"Answer the following question using the context below. Be concise and friendly.\n\nContext:\n{context}\n\nQuestion: {user_question}\nAnswer:"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role":"user","content": prompt}],
            max_tokens=300
        )
        answer = response.choices[0].message["content"]
    except Exception as e:
        answer = f"Error: {e}"
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
