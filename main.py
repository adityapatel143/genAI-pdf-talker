from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from get_from_db import retrive_data
from openai import OpenAI

load_dotenv()

gemini_client = OpenAI(
    api_key=os.getenv("GOOGLE_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

app = Flask(__name__)

# Create uploads directory if it doesn't exist
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and file.filename.endswith('.pdf'):
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return jsonify({'message': 'File uploaded successfully', 'filename': filename}), 200
    else:
        return jsonify({'error': 'Invalid file format. Please upload a PDF file'}), 400

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()  # Get JSON data from request body
    if not data or 'query' not in data:
        return jsonify({'error': 'No query provided in request body'}), 400
    
    documents = retrive_data(data['query'])

    print(documents)

    response = {
        'count': len(documents),
        'results': [{
            'content': doc.page_content,
            'metadata': doc.metadata,
            'source': doc.metadata.get('source', ''),
            'page': doc.metadata.get('page', '')
        } for doc in documents]
    }

    SYSTEM_PROMPT = f"""
        You are helphul AI Assistent who answers the user query based on the available context from pdf file.
        Please re-thing before replying. Do not take content from outsinde of pdf.
        ${jsonify(response)}
    """

    chatResult = gemini_client.chat.completions.create(
            model="gemini-2.0-flash",
            n=1,
            response_format={"type": "json_object"},
            messages= [
                {'role': 'system', 'content': SYSTEM_PROMPT},
                {'role': 'user', 'content': data['query']},
            ]
        )
    return jsonify({'message': chatResult.choices[0].message.content, 'docs': response})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
