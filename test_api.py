#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

# Configure OpenAI
api_key = os.getenv('OPENAI_API_KEY')
print(f"API Key loaded: {api_key[:20] if api_key else 'None'}...")

try:
    client = openai.OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful dental office assistant."},
            {"role": "user", "content": "I want to book an appointment"}
        ],
        max_tokens=200,
        temperature=0.7
    )
    
    print("Success! Response:", response.choices[0].message.content)
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
