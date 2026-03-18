"""
Sample Feedback Dataset for Score Comparison
This file contains realistic internship feedback data to analyze ML model performance.
"""

import json
from datetime import datetime, date

# Sample feedback dataset
feedback_dataset = [
    # Scenario 1: Excellent Matches (High original score, High actual score)
    {
        "id": 1,
        "student_id": 15,
        "internship_id": 3,
        "organization_id": 2,
        "original_match_score": 88.5,
        "student_feedback": {
            "satisfaction": 5,
            "learning": 5,
            "work_environment": 4,
            "mentor_quality": 5,
            "skill_match": 4,
            "would_recommend": True,
            "comments": "Excellent internship! Great mentorship and real-world projects."
        },
        "company_feedback": {
            "performance": 5,
            "skill_level": 4,
            "professionalism": 5,
            "learning_ability": 5,
            "would_hire": True,
            "would_recommend": True,
            "comments": "Outstanding intern! Would definitely hire full-time."
        },
        "actual_success_score": 90.0,
        "score_difference": 1.5,
        "category": "Excellent Match"
    },
    {
        "id": 2,
        "student_id": 8,
        "internship_id": 7,
        "organization_id": 4,
        "original_match_score": 91.2,
        "student_feedback": {
            "satisfaction": 4,
            "learning": 5,
            "work_environment": 5,
            "mentor_quality": 4,
            "skill_match": 5,
            "would_recommend": True,
            "comments": "Amazing experience with cutting-edge technology."
        },
        "company_feedback": {
            "performance": 4,
            "skill_level": 5,
            "professionalism": 4,
            "learning_ability": 5,
            "would_hire": True,
            "would_recommend": True,
            "comments": "Great technical skills and quick learner."
        },
        "actual_success_score": 88.0,
        "score_difference": -3.2,
        "category": "Good Match"
    },

    # Scenario 2: Poor Matches (High original score, Low actual score)
    {
        "id": 3,
        "student_id": 22,
        "internship_id": 12,
        "organization_id": 6,
        "original_match_score": 84.7,
        "student_feedback": {
            "satisfaction": 2,
            "learning": 2,
            "work_environment": 3,
            "mentor_quality": 1,
            "skill_match": 2,
            "would_recommend": False,
            "comments": "Poor mentorship and unclear expectations. Very disappointing."
        },
        "company_feedback": {
            "performance": 2,
            "skill_level": 2,
            "professionalism": 3,
            "learning_ability": 3,
            "would_hire": False,
            "would_recommend": False,
            "comments": "Skills did not match job requirements. Struggled with basic tasks."
        },
        "actual_success_score": 32.0,
        "score_difference": -52.7,
        "category": "Poor Match"
    },
    {
        "id": 4,
        "student_id": 19,
        "internship_id": 15,
        "organization_id": 8,
        "original_match_score": 82.1,
        "student_feedback": {
            "satisfaction": 1,
            "learning": 3,
            "work_environment": 2,
            "mentor_quality": 2,
            "skill_match": 1,
            "would_recommend": False,
            "comments": "Not what I expected. Limited learning opportunities."
        },
        "company_feedback": {
            "performance": 2,
            "skill_level": 1,
            "professionalism": 3,
            "learning_ability": 2,
            "would_hire": False,
            "would_recommend": False,
            "comments": "Significant skill gap. Required extensive supervision."
        },
        "actual_success_score": 28.0,
        "score_difference": -54.1,
        "category": "Poor Match"
    },

    # Scenario 3: Hidden Gems (Low original score, High actual score)
    {
        "id": 5,
        "student_id": 31,
        "internship_id": 21,
        "organization_id": 11,
        "original_match_score": 52.8,
        "student_feedback": {
            "satisfaction": 5,
            "learning": 4,
            "work_environment": 4,
            "mentor_quality": 5,
            "skill_match": 3,
            "would_recommend": True,
            "comments": "Great learning experience! Learned skills I didn't know I needed."
        },
        "company_feedback": {
            "performance": 4,
            "skill_level": 3,
            "professionalism": 5,
            "learning_ability": 5,
            "would_hire": True,
            "would_recommend": True,
            "comments": "Amazing adaptability! Quick learner who exceeded expectations."
        },
        "actual_success_score": 84.0,
        "score_difference": 31.2,
        "category": "Hidden Gem"
    },
    {
        "id": 6,
        "student_id": 27,
        "internship_id": 18,
        "organization_id": 9,
        "original_match_score": 48.3,
        "student_feedback": {
            "satisfaction": 4,
            "learning": 5,
            "work_environment": 4,
            "mentor_quality": 4,
            "skill_match": 3,
            "would_recommend": True,
            "comments": "Challenging but rewarding. Great team and supportive environment."
        },
        "company_feedback": {
            "performance": 5,
            "skill_level": 3,
            "professionalism": 4,
            "learning_ability": 5,
            "would_hire": True,
            "would_recommend": True,
            "comments": "Excellent attitude and work ethic. Picked up skills quickly."
        },
        "actual_success_score": 80.0,
        "score_difference": 31.7,
        "category": "Hidden Gem"
    },

    # Scenario 4: Expected Poor Matches (Low original score, Low actual score)
    {
        "id": 7,
        "student_id": 44,
        "internship_id": 29,
        "organization_id": 14,
        "original_match_score": 41.2,
        "student_feedback": {
            "satisfaction": 2,
            "learning": 3,
            "work_environment": 3,
            "mentor_quality": 2,
            "skill_match": 1,
            "would_recommend": False,
            "comments": "Skills mismatch made it difficult. Not a good fit for my interests."
        },
        "company_feedback": {
            "performance": 3,
            "skill_level": 2,
            "professionalism": 3,
            "learning_ability": 2,
            "would_hire": False,
            "would_recommend": False,
            "comments": "Significant skill gap. Would need extensive training."
        },
        "actual_success_score": 36.0,
        "score_difference": -5.2,
        "category": "Expected Poor"
    },

    # Scenario 5: Mixed/Average Matches
    {
        "id": 8,
        "student_id": 12,
        "internship_id": 5,
        "organization_id": 3,
        "original_match_score": 71.5,
        "student_feedback": {
            "satisfaction": 3,
            "learning": 4,
            "work_environment": 3,
            "mentor_quality": 3,
            "skill_match": 4,
            "would_recommend": True,
            "comments": "Decent experience. Some good learning opportunities."
        },
        "company_feedback": {
            "performance": 3,
            "skill_level": 4,
            "professionalism": 4,
            "learning_ability": 3,
            "would_hire": False,
            "would_recommend": True,
            "comments": "Solid performance. Met most expectations."
        },
        "actual_success_score": 68.0,
        "score_difference": -3.5,
        "category": "Average Match"
    },
    {
        "id": 9,
        "student_id": 36,
        "internship_id": 24,
        "organization_id": 12,
        "original_match_score": 67.8,
        "student_feedback": {
            "satisfaction": 4,
            "learning": 3,
            "work_environment": 4,
            "mentor_quality": 3,
            "skill_match": 3,
            "would_recommend": True,
            "comments": "Good experience overall. Would be helpful to have more structured mentoring."
        },
        "company_feedback": {
            "performance": 4,
            "skill_level": 3,
            "professionalism": 4,
            "learning_ability": 4,
            "would_hire": True,
            "would_recommend": True,
            "comments": "Good work quality. Shows potential for growth."
        },
        "actual_success_score": 72.0,
        "score_difference": 4.2,
        "category": "Average Match"
    },

    # Scenario 6: One-sided feedback
    {
        "id": 10,
        "student_id": 29,
        "internship_id": 16,
        "organization_id": 7,
        "original_match_score": 75.2,
        "student_feedback": {
            "satisfaction": 4,
            "learning": 4,
            "work_environment": 3,
            "mentor_quality": 4,
            "skill_match": 4,
            "would_recommend": True,
            "comments": "Good internship but company didn't provide feedback."
        },
        "company_feedback": None,  # Company didn't provide feedback
        "actual_success_score": 64.0,  # Only student portion calculated
        "score_difference": -11.2,
        "category": "Incomplete Feedback"
    }
]

def analyze_dataset():
    """Analyze the feedback dataset for score comparison insights."""

    print("=== INTERNSHIP FEEDBACK DATASET ANALYSIS ===")
    print(f"Total Records: {len(feedback_dataset)}")
    print()

    # Calculate statistics
    original_scores = [item["original_match_score"] for item in feedback_dataset]
    actual_scores = [item["actual_success_score"] for item in feedback_dataset]
    differences = [item["score_difference"] for item in feedback_dataset]

    print("📊 SCORE STATISTICS:")
    print(f"Average Original Match Score: {sum(original_scores)/len(original_scores):.1f}%")
    print(f"Average Actual Success Score: {sum(actual_scores)/len(actual_scores):.1f}%")
    print(f"Average Score Difference: {sum(differences)/len(differences):.1f}%")
    print()

    # Accuracy analysis
    accurate_predictions = len([d for d in differences if abs(d) <= 15])
    accuracy_rate = (accurate_predictions / len(differences)) * 100

    print("🎯 ACCURACY ANALYSIS:")
    print(f"Predictions within ±15%: {accurate_predictions}/{len(differences)} ({accuracy_rate:.1f}%)")
    print(f"Mean Absolute Error: {sum(abs(d) for d in differences)/len(differences):.1f}%")
    print()

    # Category breakdown
    categories = {}
    for item in feedback_dataset:
        cat = item["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(item)

    print("📂 CATEGORY BREAKDOWN:")
    for category, items in categories.items():
        avg_diff = sum(item["score_difference"] for item in items) / len(items)
        print(f"{category}: {len(items)} records (avg difference: {avg_diff:+.1f}%)")
    print()

    # Best and worst predictions
    best_prediction = min(feedback_dataset, key=lambda x: abs(x["score_difference"]))
    worst_prediction = max(feedback_dataset, key=lambda x: abs(x["score_difference"]))

    print("🏆 BEST PREDICTION:")
    print(f"ID {best_prediction['id']}: {best_prediction['original_match_score']:.1f}% → {best_prediction['actual_success_score']:.1f}% (difference: {best_prediction['score_difference']:+.1f}%)")

    print("💔 WORST PREDICTION:")
    print(f"ID {worst_prediction['id']}: {worst_prediction['original_match_score']:.1f}% → {worst_prediction['actual_success_score']:.1f}% (difference: {worst_prediction['score_difference']:+.1f}%)")
    print()

    # ML Improvement recommendations
    print("💡 ML MODEL IMPROVEMENT RECOMMENDATIONS:")

    overconfident = len([item for item in feedback_dataset if item["score_difference"] < -20])
    hidden_gems = len([item for item in feedback_dataset if item["score_difference"] > 20])

    if overconfident > len(feedback_dataset) * 0.2:
        print("⚠️  Model tends to overestimate - add penalty for skill mismatches")

    if hidden_gems > len(feedback_dataset) * 0.2:
        print("📈 Model misses good candidates - consider soft skills and learning ability")

    if sum(abs(d) for d in differences) / len(differences) > 20:
        print("🔧 High error rate - retrain with more diverse features")

    if accuracy_rate < 50:
        print("🔄 Poor accuracy - revise matching algorithm fundamentals")

    print()

    # Success factors
    successful_matches = [item for item in feedback_dataset if item["actual_success_score"] >= 80]
    if successful_matches:
        avg_student_satisfaction = sum(item["student_feedback"]["satisfaction"] for item in successful_matches if item["student_feedback"]) / len([item for item in successful_matches if item["student_feedback"]])
        print("✨ SUCCESS FACTORS:")
        print(f"Successful matches ({len(successful_matches)} total)")
        print(f"Average student satisfaction: {avg_student_satisfaction:.1f}/5")

        would_hire_rate = len([item for item in successful_matches if item["company_feedback"] and item["company_feedback"]["would_hire"]]) / len([item for item in successful_matches if item["company_feedback"]])
        print(f"Company would hire rate: {would_hire_rate*100:.1f}%")

def export_to_csv():
    """Export the dataset to CSV format for further analysis."""

    import csv

    filename = "feedback_analysis_sample_data.csv"

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'id', 'student_id', 'internship_id', 'organization_id',
            'original_match_score', 'actual_success_score', 'score_difference',
            'student_satisfaction', 'student_learning', 'student_work_environment',
            'student_mentor_quality', 'student_skill_match', 'student_would_recommend',
            'company_performance', 'company_skill_level', 'company_professionalism',
            'company_learning_ability', 'company_would_hire', 'company_would_recommend',
            'category', 'student_comments', 'company_comments'
        ]

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for item in feedback_dataset:
            row = {
                'id': item['id'],
                'student_id': item['student_id'],
                'internship_id': item['internship_id'],
                'organization_id': item['organization_id'],
                'original_match_score': item['original_match_score'],
                'actual_success_score': item['actual_success_score'],
                'score_difference': item['score_difference'],
                'category': item['category']
            }

            if item['student_feedback']:
                row.update({
                    'student_satisfaction': item['student_feedback']['satisfaction'],
                    'student_learning': item['student_feedback']['learning'],
                    'student_work_environment': item['student_feedback']['work_environment'],
                    'student_mentor_quality': item['student_feedback']['mentor_quality'],
                    'student_skill_match': item['student_feedback']['skill_match'],
                    'student_would_recommend': item['student_feedback']['would_recommend'],
                    'student_comments': item['student_feedback']['comments']
                })

            if item['company_feedback']:
                row.update({
                    'company_performance': item['company_feedback']['performance'],
                    'company_skill_level': item['company_feedback']['skill_level'],
                    'company_professionalism': item['company_feedback']['professionalism'],
                    'company_learning_ability': item['company_feedback']['learning_ability'],
                    'company_would_hire': item['company_feedback']['would_hire'],
                    'company_would_recommend': item['company_feedback']['would_recommend'],
                    'company_comments': item['company_feedback']['comments']
                })

            writer.writerow(row)

    print(f"📄 Dataset exported to {filename}")

if __name__ == "__main__":
    analyze_dataset()
    export_to_csv()