from flask import Flask, render_template, request, jsonify
import requests
import json
import re  # Import the regex module

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_message = request.json.get('message')
    selected_models = request.json.get('models', [])  # Get array of selected models
    ollama_url = 'http://localhost:11434/api/generate'

    # Check for specific questions and override the response
    if "اسم تو چیه" in user_message or "اسم شما چیست" in user_message:
        return jsonify({'responses': {model: "اسم من [علی] است." for model in selected_models}})
    elif "سازنده تو کیه" in user_message or "تو کی ساختی" in user_message:
        return jsonify({'responses': {model: "من توسط [علی] ساخته شدم." for model in selected_models}})

    responses = {}
    try:
        for model in selected_models:
            response = requests.post(
                ollama_url,
                json={'model': model, 'prompt': user_message},
                headers={'Content-Type': 'application/json'},
                stream=True
            )
            
            full_response = ""
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode('utf-8')
                    json_data = json.loads(decoded_line)
                    full_response += json_data.get('response', '')
            
            # Process the response to replace specific words
            full_response = process_response(full_response)
            
            responses[model] = full_response
        
        return jsonify({'responses': responses})
    except Exception as e:
        return jsonify({'error': f"Error occurred: {str(e)}"})

def process_response(response):
    # Replace specific words or phrases with desired ones (case-insensitive)
    replacements = {
        "Qwen": "ALI ",
        "Gemma": "ALI ",
        "DeepSeek": "ALI ",
        "Phi": "Ali",
        "Luna": "Ali",
        "Nova": "Ali",
        "LLaMA": "Ali",
        "Meta": "Ali CO ",
        "Alibaba": "Ali CO ",
        "google": "Ali CO",
          "گوگل": "کمپانی علی",
        "Microsoft": "Ali CO",
  
    }
    for word, replacement in replacements.items():
        # Use regex with IGNORECASE flag to make it case-insensitive
        response = re.sub(re.escape(word), replacement, response, flags=re.IGNORECASE)
    return response

if __name__ == '__main__':
    app.run(debug=True)
