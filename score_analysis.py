"""
Feedback Score Comparison and Analysis Tool
Analyzes the relationship between original ML match scores and actual success scores.
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from models import db, InternshipFeedback
from app import app

def create_score_comparison_report():
    """Generate detailed score comparison analysis for ML improvement."""

    with app.app_context():
        feedbacks = InternshipFeedback.query.all()

        if not feedbacks:
            print("❌ No feedback data found. Run generate_feedback_dataset.py first.")
            return

        # Convert to DataFrame for analysis
        data = []
        for feedback in feedbacks:
            if feedback.original_match_score and feedback.actual_success_score:
                data.append({
                    'id': feedback.id,
                    'original_score': feedback.original_match_score,
                    'actual_score': feedback.actual_success_score,
                    'difference': feedback.actual_success_score - feedback.original_match_score,
                    'student_satisfaction': feedback.student_satisfaction,
                    'student_learning': feedback.student_learning,
                    'student_skill_match': feedback.student_skill_match,
                    'company_performance': feedback.company_performance,
                    'company_skill_level': feedback.company_skill_level,
                    'student_would_recommend': feedback.student_would_recommend,
                    'company_would_hire': feedback.company_would_hire
                })

        df = pd.DataFrame(data)

        if df.empty:
            print("❌ No complete feedback records found.")
            return

        print("📊 COMPREHENSIVE SCORE COMPARISON ANALYSIS")
        print("=" * 60)

        # 1. Basic Statistics
        print(f"\n📈 Basic Statistics ({len(df)} records):")
        print(f"   Original Match Score:  {df['original_score'].mean():.1f}% ± {df['original_score'].std():.1f}")
        print(f"   Actual Success Score:  {df['actual_score'].mean():.1f}% ± {df['actual_score'].std():.1f}")
        print(f"   Average Difference:    {df['difference'].mean():.1f}% ± {df['difference'].std():.1f}")

        # 2. Correlation Analysis
        correlation = df['original_score'].corr(df['actual_score'])
        print(f"\n🔗 Correlation Analysis:")
        print(f"   Original vs Actual Score Correlation: {correlation:.3f}")

        if correlation > 0.7:
            print("   ✅ Strong positive correlation - ML model performs well")
        elif correlation > 0.4:
            print("   ⚠️  Moderate correlation - room for improvement")
        else:
            print("   ❌ Weak correlation - model needs significant improvement")

        # 3. Accuracy Analysis
        df['accurate'] = abs(df['difference']) <= 15  # Within 15% considered accurate
        accuracy_rate = df['accurate'].mean() * 100

        print(f"\n🎯 Accuracy Analysis (±15% tolerance):")
        print(f"   Accurate Predictions:    {df['accurate'].sum()}/{len(df)} ({accuracy_rate:.1f}%)")
        print(f"   Mean Absolute Error:     {abs(df['difference']).mean():.1f}%")

        # 4. Error Categories
        print(f"\n📊 Error Distribution:")
        overestimated = df[df['difference'] < -15]
        underestimated = df[df['difference'] > 15]
        accurate = df[abs(df['difference']) <= 15]

        print(f"   Overestimated (worse than predicted): {len(overestimated)} ({len(overestimated)/len(df)*100:.1f}%)")
        print(f"   Underestimated (better than predicted): {len(underestimated)} ({len(underestimated)/len(df)*100:.1f}%)")
        print(f"   Accurate predictions: {len(accurate)} ({len(accurate)/len(df)*100:.1f}%)")

        # 5. Pattern Analysis
        print(f"\n🔍 Pattern Analysis:")

        # High original, low actual (model overconfidence)
        overconfident = df[(df['original_score'] > 80) & (df['actual_score'] < 60)]
        print(f"   Overconfident matches (high orig, low actual): {len(overconfident)}")

        # Low original, high actual (hidden gems)
        hidden_gems = df[(df['original_score'] < 60) & (df['actual_score'] > 80)]
        print(f"   Hidden gems (low orig, high actual): {len(hidden_gems)}")

        # High satisfaction despite low skill match
        satisfaction_paradox = df[(df['student_satisfaction'] >= 4) & (df['student_skill_match'] <= 2)]
        print(f"   Satisfaction paradox (happy despite skill mismatch): {len(satisfaction_paradox)}")

        # 6. Recommendations for ML Improvement
        print(f"\n💡 ML Model Improvement Recommendations:")

        if len(overconfident) > len(df) * 0.1:  # More than 10% overconfident
            print("   ⚠️  Model tends to overestimate - add penalty for skill mismatches")

        if len(hidden_gems) > len(df) * 0.1:  # More than 10% hidden gems
            print("   📈 Model misses good candidates - consider soft skills and learning ability")

        if abs(df['difference']).mean() > 20:
            print("   🔧 High error rate - retrain with more diverse features")

        if correlation < 0.5:
            print("   🔄 Poor correlation - revise matching algorithm fundamentals")

        # 7. Best and Worst Predictions
        print(f"\n🏆 Best Predictions (smallest error):")
        best_predictions = df.nsmallest(3, abs(df['difference']))
        for _, row in best_predictions.iterrows():
            print(f"   ID {row['id']}: {row['original_score']:.1f}% → {row['actual_score']:.1f}% (diff: {row['difference']:+.1f}%)")

        print(f"\n💔 Worst Predictions (largest error):")
        worst_predictions = df.nlargest(3, abs(df['difference']))
        for _, row in worst_predictions.iterrows():
            print(f"   ID {row['id']}: {row['original_score']:.1f}% → {row['actual_score']:.1f}% (diff: {row['difference']:+.1f}%)")

        # 8. Success Factors Analysis
        print(f"\n✨ Success Factors Analysis:")
        successful_matches = df[df['actual_score'] >= 80]
        if len(successful_matches) > 0:
            print(f"   Successful matches ({len(successful_matches)} total):")
            print(f"   • Average student satisfaction: {successful_matches['student_satisfaction'].mean():.1f}/5")
            print(f"   • Average skill match rating: {successful_matches['student_skill_match'].mean():.1f}/5")
            print(f"   • Would recommend rate: {successful_matches['student_would_recommend'].mean()*100:.1f}%")
            print(f"   • Company would hire rate: {successful_matches['company_would_hire'].mean()*100:.1f}%")

        return df

def export_analysis_csv():
    """Export analysis data to CSV for further analysis."""
    with app.app_context():
        feedbacks = InternshipFeedback.query.all()

        data = []
        for feedback in feedbacks:
            data.append({
                'feedback_id': feedback.id,
                'student_id': feedback.student_id,
                'internship_id': feedback.internship_id,
                'organization_id': feedback.organization_id,
                'original_match_score': feedback.original_match_score,
                'actual_success_score': feedback.actual_success_score,
                'score_difference': feedback.actual_success_score - feedback.original_match_score if feedback.original_match_score and feedback.actual_success_score else None,
                'student_satisfaction': feedback.student_satisfaction,
                'student_learning': feedback.student_learning,
                'student_work_environment': feedback.student_work_environment,
                'student_mentor_quality': feedback.student_mentor_quality,
                'student_skill_match': feedback.student_skill_match,
                'student_would_recommend': feedback.student_would_recommend,
                'company_performance': feedback.company_performance,
                'company_skill_level': feedback.company_skill_level,
                'company_professionalism': feedback.company_professionalism,
                'company_learning_ability': feedback.company_learning_ability,
                'company_would_hire': feedback.company_would_hire,
                'company_would_recommend': feedback.company_would_recommend,
                'internship_start_date': feedback.internship_start_date,
                'internship_end_date': feedback.internship_end_date,
                'student_feedback_date': feedback.student_feedback_date,
                'company_feedback_date': feedback.company_feedback_date
            })

        df = pd.DataFrame(data)
        filename = 'feedback_analysis_data.csv'
        df.to_csv(filename, index=False)
        print(f"📄 Exported analysis data to {filename}")
        return filename

if __name__ == "__main__":
    print("🔍 Running score comparison analysis...")
    df = create_score_comparison_report()

    if df is not None:
        print("\n📄 Exporting data for further analysis...")
        export_analysis_csv()

        print(f"\n🎓 Key Insights Summary:")
        correlation = df['original_score'].corr(df['actual_score'])
        accuracy = (abs(df['difference']) <= 15).mean() * 100

        print(f"   • Model correlation: {correlation:.2f} ({'Good' if correlation > 0.7 else 'Needs improvement'})")
        print(f"   • Prediction accuracy: {accuracy:.1f}% ({'Good' if accuracy > 70 else 'Needs improvement'})")
        print(f"   • Average error: {abs(df['difference']).mean():.1f}%")

        if correlation < 0.5 or accuracy < 60:
            print(f"\n⚠️  RECOMMENDATION: Model needs retraining with improved features")
        else:
            print(f"\n✅ Model performance is acceptable but can be optimized")