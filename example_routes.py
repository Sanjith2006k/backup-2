"""
Flask Routes for ML-Enhanced Matching System

This file contains example Flask routes to integrate the enhanced ML matcher
into your application. Add these routes to your main app.py file.
"""

from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_login import login_required, current_user
from ai.ml_integration import (
    get_ml_match_score,
    train_ml_model_from_feedback,
    submit_student_feedback,
    submit_company_feedback,
    get_top_matches_for_internship,
    get_top_internships_for_student
)
from models import InternshipFeedback, ResearchPaper
from datetime import datetime


# ============================================================================
# STUDENT ROUTES
# ============================================================================

@app.route('/student/internships/ml-matches')
@login_required
def student_ml_matches():
    """
    Show ML-enhanced internship recommendations for the current student.
    """
    if current_user.role != 'student':
        return redirect(url_for('home'))

    # Get student profile
    student_profile = StudentProfile.query.filter_by(user_id=current_user.id).first()

    if not student_profile:
        return render_template('error.html', message='Student profile not found')

    # Get top ML matches
    matches = get_top_internships_for_student(student_profile.id, db.session, limit=20)

    return render_template('student/ml_matches.html',
                          matches=matches,
                          student=student_profile)


@app.route('/student/feedback/submit/<int:internship_id>', methods=['GET', 'POST'])
@login_required
def submit_student_feedback_route(internship_id):
    """
    Submit feedback after completing an internship.
    """
    if current_user.role != 'student':
        return redirect(url_for('home'))

    student_profile = StudentProfile.query.filter_by(user_id=current_user.id).first()
    internship = Internship.query.get(internship_id)

    if not student_profile or not internship:
        return render_template('error.html', message='Invalid request')

    if request.method == 'POST':
        feedback_data = {
            'student_id': student_profile.id,
            'internship_id': internship_id,
            'organization_id': internship.organization_id,
            'satisfaction': int(request.form.get('satisfaction')),
            'learning': int(request.form.get('learning')),
            'work_environment': int(request.form.get('work_environment')),
            'mentor_quality': int(request.form.get('mentor_quality')),
            'skill_match': int(request.form.get('skill_match')),
            'would_recommend': request.form.get('would_recommend') == 'yes',
            'comments': request.form.get('comments', ''),
            'original_match_score': student_profile.match_score
        }

        submit_student_feedback(feedback_data, db.session)

        return render_template('success.html',
                              message='Thank you for your feedback! This will help improve future recommendations.')

    return render_template('student/submit_feedback.html',
                          internship=internship)


@app.route('/student/research-papers', methods=['GET', 'POST'])
@login_required
def manage_research_papers():
    """
    Manage research papers for the student.
    """
    if current_user.role != 'student':
        return redirect(url_for('home'))

    if request.method == 'POST':
        paper = ResearchPaper(
            user_id=current_user.id,
            title=request.form.get('title'),
            authors=request.form.get('authors'),
            publication_venue=request.form.get('venue'),
            publication_date=datetime.strptime(request.form.get('pub_date'), '%Y-%m-%d').date(),
            abstract=request.form.get('abstract'),
            keywords=request.form.get('keywords'),
            domain=request.form.get('domain'),
            paper_url=request.form.get('paper_url'),
            doi=request.form.get('doi', ''),
            citation_count=int(request.form.get('citation_count', 0))
        )

        db.session.add(paper)
        db.session.commit()

        return redirect(url_for('manage_research_papers'))

    papers = ResearchPaper.query.filter_by(user_id=current_user.id).all()
    return render_template('student/research_papers.html', papers=papers)


@app.route('/student/match-details/<int:internship_id>')
@login_required
def student_match_details(internship_id):
    """
    Show detailed match breakdown for a specific internship.
    """
    if current_user.role != 'student':
        return redirect(url_for('home'))

    student_profile = StudentProfile.query.filter_by(user_id=current_user.id).first()
    internship = Internship.query.get(internship_id)

    if not student_profile or not internship:
        return render_template('error.html', message='Invalid request')

    match_result = get_ml_match_score(student_profile, internship, db.session)

    return render_template('student/match_details.html',
                          internship=internship,
                          match_result=match_result,
                          student=student_profile)


# ============================================================================
# ORGANIZATION ROUTES
# ============================================================================

@app.route('/organization/internship/<int:internship_id>/ml-matches')
@login_required
def org_ml_matches(internship_id):
    """
    Show ML-enhanced student recommendations for an internship.
    """
    if current_user.role != 'organization':
        return redirect(url_for('home'))

    internship = Internship.query.get(internship_id)

    if not internship or internship.organization_id != Organization.query.filter_by(
            user_id=current_user.id).first().id:
        return render_template('error.html', message='Invalid internship')

    # Get top ML matches
    matches = get_top_matches_for_internship(internship_id, db.session, limit=50)

    return render_template('organization/ml_matches.html',
                          matches=matches,
                          internship=internship)


@app.route('/organization/feedback/submit/<int:student_id>/<int:internship_id>',
          methods=['GET', 'POST'])
@login_required
def submit_company_feedback_route(student_id, internship_id):
    """
    Submit feedback for a student who completed an internship.
    """
    if current_user.role != 'organization':
        return redirect(url_for('home'))

    org = Organization.query.filter_by(user_id=current_user.id).first()
    student = StudentProfile.query.get(student_id)
    internship = Internship.query.get(internship_id)

    if not org or not student or not internship or internship.organization_id != org.id:
        return render_template('error.html', message='Invalid request')

    if request.method == 'POST':
        feedback_data = {
            'student_id': student_id,
            'internship_id': internship_id,
            'organization_id': org.id,
            'performance': int(request.form.get('performance')),
            'skill_level': int(request.form.get('skill_level')),
            'professionalism': int(request.form.get('professionalism')),
            'learning_ability': int(request.form.get('learning_ability')),
            'would_hire': request.form.get('would_hire') == 'yes',
            'would_recommend': request.form.get('would_recommend') == 'yes',
            'comments': request.form.get('comments', ''),
            'original_match_score': student.match_score
        }

        submit_company_feedback(feedback_data, db.session)

        return render_template('success.html',
                              message='Thank you for your feedback! This will help improve future matching.')

    return render_template('organization/submit_feedback.html',
                          student=student,
                          internship=internship)


# ============================================================================
# ADMIN ROUTES
# ============================================================================

@app.route('/admin/ml-model/train', methods=['POST'])
@login_required
def admin_train_ml_model():
    """
    Manually trigger ML model training (admin only).
    """
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403

    result = train_ml_model_from_feedback(db.session)

    return jsonify(result)


@app.route('/admin/ml-model/status')
@login_required
def admin_ml_model_status():
    """
    View ML model training status and metrics (admin only).
    """
    if current_user.role != 'admin':
        return redirect(url_for('home'))

    from models import MatchingModelMetrics

    # Get latest model metrics
    latest_model = MatchingModelMetrics.query.filter_by(
        is_active=True
    ).order_by(MatchingModelMetrics.trained_at.desc()).first()

    # Get feedback statistics
    total_feedbacks = InternshipFeedback.query.count()
    complete_feedbacks = InternshipFeedback.query.filter(
        InternshipFeedback.actual_success_score.isnot(None)
    ).count()

    student_feedbacks = InternshipFeedback.query.filter(
        InternshipFeedback.student_satisfaction.isnot(None)
    ).count()

    company_feedbacks = InternshipFeedback.query.filter(
        InternshipFeedback.company_performance.isnot(None)
    ).count()

    return render_template('admin/ml_model_status.html',
                          model=latest_model,
                          total_feedbacks=total_feedbacks,
                          complete_feedbacks=complete_feedbacks,
                          student_feedbacks=student_feedbacks,
                          company_feedbacks=company_feedbacks)


# ============================================================================
# API ROUTES (for AJAX calls)
# ============================================================================

@app.route('/api/ml-match-score', methods=['POST'])
@login_required
def api_ml_match_score():
    """
    API endpoint to get ML match score for a student-internship pair.
    """
    data = request.json
    student_id = data.get('student_id')
    internship_id = data.get('internship_id')

    student = StudentProfile.query.get(student_id)
    internship = Internship.query.get(internship_id)

    if not student or not internship:
        return jsonify({'error': 'Invalid IDs'}), 400

    match_result = get_ml_match_score(student, internship, db.session)

    return jsonify(match_result)


@app.route('/api/student-recommendations/<int:student_id>')
@login_required
def api_student_recommendations(student_id):
    """
    API endpoint to get top internship recommendations for a student.
    """
    limit = request.args.get('limit', 10, type=int)

    matches = get_top_internships_for_student(student_id, db.session, limit=limit)

    results = []
    for internship, match_result in matches:
        results.append({
            'internship_id': internship.id,
            'title': internship.title,
            'organization_id': internship.organization_id,
            'match_score': match_result['match_score'],
            'breakdown': match_result['breakdown'],
            'recommendations': match_result['recommendations']
        })

    return jsonify(results)


@app.route('/api/internship-matches/<int:internship_id>')
@login_required
def api_internship_matches(internship_id):
    """
    API endpoint to get top student matches for an internship.
    """
    if current_user.role not in ['organization', 'admin']:
        return jsonify({'error': 'Unauthorized'}), 403

    limit = request.args.get('limit', 10, type=int)

    matches = get_top_matches_for_internship(internship_id, db.session, limit=limit)

    results = []
    for student, match_result in matches:
        results.append({
            'student_id': student.id,
            'user_id': student.user_id,
            'skills': student.skills,
            'match_score': match_result['match_score'],
            'breakdown': match_result['breakdown'],
            'recommendations': match_result['recommendations']
        })

    return jsonify(results)
