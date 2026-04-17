from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='dashboard_profile')
    progress_score = models.IntegerField(default=0)
    videos_summarized = models.IntegerField(default=0)
    quizzes_taken = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

class VideoSummaryHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='video_summaries')
    video_url = models.URLField()
    title = models.CharField(max_length=255)
    summary_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Summary for {self.title} by {self.user.username}"

class QuizHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_attempts')
    topic = models.CharField(max_length=255)
    score = models.IntegerField(default=0)
    total_questions = models.IntegerField(default=10)
    accuracy = models.FloatField(default=0.0)
    attempted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.topic} Quiz by {self.user.username}"

class StudyPlannerTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='study_tasks')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    deadline = models.DateTimeField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class AINote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ai_notes')
    video_or_topic = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Note on {self.video_or_topic} by {self.user.username}"

class ActivityLog(models.Model):
    ACTION_CHOICES = [
        ('QUIZ', 'Completed a Quiz'),
        ('SUMMARY', 'Summarized a Video'),
        ('CHAT', 'Used AI Assistant'),
        ('TASK', 'Completed a Task'),
        ('NOTE', 'Created a Note'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity_logs')
    action_type = models.CharField(max_length=20, choices=ACTION_CHOICES)
    description = models.CharField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user.username} - {self.action_type} - {self.timestamp}"
