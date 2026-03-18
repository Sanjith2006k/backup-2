"""
Simple Feedback Dataset Analysis (Windows Compatible)
Analyzes internship feedback data for ML model improvement.
"""

# Sample feedback dataset
feedback_data = [
    {"id": 1, "original_score": 88.5, "actual_score": 90.0, "difference": 1.5, "category": "Excellent Match"},
    {"id": 2, "original_score": 91.2, "actual_score": 88.0, "difference": -3.2, "category": "Good Match"},
    {"id": 3, "original_score": 84.7, "actual_score": 32.0, "difference": -52.7, "category": "Poor Match"},
    {"id": 4, "original_score": 82.1, "actual_score": 28.0, "difference": -54.1, "category": "Poor Match"},
    {"id": 5, "original_score": 52.8, "actual_score": 84.0, "difference": 31.2, "category": "Hidden Gem"},
    {"id": 6, "original_score": 48.3, "actual_score": 80.0, "difference": 31.7, "category": "Hidden Gem"},
    {"id": 7, "original_score": 41.2, "actual_score": 36.0, "difference": -5.2, "category": "Expected Poor"},
    {"id": 8, "original_score": 71.5, "actual_score": 68.0, "difference": -3.5, "category": "Average Match"},
    {"id": 9, "original_score": 67.8, "actual_score": 72.0, "difference": 4.2, "category": "Average Match"},
    {"id": 10, "original_score": 75.2, "actual_score": 64.0, "difference": -11.2, "category": "Incomplete Feedback"}
]

def analyze_scores():
    print("=" * 60)
    print("INTERNSHIP FEEDBACK SCORE COMPARISON ANALYSIS")
    print("=" * 60)
    print(f"Total Records: {len(feedback_data)}")
    print()

    # Basic statistics
    original_scores = [item["original_score"] for item in feedback_data]
    actual_scores = [item["actual_score"] for item in feedback_data]
    differences = [item["difference"] for item in feedback_data]

    print("SCORE STATISTICS:")
    print("-" * 30)
    print(f"Average Original Match Score: {sum(original_scores)/len(original_scores):.1f}%")
    print(f"Average Actual Success Score: {sum(actual_scores)/len(actual_scores):.1f}%")
    print(f"Average Score Difference: {sum(differences)/len(differences):.1f}%")
    print()

    # Accuracy analysis
    accurate_predictions = len([d for d in differences if abs(d) <= 15])
    accuracy_rate = (accurate_predictions / len(differences)) * 100

    print("ACCURACY ANALYSIS:")
    print("-" * 30)
    print(f"Predictions within +/-15%: {accurate_predictions}/{len(differences)} ({accuracy_rate:.1f}%)")
    print(f"Mean Absolute Error: {sum(abs(d) for d in differences)/len(differences):.1f}%")
    print()

    # Score comparison details
    print("DETAILED SCORE COMPARISONS:")
    print("-" * 45)
    print("ID | Original -> Actual | Difference | Category")
    print("-" * 45)
    for item in feedback_data:
        diff_str = f"{item['difference']:+.1f}"
        print(f"{item['id']:2d} | {item['original_score']:6.1f}% -> {item['actual_score']:5.1f}% | {diff_str:8s} | {item['category']}")
    print()

    # Category breakdown
    categories = {}
    for item in feedback_data:
        cat = item["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(item)

    print("CATEGORY BREAKDOWN:")
    print("-" * 30)
    for category, items in categories.items():
        avg_diff = sum(item["difference"] for item in items) / len(items)
        print(f"{category}: {len(items)} records (avg difference: {avg_diff:+.1f}%)")
    print()

    # Error analysis
    overestimated = [item for item in feedback_data if item["difference"] < -15]
    underestimated = [item for item in feedback_data if item["difference"] > 15]
    accurate = [item for item in feedback_data if abs(item["difference"]) <= 15]

    print("ERROR DISTRIBUTION:")
    print("-" * 30)
    print(f"Overestimated (worse than predicted): {len(overestimated)} ({len(overestimated)/len(feedback_data)*100:.1f}%)")
    print(f"Underestimated (better than predicted): {len(underestimated)} ({len(underestimated)/len(feedback_data)*100:.1f}%)")
    print(f"Accurate predictions: {len(accurate)} ({len(accurate)/len(feedback_data)*100:.1f}%)")
    print()

    # Best and worst predictions
    best_prediction = min(feedback_data, key=lambda x: abs(x["difference"]))
    worst_prediction = max(feedback_data, key=lambda x: abs(x["difference"]))

    print("BEST AND WORST PREDICTIONS:")
    print("-" * 30)
    print(f"Best:  ID {best_prediction['id']} - {best_prediction['original_score']:.1f}% -> {best_prediction['actual_score']:.1f}% (diff: {best_prediction['difference']:+.1f}%)")
    print(f"Worst: ID {worst_prediction['id']} - {worst_prediction['original_score']:.1f}% -> {worst_prediction['actual_score']:.1f}% (diff: {worst_prediction['difference']:+.1f}%)")
    print()

    # ML Model insights
    print("ML MODEL IMPROVEMENT INSIGHTS:")
    print("-" * 30)

    # Correlation analysis (simplified)
    correlation_indicator = "Good" if accuracy_rate > 60 else "Poor" if accuracy_rate < 40 else "Moderate"
    print(f"Model Performance: {correlation_indicator} ({accuracy_rate:.1f}% accuracy)")

    if len(overestimated) > len(feedback_data) * 0.2:
        print("- WARNING: Model frequently overestimates success")
        print("- RECOMMENDATION: Add penalty factors for skill mismatches")

    if len(underestimated) > len(feedback_data) * 0.2:
        print("- INSIGHT: Model misses many successful candidates")
        print("- RECOMMENDATION: Consider soft skills and adaptability factors")

    mae = sum(abs(d) for d in differences) / len(differences)
    if mae > 20:
        print("- WARNING: High average error rate")
        print("- RECOMMENDATION: Retrain with more diverse feature set")

    print()

    # Success patterns
    successful_matches = [item for item in feedback_data if item["actual_score"] >= 75]
    print("SUCCESS PATTERNS:")
    print("-" * 30)
    print(f"High-performing internships (>75% actual score): {len(successful_matches)}")

    if successful_matches:
        avg_original = sum(item["original_score"] for item in successful_matches) / len(successful_matches)
        print(f"Average original score for successful matches: {avg_original:.1f}%")

        hidden_success = [item for item in successful_matches if item["original_score"] < 60]
        if hidden_success:
            print(f"Hidden gems (low original, high actual): {len(hidden_success)}")

    print()
    print("NEXT STEPS:")
    print("-" * 30)
    print("1. Use actual_success_score as training labels for model updates")
    print("2. Analyze overestimated matches for common failure patterns")
    print("3. Study hidden gems to identify missed success factors")
    print("4. Implement continuous learning with new feedback data")
    print("5. Focus on features that matter most for actual success")

if __name__ == "__main__":
    analyze_scores()