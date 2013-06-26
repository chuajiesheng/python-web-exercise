from flask import Flask
from flask import render_template, request
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

db.create_all()
@app.route('/')
def homepage():
	return render_template('home.html', app_name=';/', author='Helios')

@app.route('/add', methods=('GET', 'POST'))
def add():
	if request.method == 'POST':
		taskname = request.form['taskname']
		add_todo(taskname)
	return render_template('add.html')

app.run()
