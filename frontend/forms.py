from django import forms

from api.models import Package


class updateContribForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = ('authors',)
        widgets = {
            'authors': forms.CheckboxSelectMultiple
        }
