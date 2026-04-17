from django.contrib import admin
from .models import UserProfile, VideoSummaryHistory, QuizHistory, StudyPlannerTask, AINote, ActivityLog

admin.site.register(UserProfile)
admin.site.register(VideoSummaryHistory)
admin.site.register(QuizHistory)
admin.site.register(StudyPlannerTask)
admin.site.register(AINote)
admin.site.register(ActivityLog)
