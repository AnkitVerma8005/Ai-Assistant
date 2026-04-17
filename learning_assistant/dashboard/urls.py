from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),
    path('tasks/add/', views.add_task, name='add_task'),
    path('tasks/toggle/<int:task_id>/', views.toggle_task, name='toggle_task'),
    path('tasks/delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('notes/save/', views.save_note, name='save_note'),
]
