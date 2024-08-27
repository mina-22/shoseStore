from urllib.parse import urlparse
from flask import Flask, abort, render_template, request, redirect, url_for, session, flash
import database as db
import utils
import Validation
import sqlite3
import os
UPLOADS_FOLDER = 'static/img2/'
app = Flask(__name__)
connection = db.connect_to_database()
connection.row_factory = sqlite3.Row
app.secret_key = "SUPER-SECRET"
app.config['UPLOADS_FOLDER'] = UPLOADS_FOLDER

@app.route('/')
def index():
    if 'username' in session:
        if session['adminRole'] == 1:
            return render_template('adminDashborad.html')
        else:
            products = connection.execute(f"SELECT * FROM products").fetchall()
            return render_template('index.html', Products = products)
    return redirect(url_for('Login'))


@app.route('/Login', methods=['GET', 'POST'])
def Login():
    session.pop('username', None)
    session.pop('adminRole', None)
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = db.get_user(connection, username)
        if user:
            if utils.is_password_match(password,user[2]):
                session['username'] = user[1]
                session['adminRole']= user[4]
                return redirect(url_for('index'))
            else:
                flash("Invalid username or password", "danger")
                return render_template('Login.html')
        else:
            flash("Invalid username or password", "danger")
            return render_template('Login.html')
    else:
        session.pop('username', None)
        session.pop('adminRole', None)
        
        return render_template("Login.html")    


@app.route('/Register', methods=['GET', 'POST'])
def Register():
    if request.method == 'POST':
        
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        if not utils.is_strong_password(password):
            flash(
                "Sorry You Entered a weak Password Please Choose a stronger one", "danger")
            return render_template('Register.html')

        user = db.get_user(connection, username)
        if user:
            flash(
                "Username already exists. Please choose a different username.", "danger")
            return render_template('Register.html')
        else:
            db.add_user(connection,email,username,password)
            return redirect(url_for('Login'))
    else:
        session.pop('username', None)
        session.pop('adminRole', None)
        return render_template('Register.html')
    
@app.route('/Logout')
def Logout():
    session.pop('username', None)
    session.pop('adminRole', None)
    return redirect(url_for('Login'))


@app.route('/adminDashborad')
def adminDashborad():
    if 'username' in session:
        if session['adminRole']==1:
            return render_template("adminDashborad.html")
        else:
            return ("Not Found")
    else:
        return render_template("Login.html")    
    

@app.route('/AddProduct', methods=['GET', 'POST'])
def AddProduct():
    if 'username' in session:
        if session['adminRole']==1:
            if request.method=="POST":
                ProductName=request.form['ProductName']
                ProductPrice=request.form['ProductPrice']
                ProductSalePrice=request.form['ProductSalePrice']
                sale=True
                if not(Validation.priceVaild(ProductPrice)):
                    flash ("You Must Enter Price Between 5$ and 500$", "danger")
                    return render_template('AddProduct.html')
                if not(Validation.PriceSaleValdi(ProductSalePrice,ProductPrice)):
                    flash ("You Must Enter Sale Price less than the Price and greater than or equal zero", "danger")
                    return render_template('AddProduct.html')
                photo = request.files.get('profile_picture')
                if photo:
                    if not Validation.accepted_file_size(photo):
                        flash ("You Must Enter image max size of it is 12 MB", "danger")
                        return render_template('AddProduct.html')
                    elif not Validation.accepted_file(photo.filename):
                        flash ("You Must Enter image 'png', 'jpg', 'jpeg'", "danger")
                        return render_template('AddProduct.html')
                else:
                    flash("You Must Enter the Image of Product", "danger")
                    return render_template('AddProduct.html')
                if ProductSalePrice==0:
                    sale = False
                photo.save(os.path.join(app.config['UPLOADS_FOLDER'], photo.filename))
                db.add_product(connection,ProductName,ProductPrice,ProductSalePrice,photo.filename,sale)
                return render_template('adminDashborad.html')
            else:
                return render_template("AddProduct.html")
        else:
            return "Not Found"    
    else:
        return "Not Found"
@app.route('/ViewProduct')
def ViewProduct():
    if 'username' in session:
        if session['adminRole']==1:
            products = connection.execute('SELECT * FROM products').fetchall()
            return render_template("ViewProduct.html" ,Products=products)
        else:
            return ("Not Found")
    else:
        return render_template("Login.html")   

@app.route('/EditProduct',methods=['GET', 'POST'])
def EditProduct():
    if 'username' in session and session['adminRole']==1:
        if request.method=='POST':
            ProductName=request.form['ProductName']
            ProductPrice=request.form['ProductPrice']
            ProductSalePrice=request.form['ProductSalePrice']
            id=request.form['product_id']
            sale=True
            if not(Validation.priceVaild(ProductPrice)):
                flash ("You Must Enter Price Between 5$ and 500$", "danger")
                return render_template('AddProduct.html')
            if not(Validation.PriceSaleValdi(ProductSalePrice,ProductPrice)):
                flash ("You Must Enter Sale Price less than the Price and greater than or equal zero", "danger")
                return render_template('AddProduct.html')
            photo = request.files.get('profile_picture')
            if photo:
                if not Validation.accepted_file_size(photo):
                    flash ("You Must Enter image max size of it is 12 MB", "danger")
                    return render_template('AddProduct.html')
                elif not Validation.accepted_file(photo.filename):
                    flash ("You Must Enter image 'png', 'jpg', 'jpeg'", "danger")
                    return render_template('AddProduct.html')
                else:
                    photo.save(os.path.join(app.config['UPLOADS_FOLDER'], photo.filename))
            else:
                photo=""        
            if ProductSalePrice==0:
                sale = False
            if photo=="":    
                db.Edit_Product(connection,id,ProductName,ProductPrice,ProductSalePrice,photo,sale)
            else:
                db.Edit_Product(connection,id,ProductName,ProductPrice,ProductSalePrice,photo.filename,sale)
            return redirect(url_for('ViewProduct'))
        elif request.method=='GET':
            id=request.args.get('id')
            product=db.get_product(connection,id)
            return render_template("EditProduct.html",product=product)
        else:
            return ("not found")    
    else:
        return render_template("Login.html")    

@app.route('/DeleteProduct/<id>')
def DeleteProduct(id):
    if 'username' in session:
        if session['adminRole'] == 1:
            connection.execute(f"DELETE FROM products WHERE product_id = '{id}'")
            connection.execute(f"DELETE FROM orders WHERE product_id = '{id}'")
            db.delete_order(connection,id)
            connection.commit()
            return redirect(url_for('ViewProduct'))
        else:
            return("Not Found")
    else:
        return render_template("Login.html")
    
@app.route('/Collection', methods=['GET','POST'])
def collection():
    if 'username' in session and session['adminRole']==0:
        products = []
        if request.method == 'POST':
            search_query = request.form['search_query']
            products = db.search_products(connection, search_query)
        else:
            products = connection.execute(f"SELECT * FROM products").fetchall()
        productCount = len(products)
        return render_template("collection.html",Products=products,count = productCount)
    else:
        return redirect(url_for('Login'))

@app.route('/Cart')
def Cart():
    if 'username' in session and session['adminRole']==0:
        products=[]
        total=0
        
        id=db.get_id_user(connection,session['username'])
        orders=db.get_all_orders(connection,id)
        for item in orders :
            
            total+=db.get_product(connection,item[2])[3]
            products.append(db.get_product(connection,item[2]))
        
        return render_template("mina.html",products=products,total=total)
    else:
        return redirect(url_for('Login'))

@app.route('/Contact', methods=['GET', 'POST'])
def Contact():
    if 'username' in session and session['adminRole']==0:
        if request.method == 'POST':
            name = request.form["name"]
            email = request.form["email"]
            comment = request.form["comment"]
            username = request.args.get('username', session['username'])
            user = db.get_user(connection, username)
            if name and email and comment:
                db.add_comment(connection, user['user_id'], name, email, comment)
                flash("Comment has been sent", "success")
            else:
                flash("Please fill all the fields", "danger")
            return render_template("contact.html")
        if request.method == 'GET':
            return render_template("contact.html")
    else:
        return redirect(url_for('Login'))

@app.route('/AddToCart')
def AddToCart():
    if 'username' in session:
        if session['adminRole']==0:
            productId=request.args.get('product_id')
            price=request.args.get('price')
            username=session['username']
            user_id=db.get_id_user(connection,username)
            db.add_order(connection,productId,price,user_id)
            return redirect(url_for('collection'))
        else:
            return("No accses to make this operation")
    else:
        return ("you Not Uesr Login!!")        

@app.route('/ViewComents')
def ViewComents():
    if 'username' in session:
        if session['adminRole']==1:
            comments = connection.execute('SELECT * FROM comments').fetchall()
            return render_template("ViewComents.html" ,comments=comments)
        else:
            return ("Not Found")
    else:
        return render_template("Login.html") 

@app.route('/lookbook')
def lookbook():
    if 'username' in session and session['adminRole']==0:
        return render_template("lookbook.html")
    else:
        return render_template("Login.html")

@app.route('/ourStory')
def ourStory():
    if 'username' in session and session['adminRole']==0:
        return render_template("ourStory.html")
    else:
        return render_template("Login.html")
        

@app.route('/BuyNow')
def BuyNow():
    if 'username' in session and session['adminRole']==0:
        username=session['username']
        flag=request.args.get('flag')
        userid=db.get_id_user(connection,username)
        db.Buy_Now(connection,userid)
        flash(" Buy successfully ","success")
        return redirect(url_for('Cart'))
    else:
        return render_template("Login.html")    

def is_valid_url(server):
    parsed_url = urlparse(server)
    if parsed_url.scheme not in ['http', 'https']:  # lazm http aw https
        return False
    #only allow port 5000
    whitelist = [5000]
    return parsed_url.port in whitelist


@app.route('/CheckStock')
def Check_Stock():
    server = request.args.get("server")
    #third
    if not is_valid_url(server):
        abort(400, "Invalid URL")

    return redirect(server)

if __name__ == '__main__':
    app.run(debug=True)
