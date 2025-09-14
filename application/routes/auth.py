from flask import Blueprint, request, jsonify
from application.models.users import User
from application.config import db

auth_bp = Blueprint("auth", __name__)

# REGISTER
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({"status": "error", "message": "Missing fields"}), 400

    # Check if email already exists
    if User.query.filter_by(email=email).first():
        return jsonify({"status": "error", "message": "Email already registered"}), 400

    # Create new user
    user = User(name=name, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()  # user.id is now set

    print(f"📌 User created with ID: {user.id}")  # debug print

    # Return success with user_id
    return jsonify({"status": "success", "user_id": user.id}), 200

# LOGIN
@auth_bp.route("/login", methods=["POST"])
def login():
    print(" [DEBUG] /login route called")
    try:
        data = request.get_json()
        print("📥 [DEBUG] JSON reçu:", data)

        if not data:
            print("❌ [DEBUG] Aucun JSON reçu")
            return jsonify({"status": "error", "message": "No data received"}), 400

        email = data.get("email")
        password = data.get("password")

        print(f" [DEBUG] Tentative login avec email={email}, password={password}")

        # Ici tu vérifierais dans la DB
        if email == "test@test.com" and password == "1234":
            print(" [DEBUG] Login réussi")
            return jsonify({"status": "success", "message": "Login successful"}), 200
        else:
            print(" [DEBUG] Login échoué")
            return jsonify({"status": "error", "message": "Invalid credentials"}), 401

    except Exception as e:
        print(" [DEBUG] Exception:", e)
        return jsonify({"status": "error", "message": str(e)}), 500
