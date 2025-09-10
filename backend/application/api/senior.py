from flask_restful import Resource
from flask import request
from application.schema import db, User, RoleEnum, SeniorCitizen, Tasks, Query, SOSAlert, Caretaker
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from application.extensions import limiter

from functools import wraps
import uuid

def senior_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user or user.roleId != RoleEnum.SENIOR_CITIZEN:
            return {"error": "Senior citizen privileges required"}, 403
        return fn(*args, **kwargs)
    return wrapper

class SeniorDashboard(Resource):
    @senior_required

    def get(self):
        current_user_id = get_jwt_identity()
        senior = SeniorCitizen.query.filter_by(userId=current_user_id).first()
        
        if not senior:
            return {"error": "Senior citizen not found"}, 404
        
        return {
            "id": senior.userId,
            "name": senior.fullName,
            "age": senior.age,
            "location": senior.city,
            "condition": senior.medCon
        }, 200

class SeniorDashboardAPI(Resource):
    @senior_required
    def get(self):
        user_id = get_jwt_identity()

        senior = SeniorCitizen.query.filter_by(userId=user_id).first()
        if not senior:
            return {"error": "Senior citizen not found"}, 404

        caretaker_name = None
        caretaker_contact = None

        if senior.assignedCare:
            caretaker = Caretaker.query.filter_by(userId=senior.assignedCare).first()
            if caretaker:
                caretaker_name = caretaker.fullName
                caretaker_contact = caretaker.user.contact if caretaker.user else None

        return {
            "fullName": senior.fullName,
            "condition": senior.medCon,
            "caretaker": caretaker_name,
            "caretakerContact": caretaker_contact,
            "age": senior.age,
            "contact": senior.contact
        }, 200

class SeniorRoutineAPI(Resource):
    @senior_required
    def get(self):
        current_user_id = get_jwt_identity()
        today = datetime.now().date()

        tasks = Tasks.query.filter(
            Tasks.assignedTo == current_user_id
        ).all()

        result = []
        for task in tasks:
            try:
                # Try parsing ISO format (e.g. "2025-08-16T23:15")
                task_time = datetime.fromisoformat(task.duration)
                print("Parsed ISO format:", task_time)
            except ValueError:
                try:
                    # If it's only "HH:MM", parse without date
                    task_time = datetime.strptime(task.duration, "%H:%M")
                    # Attach today's date
                    task_time = datetime.combine(today, task_time.time())
                except ValueError:
                    # If invalid, skip
                    continue

            status = "completed" if task.status else (
                "upcoming" if task_time > datetime.now() else "missed"
            )

            result.append({
                "time": task_time.strftime("%I:%M %p"),
                "task": task.taskDetails,
                "caretaker": task.caretaker.fullName,
                "status": status,
                "taskId": task.taskId
            })

        return result, 200
    
    @senior_required
    def put(self):
        current_user_id = get_jwt_identity()
        data = request.get_json()
        task_id = data.get("taskId")
        print("Received task ID:", task_id)

        task = Tasks.query.filter_by(taskId=task_id, assignedTo=current_user_id).first()
        if not task:
            return {"error": "Task not found"}, 404

        task.status = True  # ✅ Mark completed
        db.session.commit()

        return {"message": "Task marked as completed"}, 200


class SeniorSOSAPI(Resource):
    @senior_required
    @limiter.limit("3 per minute")
    def post(self):
        current_user_id = get_jwt_identity()
        senior = SeniorCitizen.query.filter_by(userId=current_user_id).first()
        
        new_alert = SOSAlert(
            alertId=str(uuid.uuid4()),
            sender_id=current_user_id,
            location=senior.city,
            alertTime=datetime.now(),
            notifiedCaretaker=True,  # Assuming caretaker is notified immediately
        )
        db.session.add(new_alert)
        db.session.commit()
        
        return {"message": "SOS alert sent successfully"}, 201

class SeniorQueryAPI(Resource):
    @senior_required
    def post(self):
        current_user_id = get_jwt_identity()
        data = request.get_json()
        message = data.get('message', '').strip() if data else ''
        if not message:
            return {"error": "Message cannot be blank"}, 400

        # 🔹 Find the caretaker assigned to this senior
        senior = SeniorCitizen.query.filter_by(userId=current_user_id).first()
        if not senior:
            return {"error": "Senior not found"}, 404

        # Assuming SeniorCitizen has a relationship/column storing caretakerId
        caretaker_id = senior.assignedCare
        if not caretaker_id:
            return {"error": "No caretaker assigned to this senior"}, 400

        # 🔹 Create new query with caretaker assigned
        new_query = Query(
            queryId=str(uuid.uuid4()),
            sender_id=current_user_id,
            message=message,
            timeStamp=datetime.now(),
            status='Pending',
            assignedCaretakerId=caretaker_id
        )

        db.session.add(new_query)
        db.session.commit()
        
        return {"message": "Query raised successfully"}, 201

    @senior_required
    def get(self):
        current_user_id = get_jwt_identity()
        queries = Query.query.filter_by(sender_id=current_user_id)\
                           .order_by(Query.timeStamp.desc())\
                           .limit(5)\
                           .all()
        
        return [{
            "id": query.queryId,
            "message": query.message,
            "status": query.status,
            "timestamp": query.timeStamp.strftime("%Y-%m-%d %H:%M:%S")
        } for query in queries], 200
