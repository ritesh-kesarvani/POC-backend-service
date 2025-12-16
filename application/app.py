from config import Config
from flask import Flask
from flask_restx import Api
from flask_cors import CORS
from database import init_db
from routers import auth, dashboard, employee, profile, projects, managers, bussiness_clients


def create_app():
    app = Flask(__name__)
    # Create Flask app
    CORS(app)

    # Create API object
    api = Api(app, version="1.0", title="Multi-Namespace API",
              description="Application with multiple namespaces")

    api.add_namespace(auth.healthcheck_ns, path="/")
    api.add_namespace(auth.auth_ns, path="/api/v1/auth")
    api.add_namespace(profile.profile_ns, path="/api/v1/mysetting")
    api.add_namespace(dashboard.dashboard_ns, path="/api/v1/dashboard")
    api.add_namespace(employee.employee_ns, path="/api/v1/employee")
    api.add_namespace(projects.projects_ns, path="/api/v1/projects")
    api.add_namespace(managers.manager_ns, path="/api/v1/manager")
    api.add_namespace(bussiness_clients.bussiness_ns, path="/api/v1/bussiness")

    app.logger.setLevel(Config.LOG_LEVEL)
    app.session = init_db()
    return app


app = create_app()
if __name__ == '__main__':
    app.run(debug=True)
