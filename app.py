from flask import Flask, render_template, redirect, url_for, request, flash, request, abort ,session , logging
import mysql.connector 
from mysql.connector import Error

app = Flask(__name__)

connection = mysql.connector.connect(host='localhost',database ='samp',user='root',password='')

@app.route('/')
def index():
		return render_template('home.html')

@app.route('/loginhome', methods=['GET','POST'])
def loginhome():
		cur=connection.cursor()
		cur.execute("SELECT * from books")
		data=cur.fetchall()
		user_id=session['userid']
		cur.execute("SELECT user_name from login  WHERE user_ID = %s",[user_id])
		data1=cur.fetchone()
		return render_template('loginhome.html',data=data,data1=data1)

@app.route('/sign_up', methods=['GET','POST'])
def signup():
	if request.method == 'POST':
		username=request.form['uname']
		userid=request.form['uid']
		Emailid=request.form['emailids']
		phoneno=request.form['mobilenumber']
		password=request.form['pword']
		cur=connection.cursor()
		print('username')
		print('userid')
		print('Emailid')
		print('phoneno')
		print('password')
		cur.execute("INSERT INTO login(user_name,user_ID,Email,Mobile_number,p_word) VALUES(%s,%s,%s,%s,%s)", (username,userid,Emailid,phoneno,password))
		connection.commit()
		cur.close()
		print('signup successfull')
		return redirect(url_for('index'))
	return render_template('home.html')

@app.route('/user_login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		userid = request.form['uid']
		password = request.form['pword']
		cur=connection.cursor()
		cur.execute("SELECT * FROM login WHERE user_ID= %s AND p_word= %s",[userid,password])
		data = cur.fetchone()
		if data:
			useid=data[1]
			usename=data[0]
			useemail=data[3]
		if not data:
			print('Invalid Credentials')
			return render_template('user_login.html')

		else:
			session['logged_in']=True
			session['username']=usename
			session['email']=useemail
			session['userid']=userid
			print(session['userid'])
			print('user login success')
			return redirect(url_for('loginhome'))
		cur.close()
	return render_template('home.html')

@app.route('/addcard',methods=['GET','POST'])
def addcard():
	if request.method == 'POST':
		cc_number= request.form['ccnum']
		cc_name= request.form['ccname']
		expiry_date= request.form['expirydate']
		cvv_no= request.form['cvvno']
		cur=connection.cursor()
		cur.execute("INSERT INTO payment(cc_no,cc_name,expiry,cvv) VALUES(%s,%s,%s,%s)", (cc_number,cc_name,expiry_date,cvv_no))
		connection.commit()
		cur.close()
		print('Card Added')
		return redirect(url_for('loginhome'))
	return render_template('addcard.html')

@app.route('/address', methods=['GET','POST'])
def address():
	if request.method == 'POST':
		room_no=request.form['roomno']
		building=request.form['building']
		street=request.form['street']
		city=request.form['city']
		zipcode=request.form['zipcode']
		cur=connection.cursor()
		user_id=session['userid']
		cur.execute("INSERT INTO address(room_no,user_id,building,street,city,zipcode) VALUES(%s,%s,%s,%s,%s,%s)", (room_no,user_id,building,street,city,zipcode))
		connection.commit()
		print('Address added')
		return redirect(url_for('loginhome'))
		cur.close()
	return render_template('address.html')

@app.route('/editprofile',methods=['GET','POST'])
def editprofile():
	if request.method == 'POST':
		cur=connection.cursor()
		user_id=session['userid']
		user_name=request.form['uname']
		password=request.form['pword']
		email=request.form['email']
		mobile_number=request.form['mobilenum']
		print('mobile_number')
		cur.execute("UPDATE login SET user_name=%s , p_word=%s , Email=%s , mobile_number=%s where user_id=%s",(user_name,password,email,mobile_number,user_id))
		connection.commit()
		cur.close()
		print('Profile Edited')
		return redirect(url_for('loginhome'))
	return render_template('editprofile.html')

@app.route('/logout')
def logout():
	session.clear()
	print('Logged out')
	return redirect(url_for('index'))

@app.route('/admin_login',methods=['GET','POST'])
def adminlogin():
	if request.method == 'POST':
		admin_id = request.form['admin_id']
		admin_pword=request.form['admin_pw']
		cur=connection.cursor()
		cur.execute("SELECT * FROM admin WHERE admin_id= %s AND admin_pw= %s",[admin_id,admin_pword])
		data = cur.fetchone()
		if data:
			adminid=data[1]
		if not data:
			print('Invalid Credentialss')
			return render_template('admin_login.html')
		else:
			session['logged_in']=True
			session['adminid']=adminid
			print(session['adminid'])
			print('Admin login success')
		return redirect(url_for('adminhome'))	
		cur.close()
	return render_template('home.html')

@app.route('/adminhome',methods=['GET','POST'])
def adminhome():
	return render_template('adminhome.html')
	
@app.route('/addbooks',methods=['GET','POST'])
def addbooks():
	if request.method == 'POST':
		ISBN_number= request.form['isbnnum']
		Title_name= request.form['titlename']
		Author_name= request.form['authorname']
		Publisher_name= request.form['publishername']
		Year_publishing= request.form['yearpublishing']
		Book_description= request.form['bookdescription']
		Avail_copies= request.form['availcopies']
		Book_price= request.form['bookprice']
		cur=connection.cursor()
		cur.execute("INSERT INTO books(ISBN,Title,Author,Publisher,Year_of_publishing,Description,Available_copies,Price) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)", (ISBN_number,Title_name,Author_name,Publisher_name,Year_publishing,Book_description,Avail_copies,Book_price))
		connection.commit()
		cur.close()
		print('Book Added')
		return redirect(url_for('adminhome'))
	return render_template('addbooks.html')

@app.route('/viewbooks', methods=['GET','POST'])
def viewbooks():
		cur=connection.cursor()
		cur.execute("SELECT * from books")
		data=cur.fetchall()
		return render_template('viewbooks.html',data=data)

@app.route('/editbook',methods=['GET','POST'])
def editbook():
	if request.method == 'POST':
		Book_ids = request.form['bookids']
		cur=connection.cursor()
		cur.execute("SELECT * FROM books WHERE Book_id= %s",[Book_ids])
		data = cur.fetchone()
		connection.commit()
		cur.close()
		return render_template('editbooks.html',data=data)
	return render_template('editbook.html')

@app.route('/editdetails',methods=['GET','POST'])
def editdetails():
	if request.method == 'POST':
		ISBN_number= request.form['isbnnum']
		Title_name= request.form['titlename']
		Author_name= request.form['authorname']
		Publisher_name= request.form['publishername']
		Year_publishing= request.form['yearpublishing']
		Book_description= request.form['bookdescription']
		Avail_copies= request.form['availcopies']
		Book_price= request.form['bookprice']
		Book_ids = request.form['bookids']
		cur=connection.cursor()
		cur.execute("UPDATE books SET ISBN=%s , Title=%s , Author=%s , Publisher=%s , Year_of_publishing=%s , Description=%s , Available_copies=%s , Price=%s where Book_id=%s",(ISBN_number,Title_name,Author_name,Publisher_name,Year_publishing,Book_description,Avail_copies,Book_price,Book_ids))
		connection.commit()
		cur.close()
		print('Book Edited')
		return redirect(url_for('adminhome'))
	return render_template('editbook.html')

@app.route('/deletebook',methods=['GET','POST'])
def deletebook():
	if request.method == 'POST':
		Book_ids= request.form['bookids']
		cur=connection.	cursor()
		cur.execute("DELETE FROM books where Book_id=%s", [Book_ids])
		connection.commit()
		cur.close()
		print('Book deleted')
		return redirect(url_for('adminhome'))
	return render_template('deletebook.html')

@app.route('/add_cart',methods=['GET','POST'])
def add_cart():
	if request.method == 'POST':
		cur=connection.cursor()
		cur.execute("SELECT * FROM books")
		data=cur.fetchall()
		user_id=session['userid']
		cur.execute("SELECT user_name from login  WHERE user_ID = %s",[user_id])
		data1=cur.fetchone()
		ISBN_number = request.form['isbnnum']
		user_id = session['userid']
		cur.execute("INSERT INTO cart(user_id,ISBN) VALUES(%s,%s)",(user_id,ISBN_number))
		connection.commit()
		cur.close()
		print('Book added to the cart')
	return render_template('loginhome.html',data=data,data1=data1)

@app.route('/order_book',methods=['GET','POST'])
def order_book():
	cur=connection.cursor()
	user_id=session['userid']
	cur.execute("SELECT user_name from login  WHERE user_ID = %s",[user_id])
	data1=cur.fetchone()
	user_id=session['userid']
	cur.execute("SELECT * FROM address WHERE user_ID=%s",[user_id])
	addr_data=cur.fetchone()
	print(addr_data)
	isbn_num = request.form['isbnnum']
	book_id=request.form['bookid1']
	print(isbn_num)
	cur.execute("SELECT * FROM books WHERE book_id=%s",[book_id])
	book_data=cur.fetchone()
	print(book_data)
	cur.execute("SELECT * FROM login WHERE user_id=%s",[user_id])
	cust_data=cur.fetchone()
	cur.close()
	print(cust_data)
	print(addr_data)
	print(book_data)
	return render_template('order_book.html',addr_data=addr_data,book_data=book_data,cust_data=cust_data,data1=data1)

@app.route('/placeorder',methods=['GET','POST'])
def placeorder():
	if request.method == 'POST':
		paid=1
		cur=connection.cursor()
		ISBN_number = request.form['isbnnum']
		cur.execute("SELECT * FROM books WHERE ISBN=%s",[ISBN_number])
		data=cur.fetchall()
		user_id=session['userid']
		cur.execute("SELECT user_name from login  WHERE user_ID = %s",[user_id])
		data1=cur.fetchone()
		user_id=session['userid']
		total=request.form['total']
		cur.execute("INSERT INTO orders(user_id,ISBN,paid,total) VALUES(%s,%s,%s,%s)",(user_id,ISBN_number,paid,total))
		connection.commit()
		cur.close()
		print('Product ordered')
		return redirect(url_for('loginhome'))
	return render_template('loginhome.html',data=data,data1=data1)

@app.route('/mycart',methods=['GET','POST'])
def mycart():
	if request.method == 'GET':
		cur=connection.cursor()
		user_id=session['userid']
		cur.execute("select books.* from books join cart on books.isbn = cart.isbn where cart.user_id = %s",[user_id])
		data=cur.fetchall()
		cur.close()
		print('data')
	return render_template('mycart.html',data=data)

@app.route('/myorder',methods=['GET','POST'])
def myorder():
	if request.method == 'GET':
		cur=connection.cursor()
		user_id=session['userid']
		cur.execute("select books.* from books join orders on books.isbn = orders.isbn where orders.user_id = %s",[user_id])
		data=cur.fetchall()
		cur.close()
	return render_template('myorder.html',data=data)

if __name__=='__main__':
	app.secret_key='secret123'
	app.run(debug=True)
