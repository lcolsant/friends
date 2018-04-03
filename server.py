from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
app = Flask(__name__)
mysql = MySQLConnector(app,'users')

@app.route('/')
def index():
    return redirect('/users')

@app.route('/users')
def users():
    query = "SELECT * FROM friends"
    friends = mysql.query_db(query)
    print friends
    return render_template('users.html', all_friends=friends)

@app.route('/friends/new')
def new_friend():
    return render_template('add.html')

@app.route('/friends/add', methods=['POST'])
def create():
    print request.form['fname']
    print request.form['lname']
    print request.form['email']
    query = "INSERT INTO friends (first_name, last_name, email, created_at, updated_at) VALUES (:fname,:lname, :email, NOW(), NOW() )"
    data = {
             'fname': request.form['fname'],
             'lname': request.form['lname'],
             'email':  request.form['email'],
           }
    mysql.query_db(query, data)   


    return redirect('/users')

@app.route('/friends/<id>/show', methods=['GET'])
def show(id):

    query = "SELECT * FROM friends WHERE id=:id"
    data = {
        'id': id
    }
    friend = mysql.query_db(query, data)[0]
    return render_template('show.html', friend=friend)

@app.route('/friends/<id>/edit', methods=['GET'])
def edit(id):

    query = "SELECT * FROM friends WHERE id=:id"
    data = {
        'id': id
    }
    friend = mysql.query_db(query, data)[0]
    return render_template('edit.html', friend=friend)

@app.route('/friends/<id>/delete', methods=['GET'])
def delete(id):
    query = "SELECT first_name, last_name FROM friends WHERE id=:id"
    data = {
        'id': id
    }
    friend = mysql.query_db(query, data)[0]
    print("deleting {} from your database".format(friend))
    query = "DELETE FROM friends WHERE id=:id"
    mysql.query_db(query, data)
    return redirect('/users')

@app.route('/friends/<id>/update', methods=['POST'])
def update(id):
    query = "UPDATE friends SET first_name = :first_name, last_name = :last_name, email = :email, updated_at = NOW() WHERE id=:id"
    data = {
        'id': id,
        'first_name': request.form['fname'],
        'last_name': request.form['lname'],
        'email': request.form['email']
    }
    mysql.query_db(query, data)
    return redirect('/users')

app.run(debug=True)