__author__ = 'Alfredo Saglimbeni'
from django.db import models
from django import forms
from datetimewidget.widgets import DateTimeWidget
from django.forms.widgets import HiddenInput
from django.test import TestCase
# Test della resa del template con tutte le opzioni.
# Test della form
# Test del modello con la form

class testModel (models.Model):
    datetime = models.DateTimeField(null=False)


class testForm(forms.ModelForm):
    class Meta:
        model = testModel
        widgets = {
            'datetime': DateTimeWidget(attrs={ 'id': "datetime1"}, to="datetimeto"),
            'datetimeto': HiddenInput()
        }

def freeCropView(request):

    if request.method == 'POST': # If the form has been submitted...

        form = testForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            new_event = form.save()
    else:
        form = testForm()

    return render(request, 'example/example.html', {
        'form': form,
        })

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)
