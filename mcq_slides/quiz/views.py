from django.shortcuts import render
from .models import MCQ

def mcq_slides(request):
    mcqs = MCQ.objects.all()
    return render(request, 'quiz/slides.html', {'mcqs': mcqs})

def mcq_slides_presentation(request):
    mcqs = MCQ.objects.all()
    return render(request, 'quiz/slides_presentation.html', {'mcqs': mcqs})

def mcq_detail(request, mcq_id):
    mcq = MCQ.objects.get(id=mcq_id)
    return render(request, 'quiz/detail.html', {'mcq': mcq})
