import os
from celery import shared_task
from application.config import Config
from application.utils import format_report  # Uses Jinja2 Template
from .mail import send_email
from sqlalchemy.orm import joinedload


@shared_task(ignore_result=False, name="monthly_report")
def monthly_report():
    from application.schema import SeniorCitizen, Caretaker, Tasks, Query, User

    export_folder = Config.EXPORT_FOLDER
    if not os.path.exists(export_folder):
        os.makedirs(export_folder)

    # seniors = SeniorCitizen.query.all()
    seniors = SeniorCitizen.query.options(joinedload(SeniorCitizen.assignedCare)).all()

    print(f"Found {len(seniors)} seniors for monthly report generation.")
    generated_reports = []
    template_path = os.path.join(os.path.dirname(__file__), 'templates', 'monthly_report_senior_template.html')

    for senior in seniors:
        print(f"Generating report for senior: {senior.fullName} (ID: {senior.userId})")
        user_id = senior.userId
        # Get all tasks for this senior
        tasks = Tasks.query.filter_by(assignedTo=user_id).all()
        print(f"Found {len(tasks)} tasks for senior: {senior.fullName}")
        # Get all queries raised by this senior
        queries = Query.query.filter_by(sender_id=senior.userId).all()
        print(f"Found {len(tasks)} tasks and {len(queries)} queries for senior: {senior.fullName}")
        # Get assigned caretaker info
        caretaker = None
        caretaker_contact = None
        user= None
        if senior.assignedCare:
            print(f"In IF Senior {senior.fullName} is assigned to caretaker ID: {senior.assignedCare}")
            assigned_caretaker_id = senior.assignedCare
            print(f"Assigned caretaker ID: {assigned_caretaker_id}")
            caretaker = Caretaker.query.filter_by(userId=assigned_caretaker_id).first()
            user = User.query.filter_by(userId=assigned_caretaker_id).first()
            print(f"Found caretaker: {caretaker.fullName} (ID: {caretaker.userId})")
            caretaker_contact = user.contact if caretaker else None

        report_data = {
            'senior': senior,
            'tasks': tasks,
            'queries': queries,
            'caretaker': caretaker,
            'caretaker_contact': caretaker_contact
        }

        # Render the HTML report using the template
        report_html = format_report(template_path, report_data)
        # Save the HTML file for this senior
        report_file = os.path.join(export_folder, f"monthly_report_{senior.userId}.html")
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report_html)
        generated_reports.append(report_file)

        # Send email to the family member (emergencyEmail)
        subject = f"Monthly Report for {senior.fullName}"
        message = report_html
        to_address = senior.emergencyEmail
        if to_address:
            try:
                send_email(
                    to_address=to_address,
                    subject=subject,
                    message=message,
                    content="html",
                    attachment_file=report_file
                )
            except Exception as e:
                print(f"Failed to send email to {to_address}: {e}")

    return {"generated_reports": generated_reports}


@shared_task(ignore_result=False, name="daily_reminder")
def daily_reminder():
    return "Daily reminder sent successfully."