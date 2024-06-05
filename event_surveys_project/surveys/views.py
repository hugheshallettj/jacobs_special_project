from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Survey, Question, Response
from datetime import datetime
from django.forms import modelform_factory
from .forms import SurveyForm
    
@login_required
def create_survey(request):
    if request.method == 'POST':
        form = SurveyForm(request.POST)
        if form.is_valid():
            # Create a Survey instance without saving it to the database
            survey = form.save(commit=False)
            
            # Set the admin field to the currently logged-in user
            survey.admin = request.user
            
            # Save the instance to the database
            survey.save()
            
            # Redirect to the home page or another page
            return redirect("home")
    else:
        form = SurveyForm()
    return render(request, 'surveys/create_survey.html', {"form": form})


def survey_view(request, link):
    survey = get_object_or_404(Survey, link=link)
    if survey.start_date > datetime.today() or survey.end_date < datetime.today():
        return render(request, 'surveys/survey_unavailable.html')
    if request.method == 'POST':
        # Handle survey response submission
        pass
    return render(request, 'surveys/survey.html', {'survey': survey})

@login_required
def survey_results(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)
    responses = Response.objects.filter(survey=survey)
    return render(request, 'surveys/results.html', {'survey': survey, 'responses': responses})
