#Django views
#The Views represent the Controller of MVC architecture in Djago
#It has functions which instantiate the models and pass results to
#the views

from django.shortcuts import render_to_response
from django import forms
from Analysis import Analysis

class searchForm(forms.Form):
    input = forms.CharField()

# Create your views here.
def index(request):
    value = ''
    if request.method == 'GET' : # If form is submitted
        form = searchForm(request.GET)
        if form.is_valid():
            results = Analysis.getFreqTopics(3, 0)
            value = Analysis.getFreqfeeditemTopics(2, 1, request.GET['input']) #Store result to be passed to the view
        else:
            form = searchForm()
    return render_to_response('ui/index.html', {'form' : form, 'value' : value,})
