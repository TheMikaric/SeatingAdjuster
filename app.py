from flask import Flask
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy

#The app itself
app = Flask(__name__) # It's named like the Python file

@app.route('/') # Homepage
def index():
    return "Testing123"

if __name__ in "__main__":
    app.run(debug=True) # Debugger is on so Flask updates itself