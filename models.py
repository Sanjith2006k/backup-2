from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class InternshipFeedback(db.Model):
    """
    Stores post-internship feedback from both students and companies.
    This data is used to train the ML model for better future recommendations.
    """
    __tablename__ = 'internship_feedback'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student_profile.id'), nullable=False)
    internship_id = db.Column(db.Integer, db.ForeignKey('internship.id'), nullable=False)
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'), nullable=False)

    # Student feedback (1-5 scale)
    student_satisfaction = db.Column(db.Integer)  # Overall satisfaction
    student_learning = db.Column(db.Integer)  # Learning experience
    student_work_environment = db.Column(db.Integer)  # Work environment
    student_mentor_quality = db.Column(db.Integer)  # Mentor quality
    student_skill_match = db.Column(db.Integer)  # How well skills matched
    student_would_recommend = db.Column(db.Boolean)  # Would recommend to others
    student_comments = db.Column(db.Text)

    # Company feedback (1-5 scale)
    company_performance = db.Column(db.Integer)  # Student performance
    company_skill_level = db.Column(db.Integer)  # Actual skill level
    company_professionalism = db.Column(db.Integer)  # Professionalism
    company_learning_ability = db.Column(db.Integer)  # Learning ability
    company_would_hire = db.Column(db.Boolean)  # Would hire full-time
    company_would_recommend = db.Column(db.Boolean)  # Would recommend to other companies
    company_comments = db.Column(db.Text)

    # Match quality metadata
    original_match_score = db.Column(db.Float)  # Original ML match score
    actual_success_score = db.Column(db.Float)  # Computed from feedbacks (for training)

    # Timestamps
    internship_start_date = db.Column(db.Date)
    internship_end_date = db.Column(db.Date)
    student_feedback_date = db.Column(db.DateTime)
    company_feedback_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def compute_success_score(self):
        """
        Compute overall success score from both student and company feedback.
        Returns a score from 0-100.
        """
        student_score = 0
        company_score = 0

        # Student feedback component (40% weight)
        if all([self.student_satisfaction, self.student_learning,
                self.student_work_environment, self.student_skill_match]):
            student_avg = (self.student_satisfaction + self.student_learning +
                          self.student_work_environment + self.student_skill_match) / 4
            student_score = (student_avg / 5) * 40
            if self.student_would_recommend:
                student_score += 10  # Bonus for recommendation

        # Company feedback component (50% weight)
        if all([self.company_performance, self.company_skill_level,
                self.company_professionalism, self.company_learning_ability]):
            company_avg = (self.company_performance + self.company_skill_level +
                          self.company_professionalism + self.company_learning_ability) / 4
            company_score = (company_avg / 5) * 50
            if self.company_would_hire:
                company_score += 10  # Bonus for hire intent

        return student_score + company_score


class ResearchPaper(db.Model):
    """
    Stores student research papers and publications.
    Used to boost matching score for domain-relevant internships.
    """
    __tablename__ = 'research_paper'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, index=True, nullable=False)

    # Paper details
    title = db.Column(db.String(500), nullable=False)
    authors = db.Column(db.Text)  # Comma-separated list
    publication_venue = db.Column(db.String(300))  # Conference/Journal name
    publication_date = db.Column(db.Date)
    doi = db.Column(db.String(200))

    # Content and domain
    abstract = db.Column(db.Text)
    keywords = db.Column(db.Text)  # Comma-separated keywords
    domain = db.Column(db.String(200))  # e.g., "Machine Learning", "Web Development"

    # Links and files
    paper_url = db.Column(db.String(500))  # Link to published paper
    paper_file_path = db.Column(db.String(400))  # Uploaded PDF

    # Citations and impact
    citation_count = db.Column(db.Integer, default=0)

    # Verification
    is_verified = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class MatchingModelMetrics(db.Model):
    """
    Stores ML model performance metrics over time.
    Used for monitoring and model versioning.
    """
    __tablename__ = 'matching_model_metrics'

    id = db.Column(db.Integer, primary_key=True)
    model_version = db.Column(db.String(50), nullable=False)

    # Performance metrics
    accuracy = db.Column(db.Float)
    precision = db.Column(db.Float)
    recall = db.Column(db.Float)
    f1_score = db.Column(db.Float)
    mean_absolute_error = db.Column(db.Float)

    # Training data stats
    training_samples = db.Column(db.Integer)
    features_count = db.Column(db.Integer)

    # Model metadata
    hyperparameters = db.Column(db.Text)  # JSON string
    feature_importance = db.Column(db.Text)  # JSON string

    trained_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text)
