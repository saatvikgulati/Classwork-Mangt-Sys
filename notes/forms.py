from django import forms
from .models import Notes
class NoteCreationForm(forms.ModelForm):
    class Meta:
        model=Notes
        fields=['description','attachement']