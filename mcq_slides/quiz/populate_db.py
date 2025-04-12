import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mcq_slides.settings')
django.setup()

from quiz.models import MCQ

mcqs_data = [
    {
        'question': 'What was the target year for achieving Millennium Development Goals?',
        'option_a': '2010',
        'option_b': '2015',
        'option_c': '2020',
        'option_d': '2025',
        'correct_answer': 'b',
        'explanation': 'MDGs were established in 2000 with a target to achieve by 2015'
    },
    {
        'question': 'How many goals were there in Millennium Development Goals?',
        'option_a': '5 goals',
        'option_b': '8 goals',
        'option_c': '10 goals',
        'option_d': '12 goals',
        'correct_answer': 'b',
        'explanation': 'The 8 goals covered areas like poverty eradication, education, gender equality, health, and environmental sustainability'
    },
    # Add more MCQs here...
]

def populate_db():
    MCQ.objects.all().delete()  # Clear existing data
    for mcq_data in mcqs_data:
        MCQ.objects.create(**mcq_data)
    print("Database populated successfully!")

if __name__ == '__main__':
    populate_db() 