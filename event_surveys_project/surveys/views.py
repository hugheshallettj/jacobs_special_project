from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Survey, Question, Response, SurveyCompletion
from datetime import datetime, date
from django.forms import modelform_factory
from .forms import SurveyCreationForm, QuestionForm, generate_survey_form
from django.http import JsonResponse, HttpResponse
import json
from collections import Counter
import logging
logger = logging.getLogger(__name__)

    
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

# View to handle the display and submission of the survey
def survey_view(request, survey_id):
    # Get the survey object, or return a 404 error if not found
    survey = get_object_or_404(Survey, id=survey_id)
    
    # Generate a dynamic form for the survey based on its questions
    SurveyForm = generate_survey_form(survey)
    
    if request.method == 'POST':
        # Form submission handling
        form = SurveyForm(request.POST)
        if form.is_valid():
            # Create a SurveyCompletion object to track the completion of the survey
            completion = SurveyCompletion.objects.create(survey=survey)
            # Iterate over all questions in the survey and save the responses
            for question in survey.questions.all():
                response = Response(
                    survey=survey,
                    question=question,
                    answer=form.cleaned_data[f'question_{question.id}'],
                    survey_completion=completion
                )
                response.save()
            # Redirect to a thank-you page after successfully saving responses
            return redirect('survey_thank_you')
    else:
        # If the request method is GET, display an empty form
        form = SurveyForm()
    
    # Render the survey form
    return render(request, 'surveys/survey_view.html', {
        'survey': survey,
        'form': form,
    })

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
    """
    View to display survey results.

    Args:
        request (HttpRequest): The HTTP request object.
        survey_id (int): The ID of the survey to display results for.

    Returns:
        HttpResponse: An HTTP response containing the survey results page.

    Raises:
        Http404: If the specified survey does not exist.

    Ensures:
        The current user is the admin of the survey.
        Fetches all questions and responses for the survey.
        Calculates statistics for each question based on its type.
        Renders the survey results page with the survey, questions, responses, and statistics.
    """
    # Get the survey object, or return a 404 error if not found
    survey = get_object_or_404(Survey, id=survey_id)
    
    # Ensure the current user is the admin of the survey
    if survey.admin != request.user:
        return redirect('home')  # Redirect to home if not authorized

    # Fetch all questions and responses for the survey
    questions = survey.questions.all()
    responses = survey.responses.all()

    # Calculate statistics
    stats = {}
    for question in questions:
        question_responses = responses.filter(question=question)
        if question.question_type in ['MS', 'SS']:
            # For multi-select and single-select questions, count occurrences of each option
            all_answers = []
            for response in question_responses:
                answer = response.answer
                if question.question_type == 'MS':
                    try:
                        answer = json.loads(answer)  # Parse JSON list
                    except json.JSONDecodeError as e:
                        logger.error(f"Error decoding JSON for response ID {response.id}: {e}")
                        continue  # Skip this response if it's invalid
                else:
                    answer = [answer]
                all_answers.extend(answer)
            options_count = dict(Counter(all_answers))
            stats[question.id] = options_count
        elif question.question_type == 'INT':
            # For integer questions, calculate average, min, max
            int_answers = [int(response.answer) for response in question_responses]
            if int_answers:
                stats[question.id] = {
                    'average': sum(int_answers) / len(int_answers),
                    'min': min(int_answers),
                    'max': max(int_answers),
                }
        else:
            # For text responses, just count the number of responses
            stats[question.id] = len(question_responses)
    
    return render(request, 'surveys/survey_results.html', {
        'survey': survey,
        'questions': questions,
        'responses': responses,
        'stats': stats,
    })

# View to display a thank-you message after survey submission
def survey_thank_you(request):
    return HttpResponse("Thank you for completing the survey.")
