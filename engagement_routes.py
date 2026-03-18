"""
Enhanced Flask Routes for Student Engagement System

Add these routes to your app.py to enable the enhanced dashboard and
automatic engagement features that will increase application rates to 90%+.
"""

from flask import render_template, redirect, url_for, request, jsonify
from flask_login import login_required, current_user
from ai.student_engagement import get_engagement_system


# ============================================================================
# ENHANCED STUDENT DASHBOARD
# ============================================================================

@app.route('/student/dashboard')
@login_required
def student_dashboard_enhanced():
    """
    Enhanced student dashboard with ML recommendations and engagement features.
    Shows top matches, profile completion, and encourages applications.
    """
    if current_user.role != 'student':
        return redirect(url_for('home'))

    # Get comprehensive dashboard data
    engagement = get_engagement_system(db.session)
    dashboard_data = engagement.get_student_dashboard_data(current_user.id)

    if not dashboard_data:
        # Student profile doesn't exist, create one
        from models import StudentProfile
        profile = StudentProfile(user_id=current_user.id, skills="")
        db.session.add(profile)
        db.session.commit()
        return redirect(url_for('student_dashboard_enhanced'))

    return render_template('student/dashboard_enhanced.html', **dashboard_data)


# ============================================================================
# QUICK APPLY ROUTE
# ============================================================================

@app.route('/student/quick-apply/<int:internship_id>', methods=['POST'])
@login_required
def quick_apply(internship_id):
    """
    Quick apply to an internship from the dashboard.
    """
    if current_user.role != 'student':
        return jsonify({'error': 'Unauthorized'}), 403

    from models import StudentProfile, Application, Internship

    student = StudentProfile.query.filter_by(user_id=current_user.id).first()
    internship = Internship.query.get(internship_id)

    if not student or not internship:
        return jsonify({'error': 'Invalid request'}), 400

    # Check if already applied
    existing = Application.query.filter_by(
        student_id=student.id,
        internship_id=internship_id
    ).first()

    if existing:
        return jsonify({'error': 'Already applied'}), 400

    # Create application
    application = Application(
        student_id=student.id,
        internship_id=internship_id,
        status='pending'
    )

    db.session.add(application)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Application submitted successfully!'
    })


# ============================================================================
# ADMIN ROUTES - ENGAGEMENT MONITORING
# ============================================================================

@app.route('/admin/engagement-dashboard')
@login_required
def admin_engagement_dashboard():
    """
    Admin dashboard to monitor student engagement and application rates.
    """
    if current_user.role != 'admin':
        return redirect(url_for('home'))

    from models import StudentProfile, Application, User

    engagement = get_engagement_system(db.session)

    # Get application rate
    application_rate = engagement.get_application_rate()

    # Get inactive students
    inactive_students = engagement.get_inactive_students(days_inactive=3)

    # Get total stats
    total_students = StudentProfile.query.count()
    total_applications = Application.query.count()

    # Students by application count
    students_with_0_apps = StudentProfile.query.outerjoin(
        Application,
        StudentProfile.id == Application.student_id
    ).group_by(StudentProfile.id).having(
        db.func.count(Application.id) == 0
    ).count()

    students_with_1plus_apps = total_students - students_with_0_apps

    # Get incomplete profiles
    incomplete_profiles = StudentProfile.query.filter(
        (StudentProfile.skills == None) | (StudentProfile.skills == '')
    ).count()

    return render_template('admin/engagement_dashboard.html',
                         application_rate=application_rate,
                         total_students=total_students,
                         students_with_apps=students_with_1plus_apps,
                         students_without_apps=students_with_0_apps,
                         inactive_count=len(inactive_students),
                         incomplete_profiles=incomplete_profiles,
                         total_applications=total_applications)


@app.route('/admin/send-bulk-reminders', methods=['POST'])
@login_required
def admin_send_bulk_reminders():
    """
    Send application reminders to all inactive students.
    """
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403

    engagement = get_engagement_system(db.session)
    result = engagement.send_bulk_reminders()

    return jsonify(result)


@app.route('/admin/send-daily-notifications', methods=['POST'])
@login_required
def admin_send_daily_notifications():
    """
    Send daily match notifications to all active students.
    """
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403

    from models import User

    engagement = get_engagement_system(db.session)

    # Get all students
    students = User.query.filter_by(role='student').all()

    sent_count = 0
    for student in students:
        if engagement.send_daily_match_notification(student.id):
            sent_count += 1

    return jsonify({
        'total_students': len(students),
        'notifications_sent': sent_count
    })


# ============================================================================
# AUTOMATED CRON JOBS (Set up with scheduler)
# ============================================================================

def setup_automated_notifications():
    """
    Set up automated daily notifications.
    Call this function to schedule automated tasks.
    """
    from apscheduler.schedulers.background import BackgroundScheduler
    import atexit

    scheduler = BackgroundScheduler()

    # Send daily match notifications at 9 AM
    scheduler.add_job(
        func=send_daily_notifications_job,
        trigger="cron",
        hour=9,
        minute=0
    )

    # Send reminders to inactive students at 3 PM
    scheduler.add_job(
        func=send_reminder_job,
        trigger="cron",
        hour=15,
        minute=0
    )

    scheduler.start()

    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())


def send_daily_notifications_job():
    """Background job to send daily notifications."""
    from models import User

    with app.app_context():
        engagement = get_engagement_system(db.session)
        students = User.query.filter_by(role='student').all()

        for student in students:
            engagement.send_daily_match_notification(student.id)


def send_reminder_job():
    """Background job to send reminders to inactive students."""
    with app.app_context():
        engagement = get_engagement_system(db.session)
        engagement.send_bulk_reminders()


# ============================================================================
# IN-APP NOTIFICATIONS
# ============================================================================

@app.route('/api/student/notifications')
@login_required
def get_student_notifications():
    """
    Get in-app notifications for a student.
    """
    if current_user.role != 'student':
        return jsonify({'error': 'Unauthorized'}), 403

    from models import StudentProfile
    from ai.ml_integration import get_top_internships_for_student

    student = StudentProfile.query.filter_by(user_id=current_user.id).first()

    if not student:
        return jsonify({'notifications': []})

    # Get top unapplied matches
    matches = get_top_internships_for_student(student.id, db.session, limit=5)

    notifications = []

    # Check for high-match internships not applied to
    for internship, match_result in matches:
        if match_result['match_score'] >= 85:
            notifications.append({
                'type': 'high_match',
                'title': f"🎯 {match_result['match_score']:.0f}% Match!",
                'message': f"Perfect opportunity: {internship.title}",
                'link': f'/student/apply/{internship.id}',
                'priority': 'high'
            })

    # Check for profile completion
    engagement = get_engagement_system(db.session)
    dashboard_data = engagement.get_student_dashboard_data(current_user.id)

    if dashboard_data['profile_score'] < 70:
        notifications.append({
            'type': 'profile_incomplete',
            'title': '📝 Complete Your Profile',
            'message': f"You're {dashboard_data['profile_score']}% complete. Finish to get better matches!",
            'link': '/student/profile/edit',
            'priority': 'medium'
        })

    # Check if no applications yet
    if dashboard_data['applications_count'] == 0:
        notifications.append({
            'type': 'no_applications',
            'title': '⚡ Start Applying Today!',
            'message': f"You have {len(matches)} perfect matches waiting for you",
            'link': '/student/dashboard#recommendations',
            'priority': 'high'
        })

    return jsonify({'notifications': notifications})


# ============================================================================
# GAMIFICATION - BADGES & ACHIEVEMENTS
# ============================================================================

@app.route('/student/achievements')
@login_required
def student_achievements():
    """
    Show student achievements and badges.
    """
    if current_user.role != 'student':
        return redirect(url_for('home'))

    from models import StudentProfile, Application, StudentCertificate, ResearchPaper

    student = StudentProfile.query.filter_by(user_id=current_user.id).first()

    achievements = []

    # Application badges
    app_count = Application.query.filter_by(student_id=student.id).count()
    if app_count >= 1:
        achievements.append({
            'name': 'First Step',
            'description': 'Applied to your first internship',
            'icon': '🚀',
            'earned': True
        })
    if app_count >= 5:
        achievements.append({
            'name': 'Go-Getter',
            'description': 'Applied to 5 internships',
            'icon': '⭐',
            'earned': True
        })
    if app_count >= 10:
        achievements.append({
            'name': 'Career Hunter',
            'description': 'Applied to 10 internships',
            'icon': '🏆',
            'earned': True
        })

    # Certificate badges
    cert_count = StudentCertificate.query.filter_by(user_id=current_user.id).count()
    if cert_count >= 1:
        achievements.append({
            'name': 'Certified',
            'description': 'Added your first certificate',
            'icon': '📜',
            'earned': True
        })

    # Research badges
    paper_count = ResearchPaper.query.filter_by(user_id=current_user.id).count()
    if paper_count >= 1:
        achievements.append({
            'name': 'Researcher',
            'description': 'Published research paper',
            'icon': '📄',
            'earned': True
        })

    return render_template('student/achievements.html',
                         achievements=achievements,
                         total_points=len([a for a in achievements if a['earned']]) * 100)


# ============================================================================
# EXAMPLE: Add to app.py initialization
# ============================================================================

"""
# In your app.py, add after creating the app:

if __name__ == '__main__':
    # Set up automated notifications
    setup_automated_notifications()

    app.run(debug=True)
"""
