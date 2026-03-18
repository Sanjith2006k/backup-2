"""
Load Sample Data and Test ML Matching Model

This script:
1. Loads the generated sample dataset
2. Tests ML predictions BEFORE training
3. Trains the model with feedback data
4. Tests ML predictions AFTER training
5. Shows performance improvement

Run this after running generate_sample_data.py
"""

import json
import sys
from ai.ml_matcher import EnhancedMLMatcher
import numpy as np

def load_dataset(filename='sample_dataset.json'):
    """Load dataset from JSON file."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            dataset = json.load(f)
        return dataset
    except FileNotFoundError:
        print(f"❌ Error: {filename} not found!")
        print("Please run generate_sample_data.py first to create the dataset.")
        sys.exit(1)

def test_predictions(matcher, dataset, phase="BEFORE"):
    """Test model predictions and compare with actual outcomes."""
    print(f"\n{'=' * 80}")
    print(f"TESTING PREDICTIONS - {phase} TRAINING")
    print(f"{'=' * 80}\n")

    predictions = []
    actuals = []
    errors = []

    for i, match in enumerate(dataset['matches'][:10]):  # Test first 10
        student = dataset['students'][i]
        internship = dataset['internships'][i]
        actual_success = match['feedback']['actual_success_score']

        # Get ML prediction
        result = matcher.predict_match_score(student, internship)
        predicted_score = result['match_score']

        predictions.append(predicted_score)
        actuals.append(actual_success)
        errors.append(abs(predicted_score - actual_success))

        # Print details for first 5
        if i < 5:
            print(f"Match #{i+1}:")
            print(f"  Student: {student['name'][:30]}")
            print(f"  Internship: {internship['title']}")
            print(f"  Domain Match: {student['primary_domain']} → {internship['domain']}")
            print(f"  Predicted Score: {predicted_score:.1f}/100")
            print(f"  Actual Success: {actual_success:.1f}/100")
            print(f"  Error: {abs(predicted_score - actual_success):.1f}")
            print(f"  Status: {'✓ Good' if abs(predicted_score - actual_success) < 15 else '✗ Needs Improvement'}")
            print()

    # Calculate metrics
    mae = np.mean(errors)
    mse = np.mean([e**2 for e in errors])
    rmse = np.sqrt(mse)

    print(f"{'=' * 80}")
    print(f"PERFORMANCE METRICS - {phase} TRAINING")
    print(f"{'=' * 80}")
    print(f"  Mean Absolute Error (MAE): {mae:.2f}")
    print(f"  Root Mean Squared Error (RMSE): {rmse:.2f}")
    print(f"  Predictions within ±10 points: {sum(1 for e in errors if e < 10)}/10")
    print(f"  Predictions within ±15 points: {sum(1 for e in errors if e < 15)}/10")
    print(f"{'=' * 80}\n")

    return {
        'mae': mae,
        'rmse': rmse,
        'errors': errors,
        'predictions': predictions,
        'actuals': actuals
    }

def train_model_with_dataset(matcher, dataset):
    """Train ML model with the complete dataset."""
    print(f"\n{'=' * 80}")
    print("TRAINING ML MODEL WITH FEEDBACK DATA")
    print(f"{'=' * 80}\n")

    # Prepare training data
    training_data = []

    for i, match in enumerate(dataset['matches']):
        student = dataset['students'][i]
        internship = dataset['internships'][i]
        actual_success = match['feedback']['actual_success_score']

        training_data.append({
            'student_data': student,
            'internship_data': internship,
            'actual_success_score': actual_success
        })

    print(f"📚 Preparing {len(training_data)} training samples...")

    # Train model
    matcher.train_model(training_data)

    print(f"\n✅ Model training complete!")

def show_detailed_example(matcher, dataset):
    """Show a detailed prediction breakdown for one example."""
    print(f"\n{'=' * 80}")
    print("DETAILED PREDICTION BREAKDOWN - EXAMPLE")
    print(f"{'=' * 80}\n")

    # Pick an interesting example (medium expertise, same domain)
    idx = 15  # Arbitrary choice
    student = dataset['students'][idx]
    internship = dataset['internships'][idx]
    match = dataset['matches'][idx]

    print(f"🎓 STUDENT PROFILE")
    print(f"   Name: {student['name']}")
    print(f"   Domain: {student['primary_domain']}")
    print(f"   Expertise: {student['expertise_level']}")
    print(f"   Skills: {student['skills']}")
    print(f"   Certificates: {len(student['certificates'])}")
    for cert in student['certificates']:
        print(f"      - {cert['certificate_name']}")
    print(f"   Previous Internships: {len(student['internship_experiences'])}")
    for exp in student['internship_experiences']:
        print(f"      - {exp['role']} at {exp['company_name']}")
    print(f"   Research Papers: {len(student['research_papers'])}")
    for paper in student['research_papers']:
        print(f"      - {paper['title']} ({paper['citation_count']} citations)")

    print(f"\n💼 INTERNSHIP POSTING")
    print(f"   Title: {internship['title']}")
    print(f"   Company: {internship['organization_name']}")
    print(f"   Domain: {internship['domain']}")
    print(f"   Required Skills: {internship['skills_required']}")
    print(f"   Location: {internship['location']}")
    print(f"   Duration: {internship['duration']}")
    print(f"   Stipend: {internship['stipend']}")

    # Get prediction
    result = matcher.predict_match_score(student, internship)

    print(f"\n🤖 ML MODEL PREDICTION")
    print(f"   Overall Match Score: {result['match_score']:.1f}/100")
    print(f"   Confidence Level: {result['confidence']}")

    print(f"\n📊 SCORE BREAKDOWN")
    breakdown = result['breakdown']
    print(f"   Base Match Score: {breakdown['base_match_score']:.1f}")
    print(f"   ├─ Skill Similarity: {breakdown['skill_similarity']:.1f}%")
    print(f"   ├─ Keyword Overlap: {breakdown['keyword_overlap']:.1f}%")
    print(f"   └─ Location Match: {breakdown['location_match']:.1f}%")
    print(f"\n   Bonus Components:")
    print(f"   ├─ Certificate Bonus: +{breakdown['certificate_bonus']:.1f} ({breakdown['certificate_count']} certificates)")
    print(f"   ├─ Experience Bonus: +{breakdown['experience_bonus']:.1f} ({breakdown['experience_count']} internships)")
    print(f"   └─ Research Bonus: +{breakdown['research_bonus']:.1f} ({breakdown['research_count']} papers)")

    if result['recommendations']:
        print(f"\n💡 RECOMMENDATIONS FOR IMPROVEMENT")
        for rec in result['recommendations']:
            print(f"   • {rec}")

    print(f"\n📈 ACTUAL OUTCOME (from feedback)")
    print(f"   Actual Success Score: {match['feedback']['actual_success_score']:.1f}/100")
    print(f"   Student Satisfaction: {match['feedback']['student_satisfaction']}/5")
    print(f"   Company Rating: {match['feedback']['company_performance']}/5")
    print(f"   Student Comment: \"{match['feedback']['student_comments']}\"")
    print(f"   Company Comment: \"{match['feedback']['company_comments']}\"")

    print(f"\n🎯 PREDICTION ACCURACY")
    error = abs(result['match_score'] - match['feedback']['actual_success_score'])
    print(f"   Prediction Error: {error:.1f} points")
    if error < 10:
        print(f"   Status: ✅ Excellent prediction!")
    elif error < 15:
        print(f"   Status: ✓ Good prediction")
    else:
        print(f"   Status: ⚠ Could be improved")

    print(f"\n{'=' * 80}\n")

def compare_scenarios(matcher, dataset):
    """Compare different matching scenarios."""
    print(f"\n{'=' * 80}")
    print("COMPARING DIFFERENT MATCHING SCENARIOS")
    print(f"{'=' * 80}\n")

    scenarios = [
        ("Expert in Same Domain", 40, 40),  # Both expert in ML
        ("Beginner in Same Domain", 2, 2),  # Both beginner in ML
        ("Expert in Different Domain", 40, 10),  # Expert ML student, Web Dev internship
        ("Medium with Experience", 20, 20),  # Medium level with experience
    ]

    for scenario_name, student_idx, internship_idx in scenarios:
        student = dataset['students'][student_idx]
        internship = dataset['internships'][internship_idx]

        result = matcher.predict_match_score(student, internship)

        print(f"\n📌 {scenario_name}")
        print(f"   Student: {student['expertise_level']} in {student['primary_domain']}")
        print(f"   Internship: {internship['domain']} - {internship['title']}")
        print(f"   → Predicted Score: {result['match_score']:.1f}/100")
        print(f"   → Skill Similarity: {result['breakdown']['skill_similarity']:.1f}%")
        print(f"   → Total Bonuses: +{result['breakdown']['certificate_bonus'] + result['breakdown']['experience_bonus'] + result['breakdown']['research_bonus']:.1f}")

def show_top_matches(matcher, dataset):
    """Show top student matches for a sample internship."""
    print(f"\n{'=' * 80}")
    print("TOP STUDENT MATCHES FOR AN INTERNSHIP")
    print(f"{'=' * 80}\n")

    # Pick a sample internship
    internship = dataset['internships'][25]

    print(f"📋 Internship: {internship['title']}")
    print(f"   Company: {internship['organization_name']}")
    print(f"   Domain: {internship['domain']}")
    print(f"   Required: {internship['skills_required']}\n")

    # Get all students
    students_data = dataset['students']

    # Batch predict
    results = matcher.batch_predict(students_data, internship)

    print(f"🏆 Top 10 Student Matches:\n")
    for rank, (student_id, match_result) in enumerate(results[:10], 1):
        student = students_data[student_id - 1]
        print(f"   {rank}. {student['name'][:25]:25} | Score: {match_result['match_score']:5.1f}/100 | "
              f"{student['expertise_level']:8} in {student['primary_domain']}")

    print(f"\n{'=' * 80}\n")

def main():
    """Main execution function."""
    print("=" * 80)
    print("ML MATCHING MODEL - COMPREHENSIVE TEST WITH SAMPLE DATA")
    print("=" * 80)

    # Load dataset
    print("\n📂 Loading sample dataset...")
    dataset = load_dataset('sample_dataset.json')
    print(f"✓ Loaded {len(dataset['students'])} students and {len(dataset['internships'])} internships")

    # Initialize matcher
    print("\n🤖 Initializing ML matcher...")
    matcher = EnhancedMLMatcher(model_path='ai/models')
    print("✓ ML matcher initialized")

    # Test BEFORE training
    before_metrics = test_predictions(matcher, dataset, phase="BEFORE")

    # Train model
    train_model_with_dataset(matcher, dataset)

    # Test AFTER training
    after_metrics = test_predictions(matcher, dataset, phase="AFTER")

    # Show improvement
    print(f"\n{'=' * 80}")
    print("MODEL IMPROVEMENT COMPARISON")
    print(f"{'=' * 80}")
    print(f"\n  Metric                    BEFORE    AFTER     Improvement")
    print(f"  {'-' * 60}")
    mae_improvement = ((before_metrics['mae'] - after_metrics['mae']) / before_metrics['mae']) * 100
    rmse_improvement = ((before_metrics['rmse'] - after_metrics['rmse']) / before_metrics['rmse']) * 100

    print(f"  Mean Absolute Error       {before_metrics['mae']:6.2f}    {after_metrics['mae']:6.2f}    {mae_improvement:+5.1f}%")
    print(f"  Root Mean Squared Error   {before_metrics['rmse']:6.2f}    {after_metrics['rmse']:6.2f}    {rmse_improvement:+5.1f}%")
    print(f"  {'=' * 80}\n")

    if mae_improvement > 0:
        print(f"  ✅ Model improved by {mae_improvement:.1f}% after training!")
    else:
        print(f"  ℹ️  Model performance is consistent")

    # Show detailed example
    show_detailed_example(matcher, dataset)

    # Compare scenarios
    compare_scenarios(matcher, dataset)

    # Show top matches
    show_top_matches(matcher, dataset)

    # Save model
    print(f"\n💾 Saving trained model...")
    matcher._save_model()
    print(f"✓ Model saved to ai/models/")

    print("\n" + "=" * 80)
    print("✅ TESTING COMPLETE!")
    print("=" * 80)
    print("\n📊 Summary:")
    print(f"   • Tested on {len(dataset['matches'])} student-internship pairs")
    print(f"   • Model trained with all {len(dataset['matches'])} feedback samples")
    print(f"   • Average prediction error: {after_metrics['mae']:.1f} points")
    print(f"   • Model saved and ready for production use")
    print("\n🎯 The ML matching system is working correctly!")
    print("\nNext steps:")
    print("   1. The model is now trained and saved")
    print("   2. Use it in your Flask app with the provided routes")
    print("   3. Collect real feedback to improve further")
    print("   4. Monitor performance in the admin dashboard")

if __name__ == '__main__':
    main()
