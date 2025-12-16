from sqlalchemy import delete
from flask_restx import Namespace, Resource
from flask import request, current_app as app
from models import Bussinessgroups, Customers


bussiness_ns = Namespace(
    "BussinessGroup", description="Bussiness Groups related operations")


# CREATE - Add a new user
@bussiness_ns.route('/groups')
class User(Resource):
    def get(self):
        try:
            results = []
            bussiess_list = app.session.query(
                Bussinessgroups.id, Bussinessgroups.name).all()
            if bussiess_list:
                results = [{"id": bl.id, "name": bl.name}
                           for bl in bussiess_list]

            return results, 200
        except Exception as e:
            return {"error": str(e)}, 500


@bussiness_ns.route('/cusomters/<bg_id>')
class User(Resource):
    def get(self, bg_id):
        try:
            results = []
            customer = app.session.query(Customers.id, Customers.customer_name, Customers.customer_code).filter(
                Customers.bussiness_group_id == bg_id).all()
            if customer:
                results = [{"id": c.id, "customer_name": c.customer_name,
                            "customer_code": c.customer_code} for c in customer]

            return results, 200
        except Exception as e:
            return {"error": str(e)}, 500


@bussiness_ns.route('/cusomters')
class Customerdata(Resource):
    def get(self):
        try:
            results = []
            customers_data = app.session.query(Customers.id, Customers.customer_name, Customers.customer_code, Bussinessgroups.name.label(
                "bg_name")).select_from(Customers).join(Bussinessgroups, Customers.bussiness_group_id == Bussinessgroups.id).all()
            if customers_data:
                results = [{"id": customer.id, "bussiness_group": customer.bg_name, "customer_name": customer.customer_name,
                            "customer_code": customer.customer_code} for customer in customers_data]

            return results, 200
        except Exception as e:
            return {"error": str(e)}, 500


@bussiness_ns.route('/add-client')
class Addemployee(Resource):
    def post(self):
        data = request.get_json()
        try:
            customer_code = data['customer_code']

            # Check for duplicate customer
            customer_data = app.session.query(Customers.id).filter(
                Customers.customer_code == customer_code).first()
            if customer_data:
                return {"error": "Email already exists"}, 409

            if data.get("is_new_group"):
                new_bg = Bussinessgroups(
                    name=data.get("name")
                )
                app.session.add(new_bg)
                app.session.flush()
                bg_id = new_bg.id
            else:
                bg_id = data.get("name")

            new_rm = Customers(
                bussiness_group_id=bg_id,
                customer_code=customer_code,
                customer_name=data.get("customer_name")
            )
            app.session.add(new_rm)
            app.session.commit()
            return {
                "decs": "successfully added Customer"
            }, 200
        except Exception as e:
            app.logger.error(f"Error in adding Employee {e}")
            app.session.rollback()
            return {'error': str(e)}, 500


@bussiness_ns.route('/<id>', methods=['DELETE'])
class Removecustomer(Resource):
    def delete(self, id):
        """
        Deletes an employee based on their email address.
        """
        try:
            emp = app.session.query(Customers.id, Customers.customer_name).filter(
                Customers.id == id).first()
            if emp:
                stmt = delete(Customers).where(Customers.id == emp.id)
                app.session.execute(stmt)
                app.session.commit()
                return {
                    'message': f"Bussiness with {emp.customer_name} deleted successfully",
                }, 200
            else:
                return {
                    "desc": "Employee not found"
                }, 404

        except Exception as e:
            app.logger.error(f"Error in removing customer {e}")
            app.session.rollback()
            return {"error": str(e)}, 500
