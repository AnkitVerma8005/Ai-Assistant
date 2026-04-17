from django.shortcuts import render
from django.http import JsonResponse
import json
import os
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
from core.exceptions import (
    InvalidVideoURLError, 
    TranscriptRetrievalError, 
    AIAPIError
)
from core.utils import get_gemini_model

def summarizer_home(request):
    return render(request, 'summarizer/summarize.html')

def get_youtube_title(video_id):
    try:
        import urllib.request
        url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
        response = urllib.request.urlopen(url)
        data = json.loads(response.read())
        return data.get('title', 'Video Summary')
    except Exception:
        return 'Video Summary'

def get_video_id(url):
    """
    Extracts video ID from a YouTube URL.
    """
    query = urlparse(url)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            p = parse_qs(query.query)
            if 'v' in p:
                return p['v'][0]
        if query.path[:7] == '/embed/':
            return query.path[7:]
        if query.path[:3] == '/v/':
            return query.path[3:]
    return None

def generate_summary(request):
    if request.method != 'POST':
         return JsonResponse({'error': 'Invalid request'}, status=400)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
    video_url = data.get('url', '')
    
    video_id = get_video_id(video_url)
    if not video_id:
        raise InvalidVideoURLError("Invalid YouTube URL")
        
    video_title = get_youtube_title(video_id)
    
    # Fetch Transcript
    try:
        print(f"DEBUG: Fetching transcript for {video_id}")
        ytt_api = YouTubeTranscriptApi()
        transcript = ytt_api.fetch(video_id, languages=['en', 'hi', 'es', 'fr', 'de'])
        transcript_text = " ".join([t.text for t in transcript])
    except Exception as e:
        print(f"DEBUG: Transcript Error: {e}")
        raise TranscriptRetrievalError(f"Could not retrieve transcript: {str(e)}")
    
    # Configure Gemini and get model
    model = get_gemini_model('gemini-2.5-flash-lite')
    
    prompt = f"""
    Please provide a comprehensive summary of the following video transcript. 
    Capture the main points, key arguments, and any important conclusions.
    The summary should be well-structured using Markdown.
    - Use **Bold** for key terms.
    - Use Bullet points for lists.
    - Use Headers (##) for sections.
    - **IMPORTANT: Provide the summary in ENGLISH, even if the transcript is in another language.**
    
    Transcript:
    {transcript_text[:30000]}
    """
    
    try:
        response = model.generate_content(prompt)
        
        # Save to dashboard history automatically
        if request.user.is_authenticated:
            try:
                from dashboard.models import VideoSummaryHistory, ActivityLog
                VideoSummaryHistory.objects.create(
                    user=request.user,
                    video_url=video_url,
                    title=video_title,
                    summary_text=response.text[:500] + ('...' if len(response.text) > 500 else '')
                )
                ActivityLog.objects.create(
                    user=request.user,
                    action_type='SUMMARY',
                    description=f'Generated a summary for: {video_title}'
                )
            except Exception as outer_e:
                print(f"DEBUG: Failed to save history: {outer_e}")

        return JsonResponse({
            "title": video_title,
            "summary": response.text
        })
    except Exception as e:
        print(f"DEBUG: Gemini API Error: {e}")
        raise AIAPIError(f"AI summarization failed: {str(e)}")
