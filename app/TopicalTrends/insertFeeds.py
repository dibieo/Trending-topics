#! /usr/bin/python

#This file includes methods for inserting feeds into the database
#Feeds are inserted manually, but may be processed from a form or another input source in the future

import MySQLdb as mdb
from TopicalTrends.DBConf import DBConf as dbc

#soheilTODO we shuold only get the link, the title and description can be gotten from rss itself
#feeds = {
#"link" : "http://www.sciencenews.org/view/feed/type/news/name/articles.rss",
#"title" : "Science News",
#"description" : "News about science"
#}

# duplicates will be ignored at database insertion time (unique index is in use) 
feed_links = (
# random feeds
["http://news.yahoo.com/rss/"],
["http://news.cnet.com/2246-2_3-0.xml?tag=txt"],
["http://news.cnet.com/8300-13579_3-37.xml?tag=txt"],
["http://news.cnet.com/8300-13772_3-52.xml?tag=txt"],
["http://news.cnet.com/8300-5_3-0.xml?categoryId=2047&tag=txt"],
["http://news.cnet.com/8300-27083_3-247.xml?tag=txt"],
["http://news.cnet.com/8300-13578_3-38.xml?tag=txt"],
["http://news.cnet.com/8300-13860_3-56.xml?tag=txt"],
["http://news.cnet.com/8300-31021_3-260.xml?tag=txt"],
["http://news.cnet.com/8300-30685_3-264.xml?tag=txt"],
["http://news.cnet.com/8300-13772_3-52.xml?tag=txt"],
["http://news.cnet.com/8300-27080_3-245.xml?tag=txt"],
["http://news.cnet.com/8300-31001_3-261.xml?tag=txt"],
["http://news.cnet.com/8300-19882_3-250.xml?tag=txt"],
["http://news.cnet.com/8300-30684_3-265.xml?tag=txt"],
["http://news.cnet.com/8300-27076_3-248.xml?tag=txt"],
["http://news.cnet.com/8300-13577_3-36.xml?tag=txt"],
["http://www.sciencenews.org/view/feed/type/news/name/articles.rss"],
["http://www.physorg.com/rss-feed/"],
["http://feeds.feedburner.com/TechCrunch/"],
["http://www.jasonbrome.com/blog/index.rdf"],
["http://www.sciencenews.org/view/feed/label_id/2356/name/Atom_%2B_Cosmos.rss"],
["http://www.sciencenews.org/view/feed/label_id/2357/name/Body_%2B_Brain.rss"],
["http://www.sciencenews.org/view/feed/label_id/2362/name/Earth.rss"],
["http://www.sciencenews.org/view/feed/label_id/2337/name/Environment.rss"],
["http://www.sciencenews.org/view/feed/label_id/2363/name/Genes_%2B_Cells.rss"],
["http://www.sciencenews.org/view/feed/label_id/2364/name/Humans.rss"],
["http://www.sciencenews.org/view/feed/label_id/2365/name/Life.rss"],
["http://www.sciencenews.org/view/feed/label_id/2366/name/Matter_%2B_Energy.rss"],
["http://www.sciencenews.org/view/feed/label_id/2367/name/Molecules.rss"],
["http://www.sciencenews.org/view/feed/label_id/2/name/Other_Topics.rss"],
["http://www.sciencenews.org/view/feed/label_id/2347/name/Science_%2B_Society.rss"],
["http://www.sciencenews.org/view/feed/label_id/3/name/Science_News_For_Kids.rss"],

# tech feeds
["http://rss.sciam.com/sciam/technology"],
["http://rss.sciam.com/sciam/alternative-energy-technology"],
["http://rss.sciam.com/sciam/automotive-technology"],
["http://rss.sciam.com/sciam/communications"],
["http://rss.sciam.com/sciam/computing"],
["http://rss.sciam.com/sciam/consumer-electronics"],
["http://rss.sciam.com/sciam/energy-technology"],
["http://rss.sciam.com/sciam/topic/biometrics"],
["http://rss.sciam.com/sciam/topic/military-defense"],
["http://rss.sciam.com/sciam/topic/electrical-engineering"],
["http://rss.sciam.com/sciam/topic/fuel-cells"],
["http://rss.sciam.com/sciam/topic/military-defense"],
["http://rss.sciam.com/sciam/topic/green-technology"],
["http://rss.sciam.com/sciam/topic/how-things-work"],
["http://rss.sciam.com/sciam/topic/hydropower"],
["http://rss.sciam.com/sciam/topic/internet"],
["http://rss.sciam.com/sciam/topic/medical-nanotechnology"],
["http://rss.sciam.com/sciam/topic/nanotechnology"],
["http://rss.sciam.com/sciam/topic/optics"],
["http://rss.sciam.com/sciam/topic/privacy"],
["http://rss.sciam.com/sciam/topic/quantum-computing"],
["http://rss.sciam.com/sciam/topic/artificial-intelligence"],
["http://rss.sciam.com/sciam/topic/security"],
["http://rss.sciam.com/sciam/topic/solar-power"],
["http://rss.sciam.com/sciam/topic/spacecraft"],
["http://rss.sciam.com/sciam/topic/tidal-power"],
["http://rss.sciam.com/sciam/topic/spacecraft"],
["http://rss.sciam.com/sciam/topic/tidal-power"],
["http://rss.sciam.com/sciam/topic/transportation"],
["http://rss.sciam.com/sciam/topic/wind-power"],
["http://feeds.newscientist.com/tech"],
["http://feeds.newscientist.com/tech"],
["http://feeds.nytimes.com/nyt/rss/Technology"],
["http://feeds.nature.com/news/rss/news_s16?format=xml"],
["http://www.npr.org/rss/rss.php?id=1019"],
["http://feeds.technologyreview.com/technology_review_top_stories"],
["http://feeds.technologyreview.com/technology_review_computing"],
["http://feeds.technologyreview.com/technology_review_web"],
["http://feeds.technologyreview.com/technology_review_communications"],
["http://feeds.technologyreview.com/technology_review_energy"],
["http://feeds.technologyreview.com/technology_review_materials"],
["http://feeds.technologyreview.com/technology_review_biotech"],
["http://feeds.technologyreview.com/technology_review_biztech"],
["http://feeds.technologyreview.com/technology_review_video"],
["http://feeds.technologyreview.com/technology_review_blog_editors"],
["http://feeds.technologyreview.com/technology_review_blog_mims"],
["http://feeds.technologyreview.com/technology_review_job_postings"],
["http://feeds.technologyreview.com/technology_review_audio_top_stories"],
["http://feeds.technologyreview.com/technology_review_audio_computing"],
["http://feeds.technologyreview.com/technology_review_audio_web"],
["http://feeds.technologyreview.com/technology_review_audio_communications"],
["http://feeds.technologyreview.com/technology_review_audio_energy"],
["http://feeds.technologyreview.com/technology_review_audio_biotech"],
["http://feeds.technologyreview.com/technology_review_audio_biztech"],
["http://rss.cnn.com/rss/cnn_tech.rss"],
["http://feeds.reuters.com/reuters/technologyNews"],
["http://www.nanowerk.com/nwfeedres.xml"],
["http://www.nanowerk.com/nwfeedres.xml"],
["http://www.geek.com/articles/news/feed/"],
["http://www.geek.com/articles/feeds/"],
["http://feeds.ziffdavisenterprise.com/RSS/publishnews.xml"],
["http://enterprise.ziffdavisenterprise.com/RSS/enterprise.opml"],
["http://feeds.nytimes.com/nyt/rss/Technology"],
["http://bits.blogs.nytimes.com/feed/"],
["http://feeds.nytimes.com/nyt/rss/business-computing"],
["http://feeds.nytimes.com/nyt/rss/companies"],
["http://feeds.nytimes.com/nyt/rss/internet"],
["http://feeds.nytimes.com/nyt/rss/PersonalTech"],
["http://feeds.nytimes.com/nyt/rss/start-ups"],
["http://feeds2.feedburner.com/ziffdavis/pcmag/breakingnews"],
["http://www.computerweekly.com/rss/Financial-services-IT-news.xml"],
["http://www.computerweekly.com/rss/Public-sector-IT-news.xml"],
["http://www.computerweekly.com/rss/IT-careers-and-IT-skills.xml"],
["http://www.computerweekly.com/rss/IT-management.xml"],
["http://www.computerweekly.com/rss/Internet-technology.xml"],
["http://www.computerweekly.com/rss/Mobile-technology.xml"],
["http://www.computerweekly.com/rss/Networking-and-communication.xml"],
["http://www.computerweekly.com/rss/IT-security.xml"],
["http://www.computerweekly.com/rss/IT-services-and-outsourcing.xml"],
["http://www.computerweekly.com/rss/Enterprise-software.xml"],
["http://www.computerweekly.com/rss/IT-hardware.xml"],
["http://www.computerweekly.com/rss/Latest-IT-news.xml"],
["http://feeds.technologyreview.com/technology_review_computing"],
["http://feeds.technologyreview.com/technology_review_web"],
["http://feeds.technologyreview.com/technology_review_communications"],
["http://feeds.technologyreview.com/technology_review_energy"],
["http://feeds.technologyreview.com/technology_review_materials"],
["http://feeds.technologyreview.com/technology_review_biotech"],
["http://feeds.technologyreview.com/technology_review_biztech"],
["http://feeds.technologyreview.com/technology_review_blog_mims"],
["http://feeds.technologyreview.com/technology_review_blog_editors"],
["http://feeds.technologyreview.com/technology_review_top_stories"],

# general science feeds
["http://rss.sciam.com/ScientificAmerican-News"],
["http://www.npr.org/rss/rss.php?id=1007"],
["http://rss.sciam.com/sciam/basic-science"],
["http://rss.sciam.com/sciam/biology"],
["http://rss.sciam.com/sciam/chemistry"],
["http://rss.sciam.com/sciam/math"],
["http://rss.sciam.com/sciam/math"],
["http://rss.sciam.com/sciam/physics"],
["http://rss.sciam.com/sciam/earth-and-environment"],
["http://rss.sciam.com/sciam/everyday-science"],
["http://rss.sciam.com/sciam/science-education"],
["http://rss.sciam.com/sciam/topic/aging-and-the-elderly"],
["http://rss.sciam.com/sciam/topic/animals"],
["http://rss.sciam.com/sciam/topic/bacteria-and-viruses"],
["http://rss.sciam.com/sciam/topic/bacteria-and-viruses"],
["http://rss.sciam.com/sciam/topic/biodiversity"],
["http://rss.sciam.com/sciam/topic/cloning"],
["http://rss.sciam.com/sciam/topic/earth-science"],
["http://rss.sciam.com/sciam/topic/fractals"],
["http://rss.sciam.com/sciam/topic/genetic-engineering"],
["http://rss.sciam.com/sciam/topic/genetics"],
["http://rss.sciam.com/sciam/topic/how-things-work"],
["http://rss.sciam.com/sciam/topic/large-hadron-collider"],
["http://rss.sciam.com/sciam/topic/microbiology"],
["http://rss.sciam.com/sciam/topic/natural-disasters"],
["http://rss.sciam.com/sciam/topic/oceanography"],
["http://rss.sciam.com/sciam/topic/optical-physics"],
["http://rss.sciam.com/sciam/topic/plants"],
["http://rss.sciam.com/sciam/topic/quantum-computing"],
["http://rss.sciam.com/sciam/topic/science-ethics"],
["http://rss.sciam.com/sciam/topic/weather"],
["http://www.sciencenews.org/view/feed/name/all.rss"],
["http://feeds.nytimes.com/nyt/rss/Science"],
["http://feeds.nytimes.com/nyt/rss/Environment"],
["http://feeds.nytimes.com/nyt/rss/Space"],
["http://feeds.feedburner.com/bit-tech/all?format=xml"],
["http://www.infoworld.com/taxonomy/term/3209/feed"],
["http://www.infoworld.com/taxonomy/term/2533/feed"],
["http://www.infoworld.com/taxonomy/term/21735/feed"],
["http://www.infoworld.com/taxonomy/term/21667/feed"],
["http://www.infoworld.com/taxonomy/term/2532/feed"],
["http://www.infoworld.com/taxonomy/term/2535/feed"],
["http://www.infoworld.com/taxonomy/term/21441/feed"],
["http://www.infoworld.com/taxonomy/term/2536/feed"],
["http://www.infoworld.com/taxonomy/term/21669/feed"],
["http://www.infoworld.com/taxonomy/term/3215/feed"],
["http://www.infoworld.com/taxonomy/term/3212/feed"],
["http://www.infoworld.com/taxonomy/term/3210/feed"],
["http://www.infoworld.com/taxonomy/term/21668/feed"],
["http://www.infoworld.com/taxonomy/term/21669/feed"],
["http://www.infoworld.com/taxonomy/term/3213/feed"],
["http://www.infoworld.com/taxonomy/term/3217/feed"],
["http://www.infoworld.com/taxonomy/term/3218/feed"],
["http://www.infoworld.com/taxonomy/term/3219/feed"],  
)

#sql =  "INSERT INTO source(title, \
#       description, link, date) \
#       VALUES ('%s', '%s', '%s', '%s' )" % \
#       (feeds['title'], feeds['description'], feeds['link'], datetime.datetime.now())
try:    
    con = mdb.connect(dbc.host, dbc.user, dbc.passwrd, dbc.db, charset="utf8")
    cursor = con.cursor()

    #insert the feed links and into source table #soheilTODO: have to add link title, description and some date later on when we are actually reading the feed
    for link in feed_links:
        print(link)
        cursor.executemany("""INSERT IGNORE INTO source (link) VALUES (%s)""", [(link)])

    con.commit()
    con.close()
    print "Feeds inserted into database source table..."
except RuntimeError as error:
    print error


