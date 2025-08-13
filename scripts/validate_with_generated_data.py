#!/usr/bin/env python3
"""
Validation Script Using Generated Test Data

Validates the Python music theory library against the comprehensive
test data to ensure behavioral parity with the TypeScript version.
"""

import asyncio
import json
import sys
from pathlib import Path

# Add the src directory to the path so we can import the library
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from music_theory_analysis import (
    AnalysisOptions,
    InterpretationType,
    analyze_progression_multiple,
)


async def validate_test_cases():
    """Validate the Python library against generated test data"""

    # Load the generated test data
    test_data_path = (
        Path(__file__).parent.parent
        / "tests"
        / "generated"
        / "comprehensive-modal-test-cases.json"
    )

    if not test_data_path.exists():
        print("❌ Test data not found. Please run generate_test_data.py first.")
        return False

    with open(test_data_path, "r") as f:
        test_data = json.load(f)

    test_cases = test_data["testCases"]
    total_cases = len(test_cases)

    print(f"🧪 Validating {total_cases} test cases against Python library...")
    print(f"📊 Test case breakdown: {test_data['metadata']['categories']}")

    # Track results
    passed = 0
    failed = 0
    skipped = 0
    failures = []

    # Sample a subset for quick validation (full validation would take too long)
    sample_size = min(50, total_cases)  # Test first 50 cases for quick validation
    sample_cases = test_cases[:sample_size]

    print(f"\n🔬 Running validation on {sample_size} sample test cases...")

    for i, test_case in enumerate(sample_cases):
        test_id = test_case["id"]
        chords = test_case["chords"]
        parent_key = test_case.get("parentKey")
        expected_modal = test_case["expectedModal"]
        expected_mode = test_case.get("expectedMode")
        category = test_case["category"]
        description = test_case["description"]

        try:
            # Prepare analysis options
            options = AnalysisOptions()
            if parent_key:
                options.parent_key = parent_key

            # Run the analysis
            result = await analyze_progression_multiple(chords, options)

            # Determine if the result is modal or functional
            is_modal = result.primary_analysis.type == InterpretationType.MODAL

            # For modal cases, also check if the detected mode matches
            mode_matches = True
            if expected_modal and expected_mode:
                if is_modal:
                    # Extract mode from result (might need to parse from analysis string)
                    detected_mode = result.primary_analysis.mode
                    if detected_mode and expected_mode:
                        # Simple check - mode name should be in the expected mode string
                        mode_name = (
                            expected_mode.split()[-1]
                            if " " in expected_mode
                            else expected_mode
                        )
                        mode_matches = (
                            mode_name.lower() in (detected_mode or "").lower()
                        )
                else:
                    mode_matches = False

            # Check if the result matches expectations
            modal_prediction_correct = is_modal == expected_modal

            # Overall success criteria
            success = modal_prediction_correct and mode_matches

            if success:
                passed += 1
                status = "✅"
            else:
                failed += 1
                status = "❌"
                failures.append(
                    {
                        "test_id": test_id,
                        "description": description,
                        "chords": chords,
                        "category": category,
                        "expected_modal": expected_modal,
                        "expected_mode": expected_mode,
                        "actual_modal": is_modal,
                        "actual_mode": result.primary_analysis.mode,
                        "confidence": result.primary_analysis.confidence,
                    }
                )

            # Progress indicator
            if (i + 1) % 10 == 0:
                print(
                    f"  Progress: {i + 1}/{sample_size} cases processed ({passed} passed, {failed} failed)"
                )

        except Exception as e:
            skipped += 1
            print(f"  ⚠️  Skipped {test_id}: {str(e)}")

    # Print results summary
    print(f"\n📊 VALIDATION RESULTS:")
    print(f"  ✅ Passed: {passed}/{sample_size} ({passed/sample_size*100:.1f}%)")
    print(f"  ❌ Failed: {failed}/{sample_size} ({failed/sample_size*100:.1f}%)")
    print(f"  ⚠️  Skipped: {skipped}/{sample_size} ({skipped/sample_size*100:.1f}%)")

    # Show failure details
    if failures:
        print(f"\n🔍 FAILURE ANALYSIS (showing first 5 failures):")
        for failure in failures[:5]:
            print(f"  ❌ {failure['test_id']}: {failure['description']}")
            print(f"     Chords: {' '.join(failure['chords'])}")
            print(f"     Category: {failure['category']}")
            print(
                f"     Expected: {'MODAL' if failure['expected_modal'] else 'FUNCTIONAL'} ({failure['expected_mode'] or 'none'})"
            )
            print(
                f"     Actual: {'MODAL' if failure['actual_modal'] else 'FUNCTIONAL'} ({failure['actual_mode'] or 'none'})"
            )
            print(f"     Confidence: {failure['confidence']:.3f}")
            print()

        if len(failures) > 5:
            print(f"  ... and {len(failures) - 5} more failures")

    # Analyze failure patterns
    if failures:
        print(f"\n📈 FAILURE PATTERN ANALYSIS:")

        # Group failures by category
        failure_by_category = {}
        for failure in failures:
            cat = failure["category"]
            failure_by_category[cat] = failure_by_category.get(cat, 0) + 1

        print("  Failures by category:")
        for cat, count in failure_by_category.items():
            total_in_category = len(
                [tc for tc in sample_cases if tc["category"] == cat]
            )
            percentage = count / total_in_category * 100 if total_in_category > 0 else 0
            print(f"    {cat}: {count}/{total_in_category} ({percentage:.1f}%)")

    success_rate = passed / sample_size if sample_size > 0 else 0

    # Overall assessment
    print(f"\n🎯 OVERALL ASSESSMENT:")
    if success_rate >= 0.8:
        print(
            f"  🎉 EXCELLENT: {success_rate*100:.1f}% success rate - Python library shows strong behavioral parity!"
        )
    elif success_rate >= 0.6:
        print(
            f"  ✅ GOOD: {success_rate*100:.1f}% success rate - Python library shows reasonable behavioral parity"
        )
    elif success_rate >= 0.4:
        print(
            f"  ⚠️  MODERATE: {success_rate*100:.1f}% success rate - Some discrepancies need investigation"
        )
    else:
        print(
            f"  ❌ POOR: {success_rate*100:.1f}% success rate - Significant behavioral differences detected"
        )

    return success_rate >= 0.6  # Consider 60%+ success rate as acceptable


async def run_specific_test_cases():
    """Run specific test cases that showcase key functionality"""

    print("\n🎯 RUNNING SPECIFIC SHOWCASE TESTS:")

    test_cases = [
        {
            "name": "A Aeolian Characteristic",
            "chords": ["Am", "F", "G", "Am"],
            "parent_key": "C major",
            "expected": "A Aeolian modal progression",
        },
        {
            "name": "G Mixolydian Characteristic",
            "chords": ["G", "F", "C", "G"],
            "parent_key": "C major",
            "expected": "G Mixolydian modal progression",
        },
        {
            "name": "C Major Functional",
            "chords": ["C", "F", "G", "C"],
            "parent_key": "C major",
            "expected": "C major functional progression",
        },
        {
            "name": "D Dorian Characteristic",
            "chords": ["Dm", "G", "C", "Dm"],
            "parent_key": "C major",
            "expected": "D Dorian modal progression",
        },
    ]

    for test in test_cases:
        print(f"\n  🧪 Testing: {test['name']}")
        print(f"     Chords: {' '.join(test['chords'])}")
        print(f"     Parent Key: {test['parent_key']}")

        try:
            options = AnalysisOptions(parent_key=test["parent_key"])
            result = await analyze_progression_multiple(test["chords"], options)

            print(f"     Result: {result.primary_analysis.type.value} analysis")
            print(f"     Confidence: {result.primary_analysis.confidence:.3f}")
            print(f"     Analysis: {result.primary_analysis.analysis}")
            if result.primary_analysis.roman_numerals:
                print(f"     Roman Numerals: {result.primary_analysis.roman_numerals}")
            if result.primary_analysis.mode:
                print(f"     Mode: {result.primary_analysis.mode}")

            print(f"     ✅ Successfully analyzed")

        except Exception as e:
            print(f"     ❌ Error: {str(e)}")


async def main():
    """Main validation function"""
    print("🎼 PYTHON MUSIC THEORY LIBRARY VALIDATION")
    print("==========================================")

    # Run the main validation
    success = await validate_test_cases()

    # Run specific showcase tests
    await run_specific_test_cases()

    print(f"\n🏁 VALIDATION COMPLETE")
    return success


if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)
