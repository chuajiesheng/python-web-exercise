from flask import Flask
from flask import render_template, request, url_for, redirect, session, g
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SECRET_KEY'] = 'very secret'

db = SQLAlchemy(app)

class Todo(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	text = db.Column(db.String)
	done = db.Column(db.Boolean, default=False)

def add_todo(text):
	db.session.add(Todo(text=text))
	db.session.commit()
	print 'adding todo:', text

def mask_as_done(id):
	todo = Todo.query.get(id)
	todo.done = True
	db.session.commit()
	print 'mark as done:', id

def delete_todo(id):
	todo = Todo.query.get(id)
	db.session.delete(todo)
	db.session.commit()
	print 'delete:', id

db.create_all()

@app.before_request
def setup():
	g.username = session.get('username', None)

@app.route('/')
def homepage():
	if not session.get('username', None):
		return redirect(url_for('loginview'))
	return render_template('home.html', username=session.get('username', None), tasks=Todo.query.all())

@app.route('/login', methods=('GET', 'POST'))
def loginview():
	if request.method == 'POST':
		session['username'] = request.form['username']
		return redirect(url_for('homepage'))
	return render_template('login.html')

@app.route('/logout')
def logout():
	session['username'] = None
	return redirect(url_for('loginview'))

@app.route('/addtask', methods=('GET', 'POST'))
def add():
	if request.method == 'POST':
		taskname = request.form['taskname']
		add_todo(taskname)
	return render_template('add.html')

@app.route('/done/<int:task_id>')
def done(task_id):
	mask_as_done(task_id)
	return redirect(url_for('homepage'))

@app.route('/delete/<int:task_id>')
def delete(task_id):
	delete_todo(task_id)
	return redirect(url_for('homepage'))

app.run()
