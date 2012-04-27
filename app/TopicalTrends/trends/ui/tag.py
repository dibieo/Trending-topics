#TODO put in models folder
import MySQLdb as mdb
from DBConf import DBConf as dbc
import pdb
import traceback
class Tag:
    @staticmethod
    def findByTitle(title):
        try:
            db = mdb.Connect(dbc.host,
                                 dbc.user,
                                 dbc.passwrd,
                                 dbc.db)
            c = db.cursor()
            c.execute('''SELECT * FROM tag WHERE title = %s ''' , (title) )
            rows = c.fetchall()
            return rows
        finally:
            traceback.print_exception
            if db:
                db.commit()
                c.close()
                db.close()