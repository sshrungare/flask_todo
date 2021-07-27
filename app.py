from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime, time



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
db = SQLAlchemy(app)

class Todo(db.Model):

    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    desc = db.Column(db.String(500), nullable = False)
    date_created = db.Column(db.DateTime,default =datetime.utcnow())

    def __repr__(self) -> str:
        return f'{self.title} - {self.id}'


@app.route('/',methods = ['GET','POST'])
def index():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        td = Todo(title = title,desc = desc)
        db.session.add(td)
        db.session.commit()
    atd = Todo.query.all()
    return render_template('index.html',atd = atd)

@app.route('/show')
def show():
    print(Todo.query.all())
    return 'show'

@app.route('/update/<int:id>',methods = ['GET','POST'])
def update(id):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        filters = Todo.query.filter_by(id = id).first()
        filters.title = title
        filters.desc = desc
        db.session.add(filters)
        db.session.commit()
        return redirect("/")
    filters = Todo.query.filter_by(id = id).first()
    return render_template('update.html',filters=filters)

@app.route('/delete/<int:id>')
def delete(id):
    filters = Todo.query.filter_by(id = id).first()
    db.session.delete(filters)
    db.session.commit()
    return redirect("/")

if __name__=="__main__":
    app.run(debug=True)