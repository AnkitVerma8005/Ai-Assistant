from django.shortcuts import render
from django.http import JsonResponse
import json
from core.utils import get_gemini_model
from core.exceptions import AIAPIError

def quiz_home(request):
    return render(request, 'quiz/quiz.html')

def generate_quiz(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request'}, status=400)
        
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
    topic = data.get('topic', '')
    difficulty = data.get('difficulty', 'Medium')
    
    # Configure Gemini and get model
    model = get_gemini_model('gemini-2.5-flash-lite')
    
    prompt = f"""
    Create a multiple-choice quiz about "{topic}" with a difficulty level of {difficulty}.
    Generate 10 questions.
    Return the output STRICTLY as a JSON array of objects.
    Do not wrap the JSON in markdown code blocks.
    Each object must have the following keys:
    - "question": string
    - "options": array of 4 strings
    - "correct": integer (index of the correct option, 0-3)
    
    Example format:
    [
        {{
            "question": "What is 2+2?",
            "options": ["3", "4", "5", "6"],
            "correct": 1
        }}
    ]
    """
    
    try:
        response = model.generate_content(prompt)
        print(f"DEBUG: Gemini Response: {response.text}")
        
        # Clean response if it contains markdown formatting
        text_response = response.text.strip()
        if text_response.startswith("```json"):
            text_response = text_response[7:-3]
        elif text_response.startswith("```"):
            text_response = text_response[3:-3]
            
        quiz_data = json.loads(text_response)
        return JsonResponse({'questions': quiz_data})
        
    except Exception as e:
        print(f"DEBUG: Quiz Error: {e}")
        raise AIAPIError(f"Failed to generate quiz: {str(e)}")
