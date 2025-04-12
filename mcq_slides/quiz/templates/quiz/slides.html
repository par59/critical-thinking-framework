{% extends 'quiz/base.html' %}

{% block content %}
<div class="row">
    <div class="col-md-8 offset-md-2">
        <div id="mcqCarousel" class="carousel slide" data-bs-ride="carousel">
            <div class="carousel-inner">
                {% for mcq in mcqs %}
                <div class="carousel-item {% if forloop.first %}active{% endif %}">
                    <div class="slide">
                        <h2 class="mb-4">Question {{ forloop.counter }}</h2>
                        <p class="lead">{{ mcq.question }}</p>
                        
                        <div class="options">
                            <div class="option" onclick="checkAnswer(this, '{{ mcq.correct_answer }}')">
                                a) {{ mcq.option_a }}
                            </div>
                            <div class="option" onclick="checkAnswer(this, '{{ mcq.correct_answer }}')">
                                b) {{ mcq.option_b }}
                            </div>
                            <div class="option" onclick="checkAnswer(this, '{{ mcq.correct_answer }}')">
                                c) {{ mcq.option_c }}
                            </div>
                            <div class="option" onclick="checkAnswer(this, '{{ mcq.correct_answer }}')">
                                d) {{ mcq.option_d }}
                            </div>
                        </div>

                        <div class="explanation mt-4" style="display: none;">
                            <h5>Explanation:</h5>
                            <p>{{ mcq.explanation }}</p>
                        </div>
                    </div>
                </div>
                {% endfor %}
            </div>
            
            <button class="carousel-control-prev" type="button" data-bs-target="#mcqCarousel" data-bs-slide="prev">
                <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                <span class="visually-hidden">Previous</span>
            </button>
            <button class="carousel-control-next" type="button" data-bs-target="#mcqCarousel" data-bs-slide="next">
                <span class="carousel-control-next-icon" aria-hidden="true"></span>
                <span class="visually-hidden">Next</span>
            </button>
        </div>
    </div>
</div>

<script>
function checkAnswer(element, correctAnswer) {
    const options = element.parentElement.querySelectorAll('.option');
    const explanation = element.parentElement.nextElementSibling;
    
    // Remove correct class from all options
    options.forEach(opt => opt.classList.remove('correct'));
    
    // Add correct class to the selected option
    element.classList.add('correct');
    
    // Show explanation
    explanation.style.display = 'block';
}
</script>
{% endblock %} 