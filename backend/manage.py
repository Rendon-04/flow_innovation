from app import create_app
from extensions import db
from flask_migrate import Migrate

# ✅ Create Flask App
app = create_app()

# ✅ Set up Flask-Migrate
migrate = Migrate(app, db)

if __name__ == "__main__":
    app.run(debug=True, port=5001) 
