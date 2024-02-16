from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests

API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=AIzaSyDIRl7rr8brkwTe_8IaQSVv9QMBkKzhGGg"

from .models import Conversation
@csrf_exempt
def query_view(request):
    if request.method == 'GET' or request.method == 'POST':
        payload = request.GET.get('input_text') if request.method == 'GET' else request.POST.get('input_text')
        session_id = request.GET.get('session_id') if request.method == 'GET' else request.POST.get('session_id')

        if payload:
            response = query(payload)
            formatted_response = format_response(response)
            bot_text = formatted_response.get("text", "")
            Conversation.objects.create(bot=bot_text, user=payload, session_id=session_id)

            return JsonResponse({"text": bot_text})
        else:
            return JsonResponse({"error": "Input text is required."}, status=400)
    else:
        return JsonResponse({"error": "Only GET and POST requests are allowed."}, status=405)

def query(payload):
    response = requests.post(API_URL, json={"contents": [{"parts": [{"text": payload}]}]})
    return response.json()

def format_response(response):
    candidates = response.get('candidates', [])
    text = ''
    for candidate in candidates:
        content = candidate.get('content', {})
        parts = content.get('parts', [])
        for part in parts:
            text += part.get('text', '')
    return {"text": text}


def get_conversation(request):
    if request.method == 'GET' or request.method == 'POST':
        session_id = request.GET.get('session_id') if request.method == 'GET' else request.POST.get('session_id')
        data = Conversation.objects.filter(session_id=session_id)
        serialized_data = [{"bot": conv.bot, "user": conv.user, "session_id": conv.session_id} for conv in data]
        return JsonResponse(serialized_data, safe=False)
    else:
        return JsonResponse({"error": "Only GET and POST requests are allowed."}, status=405)

def get_session_id(request):
    session_id = request.session.session_key
    
    # Ensure session key is saved
    if not session_id:
        request.session.save()
        session_id = request.session.session_key
    
    return JsonResponse({"session_id": session_id})


def home(request):
    current_url = request.build_absolute_uri()
    data = {
        "get-session-id/": f"{current_url}get-session-id/",
        "get-chat": f"{current_url}get-chat/?session_id=your_session_id_here",
        "query": f"{current_url}query/?input_text=hi&session_id=your_session_id_here"
    }
    return JsonResponse(data)
