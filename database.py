from mysql.connector import Error, errorcode
from db_conn import Conn_db


def add_review(username, rating, comment, prod_id):
    """
        Adds a review(comment + star-rating) for a product
        to the 'Review' table.
    """
    with Conn_db() as conn:
        query = ('INSERT INTO Review'
                '(author, rating, comment, idProduct)'
                'VALUES(%s, %s, %s, %s);')
        cursor = conn.cursor()
        cursor.execute(query, (username, rating, comment, prod_id))
        conn.commit()
        cursor.close()

def create_order_history():
    """
        When a user checks out insert into the junction table 
    """

def add_to_order_history():
    """
        When user checks out add the purchased products
        to the purchase history.

        First, set the 'User_has_Order' junction table. This
        maps a user to a order which has also has a order date.

        First add the purchased product to the 'Sold_Product'
        table so it's not modified.
        Then add the purchased product and quantity to the 
        'Order_History' table.
    """
    with Conn_db() as conn:
        query = ('INSERT INTO Review'
                '(author, rating, comment, idProduct)'
                'VALUES(%s, %s, %s, %s);')
        cursor = conn.cursor()
#        cursor.execute(query, (username, rating, comment, prod_id))
        conn.commit()
        cursor.close()





def user_exists(username, check_admin=False):
    with Conn_db() as conn:
        if check_admin:
            query = "SELECT username FROM Admin WHERE username=%s;"
        else:
            query = "SELECT username FROM User WHERE username=%s;"
        cursor = conn.cursor()
        cursor.execute(query, (username,))
        attr = cursor.fetchall()
        cursor.close()
        # attr is 'None' if no user was found
        if attr:
            return True
    return False


def add_user_db(username, password):
    """
        Add a user to the 'User' table.
        If user already exists return False.
    """
    with Conn_db() as conn:
        conn.autocommit = False
        cursor = conn.cursor()
        lookup_query = 'SELECT username FROM User where username=%s'
        cursor.execute(lookup_query, (username,))

        if cursor.fetchone():
            conn.rollback() # Rollback a lookup xD
            cursor.close()
            return False # User already exists.

        insert_query = 'INSERT INTO User(username, password) VALUES(%s, %s)'
        cursor.execute(insert_query, (username, password))
        conn.commit()
        cursor.close()
    return True


def log_in(username, password, as_admin=False):
    with Conn_db() as conn:
        cursor = conn.cursor()
        if as_admin:
            lookup_query = ('SELECT username'
                            'FROM Admin'
                            'WHERE username=%s and password=%s;')
        else:
            lookup_query = ('SELECT username' 
                            'FROM User'
                            'WHERE username=%s and password=%s;')
        cursor.execute(lookup_query, (username, password))

        if cursor.fetchone():
            return True
    return False


def addProduct(pid, stock, description, price, brand):
    with Conn_db() as conn:
        cursor = conn.cursor()
        query = ('INSERT INTO product'
                '(idproduct, price, stock, description, brand)'
                'VALUES(%s,%s,%s,%s,%s);')
        cursor.execute(query, (pid, price, stock, description, brand))
        conn.commit()
        #attr = cursor.fetchone() what is fetched here?
        cursor.close()
    return True