from mysql.connector import Error, errorcode
from db_conn import Conn_db
import datetime


def add_review(username, rating, comment, prod_id):
    """
        Adds a review(comment + star-rating) for a product
        to the 'Review' table.

        Returns False if the review was not added.
    """
    with Conn_db() as conn:
        query = ('INSERT INTO Review'
                '(idUser, rating, comment, idProduct) '
                'VALUES(%s, %s, %s, %s);')
        cursor = conn.cursor()
        try:
            cursor.execute(query, (user_to_id(username), rating, comment, prod_id))
        except Error as e:
            return False
        finally:
            conn.commit()
            cursor.close()
    return True



def get_products(prod_name=None):
    """
        Note that the price's type is decimal.Decimal
    """
    with Conn_db() as conn:
        cursor = conn.cursor(dictionary=True)
        if prod_name:
            query = "SELECT * FROM Product WHERE name=%s;"
            cursor.execute(query, (prod_name,))
        else:
            query = "SELECT * FROM Product;"
            cursor.execute(query)
        attr = cursor.fetchall()
        cursor.close()
    return attr

def get_star_rating(prod_id):
    """
        Get the star-rating (scale 0-5) of prod_id
        If no ratings are given 0 is returned.
    """
    with Conn_db() as conn:
        cursor = conn.cursor()
        query = "SELECT AVG(rating) FROM Review WHERE idProduct=%s;"
        cursor.execute(query, (prod_id,))
        average = cursor.fetchone()[0]
        cursor.close()
    if average:
        return average
    return 0

def get_reviews(prod_id):
    """
        Returns a list of reviews for the product with id 'prod_id'.
        Each entry is of the form: (comment, username)
    """
    with Conn_db() as conn:
        query = ('SELECT R.comment, U.username '
                'FROM Review R '
                'WHERE R.idProduct=%s '
                'JOIN User U '
                'ON U.idUser=R.idUser;')
        cursor = conn.cursor()
        cursor.execute(query, (prod_id,))
        attr = cursor.fetchall()
        cursor.close()
    return attr


def user_to_id(username):
    """
        Assume username exists?
    """
    with Conn_db() as conn:
        query = "SELECT idUser FROM User WHERE username=%s;"
        cursor = conn.cursor()
        cursor.execute(query, (username,))
        attr = cursor.fetchall()
        cursor.close()
    # attr is 'None' if no user was found, will crash
    return attr[0][0]


def get_basket_products(user):
    """
        Returns a list of products from a users basket.
    """
    user_id = user_to_id(user)
    with Conn_db() as conn:
        query = ('SELECT P.idProduct, P.name, P.price, P.description, '
                    'P.brand, P.image_path, BE.quantity '
                    'FROM Product P '
                    'JOIN Basket_Entry BE '
                    'ON BE.idProduct=P.idProduct AND BE.idUser=%s;')
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, (user_id,))
        products = cursor.fetchall()
        conn.commit()
        cursor.close()
    return products


def add_to_basket(user, quantity, product_id):
    """
        Insert a product into the basket. If the user already have
        the product added, only the quantity is incremented.
    """
    user_id = user_to_id(user)
    with Conn_db() as conn:
        query = ('INSERT INTO Basket_Entry '
                '(quantity, idProduct, idUser) '
                'VALUES(%s, %s, %s) '
                'ON DUPLICATE KEY UPDATE quantity=quantity+%s;')
        cursor = conn.cursor()
        cursor.execute(query, (quantity, product_id, user_id, quantity))
        conn.commit()
        cursor.close()


def remove_from_basket(user, prod_id):
    user_id = user_to_id(user)
    with Conn_db() as conn:
        query = ('DELETE FROM Basket_Entry '
                'WHERE idUser=%s AND idProduct=%s;')
        cursor = conn.cursor()
        cursor.execute(query, (user_id, prod_id))
        conn.commit()
        cursor.close()


def checkout(user):
    """
        When user checks out move the purchased products
        to the purchase history.

        1) Add a new entry to 'User_has_Order' junction table.
        This creates a new orderID for a user.

        2) Add the products and quantites from the basket to 'Order_Entry'.
        NOTE: The products' name and price is copied without relations
        to the old product.

        3) Empty the basket for the specified user.
    """
    user_id = user_to_id(user)
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    with Conn_db() as conn:
        cursor = conn.cursor()
        q1 = ('INSERT INTO User_has_Order'
                '(idUser, order_date)'
                'VALUES(%s, %s);')
        cursor.execute(q1, (user_id, current_date))
        order_id = cursor.lastrowid

        q2 = ('INSERT INTO Order_Entry '
                '(idOrder, quantity, sold_prod_name, sold_prod_price) '
                'SELECT %s, BE.quantity, P.name, P.price '
                'FROM Product P '
                'JOIN Basket_Entry BE '
                'ON BE.idUser=%s AND P.idProduct=BE.idProduct;')
        cursor.execute(q2, (order_id, user_id))

        q3 = ('DELETE FROM Basket_Entry '
                    'WHERE idUser=%s;')
        cursor.execute(q3, (user_id, ))

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
            lookup_query = ('SELECT username '
                            'FROM Admin '
                            'WHERE username=%s and password=%s;')
        else:
            lookup_query = ('SELECT username ' 
                            'FROM User '
                            'WHERE username=%s and password=%s;')
        cursor.execute(lookup_query, (username, password))

        if cursor.fetchone():
            return True
    return False


def addProduct(pid, stock, description, price, brand):
    with Conn_db() as conn:
        cursor = conn.cursor()
        query = ('INSERT INTO product '
                '(idproduct, price, stock, description, brand) '
                'VALUES(%s,%s,%s,%s,%s);')
        cursor.execute(query, (pid, price, stock, description, brand))
        conn.commit()
        #attr = cursor.fetchone() what is fetched here?
        cursor.close()
    return True


def test_basket():
    add_to_basket('filip', 20, 1)
    add_to_basket('filip', 1, 2)
    add_to_basket('max', 2, 2)
    add_to_basket('max', 2, 1)
    checkout('max')


def test_reviews():
    add_review('filip', 3, 'den smakade ganska bra!', 1)
    add_review('max', 5, 'den smakade bra!', 1)


if __name__ == "__main__":
    print('Database debugging.')
    Conn_db.load_conf()
    test_reviews()
