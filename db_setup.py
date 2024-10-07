import os
import logging
from pymongo import MongoClient, ASCENDING
from pymongo.errors import CollectionInvalid, ConnectionFailure

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load environment variables (if using a .env file, use python-dotenv)
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
DB_NAME = 'job_recommendation_db'

# Connect to MongoDB with error handling
try:
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    logging.info("Connected to MongoDB successfully.")
except ConnectionFailure as e:
    logging.error(f"Could not connect to MongoDB: {e}")
    raise

# Function to create a collection with error handling
def create_collection(collection_name):
    try:
        db.create_collection(collection_name)
        logging.info(f"Collection '{collection_name}' created successfully!")
    except CollectionInvalid:
        logging.warning(f"Collection '{collection_name}' already exists.")

# Create necessary collections
create_collection('job_postings')
create_collection('users')
create_collection('companies')

# Function to create indexes for better performance
def create_indexes():
    try:
        # Index for job_postings collection
        db.job_postings.create_index([('job_title', ASCENDING)])
        db.job_postings.create_index([('location', ASCENDING)])
        db.job_postings.create_index([('experience_level', ASCENDING)])
        
        # Index for users collection
        db.users.create_index([('email', ASCENDING)], unique=True)
        
        # Index for companies collection
        db.companies.create_index([('name', ASCENDING)], unique=True)

        logging.info("Indexes created successfully.")
    except Exception as e:
        logging.error(f"Error creating indexes: {e}")

create_indexes()

# Function to insert sample data if collections are empty
def insert_sample_data():
    job_postings = [
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
        {
            "job_id": 2,
            "job_title": "Data Scientist",
            "company": "Data Analytics Corp.",
            "required_skills": ["Python", "Data Analysis", "Machine Learning"],
            "location": "Remote",
            "job_type": "Full-Time",
            "experience_level": "Intermediate",
            "description": "Analyze data and build predictive models."
        },
        # Add more sample jobs as needed
    ]

    if db.job_postings.count_documents({}) == 0:  # Check if collection is empty
        db.job_postings.insert_many(job_postings)
        logging.info("Sample job postings inserted successfully!")

    users = [
        {
            "user_id": 1,
            "name": "Alice Smith",
            "email": "alice@example.com",
            "skills": ["JavaScript", "React"],
            "experience_level": "Intermediate",
            "preferences": {
                "desired_roles": ["Software Engineer", "Frontend Developer"],
                "locations": ["San Francisco", "Remote"],
                "job_type": "Full-Time"
            }
        },
        {
            "user_id": 2,
            "name": "Bob Johnson",
            "email": "bob@example.com",
            "skills": ["Python", "Machine Learning"],
            "experience_level": "Intermediate",
            "preferences": {
                "desired_roles": ["Data Scientist", "Machine Learning Engineer"],
                "locations": ["Remote", "New York"],
                "job_type": "Full-Time"
            }
        },
        # Add more sample users as needed
    ]

    if db.users.count_documents({}) == 0:  # Check if collection is empty
        db.users.insert_many(users)
        logging.info("Sample users inserted successfully!")

    companies = [
        {
            "company_id": 1,
            "name": "Tech Solutions Inc.",
            "location": "San Francisco",
            "industry": "Technology",
            "description": "A leading tech company focused on web development."
        },
        {
            "company_id": 2,
            "name": "Data Analytics Corp.",
            "location": "Remote",
            "industry": "Analytics",
            "description": "A company specialized in data analytics solutions."
        },
        # Add more sample companies as needed
    ]

    if db.companies.count_documents({}) == 0:  # Check if collection is empty
        db.companies.insert_many(companies)
        logging.info("Sample companies inserted successfully!")

# Insert sample data
insert_sample_data()

logging.info("Database setup complete!")
