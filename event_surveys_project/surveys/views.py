from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Survey, Question, Response
from datetime import datetime, date
from django.forms import modelform_factory
from .forms import SurveyCreationForm, QuestionForm, generate_survey_form
    
@login_required
def create_survey(request):
    if request.method == 'POST':
        form = SurveyCreationForm(request.POST)
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
        form = SurveyCreationForm()
    return render(request, 'surveys/create_survey.html', {"form": form})


def survey_view(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)
    if survey.start_date > date.today() or survey.end_date < date.today() and not survey.admin==request.user:
        return render(request, 'surveys/survey_unavailable.html')
    if request.method == 'POST':
        # Handle survey response submission
        pass
    return render(request, 'surveys/survey_view.html', {'survey': survey})

@login_required
def user_surveys_list(request):
    user_surveys = Survey.objects.filter(admin=request.user)
    return render(request, 'surveys/user_surveys_list.html', {'user_surveys': user_surveys})

@login_required
def survey_edit(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)
    survey_questions = Question.objects.filter(survey=survey)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            # Create a Survey instance without saving it to the database
            question = form.save(commit=False)
            
            # Set the admin field to the currently logged-in user
            question.survey = survey
            
            # Save the instance to the database
            question.save()
            
            # Redirect to the same survey edit page to prevent form resubmission
            return redirect('survey_edit', survey_id=survey.id)
    else:
        form = QuestionForm()
    return render(request, 'surveys/survey_edit.html', {
        'survey': survey,
        'survey_questions': survey_questions,
        'question_form': form,
    })
    



@login_required
def survey_delete(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)
    if survey.admin == request.user:
        survey.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Not authorized'}, status=403)

@login_required
def question_delete(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if question.survey.admin == request.user:
        question.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Not authorized'}, status=403)
    
@login_required
def update_question_order(request):
    if request.method == 'POST':
        order = request.POST.getlist('order[]')
        for index, question_id in enumerate(order):
            Question.objects.filter(id=question_id).update(position=index)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)

@login_required
def survey_results(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)
# View to display a thank-you message after survey submission
def survey_thank_you(request):
    return HttpResponse("Thank you for completing the survey.")
