from flask import Flask, render_template
import os
import datetime
import sqlite3
from flask_sqlalchemy import SQLAlchemy


project_dir = os.path.dirname(os.path.abspath(__file__))
database_uri = "sqlite:///{}".format(os.path.join(project_dir, 'database.db'))


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
db = SQLAlchemy(app)


class TabelaExemplo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.String(200), nullable=False)


@app.route('/')
def index():  # put application's code here
    return render_template('base/index.html')


if __name__ == '__main__':
    app.run()
