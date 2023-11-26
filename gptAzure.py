#Note: The openai-python library support for Azure OpenAI is in preview.
      #Note: This code sample requires OpenAI Python library version 0.28.1 or lower.
import os
import openai
from embedded import search_docs
from flask import Flask, request, jsonify
from flask_cors import CORS
openai.api_type = "azure"
openai.api_base = "URL"
openai.api_version = "2023-07-01-preview"
openai.api_key = "Api_key"


def askGPt(prompt, quesiton):
    completion = openai.ChatCompletion.create(
        engine="gpt4GreenBox",
        messages=[
        {"role": "system", "content": str(prompt)+"Return the text in the same language as you got it and answer only questions about Harry Potter"},
        {"role": "user", "content": str(quesiton)}
        ],
        temperature=0.7,
        max_tokens=800,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
    )
    return completion.choices[0].message.content


app = Flask(__name__)
CORS(app) 

@app.route('/api/ask', methods=['POST'])
def api():
    data = request.json
    message = data.get('message', '')
    prompt = search_docs(message)
    return jsonify({
        'response': askGPt(prompt, message),
        'sources': str(prompt)
    })

if __name__ == '__main__':
    app.run(debug=True)