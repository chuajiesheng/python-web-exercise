from flask import Flask
from flask import render_template, request, url_for, redirect
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'

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
@app.route('/')
def homepage():
	return render_template('home.html', tasks=Todo.query.all())

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
