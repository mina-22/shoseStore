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
    cursor.execute(query, (email,username, hashed_password,1))
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
#     time TEXT NOT NULL,
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

# cursor.execute('''
#     DELETE FROM products WHERE product_id =3;
    
# '''
# )

# cursor.execute('''
#     UPDATE users
# SET admin = 1
# WHERE user_id = 4 or user_id = 5;
   
# '''
# )

connection.commit()