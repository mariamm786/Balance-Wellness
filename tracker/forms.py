from django import forms
from .models import SymptomLog

class SymptomLogForm(forms.ModelForm):
    class Meta:
        model = SymptomLog
        fields = ['symptom', 'severity']
        widgets = {
            'symptom': forms.TextInput(attrs={'placeholder': 'Enter symptom'}),
            'severity': forms.NumberInput(attrs={'min': 1, 'max': 5}),
        }