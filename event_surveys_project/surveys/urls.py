from django.contrib import admin
from django.urls import path, include
from surveys import views as survey_views

urlpatterns = [
    path('create-survey/', survey_views.create_survey, name='create_survey'),

    path('survey/<int:survey_id>/', survey_views.survey_view, name='survey_view'),
    path('results/<int:survey_id>/', survey_views.survey_results, name='survey_results'),
    path('my-surveys/', survey_views.user_surveys_list, name='user_surveys_list'),
    path('survey-edit/<int:survey_id>/', survey_views.survey_edit, name='survey_edit'),
    path('question/<int:question_id>/delete', survey_views.question_delete, name="question_delete"),
    path("survey/<int:survey_id>/delete", survey_views.survey_delete, name='survey_delete'),
    path('update-question-order/', survey_views.update_question_order, name='update_question_order'),
    path('survey-finished', survey_views.survey_thank_you, name="survey_thank_you")

]
