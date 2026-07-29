from flask import Blueprint, request, jsonify
from models import db, User
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth = Blueprint("auth", __name__)

@auth.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    # Check if email already exists
    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already exists"}), 400

    # Hash the password
    hashed_password = generate_password_hash(password).decode("utf-8")

    new_user = User(
        username=username,
        email=email,
        password=hashed_password
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

@auth.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    # 1. Check if the user exists in the database
    user = User.query.filter_by(email=email).first()

    # 2. Verify user exists and the password matches the hash
    if not user or not check_password_hash(user.password, password):
        return jsonify({"message": "Invalid email or password"}), 401

    # 3. Generate the JWT access token
    # We use the user's ID as the identity in the token
    access_token = create_access_token(identity=str(user.id))

    # 4. Return the token to the client
    return jsonify({
        "message": "Login successful",
        "access_token": access_token
    }), 200

@auth.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    # 1. Get the user's ID from the JWT token
    current_user_id = get_jwt_identity()

    # 2. Fetch the user from the database
    user = db.session.get(User, current_user_id)

    if not user:
        return jsonify({"message": "User not found"}), 404

    # 3. Return the protected data
    return jsonify({
        "message": f"Welcome to your profile, {user.username}!",
        "email": user.email
    }), 200