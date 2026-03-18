"""
Quick Fix Script - Allocate Internships to Existing Students

This script updates your EXISTING database to allocate internships to 90% of students.
No need to regenerate data - just run this!

Run: python quick_allocate_fix.py
"""

import random
from datetime import datetime

def calculate_match_score(student_skills, internship_skills):
    """Calculate simple match score."""
    student_set = set([s.strip().lower() for s in student_skills.split(',')])
    internship_set = set([s.strip().lower() for s in internship_skills.split(',')])

    if not internship_set:
        return 50.0

    overlap = len(student_set & internship_set) / len(internship_set)
    score = overlap * 100
    return min(100, max(0, score))

def allocate_internships():
    """Allocate internships to 90% of students in existing database."""

    print("=" * 80)
    print("QUICK FIX: ALLOCATING INTERNSHIPS TO STUDENTS")
    print("=" * 80)

    # Import Flask app
    try:
        import sys
        import os

        # Add parent directory to path if needed
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

        from app import app, db, StudentProfile, Internship, Application
    except ImportError as e:
        print(f"\n❌ Error importing app: {e}")
        print("\nTrying alternate import...")
        try:
            # Try direct import
            import app as flask_app
            app = flask_app.app
            db = flask_app.db
            StudentProfile = flask_app.StudentProfile
            Internship = flask_app.Internship
            Application = flask_app.Application
        except ImportError as e2:
            print(f"❌ Could not import: {e2}")
            print("\nPlease ensure:")
            print("  1. You're in the correct directory (where app.py is)")
            print("  2. Your Flask app is set up correctly")
            return False

    with app.app_context():
        print("\n📊 Current Database Status:")

        # Get all students
        all_students = StudentProfile.query.all()
        total_students = len(all_students)

        # Get students with allocations
        allocated_students = [s for s in all_students if s.allocated_internship]
        current_allocated = len(allocated_students)

        # Get all internships
        all_internships = Internship.query.all()
        total_internships = len(all_internships)

        print(f"   Total Students: {total_students}")
        print(f"   Currently Allocated: {current_allocated} ({(current_allocated/total_students*100):.1f}%)")
        print(f"   Total Internships: {total_internships}")

        if current_allocated >= total_students * 0.85:
            print(f"\n✅ Already have {current_allocated} students allocated!")
            print("No need to run this script.")
            return True

        print(f"\n🎯 Goal: Allocate {int(total_students * 0.9)} students (90%)")
        print("=" * 80)

        # Get unallocated students
        unallocated_students = [s for s in all_students if not s.allocated_internship]
        print(f"\n📝 Found {len(unallocated_students)} unallocated students")

        # Calculate how many to allocate (90% of total)
        target_allocated = int(total_students * 0.9)
        need_to_allocate = target_allocated - current_allocated

        print(f"   Need to allocate: {need_to_allocate} more students")

        if need_to_allocate <= 0:
            print("\n✅ Target already reached!")
            return True

        # Select students to allocate (from unallocated pool)
        students_to_allocate = random.sample(
            unallocated_students,
            min(need_to_allocate, len(unallocated_students))
        )

        print(f"\n🔄 Allocating internships to {len(students_to_allocate)} students...")

        allocated_count = 0

        for student in students_to_allocate:
            # Find best matching internship
            best_internship = None
            best_score = 0

            if student.skills and all_internships:
                for internship in all_internships:
                    if internship.skills_required:
                        score = calculate_match_score(student.skills, internship.skills_required)

                        # Add randomness for variety
                        score += random.uniform(-10, 10)

                        if score > best_score:
                            best_score = score
                            best_internship = internship

            # If no match found, pick random
            if not best_internship and all_internships:
                best_internship = random.choice(all_internships)
                best_score = random.uniform(60, 80)

            if best_internship:
                # Allocate
                student.allocated_internship = best_internship.title
                student.match_score = round(best_score, 1)

                # Update application status if exists
                application = Application.query.filter_by(
                    student_id=student.id,
                    internship_id=best_internship.id
                ).first()

                if application:
                    application.status = 'approved'

                allocated_count += 1

                if allocated_count % 10 == 0:
                    print(f"   ✓ Allocated {allocated_count}/{len(students_to_allocate)}")

        # Commit changes
        db.session.commit()

        # Final statistics
        final_allocated = StudentProfile.query.filter(
            StudentProfile.allocated_internship.isnot(None)
        ).count()

        final_rate = (final_allocated / total_students) * 100

        print(f"\n{'=' * 80}")
        print("✅ ALLOCATION COMPLETE!")
        print(f"{'=' * 80}")
        print(f"\n📊 Final Statistics:")
        print(f"   Total Students: {total_students}")
        print(f"   Allocated Students: {final_allocated} ({final_rate:.1f}%)")
        print(f"   Unallocated Students: {total_students - final_allocated} ({100-final_rate:.1f}%)")
        print(f"   Newly Allocated: {allocated_count}")

        print(f"\n✅ SUCCESS! Refresh your admin page to see the changes.")
        print(f"   URL: http://127.0.0.1:5000/admin/students")

        return True

if __name__ == '__main__':
    try:
        success = allocate_internships()
        if not success:
            print("\n❌ Allocation failed. Please check the errors above.")
            import sys
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error occurred: {e}")
        import traceback
        traceback.print_exc()
        import sys
        sys.exit(1)
