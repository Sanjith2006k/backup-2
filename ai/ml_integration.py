"""
ML Matcher Integration Utilities

This module provides helper functions to integrate the enhanced ML matcher
with the Flask application and SQLAlchemy database models.
"""

from typing import List, Dict, Optional
from datetime import datetime
from ai.ml_matcher import get_ml_matcher
import json


def prepare_student_data_for_ml(student_profile, certificates, internship_experiences,
                                  research_papers, ai_score, personality_profile=None,
                                  feedback_history=None):
    """
    Prepare student data in the format expected by the ML matcher.

    Args:
        student_profile: StudentProfile SQLAlchemy object
        certificates: List of StudentCertificate objects
        internship_experiences: List of StudentInternshipExperience objects
        research_papers: List of ResearchPaper objects
        ai_score: StudentAIScore object or None
        personality_profile: PersonalityProfile object or None
        feedback_history: List of InternshipFeedback objects or None

    Returns:
        Dictionary formatted for ML matcher
    """
    # Convert certificates
    certs_list = []
    for cert in certificates:
        certs_list.append({
            'certificate_name': cert.certificate_name,
            'related_skill': cert.related_skill or '',
            'description': cert.description or '',
            'issuing_organization': cert.issuing_organization
        })

    # Convert internship experiences
    exp_list = []
    for exp in internship_experiences:
        exp_list.append({
            'role': exp.role,
            'company_name': exp.company_name,
            'skills_used': exp.skills_used or '',
            'work_description': exp.work_description or '',
            'start_date': exp.start_date,
            'end_date': exp.end_date
        })

    # Convert research papers
    papers_list = []
    for paper in research_papers:
        papers_list.append({
            'title': paper.title,
            'abstract': paper.abstract or '',
            'keywords': paper.keywords or '',
            'domain': paper.domain or '',
            'citation_count': paper.citation_count or 0
        })

    # Calculate average feedback score if available
    avg_feedback_score = 0.5  # Default neutral score
    if feedback_history and len(feedback_history) > 0:
        total_score = sum([f.actual_success_score for f in feedback_history
                          if f.actual_success_score is not None])
        if total_score > 0:
            avg_feedback_score = (total_score / len(feedback_history)) / 100  # Normalize to 0-1

    # Personality-culture match (if available)
    personality_match = 0.5  # Default neutral
    if personality_profile:
        # Simple calculation based on personality traits (can be enhanced)
        personality_match = (personality_profile.teamwork +
                            personality_profile.creativity) / 10  # Normalize

    data = {
        'id': student_profile.id,
        'user_id': student_profile.user_id,
        'skills': student_profile.skills or '',
        'location': student_profile.location or '',
        'certificates': certs_list,
        'internship_experiences': exp_list,
        'research_papers': papers_list,
        'ai_score': ai_score.total_score if ai_score else 0,
        'avg_feedback_score': avg_feedback_score,
        'personality_culture_match': personality_match
    }

    return data


def prepare_internship_data_for_ml(internship, organization=None):
    """
    Prepare internship data in the format expected by the ML matcher.

    Args:
        internship: Internship SQLAlchemy object
        organization: Organization SQLAlchemy object or None

    Returns:
        Dictionary formatted for ML matcher
    """
    # Try to identify domain from title and skills
    matcher = get_ml_matcher()
    combined_text = f"{internship.title} {internship.skills_required}"
    domains = matcher.identify_domain(combined_text)
    primary_domain = domains[0] if domains else 'General'

    data = {
        'id': internship.id,
        'title': internship.title,
        'skills_required': internship.skills_required or '',
        'location': internship.location or 'Remote',
        'duration': internship.duration or '3 months',
        'stipend': internship.stipend or '',
        'domain': primary_domain,
        'organization_name': organization.company_name if organization else '',
        'organization_id': internship.organization_id
    }

    return data


def get_ml_match_score(student_profile, internship, db_session):
    """
    Get ML-based match score for a student-internship pair.

    Args:
        student_profile: StudentProfile object
        internship: Internship object
        db_session: SQLAlchemy database session

    Returns:
        Dictionary with match score and breakdown
    """
    # Import models (avoid circular imports)
    from models import (StudentCertificate, StudentInternshipExperience,
                       ResearchPaper, StudentAIScore, PersonalityProfile,
                       InternshipFeedback, Organization)

    # Fetch student data
    certificates = db_session.query(StudentCertificate).filter_by(
        user_id=student_profile.user_id
    ).all()

    internship_experiences = db_session.query(StudentInternshipExperience).filter_by(
        user_id=student_profile.user_id
    ).all()

    research_papers = db_session.query(ResearchPaper).filter_by(
        user_id=student_profile.user_id
    ).all()

    ai_score = db_session.query(StudentAIScore).filter_by(
        user_id=student_profile.user_id
    ).first()

    personality = db_session.query(PersonalityProfile).filter_by(
        user_id=student_profile.user_id
    ).first()

    # Get feedback history
    feedback_history = db_session.query(InternshipFeedback).filter_by(
        student_id=student_profile.id
    ).all()

    # Get organization
    organization = db_session.query(Organization).filter_by(
        id=internship.organization_id
    ).first()

    # Prepare data
    student_data = prepare_student_data_for_ml(
        student_profile, certificates, internship_experiences,
        research_papers, ai_score, personality, feedback_history
    )

    internship_data = prepare_internship_data_for_ml(internship, organization)

    # Get ML prediction
    matcher = get_ml_matcher()
    result = matcher.predict_match_score(student_data, internship_data)

    return result


def train_ml_model_from_feedback(db_session):
    """
    Train/retrain the ML model using all available feedback data.

    Args:
        db_session: SQLAlchemy database session

    Returns:
        Dictionary with training results
    """
    from models import (InternshipFeedback, StudentProfile, Internship,
                       StudentCertificate, StudentInternshipExperience,
                       ResearchPaper, StudentAIScore, PersonalityProfile,
                       Organization)

    # Get all feedback with computed success scores
    feedbacks = db_session.query(InternshipFeedback).all()

    if len(feedbacks) < 10:
        return {
            'success': False,
            'message': f'Insufficient feedback data. Need at least 10 samples, have {len(feedbacks)}.',
            'samples': len(feedbacks)
        }

    # Prepare training data
    training_data = []

    for feedback in feedbacks:
        # Compute success score if not already computed
        if feedback.actual_success_score is None:
            feedback.actual_success_score = feedback.compute_success_score()
            db_session.commit()

        # Skip if success score is 0 (incomplete feedback)
        if feedback.actual_success_score == 0:
            continue

        # Get student and internship
        student_profile = db_session.query(StudentProfile).filter_by(
            id=feedback.student_id
        ).first()

        internship = db_session.query(Internship).filter_by(
            id=feedback.internship_id
        ).first()

        if not student_profile or not internship:
            continue

        # Prepare student data (at the time of feedback, use historical data if available)
        certificates = db_session.query(StudentCertificate).filter_by(
            user_id=student_profile.user_id
        ).all()

        internship_experiences = db_session.query(StudentInternshipExperience).filter_by(
            user_id=student_profile.user_id
        ).all()

        research_papers = db_session.query(ResearchPaper).filter_by(
            user_id=student_profile.user_id
        ).all()

        ai_score = db_session.query(StudentAIScore).filter_by(
            user_id=student_profile.user_id
        ).first()

        personality = db_session.query(PersonalityProfile).filter_by(
            user_id=student_profile.user_id
        ).first()

        # Get other feedback for this student (exclude current)
        other_feedbacks = db_session.query(InternshipFeedback).filter(
            InternshipFeedback.student_id == student_profile.id,
            InternshipFeedback.id != feedback.id
        ).all()

        organization = db_session.query(Organization).filter_by(
            id=internship.organization_id
        ).first()

        # Prepare data
        student_data = prepare_student_data_for_ml(
            student_profile, certificates, internship_experiences,
            research_papers, ai_score, personality, other_feedbacks
        )

        internship_data = prepare_internship_data_for_ml(internship, organization)

        training_data.append({
            'student_data': student_data,
            'internship_data': internship_data,
            'actual_success_score': feedback.actual_success_score
        })

    if len(training_data) < 10:
        return {
            'success': False,
            'message': f'Insufficient complete feedback data. Need at least 10 samples, have {len(training_data)}.',
            'samples': len(training_data)
        }

    # Train model
    matcher = get_ml_matcher()
    matcher.train_model(training_data)

    # Save model version metadata
    from models import MatchingModelMetrics
    metrics = MatchingModelMetrics(
        model_version=f"v_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        training_samples=len(training_data),
        features_count=len(matcher.feature_names),
        feature_importance=json.dumps(matcher.feature_importance),
        is_active=True
    )

    # Deactivate previous models
    db_session.query(MatchingModelMetrics).update({'is_active': False})
    db_session.add(metrics)
    db_session.commit()

    return {
        'success': True,
        'message': 'Model trained successfully',
        'samples': len(training_data),
        'model_version': metrics.model_version
    }


def submit_student_feedback(feedback_data, db_session):
    """
    Submit student feedback after internship completion.

    Args:
        feedback_data: Dictionary containing feedback fields
        db_session: SQLAlchemy database session

    Returns:
        InternshipFeedback object or None
    """
    from models import InternshipFeedback

    # Check if feedback already exists
    existing = db_session.query(InternshipFeedback).filter_by(
        student_id=feedback_data['student_id'],
        internship_id=feedback_data['internship_id']
    ).first()

    if existing:
        # Update existing feedback
        existing.student_satisfaction = feedback_data.get('satisfaction')
        existing.student_learning = feedback_data.get('learning')
        existing.student_work_environment = feedback_data.get('work_environment')
        existing.student_mentor_quality = feedback_data.get('mentor_quality')
        existing.student_skill_match = feedback_data.get('skill_match')
        existing.student_would_recommend = feedback_data.get('would_recommend')
        existing.student_comments = feedback_data.get('comments', '')
        existing.student_feedback_date = datetime.utcnow()
        feedback = existing
    else:
        # Create new feedback
        feedback = InternshipFeedback(
            student_id=feedback_data['student_id'],
            internship_id=feedback_data['internship_id'],
            organization_id=feedback_data['organization_id'],
            student_satisfaction=feedback_data.get('satisfaction'),
            student_learning=feedback_data.get('learning'),
            student_work_environment=feedback_data.get('work_environment'),
            student_mentor_quality=feedback_data.get('mentor_quality'),
            student_skill_match=feedback_data.get('skill_match'),
            student_would_recommend=feedback_data.get('would_recommend'),
            student_comments=feedback_data.get('comments', ''),
            student_feedback_date=datetime.utcnow(),
            original_match_score=feedback_data.get('original_match_score')
        )
        db_session.add(feedback)

    # Recompute success score if both feedbacks exist
    if feedback.company_performance:
        feedback.actual_success_score = feedback.compute_success_score()

    db_session.commit()
    return feedback


def submit_company_feedback(feedback_data, db_session):
    """
    Submit company feedback after internship completion.

    Args:
        feedback_data: Dictionary containing feedback fields
        db_session: SQLAlchemy database session

    Returns:
        InternshipFeedback object or None
    """
    from models import InternshipFeedback

    # Check if feedback already exists
    existing = db_session.query(InternshipFeedback).filter_by(
        student_id=feedback_data['student_id'],
        internship_id=feedback_data['internship_id']
    ).first()

    if existing:
        # Update existing feedback
        existing.company_performance = feedback_data.get('performance')
        existing.company_skill_level = feedback_data.get('skill_level')
        existing.company_professionalism = feedback_data.get('professionalism')
        existing.company_learning_ability = feedback_data.get('learning_ability')
        existing.company_would_hire = feedback_data.get('would_hire')
        existing.company_would_recommend = feedback_data.get('would_recommend')
        existing.company_comments = feedback_data.get('comments', '')
        existing.company_feedback_date = datetime.utcnow()
        feedback = existing
    else:
        # Create new feedback
        feedback = InternshipFeedback(
            student_id=feedback_data['student_id'],
            internship_id=feedback_data['internship_id'],
            organization_id=feedback_data['organization_id'],
            company_performance=feedback_data.get('performance'),
            company_skill_level=feedback_data.get('skill_level'),
            company_professionalism=feedback_data.get('professionalism'),
            company_learning_ability=feedback_data.get('learning_ability'),
            company_would_hire=feedback_data.get('would_hire'),
            company_would_recommend=feedback_data.get('would_recommend'),
            company_comments=feedback_data.get('comments', ''),
            company_feedback_date=datetime.utcnow(),
            original_match_score=feedback_data.get('original_match_score')
        )
        db_session.add(feedback)

    # Recompute success score if student feedback exists
    if feedback.student_satisfaction:
        feedback.actual_success_score = feedback.compute_success_score()

    db_session.commit()

    # Trigger model retraining if we have enough new samples
    total_feedbacks = db_session.query(InternshipFeedback).count()
    if total_feedbacks % 10 == 0:  # Retrain every 10 new feedbacks
        train_ml_model_from_feedback(db_session)

    return feedback


def get_top_matches_for_internship(internship_id, db_session, limit=10):
    """
    Get top student matches for a given internship using ML model.

    Args:
        internship_id: ID of the internship
        db_session: SQLAlchemy database session
        limit: Maximum number of matches to return

    Returns:
        List of tuples (student_profile, match_result)
    """
    from models import Internship, StudentProfile, Organization

    internship = db_session.query(Internship).filter_by(id=internship_id).first()

    if not internship:
        return []

    # Get all students
    students = db_session.query(StudentProfile).all()

    # Get matches
    results = []
    for student in students:
        match_result = get_ml_match_score(student, internship, db_session)
        results.append((student, match_result))

    # Sort by match score
    results.sort(key=lambda x: x[1]['match_score'], reverse=True)

    return results[:limit]


def get_top_internships_for_student(student_id, db_session, limit=10):
    """
    Get top internship matches for a given student using ML model.

    Args:
        student_id: ID of the student profile
        db_session: SQLAlchemy database session
        limit: Maximum number of matches to return

    Returns:
        List of tuples (internship, match_result)
    """
    from models import StudentProfile, Internship

    student = db_session.query(StudentProfile).filter_by(id=student_id).first()

    if not student:
        return []

    # Get all active internships
    internships = db_session.query(Internship).filter_by(status='active').all()

    # Get matches
    results = []
    for internship in internships:
        match_result = get_ml_match_score(student, internship, db_session)
        results.append((internship, match_result))

    # Sort by match score
    results.sort(key=lambda x: x[1]['match_score'], reverse=True)

    return results[:limit]
