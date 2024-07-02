from django.contrib import admin
from .models import Survey, Question, Response

admin.site.register([Survey, Question, Response])
# Register your models here.
