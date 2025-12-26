from sqlalchemy import delete
from flask_restx import Namespace, Resource
from flask import current_app as app, request
from models import Project, Bussinessgroups, Customers

projects_ns = Namespace("projects", description="Project related operations")


@projects_ns.route('/available-list')
class Projects(Resource):
    def get(self):
        try:
            project_list = app.session.query(Project.id, Project.name, Customers.customer_code, Customers.customer_name, Project.hd, Project.project_currency, Bussinessgroups.name.label(
                "bussines_group")).select_from(Project).join(Bussinessgroups, Project.bussines_group == Bussinessgroups.id).join(Customers, Project.customer_id == Customers.id).all()
            if project_list:
                return [{"id": pj.id, "name": pj.name, "bussiness_group": pj.bussines_group, "customer_code": pj.customer_code, "customer_name": pj.customer_name, "hd": pj.hd, "currency": pj.project_currency} for pj in project_list]
            else:
                return []
        except Exception as e:
            return {"error": str(e)}, 500


@projects_ns.route('/add-project')
class Addproject(Resource):
    def post(self):
        data = request.get_json()
        try:
            new_project = Project(
                name=data.get("name"),
                bussines_group=data.get("bussines_group"),
                hd=data.get("hd"),
                customer_id=data.get("customer_id"),
                project_currency=data.get("currency"),
                status="Initial"
            )
            app.session.add(new_project)
            app.session.commit()
            return {
                "decs": "successfully added a new project"
            }
        except Exception as e:
            app.logger.error(f"Error in adding project {e}")
            app.session.rollback()
            return {'error': str(e)}, 500


@projects_ns.route('/<ids>', methods=['DELETE'])
class Removeemployee(Resource):
    def delete(self, ids):
        """
        Deletes an employee based on their email address.
        """
        try:
            ids_arr = ids.split(",")
            emp_arr = app.session.query(Project.id).filter(
                Project.id.in_(ids_arr)).all()
            if emp_arr:
                for emp in emp_arr:
                    stmt = delete(Project).where(Project.id == emp.id)
                    app.session.execute(stmt)
                app.session.commit()
                return {
                    'message': f"Projects deleted successfully"
                }, 200
            else:
                return {
                    "error": "Project not found"
                }, 404

        except Exception as e:
            app.logger.error(f"Error in deleting project {e}")
            app.session.rollback()
            return {"error": str(e)}, 500
