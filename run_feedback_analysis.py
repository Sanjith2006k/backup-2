"""
Feedback Dataset Generator and Analyzer
Run this script to generate sample feedback data and analyze score comparisons.
"""

import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    print("🚀 INTERNSHIP FEEDBACK ANALYSIS SYSTEM")
    print("=" * 50)

    try:
        # Import and run dataset generation
        print("\n📊 Step 1: Generating feedback dataset...")
        from generate_feedback_dataset import generate_feedback_dataset, analyze_feedback_scores

        sample_count = generate_feedback_dataset()
        print(f"✅ Successfully generated {sample_count} feedback samples")

        print("\n📈 Step 2: Analyzing feedback scores...")
        analyze_feedback_scores()

        # Import and run detailed analysis
        print("\n🔍 Step 3: Running comprehensive score comparison...")
        from score_analysis import create_score_comparison_report, export_analysis_csv

        df = create_score_comparison_report()

        if df is not None:
            print("\n📄 Step 4: Exporting analysis data...")
            export_analysis_csv()

            print("\n" + "=" * 60)
            print("🎉 ANALYSIS COMPLETE!")
            print("=" * 60)

            # Summary recommendations
            correlation = df['original_score'].corr(df['actual_score'])
            accuracy = (abs(df['difference']) <= 15).mean() * 100

            print(f"\n📋 EXECUTIVE SUMMARY:")
            print(f"   • Total feedback records analyzed: {len(df)}")
            print(f"   • ML model correlation: {correlation:.3f}")
            print(f"   • Prediction accuracy (±15%): {accuracy:.1f}%")
            print(f"   • Average prediction error: {abs(df['difference']).mean():.1f}%")

            if correlation > 0.7 and accuracy > 70:
                print(f"\n✅ MODEL STATUS: Good performance")
                print(f"   • Continue using current model")
                print(f"   • Consider minor optimizations")
            elif correlation > 0.4 and accuracy > 50:
                print(f"\n⚠️  MODEL STATUS: Moderate performance")
                print(f"   • Model needs improvement")
                print(f"   • Consider retraining with additional features")
            else:
                print(f"\n❌ MODEL STATUS: Poor performance")
                print(f"   • Model requires significant improvement")
                print(f"   • Recommend complete algorithm revision")

            print(f"\n🎯 NEXT STEPS:")
            print(f"   1. Review feedback_analysis_data.csv for detailed data")
            print(f"   2. Identify patterns in overestimated vs underestimated matches")
            print(f"   3. Use actual_success_score as training labels for model updates")
            print(f"   4. Focus on features that correlate with student satisfaction")
            print(f"   5. Implement continuous learning pipeline with new feedback")

        else:
            print("❌ Analysis failed - no data available")

    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure all required modules are installed:")
        print("   pip install pandas matplotlib numpy flask sqlalchemy")
    except Exception as e:
        print(f"❌ Error during execution: {e}")
        return 1

    return 0

if __name__ == "__main__":
    exit_code = main()

    if exit_code == 0:
        print(f"\n🚀 Ready to improve your ML model with this feedback data!")

    sys.exit(exit_code)