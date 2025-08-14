# Scripts Directory

This directory contains essential maintenance scripts for the harmonic analysis library.

## 📋 Essential Scripts

### 🎯 `confidence_calibration_analysis.py`
**Purpose**: Production confidence scoring analysis and calibration tool

**Key Features**:
- Analyzes confidence patterns between expected vs actual scores
- Uses proper parent_key context from comprehensive test cases
- Provides detailed confidence difference reporting for debugging
- Essential for maintaining system accuracy and calibration

**Usage**:
```bash
python scripts/confidence_calibration_analysis.py
```

**When to Use**:
- After making changes to confidence scoring algorithms
- When comprehensive tests show confidence mismatches
- During confidence calibration development cycles
- For debugging systematic confidence scoring issues

**Historical Significance**: Critical for identifying the parent key parsing bug that improved functional harmony success rate from 0% to 72%.

### 🏭 `generate_comprehensive_multi_layer_tests.py`  
**Purpose**: Comprehensive test case generation system

**Key Features**:
- Generates 427+ multi-layer test cases with complete analysis expectations
- Covers functional harmony, modal analysis, and chromatic analysis
- Exports to JSON and CSV formats for validation and analysis
- **FIXED** Roman numeral generation bug (Aug 2025)

**Usage**:
```bash
python scripts/generate_comprehensive_multi_layer_tests.py
```

**Output Files**:
- `tests/generated/comprehensive-multi-layer-tests.json` - Complete test data
- `tests/generated/comprehensive-multi-layer-tests.csv` - Analysis-friendly format

**When to Use**:
- After fixing bugs in test expectation generation
- Before major releases to refresh test expectations
- When updating test coverage or adding new categories

**Critical Fix**: The original version had a broken `chord_to_roman_numeral()` method that returned `"I"` for all major chords and `"ii"` for all minor chords, causing systematic test failures. This has been fixed to properly calculate Roman numerals based on chord root and key center relationships.

## 🔧 Maintenance Workflows

### Confidence Calibration Workflow
```bash
# 1. Run tests to identify confidence issues
python -m pytest tests/test_comprehensive_multi_layer_validation.py -v

# 2. Analyze confidence patterns
python scripts/confidence_calibration_analysis.py

# 3. Make algorithmic adjustments based on analysis

# 4. Validate improvements
python -m pytest tests/test_comprehensive_multi_layer_validation.py::TestComprehensiveMultiLayerValidation::test_functional_harmony_cases -v
```

### Test Regeneration Workflow (After Bug Fixes)
```bash  
# 1. Generate fresh test data with fixed expectations
python scripts/generate_comprehensive_multi_layer_tests.py

# 2. Validate against regenerated test data
python -m pytest tests/test_comprehensive_multi_layer_validation.py -v

# 3. Expected outcome: Much higher success rates due to correct expectations
```

## 📊 Integration Notes

**Script Dependencies**:
- Both scripts use `sys.path.append()` to access the main library
- Import library types like `AnalysisOptions` for consistency  
- Generate data compatible with the test suite structure

**Configuration**:
- Scripts respect library configuration patterns
- Use the same confidence thresholds as the main analysis system
- Maintain compatibility with both development and production environments

## 🚨 Recent Changes

**August 2025 - Critical Bug Fix**:
- **Fixed** `chord_to_roman_numeral()` in test generator
- **Before**: `C-F-G-C` generated expectations `["I", "I", "I", "I"]` 
- **After**: `C-F-G-C` generates correct expectations `["I", "IV", "V", "I"]`
- **Impact**: Expected to improve test success rates from ~30% to 70%+

**Cleanup**:
- **Removed** temporary debugging scripts: 
  - `analyze_test_expectations.py`
  - `analyze_test_failures.py`  
  - `comprehensive_failure_analysis.py`
  - `debug_key_detection.py`
  - `examine_specific_failures.py`
- **Kept** only essential production and infrastructure tools

## 🎯 Quality Standards

All maintained scripts include:
- ✅ Comprehensive docstring with purpose and usage
- ✅ Historical context for significant changes  
- ✅ Clear usage examples and expected outputs
- ✅ Integration notes with the main library
- ✅ Proper error handling and validation

**Maintenance Policy**: Scripts in this directory are essential infrastructure. Any modifications should be thoroughly tested and documented.