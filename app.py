from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['job_recommendation_db']

# Sample weights for matching criteria
WEIGHTS = {
    'skills': 0.5,
    'experience': 0.2,
    'roles': 0.2,
    'locations': 0.05,
    'job_type': 0.05
}

@app.route('/recommendations', methods=['POST'])
def recommend_jobs():
    user_profile = request.json
    recommendations = []

    try:
        job_postings = list(db.job_postings.find())

        for job in job_postings:
            if is_job_active(job) and is_match(user_profile, job):
                recommendations.append(job)

        # Sort recommendations based on matching score
        recommendations = sorted(recommendations, key=lambda x: x['match_score'], reverse=True)

        return jsonify(recommendations), 200
    
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

def is_job_active(job):
    """Check if the job posting is still active based on its expiry date."""
    if 'expiry_date' in job:
        return datetime.strptime(job['expiry_date'], "%Y-%m-%d") >= datetime.now()
    return True

def is_match(user_profile, job):
    """Calculate match score based on user profile and job posting."""
    score = 0
    total_weight = sum(WEIGHTS.values())

    # Check skill matches
    skills_match = any(skill in job['required_skills'] for skill in user_profile['skills'])
    if skills_match:
        score += WEIGHTS['skills']

    # Check experience level match
    experience_match = user_profile['experience_level'] == job['experience_level']
    if experience_match:
        score += WEIGHTS['experience']

    # Check role match
    role_match = any(role in job['job_title'] for role in user_profile['preferences']['desired_roles'])
    if role_match:
        score += WEIGHTS['roles']

    # Check location match
    location_match = job['location'] in user_profile['preferences']['locations']
    if location_match:
        score += WEIGHTS['locations']

    # Check job type match
    job_type_match = job['job_type'] == user_profile['preferences']['job_type']
    if job_type_match:
        score += WEIGHTS['job_type']

    # Store the match score in the job for sorting later
    job['match_score'] = score
    return score > 0  # Only consider jobs with a score greater than 0

if __name__ == '__main__':
    app.run(debug=True)
