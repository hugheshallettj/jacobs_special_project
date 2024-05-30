from django.contrib import admin
from django.urls import path, include
from surveys import views as survey_views

urlpatterns = [
    path('create-survey/', survey_views.create_survey, name='create_survey'),

    # path('survey/<str:link>/', survey_views.survey_view, name='survey_view'),
    # path('results/<int:survey_id>/', survey_views.survey_results, name='survey_results'),
]
