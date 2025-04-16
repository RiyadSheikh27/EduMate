from django import forms
from django.forms import widgets, DateInput
from . models import *

# Creating form for Notes
class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ['title','description']

# Creating form for Homework
class DateInput(forms.DateInput):
    input_type = 'date'

class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        widgets = {'due':DateInput()}
        fields = ['subject','title','description','due','is_finished']

# Creating form for Youtube
class DashboardForm(forms.Form):
    text = forms.CharField(max_length=100,label="Enter Your Search: ")

# Creating form for To-Do
class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title','is_finished']
