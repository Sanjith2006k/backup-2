"""
Sample Dataset Generator for ML Matching System

This script generates 50 realistic student-internship pairs with feedback data
to test and validate the ML matching model.

Run this script to populate your database with sample data for testing.
"""

import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()

# ============================================================================
# DOMAIN DEFINITIONS
# ============================================================================

DOMAINS = {
    'Machine Learning': {
        'skills': ['Python', 'TensorFlow', 'PyTorch', 'Scikit-learn', 'Deep Learning',
                   'Neural Networks', 'NLP', 'Computer Vision', 'Pandas', 'NumPy'],
        'roles': ['ML Engineer Intern', 'AI Research Intern', 'Deep Learning Intern',
                  'Data Science Intern', 'Computer Vision Intern'],
        'certificates': [
            'Deep Learning Specialization - Coursera',
            'TensorFlow Developer Certificate - Google',
            'Machine Learning Certificate - Stanford Online',
            'AI Programming with Python - Udacity',
            'Advanced Machine Learning - Coursera'
        ],
        'research_topics': [
            'Novel CNN Architecture for Image Classification',
            'Transformer Models for Natural Language Processing',
            'Reinforcement Learning for Game AI',
            'Generative Adversarial Networks for Image Synthesis',
            'Transfer Learning in Computer Vision'
        ]
    },
    'Web Development': {
        'skills': ['JavaScript', 'React', 'Node.js', 'HTML', 'CSS', 'MongoDB',
                   'Express', 'Vue.js', 'Angular', 'REST API', 'TypeScript'],
        'roles': ['Full Stack Developer Intern', 'Frontend Developer Intern',
                  'Backend Developer Intern', 'Web Developer Intern', 'MERN Stack Intern'],
        'certificates': [
            'Full Stack Web Development - Coursera',
            'React Developer Certification - Meta',
            'Node.js Certification - OpenJS Foundation',
            'JavaScript Algorithms - freeCodeCamp',
            'Web Development Bootcamp - Udemy'
        ],
        'research_topics': [
            'Performance Optimization in Single Page Applications',
            'Server-Side Rendering with React',
            'Microservices Architecture for Web Applications',
            'Progressive Web Apps: A Comprehensive Study',
            'GraphQL vs REST: Performance Analysis'
        ]
    },
    'Data Science': {
        'skills': ['Python', 'R', 'SQL', 'Tableau', 'Power BI', 'Pandas',
                   'Data Visualization', 'Statistics', 'Excel', 'Data Analysis'],
        'roles': ['Data Analyst Intern', 'Business Intelligence Intern',
                  'Data Science Intern', 'Analytics Intern', 'Quantitative Analyst Intern'],
        'certificates': [
            'Data Science Professional Certificate - IBM',
            'Google Data Analytics Certificate',
            'Data Analysis with Python - Coursera',
            'Tableau Desktop Specialist',
            'Microsoft Power BI Data Analyst'
        ],
        'research_topics': [
            'Predictive Analytics for Customer Churn',
            'Time Series Forecasting with ARIMA Models',
            'A/B Testing Methodologies in E-commerce',
            'Statistical Analysis of Social Media Trends',
            'Big Data Analytics with Apache Spark'
        ]
    },
    'Cybersecurity': {
        'skills': ['Network Security', 'Penetration Testing', 'Ethical Hacking',
                   'Cryptography', 'Linux', 'Security Auditing', 'Firewall', 'SIEM'],
        'roles': ['Cybersecurity Intern', 'Security Analyst Intern',
                  'Penetration Testing Intern', 'Network Security Intern', 'SOC Analyst Intern'],
        'certificates': [
            'CompTIA Security+ Certification',
            'Ethical Hacking - EC-Council',
            'Cybersecurity Fundamentals - IBM',
            'Network Security - Cisco',
            'Google Cybersecurity Certificate'
        ],
        'research_topics': [
            'Advanced Persistent Threats Detection',
            'Zero-Day Vulnerability Analysis',
            'Blockchain Security Mechanisms',
            'Machine Learning for Intrusion Detection',
            'Cloud Security Best Practices'
        ]
    },
    'Mobile Development': {
        'skills': ['Android', 'iOS', 'React Native', 'Flutter', 'Swift',
                   'Kotlin', 'Mobile UI/UX', 'Firebase', 'API Integration'],
        'roles': ['Android Developer Intern', 'iOS Developer Intern',
                  'Mobile App Developer Intern', 'React Native Developer Intern', 'Flutter Developer Intern'],
        'certificates': [
            'Android Developer Certification - Google',
            'iOS App Development - Apple',
            'React Native - Meta',
            'Flutter Development - Google',
            'Mobile App Development - Coursera'
        ],
        'research_topics': [
            'Cross-Platform Mobile Development Performance',
            'Mobile App Security Best Practices',
            'Offline-First Mobile Applications',
            'Mobile UI/UX Design Patterns',
            'Push Notification Architecture'
        ]
    },
    'Cloud Computing': {
        'skills': ['AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes',
                   'DevOps', 'Terraform', 'CI/CD', 'Linux', 'Cloud Architecture'],
        'roles': ['Cloud Engineer Intern', 'DevOps Intern',
                  'AWS Intern', 'Cloud Infrastructure Intern', 'Site Reliability Engineer Intern'],
        'certificates': [
            'AWS Certified Cloud Practitioner',
            'Microsoft Azure Fundamentals',
            'Google Cloud Associate Engineer',
            'Docker Certified Associate',
            'Kubernetes Administrator Certification'
        ],
        'research_topics': [
            'Serverless Architecture Patterns',
            'Container Orchestration at Scale',
            'Multi-Cloud Strategy Implementation',
            'Cloud Cost Optimization Techniques',
            'Infrastructure as Code Best Practices'
        ]
    }
}

CITIES = ['Bangalore', 'Mumbai', 'Delhi', 'Hyderabad', 'Pune', 'Chennai',
          'Kolkata', 'Ahmedabad', 'Remote']

COMPANIES = [
    'TechCorp Solutions', 'InnovateLabs', 'DataDrive Inc', 'CloudNine Technologies',
    'SecureNet Systems', 'WebWizards', 'AI Innovations', 'MobileFirst Apps',
    'QuantumLeap Analytics', 'NextGen Software', 'CodeCraft Studios', 'ByteBuilders',
    'AlphaStack', 'BetaWorks', 'GammaCode', 'DeltaDev', 'EpsilonTech'
]

# ============================================================================
# STUDENT PROFILE GENERATOR
# ============================================================================

def generate_student_profile(student_id, domain, expertise_level='medium'):
    """
    Generate a realistic student profile.

    Args:
        student_id: Unique student ID
        domain: Primary domain of expertise
        expertise_level: 'beginner', 'medium', 'expert'

    Returns:
        Dictionary with student data
    """
    domain_data = DOMAINS[domain]

    # Select skills based on expertise level
    if expertise_level == 'beginner':
        num_skills = random.randint(2, 4)
        num_certs = random.randint(0, 1)
        num_experiences = 0
        num_papers = 0
        ai_score = random.randint(200, 400)
    elif expertise_level == 'medium':
        num_skills = random.randint(4, 7)
        num_certs = random.randint(1, 2)
        num_experiences = random.randint(0, 1)
        num_papers = random.randint(0, 1)
        ai_score = random.randint(400, 700)
    else:  # expert
        num_skills = random.randint(7, 10)
        num_certs = random.randint(2, 4)
        num_experiences = random.randint(1, 3)
        num_papers = random.randint(1, 3)
        ai_score = random.randint(700, 1000)

    skills = random.sample(domain_data['skills'], num_skills)

    # Generate certificates
    certificates = []
    for _ in range(num_certs):
        cert_name = random.choice(domain_data['certificates'])
        related_skill = random.choice(skills)
        certificates.append({
            'certificate_name': cert_name,
            'related_skill': related_skill,
            'description': f'Comprehensive course on {related_skill}',
            'issuing_organization': cert_name.split(' - ')[-1]
        })

    # Generate internship experiences
    experiences = []
    for _ in range(num_experiences):
        duration_months = random.randint(2, 6)
        end_date = datetime.now() - timedelta(days=random.randint(30, 365))
        start_date = end_date - timedelta(days=duration_months * 30)

        experiences.append({
            'role': random.choice(domain_data['roles']),
            'company_name': random.choice(COMPANIES),
            'skills_used': ', '.join(random.sample(skills, min(3, len(skills)))),
            'work_description': f'Worked on {domain.lower()} projects involving {random.choice(skills)}',
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d')
        })

    # Generate research papers
    papers = []
    for _ in range(num_papers):
        topic = random.choice(domain_data['research_topics'])
        papers.append({
            'title': topic,
            'abstract': f'This research explores {topic.lower()} with focus on {random.choice(skills)}',
            'keywords': ', '.join(random.sample(skills, min(4, len(skills)))),
            'domain': domain,
            'citation_count': random.randint(0, 50) if expertise_level == 'expert' else random.randint(0, 10)
        })

    return {
        'id': student_id,
        'user_id': 1000 + student_id,
        'name': fake.name(),
        'skills': ', '.join(skills),
        'location': random.choice(CITIES),
        'certificates': certificates,
        'internship_experiences': experiences,
        'research_papers': papers,
        'ai_score': ai_score,
        'avg_feedback_score': 0.5,  # Will be updated based on actual feedback
        'personality_culture_match': random.uniform(0.3, 0.9),
        'expertise_level': expertise_level,
        'primary_domain': domain
    }

# ============================================================================
# INTERNSHIP GENERATOR
# ============================================================================

def generate_internship(internship_id, domain):
    """Generate a realistic internship posting."""
    domain_data = DOMAINS[domain]

    num_required_skills = random.randint(4, 7)
    required_skills = random.sample(domain_data['skills'], num_required_skills)

    stipend_ranges = {
        'Machine Learning': ('₹20,000', '₹35,000'),
        'Web Development': ('₹15,000', '₹25,000'),
        'Data Science': ('₹18,000', '₹30,000'),
        'Cybersecurity': ('₹22,000', '₹35,000'),
        'Mobile Development': ('₹18,000', '₹28,000'),
        'Cloud Computing': ('₹20,000', '₹32,000')
    }

    stipend = random.choice(stipend_ranges[domain])

    return {
        'id': internship_id,
        'title': random.choice(domain_data['roles']),
        'skills_required': ', '.join(required_skills),
        'location': random.choice(CITIES),
        'duration': random.choice(['2 months', '3 months', '6 months']),
        'stipend': stipend,
        'domain': domain,
        'organization_name': random.choice(COMPANIES),
        'organization_id': 2000 + (internship_id % 15)
    }

# ============================================================================
# FEEDBACK GENERATOR
# ============================================================================

def calculate_true_match_quality(student, internship):
    """
    Calculate the true match quality based on student profile and internship.
    This simulates real-world success.
    """
    score = 0.0

    # Skill match (40% weight)
    student_skills = set([s.strip().lower() for s in student['skills'].split(',')])
    required_skills = set([s.strip().lower() for s in internship['skills_required'].split(',')])

    if required_skills:
        skill_overlap = len(student_skills & required_skills) / len(required_skills)
        score += skill_overlap * 40

    # Domain match (20% weight)
    if student['primary_domain'] == internship['domain']:
        score += 20

    # Expertise level (15% weight)
    expertise_scores = {'beginner': 5, 'medium': 10, 'expert': 15}
    score += expertise_scores[student['expertise_level']]

    # Certificates boost (10% weight)
    cert_boost = min(len(student['certificates']) * 3, 10)
    score += cert_boost

    # Experience boost (10% weight)
    exp_boost = min(len(student['internship_experiences']) * 5, 10)
    score += exp_boost

    # Research boost (5% weight)
    research_boost = min(len(student['research_papers']) * 2.5, 5)
    score += research_boost

    # Add some randomness (±10 points)
    score += random.uniform(-10, 10)

    return max(0, min(100, score))

def generate_feedback(student, internship, true_match_quality):
    """
    Generate realistic feedback based on match quality.
    Higher match quality = better feedback from both sides.
    """
    # Base ratings on match quality
    base_rating = true_match_quality / 20  # Convert 0-100 to 0-5 scale

    # Student feedback (they rate the experience)
    student_satisfaction = max(1, min(5, int(base_rating + random.uniform(-0.5, 0.5))))
    student_learning = max(1, min(5, int(base_rating + random.uniform(-0.5, 0.5))))
    student_work_env = max(1, min(5, int(base_rating + random.uniform(-1, 1))))
    student_mentor = max(1, min(5, int(base_rating + random.uniform(-0.5, 0.5))))
    student_skill_match = max(1, min(5, int(base_rating + random.uniform(-0.3, 0.3))))
    student_recommend = true_match_quality > 60

    # Company feedback (they rate the student)
    company_performance = max(1, min(5, int(base_rating + random.uniform(-0.5, 0.5))))
    company_skill_level = max(1, min(5, int(base_rating + random.uniform(-0.3, 0.3))))
    company_professionalism = max(1, min(5, int(base_rating + random.uniform(-0.5, 1))))
    company_learning = max(1, min(5, int(base_rating + random.uniform(-0.5, 0.5))))
    company_hire = true_match_quality > 70
    company_recommend = true_match_quality > 65

    # Calculate actual success score (what the model will learn from)
    student_avg = (student_satisfaction + student_learning + student_work_env + student_skill_match) / 4
    student_score = (student_avg / 5) * 40
    if student_recommend:
        student_score += 10

    company_avg = (company_performance + company_skill_level + company_professionalism + company_learning) / 4
    company_score = (company_avg / 5) * 50
    if company_hire:
        company_score += 10

    actual_success_score = student_score + company_score

    return {
        'student_satisfaction': student_satisfaction,
        'student_learning': student_learning,
        'student_work_environment': student_work_env,
        'student_mentor_quality': student_mentor,
        'student_skill_match': student_skill_match,
        'student_would_recommend': student_recommend,
        'student_comments': generate_comment(true_match_quality, is_student=True),

        'company_performance': company_performance,
        'company_skill_level': company_skill_level,
        'company_professionalism': company_professionalism,
        'company_learning_ability': company_learning,
        'company_would_hire': company_hire,
        'company_would_recommend': company_recommend,
        'company_comments': generate_comment(true_match_quality, is_student=False),

        'actual_success_score': actual_success_score,
        'true_match_quality': true_match_quality
    }

def generate_comment(match_quality, is_student=True):
    """Generate realistic comments based on match quality."""
    if is_student:
        if match_quality > 80:
            comments = [
                "Excellent internship! Learned a lot.",
                "Amazing experience with great mentors.",
                "Perfect match for my skills and interests.",
                "Highly recommend this internship!",
                "Best learning experience of my life."
            ]
        elif match_quality > 60:
            comments = [
                "Good internship, learned new skills.",
                "Decent experience overall.",
                "Met my expectations.",
                "Good team and work culture.",
                "Valuable learning opportunity."
            ]
        else:
            comments = [
                "Skills didn't match the requirements well.",
                "Struggled with some tasks initially.",
                "Would have preferred clearer expectations.",
                "Learned but found it challenging.",
                "Not the best fit for my skill level."
            ]
    else:
        if match_quality > 80:
            comments = [
                "Outstanding intern! Exceeded expectations.",
                "Highly skilled and professional.",
                "Would definitely hire full-time.",
                "Made significant contributions to projects.",
                "One of the best interns we've had."
            ]
        elif match_quality > 60:
            comments = [
                "Good performance overall.",
                "Met project requirements.",
                "Solid contributor to the team.",
                "Good learning attitude.",
                "Performed well with guidance."
            ]
        else:
            comments = [
                "Needed significant training.",
                "Skills were below requirements.",
                "Struggled with project complexity.",
                "Required constant supervision.",
                "Would benefit from more foundational knowledge."
            ]

    return random.choice(comments)

# ============================================================================
# DATASET GENERATION
# ============================================================================

def generate_complete_dataset(num_samples=50):
    """
    Generate complete dataset with students, internships, and feedback.
    90% of students will have applied to at least one internship.

    Returns:
        Dictionary with students, internships, and feedback data
    """
    dataset = {
        'students': [],
        'internships': [],
        'matches': [],
        'applications': []  # Track student applications
    }

    print(f"Generating {num_samples} student-internship matches with feedback...\n")

    domains = list(DOMAINS.keys())
    expertise_levels = ['beginner', 'medium', 'expert']

    for i in range(num_samples):
        # Pick random domain
        domain = random.choice(domains)

        # Vary expertise levels
        if i < 10:
            expertise = 'beginner'
        elif i < 30:
            expertise = 'medium'
        else:
            expertise = random.choice(expertise_levels)

        # Sometimes match domain, sometimes mismatch for variety
        if random.random() < 0.7:  # 70% same domain
            internship_domain = domain
        else:
            internship_domain = random.choice([d for d in domains if d != domain])

        # Generate student and internship
        student = generate_student_profile(i + 1, domain, expertise)
        internship = generate_internship(i + 1, internship_domain)

        # Calculate true match quality
        match_quality = calculate_true_match_quality(student, internship)

        # Generate feedback based on match quality
        feedback = generate_feedback(student, internship, match_quality)

        # Store
        dataset['students'].append(student)
        dataset['internships'].append(internship)
        dataset['matches'].append({
            'student_id': student['id'],
            'internship_id': internship['id'],
            'organization_id': internship['organization_id'],
            'feedback': feedback,
            'match_quality': match_quality
        })

        # Progress indicator
        if (i + 1) % 10 == 0:
            print(f"✓ Generated {i + 1}/{num_samples} samples")

    # ========================================================================
    # GENERATE APPLICATIONS - 90% of students apply to at least 1 internship
    # ========================================================================
    print(f"\n📝 Generating student applications...")

    students_who_applied = 0
    total_applications = 0

    for student in dataset['students']:
        # 90% of students apply to at least one internship
        if random.random() < 0.90:
            # Determine how many internships this student applies to (1-3)
            num_applications = random.randint(1, 3)

            # Get internships sorted by match quality for this student
            student_matches = []
            for internship in dataset['internships']:
                match_quality = calculate_true_match_quality(student, internship)
                student_matches.append((internship, match_quality))

            # Sort by match quality (best matches first)
            student_matches.sort(key=lambda x: x[1], reverse=True)

            # Student tends to apply to better matches (80% chance from top 50%)
            # but sometimes applies to lower matches too
            applied_internships = set()
            for _ in range(num_applications):
                if random.random() < 0.8:
                    # Apply to a good match (top 50%)
                    top_half = student_matches[:len(student_matches)//2]
                    if top_half:
                        internship, quality = random.choice(top_half)
                        applied_internships.add(internship['id'])
                else:
                    # Apply to any internship
                    internship, quality = random.choice(student_matches)
                    applied_internships.add(internship['id'])

            # Create application records
            for internship_id in applied_internships:
                dataset['applications'].append({
                    'student_id': student['id'],
                    'internship_id': internship_id,
                    'status': random.choice(['pending', 'pending', 'pending', 'shortlisted']),  # Most are pending
                    'applied_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })
                total_applications += 1

            students_who_applied += 1

    application_rate = (students_who_applied / len(dataset['students'])) * 100

    print(f"\n✅ Dataset generation complete!")
    print(f"   - {len(dataset['students'])} students")
    print(f"   - {len(dataset['internships'])} internships")
    print(f"   - {len(dataset['matches'])} complete matches with feedback")
    print(f"   - {len(dataset['applications'])} total applications")
    print(f"   - {students_who_applied}/{len(dataset['students'])} students applied ({application_rate:.1f}%)")

    # Statistics
    match_qualities = [m['match_quality'] for m in dataset['matches']]
    print(f"\n📊 Match Quality Distribution:")
    print(f"   - Average: {sum(match_qualities)/len(match_qualities):.1f}")
    print(f"   - Min: {min(match_qualities):.1f}")
    print(f"   - Max: {max(match_qualities):.1f}")
    print(f"   - Excellent (>80): {sum(1 for q in match_qualities if q > 80)}")
    print(f"   - Good (60-80): {sum(1 for q in match_qualities if 60 < q <= 80)}")
    print(f"   - Poor (<60): {sum(1 for q in match_qualities if q <= 60)}")

    print(f"\n📋 Application Statistics:")
    print(f"   - Students who applied: {students_who_applied} ({application_rate:.1f}%)")
    print(f"   - Students who didn't apply: {len(dataset['students']) - students_who_applied} ({100-application_rate:.1f}%)")
    print(f"   - Total applications: {total_applications}")
    print(f"   - Average applications per student: {total_applications/students_who_applied:.1f}")

    return dataset

# ============================================================================
# EXPORT FUNCTIONS
# ============================================================================

def save_to_json(dataset, filename='sample_dataset.json'):
    """Save dataset to JSON file."""
    import json

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)

    print(f"\n💾 Dataset saved to {filename}")

def print_sample_data(dataset, num_samples=3):
    """Print a few sample entries for verification."""
    print(f"\n📋 Sample Data Preview (first {num_samples} entries):")
    print("=" * 80)

    for i in range(min(num_samples, len(dataset['students']))):
        student = dataset['students'][i]
        internship = dataset['internships'][i]
        match = dataset['matches'][i]

        # Get student applications
        student_apps = [app for app in dataset['applications'] if app['student_id'] == student['id']]

        print(f"\n🎓 Student #{student['id']}: {student['name']}")
        print(f"   Domain: {student['primary_domain']} | Level: {student['expertise_level']}")
        print(f"   Skills: {student['skills'][:60]}...")
        print(f"   Certificates: {len(student['certificates'])}")
        print(f"   Experience: {len(student['internship_experiences'])} internships")
        print(f"   Research: {len(student['research_papers'])} papers")
        print(f"   Applications: {len(student_apps)} internship(s) applied")

        print(f"\n💼 Internship #{internship['id']}: {internship['title']}")
        print(f"   Company: {internship['organization_name']}")
        print(f"   Domain: {internship['domain']}")
        print(f"   Required: {internship['skills_required'][:60]}...")
        print(f"   Stipend: {internship['stipend']} | Duration: {internship['duration']}")

        print(f"\n📊 Match Results:")
        print(f"   Match Quality: {match['match_quality']:.1f}/100")
        print(f"   Success Score: {match['feedback']['actual_success_score']:.1f}/100")
        print(f"   Student Rating: {match['feedback']['student_satisfaction']}/5")
        print(f"   Company Rating: {match['feedback']['company_performance']}/5")
        print(f"   Student: \"{match['feedback']['student_comments']}\"")
        print(f"   Company: \"{match['feedback']['company_comments']}\"")
        print("-" * 80)

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == '__main__':
    print("=" * 80)
    print("ML MATCHING SYSTEM - SAMPLE DATASET GENERATOR")
    print("=" * 80)

    # Install faker if not available
    try:
        from faker import Faker
    except ImportError:
        print("\n⚠️  Installing required package: faker")
        import subprocess
        subprocess.check_call(['pip', 'install', 'faker'])
        from faker import Faker
        fake = Faker()

    # Generate dataset
    dataset = generate_complete_dataset(num_samples=50)

    # Show samples
    print_sample_data(dataset, num_samples=3)

    # Save to file
    save_to_json(dataset)

    print("\n" + "=" * 80)
    print("✅ DATASET GENERATION COMPLETE!")
    print("=" * 80)
    print("\nNext steps:")
    print("1. Run: python load_sample_data.py")
    print("2. This will load the data into your database")
    print("3. Then train the ML model with this feedback data")
    print("4. Test the predictions!")
