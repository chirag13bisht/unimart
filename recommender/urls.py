from django.urls import path
from . import views

urlpatterns = [
    path('log_inquiry/<str:model_type>/<int:product_id>/', views.log_inquiry, name='log_inquiry'),
]