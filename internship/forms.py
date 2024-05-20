from django import forms
from .models import Stage

class InternshipProposalForm(forms.ModelForm):
    class Meta:
        model = Stage
        fields = ['typeStg', 'societe', 'duree', 'sujet', 'contactInfo', 'specialite']
