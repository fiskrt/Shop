import mysql.connector


class Conn_db():
    
    def __init__(self):
        print("Opening DB connection!")
        self.conn = mysql.connector.connect(user='filip', password='admin',
                                    host='localhost',
                                    database='mydb')
    def __enter__(self):
        print("Giving DB connection!")
        return self.conn
    

    def __exit__(self, type, value, traceback):
        print("Closing DB connection!")
        self.conn.close()
