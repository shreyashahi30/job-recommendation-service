from pymongo import MongoClient
from random import choice, randint
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['job_recommendation_db']

# Predefined job attributes
job_titles = [
    "Software Engineer", "Data Scientist", "Frontend Developer", 
    "Backend Developer", "Machine Learning Engineer", "DevOps Engineer", 
    "Full Stack Developer", "Data Analyst", "Quality Assurance Engineer", 
    "Systems Administrator"
]

skills = [
    ["JavaScript", "React", "Node.js"],
    ["Python", "Data Analysis", "Machine Learning"],
    ["HTML", "CSS", "JavaScript", "Vue.js"],
    ["Python", "Django", "REST APIs"],
    ["Python", "Machine Learning", "TensorFlow"],
    ["AWS", "Docker", "Kubernetes"],
    ["JavaScript", "Node.js", "Angular", "MongoDB"],
    ["SQL", "Python", "Tableau"],
    ["Selenium", "Java", "Testing"],
    ["Linux", "Networking", "Shell Scripting"]
]

locations = [
    "San Francisco", "Remote", "New York", 
    "Chicago", "Boston", "Seattle", 
    "Austin", "Los Angeles", "Miami", 
    "Washington DC"
]

job_types = ["Full-Time", "Part-Time", "Contract"]

experience_levels = ["Junior", "Intermediate", "Senior"]

def generate_random_job_posting(job_id):
    return {
        "job_id": job_id,
        "job_title": choice(job_titles),
        "company": f"{choice(['Tech', 'Data', 'Web', 'AI', 'Cloud'])} Solutions {choice(['Inc.', 'Corp.', 'LLC', 'Co.'])}",
        "required_skills": choice(skills),
        "location": choice(locations),
        "job_type": choice(job_types),
        "experience_level": choice(experience_levels),
        "expiry_date": (datetime.now() + timedelta(days=randint(30, 90))).strftime("%Y-%m-%d")  # Expiry in 1 to 3 months
    }

def validate_job_posting(job):
    required_keys = ["job_id", "job_title", "company", "required_skills", "location", "job_type", "experience_level", "expiry_date"]
    for key in required_keys:
        if key not in job:
            logger.error(f"Missing key: {key} in job posting: {job}")
            return False
    return True

# Generate and insert mock job postings
job_postings = []
for i in range(1, 11):  # Generate 10 job postings
    job = generate_random_job_posting(i)
    if validate_job_posting(job):
        job_postings.append(job)

# Insert mock job postings into the database
try:
    result = db.job_postings.insert_many(job_postings)
    logger.info(f"Mock data inserted successfully: {result.inserted_ids}")
except Exception as e:
    logger.error(f"Error inserting data: {str(e)}")
