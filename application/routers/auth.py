import jwt
from models import Users
from config import Config
from datetime import datetime, timedelta
from flask_restx import Namespace, Resource
from flask import request, current_app as app
from werkzeug.security import generate_password_hash, check_password_hash

auth_ns = Namespace("users", description="User related operations")
healthcheck_ns = Namespace("health check")


# Healthcheck API to return the service status
@healthcheck_ns.route('/healthcheck')
class Healthcheck(Resource):
    def get(self):
        return {
            "status": "success"
        }, 200


# CREATE - Add a new user
@auth_ns.route('/register')
class Signup(Resource):
    def post(self):
        data = request.get_json()
        if not data or 'first_name' not in data or 'last_name' not in data or 'email' not in data or 'password' not in data:
            return {'error': 'Name, email are required'}, 400

        try:
            # Added a check for support user only
            if data["email"] != Config.SUPPORT_USER:
                return {"error": "Website Is Available For Limited User"}, 500

            existing_user = app.session.query(Users.id).filter(
                Users.email == data["email"]).first()
            if existing_user:
                return {"error": "User already exists"}, 400

            hashed_password = generate_password_hash(
                data['password'], method='pbkdf2:sha256')
            new_entry = Users(
                name=data["first_name"] + " " + data["last_name"],
                email=data["email"],
                password=hashed_password
            )
            app.session.add(new_entry)
            app.session.commit()
            return {'message': 'User created'}, 201
        except Exception as e:
            app.logger.error(f"Error in signup {e}")
            app.session.rollback()
            return {'error': str(e)}, 500


@auth_ns.route('/login')
class Signin(Resource):
    def post(self):
        data = request.get_json()
        if not data or 'email' not in data or 'password' not in data:
            return {'error': 'email and Password are required'}, 400

        try:
            # Added a check for support user only
            if data["email"] != Config.SUPPORT_USER:
                return {"error": "Invalid User"}, 401

            user_data = app.session.query(Users.email, Users.password, Users.theme).filter(
                Users.email == data["email"]).first()
            if user_data and check_password_hash(user_data.password, data['password']):
                token = jwt.encode({
                    'username': user_data.email,
                    'exp': datetime.now() + timedelta(minutes=30)
                }, Config.SECRET_KEY, algorithm="HS256")

                return {'access_token': token, "theme": user_data.theme}, 200
            else:
                return {'desc': "Email or Password not matched"}, 401

        except Exception as e:
            app.logger.error(f"Error in log in {e}")
            app.session.rollback()
            return {'error': str(e)}, 500
