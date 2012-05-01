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
import urllib
from MyConf import MyConf as params

class searchForm(forms.Form):
    input = forms.CharField()
    
            
# Create your views here.
def index(request):
    freqTopicSets = ''
    query = ''
    freqTopics = ''


    time2 = datetime.datetime.now() 

    time1 = time2 - timedelta(days=1)
    
    print('timing: before freqTopics')
    print(datetime.datetime.now())

    freqTopics = Analysis.getFreqTopics(time1, time2, minFreq=0, k=params.maxFreqTopics)

    time22 = time1
    time11 = time22 - timedelta(days=2*params.days) # to be used to find the old frequencies of current hot topics
    freqTopics = Analysis.getTopicsFrequencyChanges(freqTopics, time11, time22) # find trendings for freq topic sets
    #pdb.set_trace() how to do debugging

    #print('timing: after freqTopics')
    #print(datetime.datetime.now())


    #if request.method == 'GET' : # If form is submitted
    form = searchForm(request.GET)
    tag = ''
    linkSets = []
    topicSet_linkSets = []
    if form.is_valid():        
        if(request.GET.has_key('input')):

            print('timing: before getFreqTopicSets')
            print(datetime.datetime.now())
            freqTopicSets = Analysis.getFreqTopicSets(request.GET['input'], time1, time2) 
            print('timing: after getFreqTopicSets')
            print(datetime.datetime.now())
   
            for topicSet in freqTopicSets:
                tag_ids = []
                links = []
                #cuz example topicSet for a query like Microsoft  = (['Blog', 'Android'], 4) so make into ['Blog', 'Android', 'Microsoft']
                topics = topicSet[0]
                topics.append(str(request.GET['input']))
                
                for topic in topics: 
                    tag = Tag.findByTitle(topic) #findByTitle returns multiple rows representing multiple tags, so the last [0][0] means get the first attribute (ie id) or the first tag in rows
                    #pdb.set_trace()
                    tag_id = tag[0][0]
                    tag_id = str(tag_id).strip('L') #seems like we get id's like '3167L' strip the L
                    tag_ids.append(tag_id)
            
                #print("in views.py:")
                print(topicSet)
                #pdb.set_trace()
                
                #print('====')
                #print(datetime.datetime.now())
                feeditems = feeditem.Feeditem.findByTags(tag_ids, time1, time2)
                #print(datetime.datetime.now())

                for item in feeditems:
                    print item[1]
                    t1 = unicode(unicode(item[1],'utf-8', errors='ignore')) # to ignore non utf-8 chars 
                    t2 = unicode(item[3])

                    links.append((t1,t2))
                linkSets.append(copy.copy(links))
                
                topicSet_linkSets = zip(freqTopicSets, linkSets)
            
    else:
        form = searchForm()
    
    if(request.GET.has_key('input')):
        query = request.GET['input']
    else:
        qeury = None
    return render_to_response('ui/index.html', {'form' : form, 'freqTopicSets':freqTopicSets, 'query':
query, 'freqTopics':freqTopics, 'linkSets':linkSets, 'topicSet_linkSets':topicSet_linkSets[::-1] })

#This gets all the hot topics
#This action is called via an Ajax toggle of the hot trends list
def topics(request):
    output = ''
    if (request.GET.has_key('sort')):
        freqTopics = ''
        output = request.GET['sort']
        time_diff = None      #The time difference
        if output == 'today':
            time_diff = 1
        elif output == 'lastweek':
            time_diff = 7
        else:
            time_diff = 30
        time2 = datetime.datetime.now()
        time1 = time2 - timedelta(days=time_diff)
    freqTopics = Analysis.getFreqTopics(time1, time2, minFreq=10, k=params.maxFreqTopics)
    time22 = time1
    time11 = time22 - timedelta(days=time_diff) # to be used to find the old frequencies of current hot topics
    print time1
    print time2
    print time11
    print time22    
    freqTopics = Analysis.getTopicsFrequencyChanges(freqTopics, time11, time22) # find trendings for freq topic sets
    return render_to_response('ui/topics.html', {'freqTopics' : freqTopics})
