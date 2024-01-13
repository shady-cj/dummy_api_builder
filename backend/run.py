from models import db
from api.v1.app import app, migrate

db.init_app(app)
migrate.init_app(app, db)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5900, debug=True)
