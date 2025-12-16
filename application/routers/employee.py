import re
import pandas as pd
from sqlalchemy import delete
from datetime import datetime
from flask_restx import Namespace, Resource
from flask import request, current_app as app
from models import Employee, Project, Bussinessgroups, Customers, Reportinmanagers
from constant import DESINATIONS, DB_DESINATIONS, ALLOCATION_GROUP, UI_ALLOCATION_GROUP


employee_ns = Namespace("employee", description="Employee related operations")


@employee_ns.route('/list')
class User(Resource):
    '''
    API to fetch the employees of all projects
    '''
    def get(self):
        try:
            # Check for duplicate email
            user_data = app.session.query(Employee).all()
            if user_data:
                existing_irm = app.session.query(
                    Reportinmanagers.id, Reportinmanagers.name).all()
                existing_irm_data = {irm.id: irm.name for irm in existing_irm}

                employee_list = []
                for res in user_data:
                    employee_list.append({
                        "id": res.id,
                        "emp_org_id": res.emp_org_id,
                        "first_name":  res.first_name,
                        "last_name":  res.last_name,
                        "email":  res.work_email,
                        "compentency":  res.compentency,
                        "reporting_to":  existing_irm_data.get(res.reporting_to),
                        "grade":  res.grade,
                        "project_id":  res.project_id,
                        "doj":  datetime.strftime(res.doj, "%Y-%m-%d"),
                        "allocation_type":  UI_ALLOCATION_GROUP.get(res.allocation_type, "P"),
                        "allocation_percent":  res.allocation_percent,
                        "allocation_date":  res.created_at.strftime("%Y-%m-%d"),
                        "designation":  DESINATIONS.get(res.designation, "Intern Software Engineer")
                    })
                return employee_list
            else:
                return []
        except Exception as e:
            app.logger.error(f"Error in fetching employees {e}")
            app.session.rollback()
            return {
                "desc": str(e)
            }, 500


@employee_ns.route('/add-employee')
class Addemployee(Resource):
    """
    API to register a new employee on project
    """
    def post(self):
        data = request.get_json()
        try:
            email = data['work_email']
            # Basic email format check
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                return {"error": "Invalid email format"}, 400

            # Check for duplicate email
            user_data = app.session.query(Employee.id).filter(
                Employee.work_email == email).first()
            if user_data:
                return {"error": "Email already exists"}, 409

            doj = datetime.strptime(data.get("doj"), "%Y-%m-%d")

            new_employee = Employee(
                emp_org_id=data.get("emp_org_id"),
                first_name=data.get("first_name"),
                last_name=data.get("last_name"),
                work_email=email,
                compentency=data.get("compentency"),
                reporting_to=data.get("reporting_to"),
                grade=data.get("grade"),
                project_id=data.get("project_id"),
                doj=doj,
                allocation_type=data.get("allocation_type"),
                allocation_percent=data.get("allocation_percent"),
                designation=data.get("designation")
            )
            app.session.add(new_employee)
            app.session.commit()
            return {
                "decs": "successfully added"
            }, 200
        except Exception as e:
            app.logger.error(f"Error in adding employee {e}")
            app.session.rollback()
            return {'error': str(e)}, 500


@employee_ns.route('/import-excel', methods=['POST'])
class Importemployee(Resource):
    """
    API to add application data from excel file
    """
    def post(self):
        app.logger.info(f"file: {request.files}, {request.content_type}")
        if not request.files.get("file"):
            return {"error": "No file part in the request"}, 400

        file = request.files['file']
        if file.name == '':
            return {"error": "No selected file"}, 400

        if file:
            try:
                filename = file.filename
                file_extension = filename.rsplit('.', 1)[1].lower()

                if file_extension == 'csv':
                    df = pd.read_csv(file)
                elif file_extension == 'xlsx':
                    df = pd.read_excel(file, sheet_name="Python Report")
                else:
                    return {"error": "Unsupported file type"}, 400

                # 'Parent BUHSSUH', 'Parent BGHSSGH', 'Parent BG', 'Parent BU', 'Parent SBU', 'User Skill Category', 'Primary Skill', 'Secondary Skill', 'Resource Manager',, 'Resource Location', 'Resignation Date', 'Last Working Date', 'Resource Entity',
                EXPECTED_COLUMNS = ['Employee ID', 'Employee Name', 'Grade', 'Designation', 'Date Of Joining', 'Email', 'IRM', 'Competency',  'Allocation Type',  'Allocation %',
                                    'Billing Type',  'Hourly Bill Rate', 'Customer Group', 'Customer Code', 'Customer Name',  'Project Name', 'Project Hour Day', 'Project Currency', 'Allocation Start Date']
                sheet_columns = df.columns.to_list()
                for ec in EXPECTED_COLUMNS:
                    if ec not in sheet_columns:
                        return {
                            "Error": "Columns are missing"
                        }, 400

                existing_users = app.session.query(
                    (Employee.emp_org_id.distinct()).label("emp_org_id")).all()
                existing_users_ids = [e.emp_org_id for e in existing_users]

                existing_projects = app.session.query((Customers.customer_code.distinct()).label(
                    "customer_code"), Project.id).select_from(Project).join(Customers, Project.customer_id == Customers.id).all()
                existing_project_ids = {
                    e.customer_code: e.id for e in existing_projects}

                existing_bussiness_group = app.session.query(
                    Bussinessgroups.id, Bussinessgroups.name).all()
                existing_bussiness_group_data = {
                    bg.name: bg.id for bg in existing_bussiness_group
                }

                existing_irm = app.session.query(
                    Reportinmanagers.id, Reportinmanagers.name).all()
                existing_irm_ids = {irm.name: irm.id for irm in existing_irm}
                for _, row in df.iterrows():
                    name_arr = row["Employee Name"].split(" ")
                    first_name = ""
                    last_name = ""
                    if name_arr:
                        first_name = name_arr[0]
                        if len(name_arr) > 1:
                            last_name = name_arr[1]

                    if row.get("Customer Code") not in existing_project_ids:
                        cg = row.get("Customer Group")
                        if existing_bussiness_group_data.get(cg):
                            bg_id = existing_bussiness_group_data[cg]
                            app.logger.info(
                                f"Bussiness Group Exists with name {cg}")
                        else:
                            new_bg = Bussinessgroups(
                                name=cg
                            )
                            app.session.add(new_bg)
                            app.session.flush()
                            bg_id = new_bg.id

                        new_cm = Customers(
                            bussiness_group_id=bg_id,
                            customer_name=row.get("Customer Name"),
                            customer_code=row.get("Customer Code")
                        )
                        app.session.add(new_cm)
                        app.session.flush()
                        cm_id = new_cm.id

                        new_project = Project(
                            name=row.get("Project Name"),
                            bussines_group=bg_id,
                            hd=row.get("Project Hour Day"),
                            customer_id=cm_id,
                            project_currency=row.get("Project Currency"),
                            status=row.get("Status", "initial")
                        )
                        app.session.add(new_project)
                        app.session.flush()
                        existing_project_ids[row.get(
                            "Customer Code")] = new_project.id
                        existing_project_ids[row.get(
                            "Customer Code")] = new_project.id

                    if row.get("IRM") not in existing_irm_ids:
                        name_arr = row["IRM"].lower().split(" ")
                        irm_email = ""
                        if name_arr:
                            irm_email = f"{name_arr[0]}.{name_arr[1] if len(name_arr) > 1 else ""}@yash.com"
                        new_irm = Reportinmanagers(
                            name=row["IRM"],
                            email=irm_email
                        )
                        app.session.add(new_irm)
                        app.session.flush()
                        irm_id = new_irm.id
                        existing_irm_ids[row["IRM"]] = irm_id
                    else:
                        irm_id = existing_irm_ids[row["IRM"]]

                    if row.get("Employee ID") not in existing_users_ids:
                        new_employee = Employee(
                            emp_org_id=row.get("Employee ID"),
                            first_name=first_name,
                            last_name=last_name,
                            work_email=row.get("Email"),
                            compentency=row.get("Competency"),
                            reporting_to=irm_id,
                            grade=row.get("Grade"),
                            project_id=existing_project_ids[row.get(
                                "Customer Code")],
                            doj=row.get("Date Of Joining"),
                            allocation_type=ALLOCATION_GROUP.get(row.get("Allocation Type"), "Pool"),
                            allocation_percent=row.get("Allocation %"),
                            designation=DB_DESINATIONS.get(
                                row.get("Designation"), "ISE"),
                            created_at=row.get("Allocation Start Date")
                        )
                        app.session.add(new_employee)
                        existing_users_ids.append(row.get("Employee ID"))
                    else:
                        app.logger.info(
                            f'{row.get("Employee ID")} Already Exists')
                app.session.commit()
                return {"message": "File uploaded and data saved successfully"}, 200

            except Exception as e:
                app.logger.error(f"Error in importing employees {e}")
                app.session.rollback()
                return {"error": "error"}, 500


@employee_ns.route('/<ids>', methods=['DELETE'])
class Removeemployee(Resource):
    def delete(self, ids):
        """
        Deletes an employee based on their email address.
        """
        try:
            ids_arr = ids.split(",")
            emp_arr = app.session.query(Employee.id).filter(
                Employee.id.in_(ids_arr)).all()
            if emp_arr:
                for emp in emp_arr:
                    stmt = delete(Employee).where(Employee.id == emp.id)
                    app.session.execute(stmt)
                app.session.commit()
                return {
                    'message': f"Employees deleted successfully"
                }, 200
            else:
                return {
                    "error": "Employee not found"
                }, 404

        except Exception as e:
            app.logger.error(f"Error in removing employee {e}")
            app.session.rollback()
            return {"error": str(e)}, 500
