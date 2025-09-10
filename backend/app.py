import os
from flask import Flask, send_from_directory, abort
from application.config import LocalDevelopementConfig
import logging
from werkzeug.security import generate_password_hash
from application.schema import db, User, RoleEnum
from flask_restful import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from application.celery_init import celery_init_app
from application.extensions import limiter
from celery.schedules import crontab
from application.task import monthly_report

from application.api.auth import CaretakerRegisterAPI, SeniorCitizenRegisterAPI, LoginAPI 
from application.api.admin import (
    AdminDashboardAPI, 
    AdminViewUsersAPI, 
    AdminAssignCaretakerAPI,
    AdminViewCaretakerRequestsAPI, 
    AdminApproveCaretakerAPI,
    AdminBlockCaretakerAPI
)
from application.api.senior import SeniorDashboardAPI, SeniorRoutineAPI, SeniorSOSAPI, SeniorQueryAPI, SeniorDashboard
from application.api.caretaker import (
    CaretakerDashboardAPI,
    CaretakerEmergencyAPI,
    CaretakerMissedTasksAPI,
    CaretakerSOSAlertsAPI,
    CaretakerQueriesAPI,
    CaretakerAddRoutineAPI,
    CaretakerGetTasksAPI,
    CaretakerEditTaskAPI,
    CaretakerDeleteTaskAPI,
    CaretakerProfileAPI,
    CaretakerUpdateProfileAPI,
    SeniorUpdateMedicalConditionAPI,
    CaretakerStatsAPI,
)
from application.api.senior import (
    SeniorDashboardAPI,
    SeniorRoutineAPI,
    SeniorSOSAPI,
    SeniorQueryAPI,
    SeniorDashboard
)


logging.basicConfig(filename='debug.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

app = None
api = None


def create_app():

    app = Flask(__name__)

    # Create 'resume' directory if it does not exist
    resume_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resume')
    os.makedirs(resume_dir, exist_ok=True)

    if os.getenv('ENV', "developement") == "production":
        raise Exception("Currently no production config is setup.")
    else:
        print("Starting local developement")
        app.config.from_object(LocalDevelopementConfig)


    db.init_app(app)
    api = Api(app)
    jwt = JWTManager(app)

    limiter.init_app(app)



    celery=celery_init_app(app)
    celery.autodiscover_tasks()




    app.app_context().push()
    db.create_all()

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Create a default admin user if it doesn't exist

    if not User.query.filter_by(roleId="ADMIN").first():
        admin_user = User(contact=1234567890,
                          isVerified=True,
                            roleId=RoleEnum.ADMIN)
        admin_user.set_password("9999999999")
        db.session.add(admin_user)
        db.session.commit()



    api.add_resource(CaretakerRegisterAPI, '/api/register/caretaker',methods=['POST'])

    api.add_resource(SeniorCitizenRegisterAPI, '/api/register/senior', methods=['POST'])
    api.add_resource(LoginAPI, '/api/login', methods=['POST'])

    # admin
    api.add_resource(AdminDashboardAPI, '/api/admin/dashboard', methods=['GET'])
    api.add_resource(AdminViewUsersAPI, '/api/admin/users', methods=['GET'])
    api.add_resource(AdminAssignCaretakerAPI, '/api/admin/assign-caretaker', methods=['POST'])
    api.add_resource(AdminViewCaretakerRequestsAPI, '/api/admin/caretaker-requests')
    api.add_resource(AdminApproveCaretakerAPI, '/api/admin/approve-caretaker')
    api.add_resource(AdminBlockCaretakerAPI, '/api/admin/block-caretaker', methods=['POST'])

    #caretaker
    api.add_resource(CaretakerDashboardAPI, '/api/caretaker/dashboard', methods=['GET'])
    api.add_resource(CaretakerEmergencyAPI, '/api/caretaker/emergencies', methods=['GET','PUT'])
    api.add_resource(CaretakerMissedTasksAPI, '/api/caretaker/missed-tasks', methods=['GET'])
    api.add_resource(CaretakerSOSAlertsAPI, '/api/caretaker/sos-alerts', methods=['GET'])
    api.add_resource(CaretakerQueriesAPI, '/api/caretaker/queries', methods=['GET','PUT'])
    api.add_resource(CaretakerAddRoutineAPI, '/api/caretaker/routine', methods=['POST'])
    api.add_resource(CaretakerGetTasksAPI, '/api/caretaker/tasks', methods=['GET'])
    api.add_resource(CaretakerEditTaskAPI, '/api/caretaker/tasks/<string:task_id>', methods=['PUT'])
    api.add_resource(CaretakerDeleteTaskAPI, '/api/caretaker/tasks/<string:task_id>', methods=['DELETE'])
    api.add_resource(CaretakerProfileAPI, '/api/caretaker/profile', methods=['GET'])
    api.add_resource(CaretakerUpdateProfileAPI, '/api/caretaker/profile')
    api.add_resource(SeniorUpdateMedicalConditionAPI, '/api/senior/<string:senior_id>/medical-condition')
    api.add_resource(CaretakerStatsAPI, '/api/caretaker/stats', methods=['GET'])

    #senior citizen
    api.add_resource(SeniorDashboard, '/api/senior', methods=['GET']) #to check security
    api.add_resource(SeniorDashboardAPI, '/api/senior/dashboard', methods=['GET'])
    api.add_resource(SeniorRoutineAPI, '/api/senior/routine', methods=['GET','PUT'])
    api.add_resource(SeniorSOSAPI, '/api/senior/sos', methods=['POST'])
    api.add_resource(SeniorQueryAPI, '/api/senior/query', methods=['GET', 'POST'])
    
    @app.route('/', methods=['GET'])
    def home():
        return "Welcome to the SeniorSphere API" , 200

    return app, api, jwt ,celery

app, api, jwt ,celery = create_app()

@app.route('/api/resume/<filename>', methods=['GET'])
def serve_resume(filename):
    resume_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resume')
    try:
        return send_from_directory(resume_dir, filename, as_attachment=False)
    except FileNotFoundError:
        abort(404, description="Resume not found")


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        # crontab(minute=0, hour=0),
        crontab(minute='*/1'),
        monthly_report.s(),
    )

if __name__ == '__main__':
    app.run(debug=True)