import re
from sqlalchemy import delete
from models import Reportinmanagers
from flask_restx import Namespace, Resource
from flask import request, current_app as app


manager_ns = Namespace(
    "Managers", description="Reporting manager related operations")


# CREATE - Add a new user
@manager_ns.route('/reporting-managers')
class Reportingmanagers(Resource):
    def get(self):
        try:
            results = []
            managers_list = app.session.query(
                Reportinmanagers.id, Reportinmanagers.email, Reportinmanagers.name).all()
            if managers_list:
                for ml in managers_list:
                    results.append({
                        "id": ml.id, "name": ml.name, "email": ml.email
                    })

            return results, 200
        except Exception as e:
            return {"error": str(e)}, 500


@manager_ns.route('/add-manager')
class Addmanager(Resource):
    def post(self):
        data = request.get_json()
        try:
            email = data['email']
            # Basic email format check
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                return {"error": "Invalid email format"}, 400

            # Check for duplicate email
            user_data = app.session.query(Reportinmanagers.id).filter(
                Reportinmanagers.email == email).first()
            if user_data:
                return {"error": "Email already exists"}, 409

            new_rm = Reportinmanagers(
                name=data.get("name"),
                email=email
            )
            app.session.add(new_rm)
            app.session.commit()
            return {
                "decs": "successfully added Reporting manager"
            }, 200
        except Exception as e:
            app.logger.error(f"Error in addinf manager {e}")
            app.session.rollback()
            return {'error': str(e)}, 500


@manager_ns.route('/<string:email>', methods=['DELETE'])
class Removemanager(Resource):
    def delete(self, email):
        """
        Deletes an employee based on their email address.
        """
        try:
            emp = app.session.query(Reportinmanagers.id).filter(
                Reportinmanagers.email == email).first()
            if emp:
                stmt = delete(Reportinmanagers).where(
                    Reportinmanagers.id == emp.id)
                app.session.execute(stmt)
                app.session.commit()
                return {
                    'message': f"Manager {email} deleted successfully",
                    'deleted_email': email
                }, 200
            else:
                return {
                    "error": "Employee not found"
                }, 404

        except Exception as e:
            app.logger.error(f"Error in deleting manager {e}")
            app.session.rollback()
            return {"error": str(e)}, 500
