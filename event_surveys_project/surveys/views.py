from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Survey, Question, Response
from datetime import datetime

@login_required
def create_survey(request):
    if request.method == 'POST':
        # Handle survey creation form submission
        pass
    return render(request, 'surveys/create_survey.html')

# def survey_view(request, link):
#     survey = get_object_or_404(Survey, link=link)
#     if survey.start_date > datetime.today() or survey.end_date < datetime.today():
#         return render(request, 'surveys/survey_unavailable.html')
#     if request.method == 'POST':
#         # Handle survey response submission
#         pass
#     return render(request, 'surveys/survey.html', {'survey': survey})

# @login_required
# def survey_results(request, survey_id):
#     survey = get_object_or_404(Survey, id=survey_id)
#     responses = Response.objects.filter(survey=survey)
#     return render(request, 'surveys/results.html', {'survey': survey, 'responses': responses})
