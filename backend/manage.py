from app import create_app
from extensions import db
from flask_migrate import Migrate

app = create_app()  # Create the app instance using the factory function
migrate = Migrate(app, db)

if __name__ == "__main__":
    app.run(debug=True)  # TODO: Set to False in production