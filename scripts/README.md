# Scripts Directory

This directory contains essential scripts for music theory analysis library maintenance and calibration.

## 📋 Script Overview

### `confidence_calibration_analysis.py` ⚙️
**Purpose**: Confidence scoring analysis and calibration tool

**Key Features**:
- Analyzes functional harmony confidence patterns
- Analyzes modal characteristic confidence patterns
- Uses proper parent_key context from test cases
- Provides detailed confidence difference reporting

**Usage**:
```bash
python scripts/confidence_calibration_analysis.py
```

**When to Use**:
- After making changes to confidence scoring algorithms
- When test expectations seem misaligned with actual output
- For debugging why tests are failing due to confidence mismatches
- During confidence calibration iterations

**Historical Significance**: This tool was essential for identifying and fixing the critical parent key parsing bug where "C major" was incorrectly parsed as "C minor", leading to a major improvement in functional harmony analysis from 0% to 72% success rate.

### `generate_comprehensive_multi_layer_tests.py` 🏭
**Purpose**: Comprehensive test case generation system

**Key Features**:
- Generates 427+ multi-layer test cases with full analysis expectations
- Supports functional harmony, modal analysis, and chromatic analysis expectations
- Includes confidence scoring expectations for all analysis types
- Exports to both JSON and CSV formats
- Direct port of the frontend TypeScript test generator

**Usage**:
```bash
python scripts/generate_comprehensive_multi_layer_tests.py
```

**Output Files**:
- `tests/generated/comprehensive-multi-layer-tests.json` - Complete test data
- `tests/generated/comprehensive-multi-layer-tests.csv` - Spreadsheet format

**When to Use**:
- When updating test expectations after algorithm changes
- Before major releases to ensure comprehensive coverage
- When adding new test categories or edge cases
- For behavioral parity validation with TypeScript frontend

## 🔧 Maintenance Guidelines

### Script Lifecycle Management

**Keep These Scripts** ✅:
- Core functionality that supports ongoing development
- Tools used for production calibration and debugging
- Scripts referenced by CI/CD or regular maintenance workflows

**Remove Scripts** ❌:
- One-time debugging scripts that solved specific issues
- Temporary analysis tools that are no longer needed
- Superseded versions of existing tools

### Documentation Standards

Each maintained script should include:
- Clear docstring with purpose and usage
- Key features list
- Usage examples
- Historical context if significant
- Author and date information

### Script Categories

1. **Production Tools** (`confidence_calibration_analysis.py`)
   - Used for ongoing calibration and debugging
   - Essential for maintaining system accuracy

2. **Development Infrastructure** (`generate_comprehensive_multi_layer_tests.py`)
   - Core test generation and validation
   - Required for behavioral parity maintenance

## 📊 Usage Examples

### Confidence Calibration Workflow

```bash
# 1. Run comprehensive tests to identify confidence issues
python -m pytest tests/test_comprehensive_multi_layer_validation.py -v

# 2. Analyze confidence patterns
python scripts/confidence_calibration_analysis.py

# 3. Make calibration adjustments to algorithms

# 4. Validate improvements
python -m pytest tests/test_comprehensive_multi_layer_validation.py::TestComprehensiveMultiLayerValidation::test_functional_harmony_cases -v
```

### Test Data Regeneration Workflow

```bash
# 1. Generate fresh test data
python scripts/generate_comprehensive_multi_layer_tests.py

# 2. Run validation against new test data
python -m pytest tests/test_comprehensive_multi_layer_validation.py -v

# 3. Commit updated test data if appropriate
git add tests/generated/comprehensive-multi-layer-tests.json
git commit -m "Update comprehensive test expectations"
```

## 🎯 Integration with Main Library

These scripts integrate with the main library through:

- **Import Path**: All scripts use `sys.path.append()` to access the library
- **Type Compatibility**: Use library types like `AnalysisOptions` for consistency
- **Test Data**: Generate data compatible with the test suite structure
- **Configuration**: Respect library configuration patterns and conventions
