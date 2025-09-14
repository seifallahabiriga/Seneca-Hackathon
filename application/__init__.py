from flask import Flask, request
from flask_cors import CORS
from application.config import Config, db



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    CORS(app)
    from application.routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    # Import and register blueprints
    from application.routes.sum import sum_bp
    print("✅ Blueprint importé avec succès")
    app.register_blueprint(sum_bp)
    print("✅ Blueprint enregistré avec succès")
    print("🔍 Routes disponibles :")
    for rule in app.url_map.iter_rules():
        print(f"  {rule.rule} -> {rule.endpoint}")


    with app.app_context():
        db.create_all()  # Create tables

    return app
