import sqlite3

connection = sqlite3.connect('database.db')
cursor = connection.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS products(
    product_id INTEGER PRIMARY KEY NOT NULL,
    product_name TEXT NOT NULL,
    image_path TEXT NOT NULL,
    price REAL NOT NULL,
    on_sale INTEGER NOT NULL,
    sale_price REAL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER PRIMARY KEY NOT NULL,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    email TEXT NOT NULL,
    admin INTEGER NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders(
    order_id INTEGER PRIMARY KEY NOT NULL,
    user_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    total_price REAL NOT NULL,
    purchased INTEGER NOT NULL,
    time TEXT NOT NULL,
    FOREIGN KEY(product_id) REFERENCES products(product_id),
    FOREIGN KEY(user_id) REFERENCES users(user_id)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS comments(
    comment_id INTEGER PRIMARY KEY NOT NULL,
    user_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    message TEXT NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users
    )
''')

cursor.execute('''
    INSERT INTO users (user_id, username, password, email, admin)
    VALUES (1, 'admin', 'admin', 'admin@admin.com', 1)
'''
)