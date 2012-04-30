#TODO: put this file in a 'models' package
import MySQLdb as mdb
from DBConf import DBConf as dbc
import pdb
import traceback

class Feeditem:

    ''' returns feed items that contain all the tags in "tag_ids" '''
    #TODO add time span
    @staticmethod
    def findByTags(tag_ids, time1, time2):
        '''
            finds feeditems containing tags with tag_ids ids
        '''
        try:
            db = mdb.Connect(dbc.host, dbc.user, dbc.passwrd, dbc.db)
            c = db.cursor()
            
            count = 0
            sqlConds = ''
            for tag_id in tag_ids:
                sqlConds += '''item_tag.feeditem_id IN (SELECT item_tag.feeditem_id FROM feeditem_tag item_tag WHERE item_tag.tag_id = '%s')''' %(tag_id)
                count += 1
                if(count < len(tag_ids) ):
                    sqlConds+= ' AND '
            sql = '''SELECT * from feeditem WHERE `date` >=  '%s' AND `date` <= '%s' AND id IN (SELECT DISTINCT item_tag.feeditem_id FROM feeditem_tag item_tag WHERE %s)''' %(time1, time2, sqlConds)
            c.execute(sql)

            feeditems = c.fetchall()
            return feeditems 

        finally:
            print('error in  Feeditem#findByTags ')
            traceback.print_exception
            if db:
                db.commit()
                c.close()
                db.close()
