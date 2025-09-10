from functools import wraps
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from flask import jsonify, request
from application.schema import db
from application.schema import User, RoleEnum,Caretaker
from application.extensions import limiter


def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user or user.roleId != RoleEnum.ADMIN:
            return jsonify({"error": "Admin privileges required"}), 403
        return fn(*args, **kwargs)
    return wrapper



class AdminDashboardAPI(Resource):
    @admin_required

    @limiter.limit("10 per minute")  # Limit to 10 requests per minute
    def get(self):
        user_count = User.query.filter_by(roleId=RoleEnum.SENIOR_CITIZEN).count()
        caretaker_count = User.query.filter_by(roleId=RoleEnum.CARETAKER).count()
        return jsonify({
            "user_count": user_count,
            "caretaker_count": caretaker_count
        })


class AdminViewUsersAPI(Resource):
    @admin_required

    @limiter.limit("5 per minute")  # Limit to 5 requests per minute
    def get(self):
        users = User.query.all()
        user_data = []

        for user in users:
            if user.roleId == RoleEnum.SENIOR_CITIZEN:
                senior = user.senior_citizen
                user_data.append({
                    "id": user.userId,
                    "name": senior.fullName,
                    "role": "Senior Citizen",
                    "age": senior.age,
                    "contact": senior.contact,
                    "languages": senior.languages,
                    "city": senior.city,
                    "state": senior.state,
                    "emergencyContact": senior.emergencyContact,
                    "emergencyContactName": senior.emergencyContactName,
                    "emergencyEmail": senior.emergencyEmail,
                    "assignedCaretaker": senior.assignedCare
                })
            elif user.roleId == RoleEnum.CARETAKER:
                caretaker = user.caretaker
                user_data.append({
                    "id": user.userId,
                    "name": caretaker.fullName,
                    "role": "Caretaker",
                    "age": caretaker.age,
                    "email": caretaker.email,
                    "qualification": caretaker.qualification,
                    "languages": caretaker.languages,
                    "about": caretaker.about,
                    "resumePath": caretaker.resumePath
                })
            elif user.roleId == RoleEnum.ADMIN:
                user_data.append({
                    "id": user.userId,
                    "name": "Admin",
                    "role": "Admin",
                    "contact": user.contact,
                    "memberSince": user.memberSince.strftime("%Y-%m-%d %H:%M:%S"),
                    "lastLogin": user.lastLogin.strftime("%Y-%m-%d %H:%M:%S") if user.lastLogin else None
                })
        print("User data fetched for admin dashboard:", user_data)
        return jsonify(user_data)

class AdminBlockCaretakerAPI(Resource):
    @admin_required
    def post(self):
        data = request.get_json()
        caretaker_id = data.get('caretaker_id')
        action = data.get('action')  # "block" or "unblock"

        if not caretaker_id or action not in ["block", "unblock"]:
            return {"error": "caretaker_id and valid action (block/unblock) are required"}, 400

        caretaker = User.query.get(caretaker_id)
        if not caretaker or caretaker.roleId != RoleEnum.CARETAKER:
            return {"error": "Caretaker not found"}, 404

        if action == "block":
            caretaker.isBlocked = True
            message = "Caretaker blocked successfully"
        elif action == "unblock":
            caretaker.isBlocked = False
            message = "Caretaker unblocked successfully"

        db.session.commit()
        return {"message": message}, 200
    
class AdminAssignCaretakerAPI(Resource):
    @admin_required
    @limiter.limit("10 per minute")  # Limit to 10 assignments per minute
    def post(self):
        data = request.get_json()
        senior_id = data.get('senior_id')
        caretaker_id = data.get('caretaker_id')  # Can be null for unassigning

        if not senior_id:
            return {"error": "senior_id is required"}, 400

        senior = User.query.get(senior_id)

        if not senior or senior.roleId != RoleEnum.SENIOR_CITIZEN:
            return {"error": "Senior Citizen not found"}, 404

        if caretaker_id:
            caretaker = User.query.get(caretaker_id)
            if not caretaker or caretaker.roleId != RoleEnum.CARETAKER:
                return {"error": "Caretaker not found"}, 404

            # Assign the caretaker to the senior citizen
            senior.senior_citizen.assignedCare = caretaker.userId
            message = f"Caretaker {caretaker.caretaker.fullName} assigned to Senior Citizen {senior.senior_citizen.fullName}"
        else:
            # Unassign the caretaker
            senior.senior_citizen.assignedCare = None
            message = f"Caretaker unassigned from Senior Citizen {senior.senior_citizen.fullName}"

        db.session.commit()


        return {"message": message}, 200
    
class AdminViewCaretakerRequestsAPI(Resource):
    @admin_required

    @limiter.limit("5 per minute")  # Limit to 5 requests per minute
    def get(self):
        # Fetch caretakers who are not verified yet
        print("Fetching pending caretakers")
        pending_caretakers = Caretaker.query.join(User).filter(User.isVerified == False).all()
        print(pending_caretakers)
        return jsonify([
            {
                "id": caretaker.userId,
                "name": caretaker.fullName,
                "email": caretaker.email,
                "qualification": caretaker.qualification,
                "languages": caretaker.languages,
                "about": caretaker.about,
                "resumePath": caretaker.resumePath
            } for caretaker in pending_caretakers
        ])

class AdminApproveCaretakerAPI(Resource):
    @admin_required
    @limiter.limit("10 per minute")  # Limit to 10 approvals per minute
    def post(self):
        data = request.get_json()
        caretaker_id = data.get('caretaker_id')
        action = data.get('action')  # "approve" or "reject"
        print(f"Admin action: {action} on caretaker_id: {caretaker_id}")
        if not caretaker_id or action not in ["approve", "reject"]:
            return {"error": "caretaker_id and valid action (approve/reject) are required"}, 400

        caretaker = User.query.get(caretaker_id)
        if not caretaker or caretaker.roleId != RoleEnum.CARETAKER:
            return {"error": "Caretaker not found"}, 404

        if action == "approve":
            caretaker.isVerified = 1
            db.session.commit()

            return {"message": "Caretaker approved successfully"}, 200
        elif action == "reject":
            caretaker.isVerified = 2
            db.session.commit()

            return {"message": "Caretaker rejected successfully"}, 200