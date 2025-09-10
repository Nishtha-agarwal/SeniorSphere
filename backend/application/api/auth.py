from flask import request, current_app
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from application.schema import db, User, RoleEnum, Caretaker, SeniorCitizen
from application.extensions import limiter
import os
import re

class CaretakerRegisterAPI(Resource):
    def post(self):
        # Use form-data for file upload
        email = request.form.get('email')
        password = request.form.get('password')
        fullName = request.form.get('fullName')
        age = request.form.get('age')
        contact = request.form.get('contact')
        qualifications = request.form.get('qualifications')
        languages = request.form.get('languages')
        resume_file = request.files.get('resume')
        about = request.form.get('about')

        print(email, password, fullName, age, contact, qualifications, languages, resume_file, about)

        # Check required fields
        if not all([email, password, fullName, age, contact, resume_file]):
            return {"error": "Missing required fields"}, 400
        if not resume_file.filename.lower().endswith('.pdf'):
            return {"error": "Resume must be a PDF file"}, 400

        if User.query.filter_by(contact=contact).first():
            return {"error": "Number already registered"}, 400

        try:
            user = User(contact=contact, roleId=RoleEnum.CARETAKER)
            user.set_password(password)
            db.session.add(user)
            db.session.flush()  # To get userId

            # Save resume file
            resume_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../resume')
            os.makedirs(resume_dir, exist_ok=True)
            resume_filename = f"{user.userId}.pdf"
            resume_path = os.path.join(resume_dir, resume_filename)
            resume_file.save(resume_path)
            db_resume_path = f"{resume_filename}"

            caretaker = Caretaker(
                userId=user.userId,
                fullName=fullName,
                age=age,
                email=email,
                qualification=qualifications,
                about=about,
                languages=languages,
                resumePath=db_resume_path
            )
            db.session.add(caretaker)

            db.session.commit()
            return {"message": "Caretaker registered successfully"}, 201
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500
        

class SeniorCitizenRegisterAPI(Resource):
    def post(self):
        data = request.get_json()

        # Extract fields    
        fullName = data.get('fullName')
        age = data.get('age')
        password = data.get('password')
        contact = data.get('contact')
        languages = data.get('languages')
        pinCode = data.get('pinCode')
        city = data.get('city')
        state = data.get('state')
        emergencyContact = data.get('emergencyContact')
        emergencyContactName = data.get('emergencyContactName')
        emergencyEmail = data.get('emergencyEmail')

        print(fullName, age, password, contact, languages, pinCode, city, state, emergencyContact, emergencyContactName, emergencyEmail)

        # Validation
        errors = []
        if not fullName: errors.append("Full name is required.")
        if not age or int(age) < 0: errors.append("Valid age is required.")
        if not password or not (4 <= len(password) <= 10): errors.append("Password must be 4-10 characters.")
        if not contact or len(contact) < 8: errors.append("Valid mobile number is required.")
        if not languages: errors.append("Languages are required.")
        if not pinCode: errors.append("PIN code is required.")
        if not city: errors.append("City is required.")
        if not state: errors.append("State is required.")
        if not emergencyContact or not emergencyContact.isdigit() or len(emergencyContact) < 8:
            errors.append("Valid emergency contact number is required.")
        if not emergencyContactName: errors.append("Emergency contact name is required.")

        # Optional: Validate email format if emergencyEmail is provided
        if emergencyEmail:
            email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
            if not re.match(email_regex, emergencyEmail):
                errors.append("Invalid emergency email format.")

        # Check for duplicate contact
        if User.query.filter_by(contact=contact).first():
            errors.append("Mobile number already registered.")

        if errors:
            return {"errors": errors}, 400

        try:
            # Create User
            user = User(contact=contact, roleId=RoleEnum.SENIOR_CITIZEN, isVerified=True)
            user.set_password(password)
            db.session.add(user)
            db.session.flush()  # To get userId

            # Create SeniorCitizen
            senior = SeniorCitizen(
                userId=user.userId,
                fullName=fullName,
                age=int(age),
                contact=int(contact),
                # languages=",".join(languages) if isinstance(languages, list) else languages,
                languages=languages,
                pinCode=pinCode,
                city=city,
                state=state,
                emergencyContact=int(emergencyContact),
                emergencyContactName=emergencyContactName,
                emergencyEmail=emergencyEmail
            )
            db.session.add(senior)
            db.session.commit()
            return {"message": "Senior Citizen registered successfully"}, 201
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500
        

class LoginAPI(Resource):
    @limiter.limit("5 per minute")
    def post(self):
        data = request.get_json()
        contact = data.get('contact')
        password = data.get('password')

        if not contact or not password:
            return {"error": "Contact and password are required."}, 400

        user = User.query.filter_by(contact=contact).first()
        if not user or not user.check_password(password):
            return {"error": "Invalid contact or password."}, 401

        seniors = SeniorCitizen.query.all()
        print(seniors)
        # Create JWT token
        access_token = create_access_token(identity=str(user.userId))
        return {
            "message": "Login successful",
            "access_token": access_token,
            "role": user.roleId.name,
            "userId": user.userId,
            "isBlocked": user.isBlocked,
            "isVerified": user.isVerified
        }, 200