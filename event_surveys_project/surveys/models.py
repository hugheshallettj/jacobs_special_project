from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _ # this doesnt change the functionality of the code
from django.conf import settings # this imports the settings so that we can use our custom auth user model
from datetime import date, datetime

# Create your models here.
class Survey(models.Model):

    admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    date_created = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)
    

    class Meta:
        verbose_name = _("Survey") # the underscore is a translation key for django
        verbose_name_plural = _("Surveys")

    def __str__(self):
        return f"{self.title} | {self.start_date}"

    def get_absolute_url(self):
        return reverse("Survey_detail", kwargs={"pk": self.pk})
    
    def completion_count(self):
        return self.completions.count()
    
class Question(models.Model):
    
    QUESTION_TYPES = (
        ('MS', 'Multi Select'),
        ('SS','Single Select'),
        ('STX','Short Text'),
        ('LTX','Long Text'),
        ('DAT','Date'),
        ('INT', 'Integer'),
    )

    
    survey = models.ForeignKey(Survey, related_name='questions', on_delete=models.CASCADE)
    question_text = models.CharField(max_length=255)
    question_type = models.CharField(max_length=3, choices=QUESTION_TYPES)
    select_options = models.JSONField(null=True, default=list, blank=True)

    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")

    def __str__(self):
        return self.question_text

    def get_absolute_url(self):
        return reverse("Question_detail", kwargs={"pk": self.pk})
    
class SurveyCompletion(models.Model):
    
    survey = models.ForeignKey(Survey, related_name='completions', on_delete=models.CASCADE)
    completion_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _("Survey Completion")
        verbose_name_plural = _("Survey Completions")

    def __str__(self):
        return f"Completion of {self.survey.title} on {self.completion_date}"
    
class Response(models.Model):

    survey = models.ForeignKey(Survey, related_name='responses', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='responses', on_delete=models.CASCADE)
    answer = models.TextField()
    survey_completion = models.ForeignKey(SurveyCompletion, related_name='responses', on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Response")
        verbose_name_plural = _("Responses")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Response_detail", kwargs={"pk": self.pk})


