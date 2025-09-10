from flask_restful import Resource
from flask import jsonify, request
from application.schema import db, User, RoleEnum, Caretaker, SeniorCitizen, SOSAlert, Query, Tasks
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timedelta
from functools import wraps
import uuid
from application.extensions import limiter

# ------------------ Decorator ------------------
def caretaker_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user or user.roleId != RoleEnum.CARETAKER:
            return jsonify({"error": "Caretaker privileges required"}), 403
        return fn(*args, **kwargs)
    return wrapper

# ------------------ Helper Function ------------------
def get_assigned_senior_ids(caretaker_id):
    caretaker = Caretaker.query.filter_by(userId=caretaker_id).first()
    if not caretaker:
        return None, []
    assigned = SeniorCitizen.query.filter_by(assignedCare=caretaker.userId).all()
    return caretaker, [s.userId for s in assigned]

# ------------------ APIs ------------------
class CaretakerDashboardAPI(Resource):
    @caretaker_required
    def get(self):
        
        current_user_id = get_jwt_identity()
        caretaker = Caretaker.query.filter_by(userId=current_user_id).first()
        if not caretaker:
            return {"error": "Caretaker not found"}, 404

        print("Fetching assigned seniors for caretaker:", caretaker.userId)
        assigned_seniors = SeniorCitizen.query.filter_by(assignedCare=caretaker.userId).all()
        print(f"Found {len(assigned_seniors)} assigned seniors : {assigned_seniors}")
        return jsonify([
            {
                "id": senior.userId,
                "name": senior.fullName,
                "age": senior.age,
                "contact": senior.contact,
                "city": senior.city,
                "medCon": senior.medCon,
                "state": senior.state,
                "pinCode": senior.pinCode,
                "languages": senior.languages,
                "emergencyContact": senior.emergencyContact,
                "emergencyContactName": senior.emergencyContactName,
                "emergencyEmail": senior.emergencyEmail
            } for senior in assigned_seniors
        ])

class CaretakerEmergencyAPI(Resource):
    @caretaker_required
    def get(self):
        print("Testing")
        current_user_id = get_jwt_identity()
        caretaker, senior_ids = get_assigned_senior_ids(current_user_id)
        print(caretaker, senior_ids)

        if not caretaker:
            return {"error": "Caretaker not found"}, 404

        # Explicitly join SOSAlert with SeniorCitizen
        alerts = db.session.query(SOSAlert, SeniorCitizen).join(
            SeniorCitizen, SOSAlert.sender_id == SeniorCitizen.userId
        ).filter(
            SOSAlert.sender_id.in_(senior_ids),
            SOSAlert.isResolved == False
        ).all()

        print(alerts)

        # ✅ Return dict/list, NOT jsonify
        return [{
            "alertId": alert.alertId,
            "name": senior.fullName,
            "issue": f"Emergency Alert at {alert.location}",
            "condition": senior.medCon
        } for alert, senior in alerts], 200
    
    @caretaker_required
    def put(self):
        data = request.get_json()
        alert_id = data.get("alertId")

        alert = SOSAlert.query.filter_by(alertId=alert_id).first()
        if not alert:
            return {"error": "Alert not found"}, 404

        alert.isResolved = True
        db.session.commit()
        return {"message": "Resolved successfully"}, 200


from datetime import datetime
from flask import jsonify

class CaretakerMissedTasksAPI(Resource):
    @caretaker_required
    def get(self):
        current_user_id = get_jwt_identity()
        now = datetime.utcnow()

        # Get all pending tasks
        tasks = Tasks.query.filter_by(
            assignedBy=current_user_id,
            status=False
        ).all()

        missed = []
        for task in tasks:
            try:
                # Parse duration string into datetime
                due_time = datetime.fromisoformat(task.duration)

                # If current time passed the due_time and still pending → missed
                if due_time < now:
                    missed.append({
                        "date": due_time.strftime("%B %d"),
                        "senior": task.senior.fullName,
                        "task": task.taskDetails
                    })
            except Exception as e:
                print(f"Error parsing duration for task {task.taskId}: {e}")
                continue

        return jsonify(missed)


class CaretakerSOSAlertsAPI(Resource):
    @caretaker_required
    def get(self):
        current_user_id = get_jwt_identity()
        caretaker, senior_ids = get_assigned_senior_ids(current_user_id)
        if not caretaker:
            return {"error": "Caretaker not found"}, 404

        alerts = SOSAlert.query.filter(
            SOSAlert.sender_id.in_(senior_ids)
        ).order_by(SOSAlert.alertTime.desc()).limit(10).all()

        return jsonify([{
            "time": alert.alertTime.strftime("%I:%M %p"),
            "senior": alert.sender.fullName,
            "reason": f"Emergency at {alert.location}",
            "condition": alert.sender.medCon,
            "isResolved": alert.isResolved
        } for alert in alerts])

class CaretakerQueriesAPI(Resource):
    @caretaker_required
    def get(self):
        current_user_id = get_jwt_identity()

        queries = Query.query.filter_by(
            assignedCaretakerId=current_user_id,
            status='Pending'
        ).order_by(Query.timeStamp.desc()).all()

        return jsonify([{
            "date": query.timeStamp.strftime("%B %d"),
            "senior": query.sender.fullName,
            "question": query.message,
            "queryId": query.queryId,
            "status": query.status
        } for query in queries])
    
    @caretaker_required
    def put(self):
        data = request.get_json()
        query_id = data.get("queryId")
        print("Received query ID:", query_id)

        query = Query.query.filter_by(queryId=query_id).first()
        if not query:
            return {"error": "Query not found"}, 404
        
        query.status = "Resolved"
        db.session.commit()

        return {"message": "Query marked as resolved"}, 200

        

class SeniorHealthUpdateAPI(Resource):
    @jwt_required()
    def put(self, senior_id):
        user_id = get_jwt_identity()
        senior = SeniorCitizen.query.get(senior_id)

        if not senior:
            return {"error": "Senior not found"}, 404

        if user_id != senior.userId and user_id != senior.assignedCare:
            return {"error": "Not authorized to update health condition"}, 403

        data = request.get_json()
        new_condition = data.get("condition")
        if not new_condition:
            return {"error": "Condition field is required"}, 400

        senior.medCon = new_condition
        db.session.commit()

        return {"message": "Health condition updated successfully"}

class CaretakerAddRoutineAPI(Resource):
    @caretaker_required
    @limiter.limit("10 per minute")  # Limit to 10 requests per minute
    def post(self):
        data = request.get_json()
        senior_id = data.get('senior_id')
        task_name = data.get('task_name')
        details = data.get('details')
        duration = data.get('duration')

        if not senior_id or not task_name or not details or not duration:
            return {"error": "All fields (senior_id, task_type, details, duration) are required"}, 400

        # Check if the senior exists
        senior = User.query.get(senior_id)
        if not senior or senior.roleId != RoleEnum.SENIOR_CITIZEN:
            return {"error": "Senior Citizen not found"}, 404
        print(data)
        # Add the task
        new_task = Tasks(
            taskId=str(uuid.uuid4()),
            assignedTo=senior_id,
            taskName=task_name,
            taskDetails=details,
            duration=duration,
            assignedBy=get_jwt_identity(),
            status=False  # Default status is incomplete
        )
        db.session.add(new_task)
        db.session.commit()

        return {"message": "Task added successfully"}, 201

class CaretakerGetTasksAPI(Resource):
    @caretaker_required
    def get(self):
        current_user_id = get_jwt_identity()

        # Fetch all tasks assigned by the caretaker
        tasks = Tasks.query.filter_by(assignedBy=current_user_id).all()

        if not tasks:
            return {"message": "No tasks found"}, 200

        return jsonify([
            {
                "id": task.taskId,
                "taskName": task.taskName,
                "details": task.taskDetails,
                "duration": task.duration,
                "status": "Completed" if task.status else "Pending",
                "senior": {
                    "id": task.assignedTo,
                    "name": task.senior.fullName,
                    "city": task.senior.city
                }
            } for task in tasks
        ])
    
class CaretakerEditTaskAPI(Resource):
    @caretaker_required
    def put(self, task_id):
        current_user_id = get_jwt_identity()
        task = Tasks.query.filter_by(taskId=task_id, assignedBy=current_user_id).first()

        if not task:
            return {"error": "Task not found or not authorized to edit"}, 404

        data = request.get_json()
        task_name = data.get('task_name')
        details = data.get('details')
        duration = data.get('duration')
        status = data.get('status')

        if not task_name or not details or not duration:
            return {"error": "All fields (task_name, details, duration) are required"}, 400

        # Update task details
        task.taskName = task_name
        task.taskDetails = details
        task.duration = duration
        task.status = status == "Completed"
        db.session.commit()

        return {"message": "Task updated successfully"}, 200

class CaretakerDeleteTaskAPI(Resource):
    @caretaker_required
    def delete(self, task_id):
        current_user_id = get_jwt_identity()
        task = Tasks.query.filter_by(taskId=task_id, assignedBy=current_user_id).first()

        if not task:
            return {"error": "Task not found or not authorized to delete"}, 404

        db.session.delete(task)
        db.session.commit()

        return {"message": "Task deleted successfully"}, 200
    
class CaretakerProfileAPI(Resource):
    @caretaker_required
    def get(self):
        current_user_id = get_jwt_identity()
        caretaker = Caretaker.query.filter_by(userId=current_user_id).first()
        caretaker_user = User.query.get(current_user_id)

        print(caretaker)
        if not caretaker:
            return {"error": "Caretaker not found"}, 404

        return {
            "id": caretaker.userId,
            "name": caretaker.fullName,
            "age": caretaker.age,
            "contact": caretaker_user.contact,
            "email": caretaker.email,
            "languages": caretaker.languages.split(',') if caretaker.languages else [],
            "qualifications": caretaker.qualification.split(',') if caretaker.qualification else [],
            "about": caretaker.about,
            'resume': caretaker.resumePath,
        }

class CaretakerUpdateProfileAPI(Resource):
    @caretaker_required
    def put(self):
        current_user_id = get_jwt_identity()
        caretaker = Caretaker.query.filter_by(userId=current_user_id).first()
        
        caretaker_user = User.query.get(current_user_id)

        if not caretaker:
            return {"error": "Caretaker not found"}, 404

        data = request.get_json()
        caretaker_user.contact = data.get('phone', caretaker.user.contact)
        caretaker.languages = ','.join(data.get('languages', caretaker.languages.split(',')))
        caretaker.qualification = ','.join(data.get('qualifications', caretaker.qualification.split(',')))
        caretaker.about = data.get('about', caretaker.about)

        db.session.commit()
        return {"message": "Caretaker details updated successfully"}

class SeniorUpdateMedicalConditionAPI(Resource):
    @caretaker_required
    def put(self, senior_id):
        current_user_id = get_jwt_identity()
        senior = SeniorCitizen.query.filter_by(userId=senior_id, assignedCare=current_user_id).first()

        if not senior:
            return {"error": "Senior not found or not assigned to this caretaker"}, 404

        data = request.get_json()
        senior.medCon = data.get('condition', senior.medCon)

        db.session.commit()
        return {"message": "Medical condition updated successfully"}
    
class CaretakerStatsAPI(Resource):
    @caretaker_required
    def get(self):
        current_user_id = get_jwt_identity()

        # Get the caretaker
        caretaker = Caretaker.query.filter_by(userId=current_user_id).first()
        if not caretaker:
            return {"error": "Caretaker not found"}, 404

        # Get assigned senior citizens
        assigned_seniors = SeniorCitizen.query.filter_by(assignedCare=current_user_id).count()

        # Get SOS alerts
        sos_alerts = SOSAlert.query.filter(SOSAlert.sender_id.in_(
            [senior.userId for senior in SeniorCitizen.query.filter_by(assignedCare=current_user_id).all()]
        )).count()

        # Get emergency alerts
        emergency_alerts = SOSAlert.query.filter(
            SOSAlert.sender_id.in_(
                [senior.userId for senior in SeniorCitizen.query.filter_by(assignedCare=current_user_id).all()]
            ),
            SOSAlert.isResolved == False
        ).count()

        # Get tasks created by the caretaker
        tasks_created = Tasks.query.filter_by(assignedBy=current_user_id).count()

        return {
            "assigned_seniors": assigned_seniors,
            "sos_alerts": sos_alerts,
            "emergency_alerts": emergency_alerts,
            "tasks_created": tasks_created
        }