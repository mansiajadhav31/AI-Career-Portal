import os
from resume_matcher import extract_resume_text, calculate_match_score

# Test with a sample file
test_file = "uploads/test.txt"

# Create a test file
with open(test_file, 'w') as f:
    f.write("""
    Experienced Python Developer with skills in Django, Flask, and SQL.
    Worked on machine learning projects using TensorFlow.
    """)

# Extract text
text = extract_resume_text(test_file)
print(f"Extracted text: {text[:100]}...")

# Calculate match
job_desc = "Looking for Python Developer with Django and ML experience"
score, skills = calculate_match_score(text, job_desc)
print(f"Match Score: {score}%")
print(f"Matched Skills: {skills}")