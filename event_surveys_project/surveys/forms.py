from django import forms
from .models import Survey, Question, Response


class SurveyCreationForm(forms.ModelForm):
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

class SurveyResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['answer']

def generate_survey_form(survey):
    class SurveyForm(forms.Form):
        def __init__(self, *args, **kwargs):
            super(SurveyForm, self).__init__(*args, **kwargs)
            for question in survey.questions.all():
                if question.question_type == 'MS' or question.question_type == 'SS':
                    choices = [(opt, opt) for opt in question.select_options]
                    if question.question_type == 'MS':
                        self.fields[f'question_{question.id}'] = forms.MultipleChoiceField(
                            choices=choices, widget=forms.CheckboxSelectMultiple, label=question.question_text)
                    else:
                        self.fields[f'question_{question.id}'] = forms.ChoiceField(
                            choices=choices, widget=forms.RadioSelect, label=question.question_text)
                elif question.question_type == 'STX':
                    self.fields[f'question_{question.id}'] = forms.CharField(label=question.question_text, widget=forms.TextInput)
                elif question.question_type == 'LTX':
                    self.fields[f'question_{question.id}'] = forms.CharField(label=question.question_text, widget=forms.Textarea)
                elif question.question_type == 'DAT':
                    self.fields[f'question_{question.id}'] = forms.DateField(label=question.question_text, widget=forms.DateInput(attrs={'type': 'date'}))
                elif question.question_type == 'INT':
                    self.fields[f'question_{question.id}'] = forms.IntegerField(label=question.question_text)
    return SurveyForm

