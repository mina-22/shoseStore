import sqlite3
import utils
def connect_to_database(name='database.db'):
    return sqlite3.connect(name, check_same_thread=False)

connection = sqlite3.connect('database.db')
cursor = connection.cursor()

def add_user(connection,email,username,password):
    cursor = connection.cursor()
    hashed_password = utils.hash_password(password)
    query = '''INSERT INTO users (email,username, password,admin) VALUES (?,?,?,?)'''
    cursor.execute(query, (email,username, hashed_password,0))
    connection.commit()

def get_user(connection, username):
    cursor = connection.cursor()
    query = '''SELECT * FROM users WHERE username = ?'''
    cursor.execute(query, (username,))
    return cursor.fetchone()

def add_product(connection,name,price,saleprice,photo,sale):
    cursor = connection.cursor()
    query = '''INSERT INTO products (product_name,image_path,price,sale_price,on_sale) VALUES (?,?,?,?,?)'''
    cursor.execute(query, (name,photo, price,saleprice,sale))
    connection.commit()

def search_products(connection, search_query):
    cursor = connection.cursor()
    query = '''SELECT * FROM products WHERE product_name LIKE ?'''
    cursor.execute(query,(f"%{search_query}%",))
    return cursor.fetchall()

def add_comment(connection, userid, name, email,message):
    cursor = connection.cursor()
    cursor.execute('''
                  INSERT INTO comments (user_id, name, email, message)
                   Values(?, ?, ?,?)
                   ''',(userid, name, email, message))
    connection.commit()


def add_order(connection, product_id,price,user_id):
    price=float(price)
    product_id=int(product_id)
    cursor=connection.cursor()
    query = '''INSERT INTO orders (user_id,product_id,total_price,purchased) VALUES (?,?,?,?)'''
    cursor.execute(query,(user_id,product_id,price,0,))
    connection.commit()

def get_id_user(connection,username):
    cursor=connection.cursor()
    query = '''SELECT user_id FROM users WHERE username = ?'''
    cursor.execute(query, (username,))
    return cursor.fetchone()[0]


def get_all_orders(connection,id):
    cursor = connection.cursor()
    query='''SELECT * FROM orders WHERE user_id=? AND purchased=0'''
    cursor.execute(query,(id,))
    return cursor.fetchall()

def get_product(connection,id):
    cursor=connection.cursor()
    query=''' SELECT * FROM products WHERE product_id=? '''
    cursor.execute(query,(id,))
    return cursor.fetchone()


def Buy_Now(connection,id):
    cursor=connection.cursor()
    query='''   UPDATE orders SET purchased = 1 WHERE user_id = ?  '''
    cursor.execute(query,(id,))
    connection.commit()


def Edit_Product(connection,id,name,price,saleprice,photo,sale):
    cursor = connection.cursor()
    if photo=="":
        query = ''' UPDATE products SET product_name = ?, price = ?, on_sale = ? , sale_price=? WHERE product_id = ? '''
        cursor.execute(query,(name,price,sale,saleprice,id,))
        connection.commit()
    else:
        query = ''' UPDATE products SET product_name = ? , image_path=? , price = ?, on_sale = ? , sale_price=?  WHERE product_id = ? '''
        cursor.execute(query,(name,photo,price,sale,saleprice,id,))
        connection.commit()

# def get_products(connection):
#     cursor = connection.cursor()
#     query= ''' SELECT * FROM products '''
#     cursor.execute(query)
#     return cursor.fetchone()

# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS products(
#     product_id INTEGER PRIMARY KEY NOT NULL,
#     product_name TEXT NOT NULL,
#     image_path TEXT NOT NULL,
#     price REAL NOT NULL,
#     on_sale INTEGER NOT NULL,
#     sale_price REAL
#     )
# ''')

# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS users(
#     user_id INTEGER PRIMARY KEY NOT NULL,
#     username TEXT NOT NULL,
#     password TEXT NOT NULL,
#     email TEXT NOT NULL,
#     admin INTEGER NOT NULL
#     )
# ''')

# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS orders(
#     order_id INTEGER PRIMARY KEY NOT NULL,
#     user_id INTEGER NOT NULL,
#     product_id INTEGER NOT NULL,
#     total_price REAL NOT NULL,
#     purchased INTEGER NOT NULL,
#     FOREIGN KEY(product_id) REFERENCES products(product_id),
#     FOREIGN KEY(user_id) REFERENCES users(user_id)
#     )
# ''')

# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS comments(
#     comment_id INTEGER PRIMARY KEY NOT NULL,
#     user_id INTEGER NOT NULL,
#     name TEXT NOT NULL,
#     email TEXT NOT NULL,
#     message TEXT NOT NULL,
#     FOREIGN KEY(user_id) REFERENCES users
#     )
# ''')

# cursor.execute('''
#     INSERT INTO users (username, password, email, admin)
#     VALUES ('mina', '123456', 'mina@gmail.com', 1)
# '''
# )

def delete_order(connection,id):
    cursor=connection.cursor()
    query=''' DELETE FROM orders WHERE purchased =0 And product_id=? '''
    cursor.execute(query,(id,))
    connection.commit()

# cursor.execute('''
#     DELETE FROM orders WHERE purchased =0  
   
# '''
# )

# cursor.execute('''
#     UPDATE users
# SET admin = 1
# WHERE user_id = 4 or user_id = 5;
   
# '''
# )


# cursor.execute('''
#     DROP TABLE orders
# ''')

connection.commit()
