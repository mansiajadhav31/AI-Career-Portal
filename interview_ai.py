import random
import json

# Question templates by job role and difficulty
INTERVIEW_QUESTIONS = {
    'Software Developer': {
        'Beginner': [
            "What is the difference between let, const, and var in JavaScript?",
            "Explain what REST API is and how it works.",
            "What is version control and why is it important?",
            "Explain the difference between SQL and NoSQL databases.",
            "What are the basic principles of Object-Oriented Programming?",
            "What is the difference between Git merge and rebase?",
            "Explain what a closure is in JavaScript.",
            "What is responsive web design?"
        ],
        'Mid': [
            "Explain the concept of hoisting in JavaScript.",
            "How would you optimize a slow-loading web page?",
            "What is the difference between authentication and authorization?",
            "Explain how you would design a URL shortening service.",
            "What are microservices and their advantages?",
            "Explain the event loop in JavaScript.",
            "How do you handle memory leaks in your application?",
            "What is the difference between SQL injection and XSS attacks?"
        ],
        'Senior': [
            "Describe a complex system you designed. What challenges did you face?",
            "How do you ensure code quality in a large team?",
            "Explain the CAP theorem and its implications.",
            "How would you migrate a monolithic app to microservices?",
            "Describe your experience with system architecture and scalability.",
            "How do you handle technical debt in a project?",
            "Explain how you would implement a real-time notification system.",
            "What strategies do you use for disaster recovery?"
        ]
    },
    'Data Scientist': {
        'Beginner': [
            "What is the difference between supervised and unsupervised learning?",
            "Explain what p-value means in statistics.",
            "What is the purpose of train-test split?",
            "Explain bias-variance tradeoff.",
            "What is the difference between correlation and causation?",
            "What are the common data cleaning techniques?",
            "Explain what a confusion matrix is."
        ],
        'Mid': [
            "How do you handle imbalanced datasets?",
            "Explain how gradient descent works.",
            "What is the difference between bagging and boosting?",
            "How do you detect overfitting?",
            "Explain feature engineering and its importance.",
            "What metrics would you use for a classification problem?",
            "How do you handle missing data?"
        ],
        'Senior': [
            "Describe an end-to-end ML project you led.",
            "How do you deploy ML models in production?",
            "Explain how to handle concept drift in ML models.",
            "What is your approach to model interpretability?",
            "How do you ensure reproducibility in ML experiments?",
            "Explain A/B testing methodology for ML models."
        ]
    },
    'DevOps Engineer': {
        'Beginner': [
            "What is CI/CD and why is it important?",
            "Explain the difference between containers and virtual machines.",
            "What is infrastructure as code?",
            "Explain the basic concepts of Kubernetes.",
            "What is the difference between Git and Jenkins?"
        ],
        'Mid': [
            "How do you set up a complete CI/CD pipeline?",
            "Explain blue-green deployment strategy.",
            "How do you monitor system health in production?",
            "What tools do you use for logging and monitoring?",
            "Explain how to handle secrets management."
        ],
        'Senior': [
            "Design a high-availability architecture on AWS.",
            "How do you implement zero-downtime deployments?",
            "Explain disaster recovery strategies for cloud infrastructure.",
            "How do you optimize cloud costs while maintaining performance?",
            "Describe a challenging production issue you resolved."
        ]
    }
}

DEFAULT_QUESTIONS = {
    'Beginner': [
        "Tell me about yourself.",
        "What are your strengths and weaknesses?",
        "Why do you want to work here?",
        "Where do you see yourself in 5 years?",
        "Describe a challenge you overcame."
    ],
    'Mid': [
        "Describe a time you led a team project.",
        "How do you handle conflicts with coworkers?",
        "Tell me about a difficult technical problem you solved.",
        "How do you stay updated with new technologies?",
        "Describe your most successful project."
    ],
    'Senior': [
        "Tell me about a time you failed and what you learned.",
        "How do you mentor junior developers?",
        "Describe your leadership style.",
        "How do you handle pressure and deadlines?",
        "What would you change about our current tech stack?"
    ]
}

def generate_interview_questions(job_role, experience_level):
    """Generate interview questions based on role and level"""
    
    # Get role-specific questions
    role_questions = INTERVIEW_QUESTIONS.get(job_role, {})
    level_questions = role_questions.get(experience_level, [])
    
    # Add default behavioral questions
    behavioral = DEFAULT_QUESTIONS.get(experience_level, DEFAULT_QUESTIONS['Mid'])
    
    # Combine and select random questions
    all_questions = level_questions + behavioral
    
    # If not enough questions, add more behavioral
    while len(all_questions) < 5:
        all_questions.extend(DEFAULT_QUESTIONS['Mid'])
    
    # Select 5-7 random questions
    num_questions = min(7, max(5, len(all_questions)))
    selected = random.sample(all_questions, num_questions)
    
    return selected

def evaluate_answers(questions, answers):
    """Evaluate answers and provide feedback"""
    
    feedback = []
    total_score = 0
    
    for i, (question, answer) in enumerate(zip(questions, answers)):
        if not answer or len(answer.strip()) < 10:
            score = 20
            comment = "Your answer was too brief. Please elaborate more with specific examples."
        elif len(answer) < 50:
            score = 40
            comment = "Good start, but add more detail and specific examples to strengthen your answer."
        elif len(answer) < 150:
            score = 70
            comment = "Good answer with solid points. Consider adding more specific metrics or outcomes."
        else:
            score = 90
            comment = "Excellent! Detailed answer with good structure and specific examples."
        
        # Adjust score based on keywords
        keywords = ['example', 'experience', 'project', 'team', 'result', 'learned']
        for kw in keywords:
            if kw.lower() in answer.lower():
                score = min(95, score + 5)
        
        total_score += score
        
        feedback.append({
            'question': question,
            'answer_preview': answer[:200] + '...' if len(answer) > 200 else answer,
            'score': score,
            'comment': comment,
            'suggestion': get_suggestion(score)
        })
    
    return feedback, total_score

def get_suggestion(score):
    """Get improvement suggestion based on score"""
    if score < 40:
        return "Practice structuring answers using the STAR method (Situation, Task, Action, Result)"
    elif score < 70:
        return "Add specific metrics and examples. Quantify your achievements when possible."
    else:
        return "Great job! Keep practicing to maintain this level of excellence."