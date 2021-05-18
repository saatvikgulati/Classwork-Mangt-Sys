from .models import Answer,Reason
from django import forms
class AnswerCreateForm(forms.ModelForm):
    class Meta:
        model=Answer
        fields=['content','pdf']
class MarksForm(forms.ModelForm):
    class Meta:
        model=Answer
        fields=['marks']

class AnswerUpdateForm(forms.ModelForm):
    class Meta:
        model=Answer
        fields=['content','pdf']

class ReasonForm(forms.ModelForm):
    class Meta:
        model=Reason
        fields=['reason']