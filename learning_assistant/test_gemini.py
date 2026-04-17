import os
import sys
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
try:
    genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
    model = genai.GenerativeModel('gemini-2.0-flash-lite')
    response = model.generate_content('Hello')
    print('SUCCESS! Response:', response.text)
except Exception as e:
    print('ERROR:', e)
    
try:
    model2 = genai.GenerativeModel('gemini-1.5-flash')
    response2 = model2.generate_content('Hello')
    print('SUCCESS! 1.5 Response:', response2.text)
except Exception as e:
    print('1.5 ERROR:', e)
