# -*- coding: utf-8 -*-
import urllib
from xml.dom import minidom #got the idea from http://developer.yahoo.com/python/python-xml.html
import MySQLdb

#uses the services described here: http://wdm.cs.waikato.ac.nz:8080/services/?suggest

baseUrl = "http://wikipedia-miner.cms.waikato.ac.nz/services/"

#uses the wikify service    
def getAllTopics(textToWikify):
	#call wikify
	url = baseUrl + 'wikify?source='
	dom = minidom.parse(urllib.urlopen (url + textToWikify))
	print(dom)
	print(url+ textToWikify)
	topics = dom.getElementsByTagName('detectedTopic')
	
	#print tsgs to console
	for topic in topics:
		topic_string = topic.getAttribute('title')
		print(topic_string)
		
	#store results in db
	
	
	return topics
	
def getSortedPairwiseRelatednesses(text):
	
	url = 'compare?ids1='
	topicDifferences = []
	allTopics = getAllTopics(text)
	
	for topic in allTopics:
		url = url + topic.getAttribute('id') + ','
	
	#get rid of the extra comma at the end
	url = url[:-1]
	url = url + '&ids2='
	for topic in allTopics:
		url = url + topic.getAttribute('id') + ','
	url = url[:-1]
	url = url+'&titles'
	
	#soheilTodo delete later
	print(baseUrl + url)
	#use the compare service, with many to many topic comparison
	dom = minidom.parse(urllib.urlopen(baseUrl + url))
	
	topicRelatednesses = dom.getElementsByTagName("Measure")
	
	sortedRelatednesses = sorted(topicRelatednesses, key = lambda measure:measure.firstChild.nodeValue)
	printComparisonResults(sortedRelatednesses)
	return sortedRelatednesses
	
def printComparisonResults(comparisons):
	for c in comparisons:		
		print("t1:"+c.getAttribute('highTitle')+" t2:"+c.getAttribute('lowTitle')+" relatedness measure:"+ c.firstChild.nodeValue)
		
def getFileTopics(filePath):
	f = open(filePath)
	text = ""
	for line in f:
		text = text + line
		
	getSortedPairwiseRelatednesses(text)
	
#here's how this method works:
#what's passed in is a list of topics compared pairwise and sorted based on the relatedness of the topic pairs
#the topic pairs with the highest levels of relatedness are considered to be the cores or seeds from which the topic set will be grown
# for each topic not already inside the selected topics set
# sum relatedness to all topics already selected
# the topic with the greatest sum is our candidate for inclusion in the set
# we can divide this by some function of the number of topics already in the set to punish for size increase  
#def growTopicSet(sortedPairwiseRelatednesses, topics):
	#alreadySelectedTopics = []
	#alreadySelectedTopics[0] =  sortedPairwiseRelatednesses[]  #note development has stopped right here, uncommenting this will give you a bug due to empty []
	
	
	
	
	
	
# 	<WikipediaMiner service="/services/compare">
#	<Request ids1="17362" ids2="711147,89074,89073" titles="true"/>
#	<Response>
#   <Measures>
#	<Measure highId="89073" highTitle="Kea" lowId="17362" lowTitle="Kiwi">0.721</Measure>
#	<Measure highId="89074" highTitle="Kakapo" lowId="17362" lowTitle="Kiwi">0.789</Measure>
#	<Measure highId="711147" highTitle="Takahē" lowId="17362" lowTitle="Kiwi">0</Measure>
#	</Measures>
#	</Response>
#	</WikipediaMiner>

	 
		
	
		
	
			
			
		
	

			
		
		
		
		
        
