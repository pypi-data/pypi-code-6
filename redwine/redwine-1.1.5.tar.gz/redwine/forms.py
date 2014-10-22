from django import forms
from .models import Penalty

class newPenaltyForm(forms.ModelForm):
    reason = forms.CharField(help_text="Begrunnelse for vinstraff")
    amount = forms.IntegerField( initial=0)
    giver = forms.IntegerField(widget=forms.HiddenInput())
    to = forms.IntegerField(widget=forms.HiddenInput())

    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Penalty
        fields = [reason, amount, giver, to]
