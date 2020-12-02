import mysql.connector
import json


class Conn_db:
    """
        Use this class for connecting to DB with
        automatic close.
    """
    db_conf     = {}
    def __init__(self):
        self.conn = mysql.connector.connect(**Conn_db.db_conf)

    @staticmethod 
    def load_conf():
        #'C:\\Users\\alexa\\PycharmProjects\\Shop\\db_conf.json'
        with open('db_conf.json') as f:
            Conn_db.db_conf = json.load(f) 

    def __enter__(self):
        return self.conn
    
    def __exit__(self, type, value, traceback):
        # TODO: How are exceptions handled?
        self.conn.close()
