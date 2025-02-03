from flask import Flask, render_template, redirect, url_for, request, flash, request, abort
import mysql.connector 
app = Flask(__name__)

@app.route('/viewbooks')
def viewbooks():
		cur=connection.cursor()
		cur.execute("SELECT * from books")
		data=cur.fetchall()
		return render_template('viewbooks.html',data=data)