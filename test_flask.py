#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

app = Flask(__name__)

def get_ai_response(user_query):
    """Get AI response for dental queries"""
    try:
        system_prompt = "You are a helpful dental office assistant. Be friendly and helpful."
        
        client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query}
            ],
            max_tokens=200,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"OpenAI API Error: {e}")
        import traceback
        traceback.print_exc()
        return f"Error: {str(e)}"

@app.route('/test', methods=['POST'])
def test():
    data = request.get_json()
    user_query = data.get('query', '')
    response = get_ai_response(user_query)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
