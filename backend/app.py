from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config.from_object("config")
#Set the database URI and disable track modifications warning    TODO
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'  # or use your actual DB URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Import routes
from routes import *

if __name__ == "__main__":
    app.run(debug=True)

