 Job Recommendation System

 Project Overview

The Job Recommendation System is a web application designed to help users find suitable job postings based on their skills, experience, and preferences. The system utilizes a MongoDB database to store job postings, user profiles, and company information. It features a RESTful API built with Flask, allowing users to submit their profiles and receive personalized job recommendations.

 Key Features

- Job recommendations based on user profiles
- Support for multiple user preferences (location, job type, desired roles)
- MongoDB for data storage and management
- CORS support for cross-origin requests
- Sample data for job postings, users, and companies

 Technologies Used

- Python
- Flask
- Flask-CORS
- PyMongo
- MongoDB

 Project Structure

```plaintext
job_recommendation_system/
│
├── app.py                    # Main Flask application
├── db_setup.py               # MongoDB setup and sample data insertion
├── requirements.txt          # Python package dependencies
└── README.md                 # Project documentation

Setup Instructions
Prerequisites
1) Python 3.x
2) MongoDB installed and running
3) pip (Python package installer)

Installation
Clone the repository: git clone https://github.com/yourusername/job_recommendation_system.git
cd job_recommendation_system

Create a virtual environment (optional but recommended):
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

Install the required packages:
Create a requirements.txt file and add the following dependencies:
1) Flask
2) Flask-CORS
3) pymongo
4) python-dotenv

Then run:
pip install -r requirements.txt

Set up the MongoDB database: Make sure MongoDB is running locally on the default port. You can use db_setup.py to create the necessary collections and insert sample data.

Run the following command:
python db_setup.py
Run the Flask application:

Start the Flask server by running:
python app.py
The application will be accessible at http://127.0.0.1:5000.

Usage
API Endpoints
1. Get Job Recommendations
Endpoint: /recommendations

Method: POST

Request Body:
{
    "name": "Alice Smith",
    "email": "alice@example.com",
    "skills": ["JavaScript", "React"],
    "experience_level": "Intermediate",
    "preferences": {
        "desired_roles": ["Software Engineer", "Frontend Developer"],
        "locations": ["San Francisco", "Remote"],
        "job_type": "Full-Time"
    }
}
Response:
Returns a JSON array of recommended job postings based on the user's profile.
[
    {
        "job_id": 1,
        "job_title": "Software Engineer",
        "company": "Tech Solutions Inc.",
        "required_skills": ["JavaScript", "React", "Node.js"],
        "location": "San Francisco",
        "job_type": "Full-Time",
        "experience_level": "Intermediate",
        "description": "Develop and maintain web applications."
    },
    ...
]
Additional Notes
You may use tools like Postman or curl to test the API endpoints.
Ensure MongoDB is running before starting the Flask application.
Modify app.py and db_setup.py as needed to add more features or change the data schema.
