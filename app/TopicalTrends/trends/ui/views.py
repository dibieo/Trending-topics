#Django views
#The Views represent the Controller of MVC architecture in Djago
#It has functions which instantiate the models and pass results to
#the views

from django.shortcuts import render_to_response
from django import forms
from Analysis import Analysis
import datetime
from datetime import timedelta
#from datetime import date, timedelta
import feeditem
from tag import Tag
import pdb
import copy

class searchForm(forms.Form):
    input = forms.CharField()

# Create your views here.
def index(request):
    freqTopicSets = ''
    query = ''
    freqTopics = ''

    time2 = datetime.datetime.now()  # Get current time stamp
   # time2 = datetime.date(2012, 4, 29)
    time1 = time2 - timedelta(days=8) # Find trends from the last 8 days.
    freqTopics = Analysis.getFreqTopics(time1, time2, minFreq=10, k=0)
    #pdb.set_trace() how to do debugging

    #if request.method == 'GET' : # If form is submitted
    form = searchForm(request.GET)
    tag = ''
    linkSets = []
    topicSet_linkSets = []
    if form.is_valid():        
        if(request.GET.has_key('input')):
            freqTopicSets = Analysis.getFreqTopicSets(request.GET['input']) 
   
            for topicSet in freqTopicSets:
                tag_ids = []
                links = []
                #cuz example topicSet for a query like Microsoft  = (['Blog', 'Android'], 4) so make into ['Blog', 'Android', 'Microsoft']
                topics = topicSet[0]
                topics.append(request.GET['input'])
                
                for topic in topics: 
                    tag = Tag.findByTitle(topic) #findByTitle returns multiple rows representing multiple tags, so the last [0][0] means get the first attribute (ie id) or the first tag in rows
                    #pdb.set_trace()
                    tag_id = tag[0][0]
                    tag_id = str(tag_id).strip('L') #seems like we get id's like '3167L' strip the L
                    tag_ids.append(tag_id)
            
                print(topicSet)
                #pdb.set_trace()
                feeditems = feeditem.Feeditem.findByTags(tag_ids)
                for item in feeditems:
                    links.append((item[1],item[3]))
                linkSets.append(copy.copy(links))
                
                topicSet_linkSets = zip(freqTopicSets, linkSets)
            
    else:
        form = searchForm()
    
    if(request.GET.has_key('input')):
        query = request.GET['input']
    else:
        qeury = None
    return render_to_response('ui/index.html', {'form' : form, 'freqTopicSets':freqTopicSets, 'query':
query, 'freqTopics':freqTopics, 'linkSets':linkSets, 'topicSet_linkSets':topicSet_linkSets })
