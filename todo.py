from flask import Flask
from flask import render_template
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'

db = SQLAlchemy(app)
db.create_all()

class Todo(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	text = db.Column(db.String)
	done = db.Column(db.Boolean)

def add_todo(text):
	db.session.add(Item(text=text))
	db.session.commit()
	print 'adding todo:', text

@app.route('/')
def homepage():
	return render_template('home.html', app_name=';/', author='Helios')

app.run()
