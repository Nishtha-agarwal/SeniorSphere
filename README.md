# SeniorSphere

This project is a user-centered web app tailored to address key challenges faced by senior citizens — such as managing medications, staying socially connected, and accessing help during emergencies. Developed with empathy and real-world user input, the app aims to provide a seamless and supportive digital experience for the elderly community.

## Key Features

### Daily Routine Management
- **Caretaker Functionality**: Create, update, and assign personalized daily routines for seniors (task type, details, and duration).  
- **Senior Citizen Access**: Seniors view their routines in the **Daily Routine Dashboard**, receive reminders for medications, exercises, and activities, and access health resources/articles curated by caretakers.

### Emergency SOS Support
- **SOS Integration**: A prominently placed SOS button on the senior dashboard instantly alerts assigned caretakers.  
- **Follow-up Actions**: Caretakers can respond to SOS alerts by arranging timely medical interventions or appointments.

### Authentication & User Access
- **Secure Login & Registration**: Supports role-based access for caretakers and seniors, ensuring privacy and data protection.

### Query & Support System
- **Raise Query**: Seniors can raise support tickets for assistance with daily tasks, technical support, or other non-medical needs.  
- **Caretaker Resolution**: Caretakers view and resolve these queries directly from their dashboard.

### User Experience Highlights
- **Sidebar Navigation**: Context-aware menus tailored to roles (Admin, Caretaker, Senior).  
- **Dashboard Widgets**: Charts, emergency alerts, and task lists for quick decision-making.  
- **Real-time Updates**: SPA architecture ensures instant reflection of changes in routines, alerts, and queries.

## Tools & Technologies

- **Frontend**: Vue.js, Bootstrap, HTML/CSS
- **Backend**: Flask-RESTful API, SQLite, JWT
- **Task Management**: Celery, Redis
- **Natural Language Processing**: Sentiment analysis for scoring system
- **Package Management**: Vue CLI, npm

## How to Run the Project

### Prerequisites

Ensure you have the following installed on your system:

- **Python** (>=3.8)
- **Node.js** (>=14.x) and **npm**
- **Redis**

### Steps to Run

#### 1. Clone the Repository

Backend Setup
- cd backend
- python -m venv venv
- source venv/bin/activate  # On Windows: venv\Scripts\activate
- pip install -r req.txt

Start Redis server
- redis-server   (in Windows Subsystem linux (WSL) )
- cd backend
- celery -A app.celery worker --loglevel=info
- celery -A app.celery beat --loglevel=info

Running the app
- python app.py


Frontend Setup
- cd ../frontend
- npm install
- npm run serve

``'


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
