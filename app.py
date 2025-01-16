from flask import Flask, render_template, redirect, request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy

#The app itself
app = Flask(__name__) # It's named like the Python file
Scss(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)

# Class -- row of data
class MyPerson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), default='TecMinds',nullable=False)
    team = db.Column(db.String(20), nullable=False)

    def __repr__(self) -> str:
        return f'Person with ID of {self.id}, is named {self.name} and is in the team {self.team}'


@app.route('/',methods=["POST","GET"]) # Homepage
def index():
    # Add a person to the database
    if request.method == "POST":
        name = request.form['name']
        new_person = MyPerson(name=name,team='TecMinds')    
        try:
            db.session.add(new_person)
            db.session.commit() # Actually commit that to the database
            return redirect('/')
        except Exception as e:
            print(f'Error: {e}')
            return f'Error: {e}'
        
    # Get all the people from the database
    else:
        persons = MyPerson.query.order_by(MyPerson.id).all()
        return render_template('index.html', persons=persons)

# Delete a person from the database
@app.route("/delete/<int:id>")
def delete(id:int):
    delete_person = MyPerson.query.get_or_404(id)
    try:
        db.session.delete(delete_person)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        print(f'Error: {e}')
        return f'Error: {e}'

#Edit an item
@app.route("/edit/<int:id>",methods=["POST","GET"])
def edit(id:int):
    person = MyPerson.query.get_or_404(id)
    if request.method == "POST":
        person.name = request.form['name']
        try:
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(f'Error: {e}')
            return f'Error: {e}' 
    else:
        return render_template('edit.html', person=person)
    
if __name__ in "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True) # Debugger is on so Flask updates itself