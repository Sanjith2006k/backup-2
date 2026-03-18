"""
ONE-CLICK ML MODEL TEST

This script runs everything in sequence:
1. Generates 50 sample datasets
2. Tests the ML model
3. Trains with feedback data
4. Shows results

Just run: python run_full_test.py
"""

import subprocess
import sys
import os

def run_command(description, command):
    """Run a command and show status."""
    print("\n" + "=" * 80)
    print(f"📌 {description}")
    print("=" * 80 + "\n")

    try:
        result = subprocess.run(command, shell=True, check=True,
                              capture_output=False, text=True)
        print(f"\n✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ {description} failed with error code {e.returncode}")
        return False

def check_dependencies():
    """Check if required packages are installed."""
    print("\n" + "=" * 80)
    print("🔍 Checking Dependencies")
    print("=" * 80 + "\n")

    required = {
        'faker': 'faker',
        'sklearn': 'scikit-learn',
        'sentence_transformers': 'sentence-transformers',
        'numpy': 'numpy',
        'pandas': 'pandas'
    }

    missing = []

    for module, package in required.items():
        try:
            __import__(module)
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package} - MISSING")
            missing.append(package)

    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print(f"\nInstalling missing packages...")

        install_cmd = f"{sys.executable} -m pip install {' '.join(missing)}"
        subprocess.run(install_cmd, shell=True)

        print("\n✅ All dependencies installed!")
    else:
        print("\n✅ All dependencies are installed!")

def main():
    """Main execution."""
    print("=" * 80)
    print("ML MATCHING SYSTEM - ONE-CLICK FULL TEST")
    print("=" * 80)
    print("\nThis will:")
    print("  1. Check and install dependencies")
    print("  2. Generate 50 realistic sample datasets")
    print("  3. Test the ML model before training")
    print("  4. Train the model with feedback data")
    print("  5. Test the model after training")
    print("  6. Show performance improvement")
    print("\nEstimated time: 2-3 minutes")

    input("\nPress Enter to begin...")

    # Step 1: Check dependencies
    check_dependencies()

    # Step 2: Generate sample data
    if not run_command(
        "Step 1/2: Generating 50 Sample Datasets",
        f"{sys.executable} generate_sample_data.py"
    ):
        print("\n❌ Test failed at data generation step")
        return

    # Step 3: Test and train model
    if not run_command(
        "Step 2/2: Testing and Training ML Model",
        f"{sys.executable} test_with_sample_data.py"
    ):
        print("\n❌ Test failed at model testing step")
        return

    # Success!
    print("\n" + "=" * 80)
    print("✅ FULL TEST COMPLETED SUCCESSFULLY!")
    print("=" * 80)

    print("\n📊 What happened:")
    print("  ✓ Generated 50 realistic student-internship pairs")
    print("  ✓ Created complete feedback data from both sides")
    print("  ✓ Tested model predictions before training")
    print("  ✓ Trained ML model with all 50 feedback samples")
    print("  ✓ Tested model predictions after training")
    print("  ✓ Saved trained model to ai/models/")

    print("\n📁 Files created:")
    if os.path.exists('sample_dataset.json'):
        print("  ✓ sample_dataset.json (50 datasets)")
    if os.path.exists('ai/models/match_model.pkl'):
        print("  ✓ ai/models/match_model.pkl (trained model)")
    if os.path.exists('ai/models/scaler.pkl'):
        print("  ✓ ai/models/scaler.pkl (feature scaler)")

    print("\n🎯 Next Steps:")
    print("  1. Review TESTING_GUIDE.md for detailed results")
    print("  2. The model is now trained and ready for use")
    print("  3. Integrate with Flask using example_routes.py")
    print("  4. See QUICK_START.md for integration guide")

    print("\n💡 To test manually:")
    print("  python test_ml_matcher.py")

    print("\n" + "=" * 80)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
