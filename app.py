from __future__ import annotations
from flask import Flask, render_template, redirect, request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship

#The app itself
app = Flask(__name__) # It's named like the Python file
Scss(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Class -- row of data
class MyPerson(db.Model):
    __tablename__ = 'Persons'
    id :  Mapped[int] = mapped_column(primary_key=True)
    
with app.app_context():
    db.create_all()

@app.route('/',methods=["POST","GET"]) # Homepage
def index():
    return render_template('index.html')

@app.route('/create/person',methods=["POST","GET"]) # Create a person
def create_person():
    # Add a person to the database
    if request.method == "POST":
        name = request.form['name']
        new_person = MyPerson(name=name,team='TecMinds')    
        try:
            db.session.add(new_person)
            db.session.commit() # Actually commit that to the database
            return redirect('/create/person')
        except Exception as e:
            print(f'Error: {e}')
            return f'Error: {e}'
        
    # Get all the people from the database
    else:
        persons = MyPerson.query.order_by(MyPerson.id).all()
        return render_template('create_person.html', persons=persons)

# Delete a person from the database
@app.route("/delete/person/<int:id>")
def delete_person(id:int):
    delete_person = MyPerson.query.get_or_404(id)
    try:
        db.session.delete(delete_person)
        db.session.commit()
        return redirect("/create/person")
    except Exception as e:
        print(f'Error: {e}')
        return f'Error: {e}'


@app.route("/edit/person/<int:id>",methods=["POST","GET"])
def edit_person(id:int):
    person = MyPerson.query.get_or_404(id)
    if request.method == "POST":
        person.name = request.form['name']
        try:
            db.session.commit()
            return redirect('/create/person')
        except Exception as e:
            print(f'Error: {e}')
            return f'Error: {e}' 
    else:
        return render_template('edit_person.html', person=person)
    

if __name__ == "__main__":

    app.run() # Debugger is on so Flask updates itself