from django import forms
# from django.contrib.auth.forms import AuthenticationForm 

class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)
    
class GradeForm(forms.Form):
    RollNumber = forms.IntegerField()
    Course = forms.CharField(max_length=10)
    Grade = forms.CharField(max_length=2)
