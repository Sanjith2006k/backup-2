"""
Generate sample feedback dataset for score comparison and ML training.
This script creates realistic internship feedback data covering various scenarios.
"""

import random
from datetime import datetime, date, timedelta
from models import db, InternshipFeedback
from app import app

def generate_feedback_dataset():
    """Generate comprehensive feedback dataset with various scenarios."""

    with app.app_context():
        # Clear existing feedback data (optional - comment out if you want to keep existing data)
        # InternshipFeedback.query.delete()

        feedback_samples = []

        # Scenario 1: Excellent Matches (High original score, High feedback)
        for i in range(15):
            feedback = InternshipFeedback(
                student_id=random.randint(1, 50),
                internship_id=random.randint(1, 30),
                organization_id=random.randint(1, 20),

                # High student feedback (4-5 range)
                student_satisfaction=random.randint(4, 5),
                student_learning=random.randint(4, 5),
                student_work_environment=random.randint(4, 5),
                student_mentor_quality=random.randint(4, 5),
                student_skill_match=random.randint(4, 5),
                student_would_recommend=True,
                student_comments="Excellent internship experience! Great learning opportunities and supportive team.",

                # High company feedback (4-5 range)
                company_performance=random.randint(4, 5),
                company_skill_level=random.randint(4, 5),
                company_professionalism=random.randint(4, 5),
                company_learning_ability=random.randint(4, 5),
                company_would_hire=True,
                company_would_recommend=True,
                company_comments="Outstanding intern! Would definitely hire full-time.",

                # High original match score (85-95%)
                original_match_score=random.uniform(85, 95),

                # Dates
                internship_start_date=date.today() - timedelta(days=random.randint(60, 180)),
                internship_end_date=date.today() - timedelta(days=random.randint(1, 30)),
                student_feedback_date=datetime.now() - timedelta(days=random.randint(1, 15)),
                company_feedback_date=datetime.now() - timedelta(days=random.randint(1, 15))
            )
            feedback_samples.append(feedback)

        # Scenario 2: Poor Matches (High original score, Low feedback)
        for i in range(10):
            feedback = InternshipFeedback(
                student_id=random.randint(1, 50),
                internship_id=random.randint(1, 30),
                organization_id=random.randint(1, 20),

                # Low student feedback (1-2 range)
                student_satisfaction=random.randint(1, 2),
                student_learning=random.randint(1, 3),
                student_work_environment=random.randint(1, 2),
                student_mentor_quality=random.randint(1, 2),
                student_skill_match=random.randint(1, 2),
                student_would_recommend=False,
                student_comments="Not what I expected. Poor mentorship and limited learning opportunities.",

                # Low company feedback (1-3 range)
                company_performance=random.randint(1, 3),
                company_skill_level=random.randint(1, 3),
                company_professionalism=random.randint(2, 4),
                company_learning_ability=random.randint(2, 3),
                company_would_hire=False,
                company_would_recommend=False,
                company_comments="Skills didn't match expectations. Struggled with basic tasks.",

                # High original match score but poor outcome (80-90%)
                original_match_score=random.uniform(80, 90),

                # Dates
                internship_start_date=date.today() - timedelta(days=random.randint(60, 180)),
                internship_end_date=date.today() - timedelta(days=random.randint(1, 30)),
                student_feedback_date=datetime.now() - timedelta(days=random.randint(1, 15)),
                company_feedback_date=datetime.now() - timedelta(days=random.randint(1, 15))
            )
            feedback_samples.append(feedback)

        # Scenario 3: Surprising Good Matches (Low original score, High feedback)
        for i in range(12):
            feedback = InternshipFeedback(
                student_id=random.randint(1, 50),
                internship_id=random.randint(1, 30),
                organization_id=random.randint(1, 20),

                # High student feedback despite low original match
                student_satisfaction=random.randint(4, 5),
                student_learning=random.randint(4, 5),
                student_work_environment=random.randint(3, 5),
                student_mentor_quality=random.randint(4, 5),
                student_skill_match=random.randint(3, 4),  # Slightly lower as expected
                student_would_recommend=True,
                student_comments="Great experience! Learned skills I didn't know I needed.",

                # High company feedback
                company_performance=random.randint(4, 5),
                company_skill_level=random.randint(3, 4),  # Skills grew during internship
                company_professionalism=random.randint(4, 5),
                company_learning_ability=random.randint(5, 5),  # Excellent learner
                company_would_hire=True,
                company_would_recommend=True,
                company_comments="Amazing adaptability! Quick learner who exceeded expectations.",

                # Low original match score but great outcome (45-65%)
                original_match_score=random.uniform(45, 65),

                # Dates
                internship_start_date=date.today() - timedelta(days=random.randint(60, 180)),
                internship_end_date=date.today() - timedelta(days=random.randint(1, 30)),
                student_feedback_date=datetime.now() - timedelta(days=random.randint(1, 15)),
                company_feedback_date=datetime.now() - timedelta(days=random.randint(1, 15))
            )
            feedback_samples.append(feedback)

        # Scenario 4: Expected Poor Matches (Low original score, Low feedback)
        for i in range(8):
            feedback = InternshipFeedback(
                student_id=random.randint(1, 50),
                internship_id=random.randint(1, 30),
                organization_id=random.randint(1, 20),

                # Low student feedback
                student_satisfaction=random.randint(2, 3),
                student_learning=random.randint(2, 3),
                student_work_environment=random.randint(2, 4),
                student_mentor_quality=random.randint(2, 3),
                student_skill_match=random.randint(1, 2),
                student_would_recommend=False,
                student_comments="Skills mismatch made it difficult. Not a good fit.",

                # Low company feedback
                company_performance=random.randint(2, 3),
                company_skill_level=random.randint(1, 2),
                company_professionalism=random.randint(3, 4),
                company_learning_ability=random.randint(2, 3),
                company_would_hire=False,
                company_would_recommend=False,
                company_comments="Significant skill gap. Would need extensive training.",

                # Low original match score and poor outcome (30-50%)
                original_match_score=random.uniform(30, 50),

                # Dates
                internship_start_date=date.today() - timedelta(days=random.randint(60, 180)),
                internship_end_date=date.today() - timedelta(days=random.randint(1, 30)),
                student_feedback_date=datetime.now() - timedelta(days=random.randint(1, 15)),
                company_feedback_date=datetime.now() - timedelta(days=random.randint(1, 15))
            )
            feedback_samples.append(feedback)

        # Scenario 5: Mixed/Average Matches (Medium scores across board)
        for i in range(20):
            feedback = InternshipFeedback(
                student_id=random.randint(1, 50),
                internship_id=random.randint(1, 30),
                organization_id=random.randint(1, 20),

                # Average student feedback (3-4 range)
                student_satisfaction=random.randint(3, 4),
                student_learning=random.randint(3, 4),
                student_work_environment=random.randint(3, 4),
                student_mentor_quality=random.randint(3, 4),
                student_skill_match=random.randint(3, 4),
                student_would_recommend=random.choice([True, False]),
                student_comments="Decent experience. Some good learning opportunities.",

                # Average company feedback
                company_performance=random.randint(3, 4),
                company_skill_level=random.randint(3, 4),
                company_professionalism=random.randint(3, 4),
                company_learning_ability=random.randint(3, 4),
                company_would_hire=random.choice([True, False]),
                company_would_recommend=random.choice([True, False]),
                company_comments="Solid performance. Met most expectations.",

                # Medium original match score (65-80%)
                original_match_score=random.uniform(65, 80),

                # Dates
                internship_start_date=date.today() - timedelta(days=random.randint(60, 180)),
                internship_end_date=date.today() - timedelta(days=random.randint(1, 30)),
                student_feedback_date=datetime.now() - timedelta(days=random.randint(1, 15)),
                company_feedback_date=datetime.now() - timedelta(days=random.randint(1, 15))
            )
            feedback_samples.append(feedback)

        # Scenario 6: One-sided feedback (only student OR company provided feedback)
        for i in range(10):
            feedback = InternshipFeedback(
                student_id=random.randint(1, 50),
                internship_id=random.randint(1, 30),
                organization_id=random.randint(1, 20),
                original_match_score=random.uniform(60, 85),
                internship_start_date=date.today() - timedelta(days=random.randint(60, 180)),
                internship_end_date=date.today() - timedelta(days=random.randint(1, 30))
            )

            if i % 2 == 0:  # Student feedback only
                feedback.student_satisfaction = random.randint(2, 5)
                feedback.student_learning = random.randint(2, 5)
                feedback.student_work_environment = random.randint(2, 5)
                feedback.student_mentor_quality = random.randint(2, 5)
                feedback.student_skill_match = random.randint(2, 5)
                feedback.student_would_recommend = random.choice([True, False])
                feedback.student_comments = "Student provided feedback but company didn't respond."
                feedback.student_feedback_date = datetime.now() - timedelta(days=random.randint(1, 15))
            else:  # Company feedback only
                feedback.company_performance = random.randint(2, 5)
                feedback.company_skill_level = random.randint(2, 5)
                feedback.company_professionalism = random.randint(2, 5)
                feedback.company_learning_ability = random.randint(2, 5)
                feedback.company_would_hire = random.choice([True, False])
                feedback.company_would_recommend = random.choice([True, False])
                feedback.company_comments = "Company provided feedback but student didn't respond."
                feedback.company_feedback_date = datetime.now() - timedelta(days=random.randint(1, 15))

            feedback_samples.append(feedback)

        # Add all samples to database
        for feedback in feedback_samples:
            # Compute actual success score
            feedback.actual_success_score = feedback.compute_success_score()
            db.session.add(feedback)

        # Commit all changes
        db.session.commit()

        print(f"✅ Generated {len(feedback_samples)} feedback samples")
        print(f"📊 Dataset breakdown:")
        print(f"   • Excellent matches: 15 samples")
        print(f"   • Poor matches (high original score): 10 samples")
        print(f"   • Surprising good matches: 12 samples")
        print(f"   • Expected poor matches: 8 samples")
        print(f"   • Mixed/average matches: 20 samples")
        print(f"   • One-sided feedback: 10 samples")

        return len(feedback_samples)

def analyze_feedback_scores():
    """Analyze the generated feedback data to show score comparisons."""

    with app.app_context():
        feedbacks = InternshipFeedback.query.all()

        if not feedbacks:
            print("❌ No feedback data found. Run generate_feedback_dataset() first.")
            return

        print("\n📈 FEEDBACK SCORE ANALYSIS")
        print("=" * 50)

        # Calculate statistics
        original_scores = [f.original_match_score for f in feedbacks if f.original_match_score]
        success_scores = [f.actual_success_score for f in feedbacks if f.actual_success_score]

        print(f"\n📊 Overall Statistics:")
        print(f"   • Total feedback records: {len(feedbacks)}")
        print(f"   • Average original match score: {sum(original_scores)/len(original_scores):.1f}%")
        print(f"   • Average actual success score: {sum(success_scores)/len(success_scores):.1f}%")

        # Analyze accuracy of original matching
        accurate_predictions = 0
        inaccurate_predictions = 0

        for feedback in feedbacks:
            if feedback.original_match_score and feedback.actual_success_score:
                diff = abs(feedback.original_match_score - feedback.actual_success_score)
                if diff <= 15:  # Within 15% considered accurate
                    accurate_predictions += 1
                else:
                    inaccurate_predictions += 1

        accuracy_rate = accurate_predictions / (accurate_predictions + inaccurate_predictions) * 100

        print(f"\n🎯 ML Model Accuracy Analysis:")
        print(f"   • Accurate predictions (±15%): {accurate_predictions}")
        print(f"   • Inaccurate predictions: {inaccurate_predictions}")
        print(f"   • Overall accuracy rate: {accuracy_rate:.1f}%")

        # Show some example comparisons
        print(f"\n🔍 Sample Score Comparisons:")
        print("   Original → Actual | Difference | Notes")
        print("   " + "-" * 45)

        sample_feedbacks = random.sample(feedbacks, min(10, len(feedbacks)))
        for feedback in sample_feedbacks:
            if feedback.original_match_score and feedback.actual_success_score:
                diff = feedback.actual_success_score - feedback.original_match_score
                diff_str = f"+{diff:.1f}" if diff > 0 else f"{diff:.1f}"

                if abs(diff) <= 10:
                    note = "✅ Good prediction"
                elif diff > 10:
                    note = "📈 Better than expected"
                elif diff < -10:
                    note = "📉 Worse than expected"
                else:
                    note = "⚠️ Significant difference"

                print(f"   {feedback.original_match_score:5.1f}% → {feedback.actual_success_score:5.1f}% | {diff_str:8s} | {note}")

        # Show best and worst matches
        best_match = max(feedbacks, key=lambda f: f.actual_success_score or 0)
        worst_match = min(feedbacks, key=lambda f: f.actual_success_score or 100)

        print(f"\n🏆 Best Match (ID {best_match.id}):")
        print(f"   • Original score: {best_match.original_match_score:.1f}%")
        print(f"   • Actual score: {best_match.actual_success_score:.1f}%")
        print(f"   • Student satisfaction: {best_match.student_satisfaction}/5")
        print(f"   • Company performance: {best_match.company_performance}/5")

        print(f"\n💔 Worst Match (ID {worst_match.id}):")
        print(f"   • Original score: {worst_match.original_match_score:.1f}%")
        print(f"   • Actual score: {worst_match.actual_success_score:.1f}%")
        print(f"   • Student satisfaction: {worst_match.student_satisfaction}/5")
        print(f"   • Company performance: {worst_match.company_performance}/5")

if __name__ == "__main__":
    print("🚀 Generating feedback dataset...")
    generate_feedback_dataset()

    print("\n" + "=" * 60)
    analyze_feedback_scores()

    print(f"\n💡 Next steps:")
    print("   • Use this data to train your ML model")
    print("   • Compare original vs actual scores to improve matching")
    print("   • Identify patterns in successful vs unsuccessful matches")
    print("   • Update matching algorithm based on feedback trends")