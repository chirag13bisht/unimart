from django.urls import path
from . import views

urlpatterns = [
    # This will make our API available at /api/query/
    path('query/', views.chatbot_query, name='chatbot_query'),
]