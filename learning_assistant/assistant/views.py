from django.shortcuts import render
from django.http import JsonResponse
import json
from core.utils import get_gemini_model
from core.exceptions import AIAPIError

def assistant_home(request):
    return render(request, 'assistant/assistant.html')

def chat_api(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request'}, status=400)
        
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
    user_message = data.get('message', '')
    
    # Configure Gemini and get model
    model = get_gemini_model('gemini-2.5-flash-lite')
    
    # Append instruction for better formatting
    enhanced_message = f"{user_message}\n\nPlease format your response using Markdown. Use bullet points, bold text for emphasis, and code blocks where appropriate. Keep it structured and easy to read."
    
    try:
        chat = model.start_chat(history=[])
        response = chat.send_message(enhanced_message)
        return JsonResponse({'response': response.text})
    except Exception as e:
        raise AIAPIError(f"AI chat failed: {str(e)}")
