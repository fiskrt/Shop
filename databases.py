import sqlite3

def adminTable(self,cursor):
        sql_create_table = """ CREATE TABLE IF NOT EXISTS admins (
                                                id integer PRIMARY KEY,
                                                name text NOT NULL
                                                ); """
        cursor.execute(sql_create_table)



def customerTable(self,cursor):
    sql_create_table = """ CREATE TABLE IF NOT EXISTS customer (
                                                id integer PRIMARY KEY,
                                                name text NOT NULL
                                                birthdate text NOT NULL,
                                                gender TEXT NOT NULL,
                                                adress TEXT, 
                                                localAreaCode text,
                                                profilePic blob,
                                                email text NOT NULL,
                                                password text NOT NULL                                                
                                                ); """
    cursor.execute(sql_create_table)


def productsTable(self,cursor):
    sql_create_table = """ CREATE TABLE IF NOT EXISTS products (
                                                id integer PRIMARY KEY,
                                                price real NOT NULL,
                                                stockStatus integer,
                                                description text, 
                                                picture blob, 
                                                meanRating real,
                                                brand text
                                                ); """
    cursor.execute(sql_create_table)


def shoppingBasketTable(self,cursor):
    sql_create_table = """ CREATE TABLE IF NOT EXISTS shoppingBasket (
                                                    id integer,
                                                    productName text, 
                                                    date text,
                                                    price real,
                                                    CONSTRAINT fk_products 
                                                    FOREIGN KEY (id)
                                                    REFERENCES products(id)
                                                    ); """
    cursor.execute(sql_create_table)


def purchaseHistoryTable(self, cursor):
    sql_create_table = """ CREATE TABLE IF NOT EXISTS admins (
                                                    id integer,
                                                    price real NOT NULL,
                                                    CONSTRAINT fk_products 
                                                    FOREIGN KEY (id)
                                                    REFERENCES products(id)
                                                    ); """
    cursor.execute(sql_create_table)


def productCategoriesTable(self, cursor):
    sql_create_table = """ CREATE TABLE IF NOT EXISTS productcategories (
                                                        id text,
                                                        categoryName text,
                                                        FOREIGN KEY (id)
                                                        REFERENCES products(id)                                    
                                                        ); """
    cursor.execute(sql_create_table)

#def addToTable(tableName,):


conn = sqlite3.connect('database.db')
cursor = conn.cursor()
adminTable(cursor)
customerTable(cursor)
print("Opened database successfully")

sqlite_select_query = """SELECT * from product"""
rows = cursor.execute(sqlite_select_query)

print("Table created successfully")

for row in rows:
    print(row)

conn.close()