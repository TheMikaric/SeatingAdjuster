from flask import Flask, render_template
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
    return render_template('index.html')


if __name__ in "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True) # Debugger is on so Flask updates itself