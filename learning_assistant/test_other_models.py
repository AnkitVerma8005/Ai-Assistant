import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

models_to_test = [
    'gemini-2.0-flash',
    'gemini-2.5-flash-lite',
    'gemini-flash-lite-latest',
]

for m in models_to_test:
    try:
        model = genai.GenerativeModel(m)
        response = model.generate_content('Hello')
        print(f'{m} SUCCESS:', response.text)
        break # stop if we find one that works
    except Exception as e:
        print(f'{m} ERROR:', e)
