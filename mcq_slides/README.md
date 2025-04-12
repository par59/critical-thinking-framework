# MCQ Slides Presentation

An interactive MCQ (Multiple Choice Questions) presentation system built with Django and Reveal.js.

## Features

- Interactive MCQ slides
- Two viewing modes:
  - Carousel View
  - Presentation View (using Reveal.js)
- Clickable options
- Answer explanations
- Responsive design
- Full-screen presentation mode

## Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/yourusername/mcq-slides.git
cd mcq-slides
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Start the development server:
```bash
python manage.py runserver
```

6. Access the application:
- Main view: http://127.0.0.1:8000/
- Presentation view: http://127.0.0.1:8000/presentation/

## Presentation Controls

- Arrow keys: Navigate between slides
- Space: Next slide
- F: Fullscreen mode
- Esc: Overview mode
- S: Speaker notes
- B: Pause/black screen

## Project Structure

```
mcq-slides/
├── manage.py
├── requirements.txt
├── README.md
├── mcq_slides/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── quiz/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── tests.py
    ├── urls.py
    ├── views.py
    └── templates/
        └── quiz/
            ├── base.html
            ├── slides.html
            └── slides_presentation.html
```

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License. 