from django import forms
from .models import Assignment

class DateInput(forms.DateInput):
    input_type='date'

class AssignmentCreateForm(forms.ModelForm):
    #course=forms.ModelChoiceField(queryset=Course.objects.all(),empty_label=None)
    class Meta:
        model=Assignment
        widgets={'expires_on':DateInput()}
        fields=['content','course','subject','expires_on','pdf','assignment_marks']