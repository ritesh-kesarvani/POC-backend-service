from sqlalchemy import func
from datetime import datetime
from collections import defaultdict
from models import Employee, Project
from utility import shorten_name_initial
from flask_restx import Namespace, Resource
from flask import current_app as app, request

dashboard_ns = Namespace(
    "dashboard", description="Dashboard related operations")


@dashboard_ns.route('/insights')
class Insights(Resource):
    def get(self):
        try:
            call_from = request.args.get("callFrom")
            rows = app.session.query(
                Employee.id.label("emp_id"),
                Employee.grade,
                Employee.allocation_type,
                Employee.project_id,
                Project.id.label("project_id"),
                Project.name,
                Project.hd,
                Employee.created_at,
                Project.status
            ).select_from(Employee).outerjoin(Project, Employee.project_id == Project.id).all()

            projects_data = app.session.query(
                func.count(Project.id).label("p")).first()

            allocation_counter = {}
            grade_counter = {}
            graph_data = {"ver": [], "hor": []}
            bar_graph_data = []
            total_billable_hours = 0
            project_hour_results = []
            project_emp_counter = defaultdict(lambda: {"billable": 0, "t": 0})

            # Aggregate in SINGLE PASS
            for r in rows:
                # Employees in each project
                if r.allocation_type in {"B", "PB"}:
                    project_emp_counter[r.project_id]["billable"] += 1
                project_emp_counter[r.project_id]["t"] += 1

            for r in rows:
                if call_from == "pgch":
                    # Grade distribution
                    grade_counter[r.grade] = grade_counter.get(r.grade, 0) + 1
                else:
                    if call_from == "d":
                        # Allocation distribution
                        allocation_counter[r.allocation_type.lower()] = allocation_counter.get(
                            r.allocation_type.lower(), 0) + 1

                    name = shorten_name_initial(r.name if r.name else "")
                    if r.project_id and r.status != "Escalate":
                        employees = project_emp_counter.get(
                            r.project_id, {}).get("t", 0)

                        if call_from == "bgph":
                            # Employees per project
                            bg = {
                                "employees": employees,
                                "name": name
                            }
                            if bg not in bar_graph_data:
                                bar_graph_data.append(bg)
                        else:
                            dy = (datetime.now().date() -
                                  r.created_at.date()).days

                            if call_from == "d" and r.allocation_type in {"B", "PB"}:
                                billable_emp = project_emp_counter.get(
                                    r.project_id, {}).get("billable", 0)
                                tl_hours = int(dy) * r.hd * billable_emp
                                total_billable_hours += tl_hours
                                # Billable Hours Percentage per project
                                if name not in graph_data["ver"]:
                                    graph_data["ver"].append(name)
                                    graph_data["hor"].append(
                                        tl_hours if tl_hours > 0 else 0)

                            phr = {
                                "name": name,
                                "employees": employees,
                                "hours_a_day": r.hd
                            }
                            if phr not in project_hour_results:
                                project_hour_results.append(phr)

            response = []

            if call_from == "d":
                response = {
                    "emp_count": len(rows),
                    "allocation": allocation_counter,
                    "projects_tt": projects_data.p,
                    "total_billable_hours": total_billable_hours,
                    "graph": graph_data,
                }
            elif call_from == "bgph" and bar_graph_data:
                response = bar_graph_data.copy()
            elif call_from == "agph" and project_hour_results:
                response = project_hour_results.copy()
            elif call_from == "pgch":
                # Employees per grade
                response = [{"name": f"{g} Grade", "value": c}
                            for g, c in grade_counter.items()]

            return response, 200
        except Exception as e:
            app.session.rollback()
            return {"error": str(e)}, 500
