from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import UserProfile, VideoSummaryHistory, QuizHistory, StudyPlannerTask, ActivityLog, AINote

@login_required
def dashboard_home(request):
    # Ensure UserProfile exists
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    # Fetch data for dashboard
    summaries = VideoSummaryHistory.objects.filter(user=request.user).order_by('-created_at')[:5]
    quizzes = QuizHistory.objects.filter(user=request.user).order_by('-attempted_at')[:5]
    tasks = StudyPlannerTask.objects.filter(user=request.user).order_by('is_completed', 'deadline', '-created_at')
    activity_logs = ActivityLog.objects.filter(user=request.user)[:10]
    ai_notes = AINote.objects.filter(user=request.user).order_by('-created_at')[:5]

    context = {
        'profile': profile,
        'summaries': summaries,
        'quizzes': quizzes,
        'tasks': tasks,
        'activity_logs': activity_logs,
        'ai_notes': ai_notes,
    }
    return render(request, 'dashboard/dashboard.html', context)

@login_required
def add_task(request):
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        deadline = request.POST.get('deadline') or None
        if title:
            StudyPlannerTask.objects.create(
                user=request.user,
                title=title,
                description=description,
                deadline=deadline
            )
            # Log activity
            ActivityLog.objects.create(
                user=request.user,
                action_type='TASK',
                description=f'Added a new study task: {title}'
            )
    return redirect('dashboard_home')

@login_required
def toggle_task(request, task_id):
    if request.method == "POST":
        task = get_object_or_404(StudyPlannerTask, id=task_id, user=request.user)
        task.is_completed = not task.is_completed
        task.save()
        if task.is_completed:
            ActivityLog.objects.create(
                user=request.user,
                action_type='TASK',
                description=f'Completed task: {task.title}'
            )
        return JsonResponse({'status': 'success', 'is_completed': task.is_completed})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def delete_task(request, task_id):
    if request.method == "POST":
        task = get_object_or_404(StudyPlannerTask, id=task_id, user=request.user)
        task.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def save_note(request):
    if request.method == "POST":
        import json
        try:
            data = json.loads(request.body)
            title = data.get('title', 'Untitled Note')
            content = data.get('content', '')
            if content:
                AINote.objects.create(
                    user=request.user,
                    video_or_topic=title,
                    content=content
                )
                ActivityLog.objects.create(
                    user=request.user,
                    action_type='NOTE',
                    description=f'Saved a note: {title}'
                )
                return JsonResponse({'status': 'success'})
        except json.JSONDecodeError:
            pass
    return JsonResponse({'status': 'error'}, status=400)
