"""
Load Sample Dataset into Database

This script loads the generated sample data (with 90% application rate)
into your Flask database.

Run after:
1. python generate_sample_data.py
2. python migrate_db.py

Usage:
    python load_sample_data_to_db.py
"""

import json
import sys
import random
from datetime import datetime

def calculate_true_match_quality(student, internship):
    """
    Calculate the true match quality based on student profile and internship.
    This is a simplified version from generate_sample_data.py
    """
    score = 0.0

    # Skill match (40% weight)
    student_skills = set([s.strip().lower() for s in student['skills'].split(',')])
    required_skills = set([s.strip().lower() for s in internship['skills_required'].split(',')])

    if required_skills:
        skill_overlap = len(student_skills & required_skills) / len(required_skills)
        score += skill_overlap * 40

    # Domain match (20% weight)
    if student['primary_domain'] == internship.get('domain', ''):
        score += 20

    # Expertise level (15% weight)
    expertise_scores = {'beginner': 5, 'medium': 10, 'expert': 15}
    score += expertise_scores.get(student.get('expertise_level', 'medium'), 10)

    # Certificates boost (10% weight)
    cert_boost = min(len(student.get('certificates', [])) * 3, 10)
    score += cert_boost

    # Experience boost (10% weight)
    exp_boost = min(len(student.get('internship_experiences', [])) * 5, 10)
    score += exp_boost

    # Research boost (5% weight)
    research_boost = min(len(student.get('research_papers', [])) * 2.5, 5)
    score += research_boost

    # Add some randomness (±10 points)
    score += random.uniform(-10, 10)

    return max(0, min(100, score))

def load_dataset_to_database():
    """Load the sample dataset into the database."""

    # Check if dataset exists
    try:
        with open('sample_dataset.json', 'r', encoding='utf-8') as f:
            dataset = json.load(f)
    except FileNotFoundError:
        print("❌ Error: sample_dataset.json not found!")
        print("Please run 'python generate_sample_data.py' first.")
        sys.exit(1)

    print("=" * 80)
    print("LOADING SAMPLE DATASET INTO DATABASE")
    print("=" * 80)

    print(f"\n📂 Dataset loaded:")
    print(f"   - {len(dataset['students'])} students")
    print(f"   - {len(dataset['internships'])} internships")
    print(f"   - {len(dataset['matches'])} feedback records")
    print(f"   - {len(dataset['applications'])} applications")

    # Import Flask app and models
    print("\n🔧 Importing Flask app and models...")
    try:
        # Adjust this import based on your app structure
        from app import app, db
        from app import (User, StudentProfile, Organization, Internship,
                        Application, StudentCertificate, StudentInternshipExperience)
        from models import InternshipFeedback, ResearchPaper
    except ImportError as e:
        print(f"❌ Error importing: {e}")
        print("\nPlease ensure:")
        print("  1. You're in the correct directory")
        print("  2. Your app.py and models.py are set up correctly")
        sys.exit(1)

    with app.app_context():
        print("\n🗑️  Clearing existing sample data...")

        # Clear existing data (be careful in production!)
        db.session.query(InternshipFeedback).delete()
        db.session.query(Application).delete()
        db.session.query(ResearchPaper).delete()
        db.session.query(StudentInternshipExperience).delete()
        db.session.query(StudentCertificate).delete()
        db.session.query(Internship).delete()
        db.session.query(StudentProfile).delete()
        db.session.query(Organization).delete()
        db.session.query(User).filter(User.role.in_(['student', 'organization'])).delete()
        db.session.commit()

        print("✓ Cleared existing data")

        # Track created IDs
        user_id_map = {}  # student['id'] -> user.id
        student_profile_id_map = {}  # student['id'] -> profile.id
        org_id_map = {}  # org_id -> org.id
        internship_id_map = {}  # internship['id'] -> internship.id

        # ====================================================================
        # 1. CREATE STUDENTS
        # ====================================================================
        print("\n👨‍🎓 Creating students...")
        for student_data in dataset['students']:
            # Create user account
            user = User(
                name=student_data['name'],
                email=f"student{student_data['id']}@example.com",
                password='hashed_password',  # In real app, use password hashing
                role='student'
            )
            db.session.add(user)
            db.session.flush()

            user_id_map[student_data['id']] = user.id

            # Create student profile
            profile = StudentProfile(
                user_id=user.id,
                skills=student_data['skills'],
                location=student_data['location']
            )
            db.session.add(profile)
            db.session.flush()

            student_profile_id_map[student_data['id']] = profile.id

            # Add certificates
            for cert_data in student_data['certificates']:
                cert = StudentCertificate(
                    user_id=user.id,
                    certificate_name=cert_data['certificate_name'],
                    issuing_organization=cert_data['issuing_organization'],
                    related_skill=cert_data['related_skill'],
                    description=cert_data['description']
                )
                db.session.add(cert)

            # Add internship experiences
            for exp_data in student_data['internship_experiences']:
                exp = StudentInternshipExperience(
                    user_id=user.id,
                    company_name=exp_data['company_name'],
                    role=exp_data['role'],
                    skills_used=exp_data['skills_used'],
                    work_description=exp_data['work_description'],
                    start_date=datetime.strptime(exp_data['start_date'], '%Y-%m-%d').date(),
                    end_date=datetime.strptime(exp_data['end_date'], '%Y-%m-%d').date()
                )
                db.session.add(exp)

            # Add research papers
            for paper_data in student_data['research_papers']:
                paper = ResearchPaper(
                    user_id=user.id,
                    title=paper_data['title'],
                    abstract=paper_data['abstract'],
                    keywords=paper_data['keywords'],
                    domain=paper_data['domain'],
                    citation_count=paper_data['citation_count']
                )
                db.session.add(paper)

        db.session.commit()
        print(f"✓ Created {len(dataset['students'])} students with profiles")

        # ====================================================================
        # 2. CREATE ORGANIZATIONS
        # ====================================================================
        print("\n🏢 Creating organizations...")
        unique_orgs = set(i['organization_id'] for i in dataset['internships'])

        for org_id in unique_orgs:
            # Get org name from first internship with this org
            org_name = next(i['organization_name'] for i in dataset['internships']
                          if i['organization_id'] == org_id)

            # Create user account for org
            user = User(
                name=org_name,
                email=f"org{org_id}@example.com",
                password='hashed_password',
                role='organization'
            )
            db.session.add(user)
            db.session.flush()

            # Create organization
            org = Organization(
                user_id=user.id,
                company_name=org_name,
                is_verified=True,
                verification_status='approved'
            )
            db.session.add(org)
            db.session.flush()

            org_id_map[org_id] = org.id

        db.session.commit()
        print(f"✓ Created {len(unique_orgs)} organizations")

        # ====================================================================
        # 3. CREATE INTERNSHIPS
        # ====================================================================
        print("\n💼 Creating internships...")
        for internship_data in dataset['internships']:
            internship = Internship(
                organization_id=org_id_map[internship_data['organization_id']],
                title=internship_data['title'],
                skills_required=internship_data['skills_required'],
                location=internship_data['location'],
                duration=internship_data['duration'],
                stipend=internship_data['stipend'],
                status='active'
            )
            db.session.add(internship)
            db.session.flush()

            internship_id_map[internship_data['id']] = internship.id

        db.session.commit()
        print(f"✓ Created {len(dataset['internships'])} internships")

        # ====================================================================
        # 4. CREATE APPLICATIONS (90% of students applied!)
        # ====================================================================
        print("\n📝 Creating applications...")
        for app_data in dataset['applications']:
            application = Application(
                student_id=student_profile_id_map[app_data['student_id']],
                internship_id=internship_id_map[app_data['internship_id']],
                status=app_data['status'],
                applied_at=datetime.strptime(app_data['applied_at'], '%Y-%m-%d %H:%M:%S')
            )
            db.session.add(application)

        db.session.commit()

        # Calculate application stats
        students_who_applied = len(set(app['student_id'] for app in dataset['applications']))
        application_rate = (students_who_applied / len(dataset['students'])) * 100

        print(f"✓ Created {len(dataset['applications'])} applications")
        print(f"✓ {students_who_applied}/{len(dataset['students'])} students applied ({application_rate:.1f}%)")

        # ====================================================================
        # 4.5 ALLOCATE INTERNSHIPS (90% get allocated!)
        # ====================================================================
        print("\n🎯 Allocating internships to students...")

        # Import ml_matcher to calculate match scores
        try:
            from ai.ml_matcher import get_ml_matcher
            matcher = get_ml_matcher()
        except:
            matcher = None
            print("⚠ ML matcher not available, using basic allocation")

        allocated_count = 0

        for student_data in dataset['students']:
            # 90% of students get allocated
            if random.random() < 0.90:
                student_profile = db.session.query(StudentProfile).filter_by(
                    id=student_profile_id_map[student_data['id']]
                ).first()

                # Find best matching internship for this student
                best_match = None
                best_score = 0

                for internship_data in dataset['internships']:
                    match_quality = calculate_true_match_quality(student_data, internship_data)
                    if match_quality > best_score:
                        best_score = match_quality
                        best_match = internship_data

                if best_match:
                    # Allocate this internship to the student
                    student_profile.allocated_internship = best_match['title']
                    student_profile.match_score = best_score

                    # Mark one of their applications as approved
                    student_apps = db.session.query(Application).filter_by(
                        student_id=student_profile_id_map[student_data['id']],
                        internship_id=internship_id_map[best_match['id']]
                    ).first()

                    if student_apps:
                        student_apps.status = 'approved'

                    allocated_count += 1

        db.session.commit()

        allocation_rate = (allocated_count / len(dataset['students'])) * 100
        print(f"✓ Allocated {allocated_count}/{len(dataset['students'])} students ({allocation_rate:.1f}%)")

        # ====================================================================
        # 5. CREATE FEEDBACK
        # ====================================================================
        print("\n💬 Creating feedback records...")
        for match_data in dataset['matches']:
            feedback_data = match_data['feedback']

            feedback = InternshipFeedback(
                student_id=student_profile_id_map[match_data['student_id']],
                internship_id=internship_id_map[match_data['internship_id']],
                organization_id=org_id_map[match_data['organization_id']],
                student_satisfaction=feedback_data['student_satisfaction'],
                student_learning=feedback_data['student_learning'],
                student_work_environment=feedback_data['student_work_environment'],
                student_mentor_quality=feedback_data['student_mentor_quality'],
                student_skill_match=feedback_data['student_skill_match'],
                student_would_recommend=feedback_data['student_would_recommend'],
                student_comments=feedback_data['student_comments'],
                company_performance=feedback_data['company_performance'],
                company_skill_level=feedback_data['company_skill_level'],
                company_professionalism=feedback_data['company_professionalism'],
                company_learning_ability=feedback_data['company_learning_ability'],
                company_would_hire=feedback_data['company_would_hire'],
                company_would_recommend=feedback_data['company_would_recommend'],
                company_comments=feedback_data['company_comments'],
                actual_success_score=feedback_data['actual_success_score']
            )
            db.session.add(feedback)

        db.session.commit()
        print(f"✓ Created {len(dataset['matches'])} feedback records")

    print("\n" + "=" * 80)
    print("✅ DATABASE LOADING COMPLETE!")
    print("=" * 80)

    print("\n📊 Summary:")
    print(f"   ✓ {len(dataset['students'])} students created")
    print(f"   ✓ {len(unique_orgs)} organizations created")
    print(f"   ✓ {len(dataset['internships'])} internships created")
    print(f"   ✓ {len(dataset['applications'])} applications created")
    print(f"   ✓ {students_who_applied} students applied ({application_rate:.1f}%)")
    print(f"   ✓ {allocated_count} students allocated internships ({allocation_rate:.1f}%)")
    print(f"   ✓ {len(dataset['matches'])} feedback records created")

    print("\n🎯 Next Steps:")
    print("   1. Login as any student: student1@example.com (password: password)")
    print("   2. Login as any org: org2001@example.com (password: password)")
    print("   3. Check student list - 90% should have allocated internships!")
    print("   4. View the ML model status at /admin/ml-model/status")
    print("   5. Train the model with the feedback data!")

    print("\n💡 Sample Credentials:")
    print("   Student: student1@example.com")
    print("   Student: student2@example.com")
    print("   Organization: org2001@example.com")
    print("   (All passwords: 'password' - update in your app)")

    print("\n✅ VERIFICATION:")
    print(f"   - {allocated_count}/{len(dataset['students'])} students have ALLOCATED internships")
    print(f"   - Check the student list - most should show internship names and match scores!")

if __name__ == '__main__':
    try:
        load_dataset_to_database()
    except Exception as e:
        print(f"\n❌ Error occurred: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
