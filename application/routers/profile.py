from models import Users
from config import Config
from flask import current_app as app
from flask_restx import Namespace, Resource

profile_ns = Namespace("Profile", description="Profile related operations")


@profile_ns.route('/user')
class User(Resource):
    def get(self):
        try:
            user_data = app.session.query(Users.name, Users.email, Users.theme, Users.created_at).filter(
                Users.email == Config.SUPPORT_USER).first()
            if user_data:
                data = {
                    "name": user_data.name,
                    "email": user_data.email,
                    "theme": user_data.theme,
                    "designation": "Admin",
                    "role_id": 1,
                    "created_on": user_data.created_at.strftime("%d/%m/%Y %H:%M:%S")
                }
                return data

            return {'message': 'User created'}, 201
        except Exception as e:
            app.session.rollback()
            return {'error': str(e)}, 500
