from django.urls import path
from . import views

urlpatterns = [
    path('', views.mcq_slides, name='mcq_slides'),
    path('presentation/', views.mcq_slides_presentation, name='mcq_slides_presentation'),
    path('mcq/<int:mcq_id>/', views.mcq_detail, name='mcq_detail'),
] 