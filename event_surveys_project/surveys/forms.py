from django import forms
from .models import Survey, Question


class SurveyForm(forms.ModelForm):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Survey
        exclude = ["admin"]

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        exclude = ["survey"]
        widgets = {
            'select_options': forms.HiddenInput(),
            'position': forms.HiddenInput(),
            
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['select_options'].required = False
