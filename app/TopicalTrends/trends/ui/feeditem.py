#TODO: put this file in a 'models' package
import MySQLdb as mdb
from DBConf import DBConf as dbc
import pdb
import traceback

class Feeditem:

    ''' returns feed items that contain all the tags in "tag_ids" '''
    #TODO add time span
    @staticmethod
    def findByTags(tag_ids):
        try:
            db = mdb.Connect(dbc.host, dbc.user, dbc.passwrd, dbc.db)
            c = db.cursor()
            
#the final query will be something like this:
#SELECT * FROM feeditem WHERE feeditem.id IN (SELECT ft1.feeditem_id FROM 
#THE fromClause:
#feeditem_tag ft1, feeditem_tag ft2, feeditem_tag ft3 

#WHERE
#THE whereClause1:
#ft1.tag_id = '4916' AND ft2.tag_id = '4925' AND ft3.tag_id = '4917' AND 

#THE WHERE2 CLAUSE:
#ft1.feeditem_id = ft2.feeditem_id AND ft1.feeditem_id = ft3.feeditem_id
#)

            fromClause = ''
            whereClause1 = ''
            whereClause2 = ''
            for i in range(len(tag_ids)):
                fromClause += 'feeditem_tag ft'+str(i)+', '
                whereClause1 += 'ft'+str(i)+'.tag_id = '+tag_ids[i]+' AND '
                if(i != len(tag_ids)-1 ):
                    whereClause2 += 'ft'+str(i)+'.feeditem_id = ft'+str(i+1)+'.feeditem_id AND '
            
            #remove that last extra coma
            fromClause = fromClause[0:-2]
            #remove the last extra AND
            whereClause2 = whereClause2[0:-4]
            
            #sql = "SELECT * FROM feeditem WHERE feeditem.id IN (SELECT ft1.feeditem_id FROM"+ +fromClause+" WHERE "+whereClause1+whereClause2+")"
            sql = '''SELECT * FROM feeditem WHERE feeditem.id IN (SELECT ft0.feeditem_id FROM %s WHERE %s %s)''' %(fromClause, whereClause1, whereClause2)
            
          # count = 0
          # sqlConds = ''
          # for tag_id in tag_ids:
          #     sqlConds += '''item_tag.feeditem_id IN (SELECT item_tag.feeditem_id FROM feeditem_tag item_tag WHERE item_tag.tag_id = '%s')''' %(tag_id)
          #     count += 1
          #     if(count < len(tag_ids) ):
          #         sqlConds+= ' AND '
          #sql = '''SELECT * from feeditem WHERE id IN (SELECT DISTINCT item_tag.feeditem_id FROM feeditem_tag item_tag WHERE %s)''' %(sqlConds)
            c.execute(sql)

            feeditems = c.fetchall()
            return feeditems 

        finally:
            traceback.print_exception
            if db:
                db.commit()
                c.close()
                db.close()
