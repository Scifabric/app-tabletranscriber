import psycopg2
from app_tt.core import app


class Connect:
    """
    Class to connect to a postgresql server
    """
    global cur
    global conn

    def __init__(self):
        try:
            self.conn = psycopg2.connect(app.config['TT_DB_URI'])

            self.cur = self.conn.cursor

        except:
            print "Error to connect database"

    def __del__(self):
        print "Conection finished"
        del self


class Model:
    """
    Class that make calls to tt4 db
    """

    def __init__(self):
        print

    def insert_db(self, table, **kwargs):
        """
        Insert row into a table of the db
        :params table: table to insert the row
        :params **kwargs: values to be inserted
        :returns: if the insertion was ok
        :rtype: bool
        """

        db_conection = Connect()
        conn = db_conection.conn
        qry = db_conection.cur()
        try:
            qry.execute("insert into %s %s values%s;" %
                        (table, str(tuple(kwargs.keys())).replace("\'", ""),
                        str(tuple(kwargs.values()))))
            conn.commit()
            conn.close()
            return True
        except Exception, e:
            print str(e)
            return False

    def del_where(self, *args):
        db_connection = Connect()
        conn = db_connection.conn
        qry = db_connection.cur()

        try:
            qry.execute("delete from %s x where x.%s='%s';" %
                        (args[0], args[1], args[2]))
            conn.commit()
            conn.close()
            return True
        except Exception, e:
            print str(e)
            return False

    def get_cells(self, book_id, page, table):
        db_connection = Connect()
        qry = db_connection.cur()

        try:
            qry.execute("SELECT c.x0, c.y0, c.x1, c.y1, c.text\
                        FROM cell c, book b, page p, page_table t\
                        WHERE b.id='%s' and p.id=%d and t.id=%d" %
                        (book_id, page, table))
        except Exception, e:
            print str(e)

        return qry.fetchall()

    def get_table_url(self, book_id, page, table):
        db_connection = Connect()
        qry = db_connection.cur()

        try:
            qry.execute("SELECT t.url \
                        FROM page_table t, book b, page p \
                        WHERE b.id='%s' and p.id=%d and t.id=%d" %
                        (book_id, page, table))
        except Exception, e:
            print str(e)
            return ""

        return qry.fetchall()[0][0]

    def __del__(self):
        del self
