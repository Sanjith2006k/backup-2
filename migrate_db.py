"""
Database Migration Script for ML-Enhanced Matching System

This script adds the new database tables required for the ML matching system:
- InternshipFeedback: Stores post-internship feedback from students and companies
- ResearchPaper: Stores student research publications
- MatchingModelMetrics: Stores ML model performance metrics

Run this script to update your existing database with the new tables.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Create Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Import all models (including new ones)
class InternshipFeedback(db.Model):
    """Stores post-internship feedback from both students and companies."""
    __tablename__ = 'internship_feedback'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, nullable=False)
    internship_id = db.Column(db.Integer, nullable=False)
    organization_id = db.Column(db.Integer, nullable=False)

    # Student feedback (1-5 scale)
    student_satisfaction = db.Column(db.Integer)
    student_learning = db.Column(db.Integer)
    student_work_environment = db.Column(db.Integer)
    student_mentor_quality = db.Column(db.Integer)
    student_skill_match = db.Column(db.Integer)
    student_would_recommend = db.Column(db.Boolean)
    student_comments = db.Column(db.Text)

    # Company feedback (1-5 scale)
    company_performance = db.Column(db.Integer)
    company_skill_level = db.Column(db.Integer)
    company_professionalism = db.Column(db.Integer)
    company_learning_ability = db.Column(db.Integer)
    company_would_hire = db.Column(db.Boolean)
    company_would_recommend = db.Column(db.Boolean)
    company_comments = db.Column(db.Text)

    # Match quality metadata
    original_match_score = db.Column(db.Float)
    actual_success_score = db.Column(db.Float)

    # Timestamps
    internship_start_date = db.Column(db.Date)
    internship_end_date = db.Column(db.Date)
    student_feedback_date = db.Column(db.DateTime)
    company_feedback_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def compute_success_score(self):
        """Compute overall success score from both student and company feedback."""
        student_score = 0
        company_score = 0

        if all([self.student_satisfaction, self.student_learning,
                self.student_work_environment, self.student_skill_match]):
            student_avg = (self.student_satisfaction + self.student_learning +
                          self.student_work_environment + self.student_skill_match) / 4
            student_score = (student_avg / 5) * 40
            if self.student_would_recommend:
                student_score += 10

        if all([self.company_performance, self.company_skill_level,
                self.company_professionalism, self.company_learning_ability]):
            company_avg = (self.company_performance + self.company_skill_level +
                          self.company_professionalism + self.company_learning_ability) / 4
            company_score = (company_avg / 5) * 50
            if self.company_would_hire:
                company_score += 10

        return student_score + company_score


class ResearchPaper(db.Model):
    """Stores student research papers and publications."""
    __tablename__ = 'research_paper'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, index=True, nullable=False)

    title = db.Column(db.String(500), nullable=False)
    authors = db.Column(db.Text)
    publication_venue = db.Column(db.String(300))
    publication_date = db.Column(db.Date)
    doi = db.Column(db.String(200))

    abstract = db.Column(db.Text)
    keywords = db.Column(db.Text)
    domain = db.Column(db.String(200))

    paper_url = db.Column(db.String(500))
    paper_file_path = db.Column(db.String(400))

    citation_count = db.Column(db.Integer, default=0)
    is_verified = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class MatchingModelMetrics(db.Model):
    """Stores ML model performance metrics over time."""
    __tablename__ = 'matching_model_metrics'

    id = db.Column(db.Integer, primary_key=True)
    model_version = db.Column(db.String(50), nullable=False)

    accuracy = db.Column(db.Float)
    precision = db.Column(db.Float)
    recall = db.Column(db.Float)
    f1_score = db.Column(db.Float)
    mean_absolute_error = db.Column(db.Float)

    training_samples = db.Column(db.Integer)
    features_count = db.Column(db.Integer)

    hyperparameters = db.Column(db.Text)
    feature_importance = db.Column(db.Text)

    trained_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text)


def migrate_database():
    """Create new tables in the database."""
    with app.app_context():
        print("Creating new tables for ML-enhanced matching system...")

        # Create tables
        db.create_all()

        print("✓ Created table: internship_feedback")
        print("✓ Created table: research_paper")
        print("✓ Created table: matching_model_metrics")

        print("\nDatabase migration completed successfully!")
        print("\nNext steps:")
        print("1. Collect feedback from students and companies after internships")
        print("2. Students can add their research papers")
        print("3. Once you have at least 10 complete feedbacks, train the ML model")
        print("4. The model will automatically improve recommendations over time")


if __name__ == '__main__':
    migrate_database()
