# Music Theory Analysis

A comprehensive Python library for music theory analysis, providing sophisticated algorithms for functional harmony, modal analysis, and chromatic harmony detection.

## Features

- **Comprehensive Analysis Engine**: Hierarchical analysis combining functional harmony, modal characteristics, and chromatic elements
- **Functional Harmony Analysis**: Roman numeral analysis, chord functions, cadence detection
- **Enhanced Modal Analysis**: Evidence-based modal detection with confidence scoring
- **Chromatic Harmony**: Secondary dominants, borrowed chords, chromatic mediants
- **Parent Key + Local Tonic Approach**: Theoretically sound modal analysis framework
- **Calibrated Confidence Scoring**: Music theory-validated confidence levels for pedagogical appropriateness
- **Extensive Test Coverage**: 427 sophisticated multi-layer test cases with 56%+ validation success
- **Production Ready**: Meets validation targets for modal (56%+) and functional (50%+) analysis

## Installation

```bash
pip install harmonic-analysis
```

## Quick Start

```python
from harmonic_analysis import analyze_progression_multiple, AnalysisOptions

# Simple analysis with calibrated confidence scoring
result = await analyze_progression_multiple(['C', 'Am', 'F', 'G'])

print(f"Primary: {result.primary_analysis.type.value}")
print(f"Analysis: {result.primary_analysis.analysis}")
print(f"Confidence: {result.primary_analysis.confidence:.2f}")

# Analysis with options for enhanced results
options = AnalysisOptions(
    parent_key="C major",
    pedagogical_level="intermediate",
    confidence_threshold=0.6
)

result = await analyze_progression_multiple(['C', 'Am', 'F', 'G'], options)

# Access detailed results
print(f"Roman numerals: {result.primary_analysis.roman_numerals}")
print(f"Evidence count: {len(result.primary_analysis.evidence)}")

# Multiple interpretations with confidence-based ranking
for i, alt in enumerate(result.alternative_analyses):
    print(f"Alternative {i+1}: {alt.type.value} (confidence: {alt.confidence:.2f})")
    print(f"  {alt.analysis}")
```

## Core Concepts

### Analysis Hierarchy

The library uses a three-tier analysis approach:

1. **Functional Harmony** (Foundation) - Roman numerals, chord functions, cadences
2. **Modal Analysis** (Enhancement) - Applied when modal characteristics are detected
3. **Chromatic Analysis** (Advanced) - Secondary dominants, borrowed chords, etc.

### Parent Key + Local Tonic Approach

All modal analysis follows the **Parent Key Signature + Local Tonic** model:

- **Parent Key Signature**: The underlying scale and key signature (e.g., C major, no sharps/flats)
- **Local Tonic**: The note that functions as the tonal center (e.g., G)
- **Mode**: The combination (e.g., G Mixolydian = C major scale with G as tonic)

This approach ensures theoretically sound and pedagogically valuable modal analysis.

## API Reference

### Core Classes

#### `ComprehensiveAnalysisEngine`

The main analysis engine that coordinates all analytical approaches.

**Methods:**

- `analyze_comprehensively(progression_input: str, parent_key: str = None) -> ComprehensiveAnalysisResult`
- `analyze_with_multiple_interpretations(progression_input: str, options: AnalysisOptions = None) -> MultipleInterpretationResult`

#### `FunctionalHarmonyAnalyzer`

Specialized analyzer for functional harmony analysis.

**Methods:**

- `analyze_functionally(chord_symbols: List[str], parent_key: str = None) -> FunctionalAnalysisResult`

#### `EnhancedModalAnalyzer`

Advanced modal analysis with evidence-based confidence scoring.

**Methods:**

- `analyze_modal_characteristics(chord_symbols: List[str], parent_key: str = None) -> ModalAnalysisResult`

### Data Structures

#### `ComprehensiveAnalysisResult`

```python
@dataclass
class ComprehensiveAnalysisResult:
    functional: FunctionalAnalysisResult
    modal: Optional[ModalEnhancementResult]
    chromatic: Optional[ChromaticAnalysisResult]
    primary_approach: Literal['functional', 'modal', 'chromatic']
    confidence: float
    explanation: str
    pedagogical_value: str
    user_input: UserInputContext
```

#### `FunctionalAnalysisResult`

```python
@dataclass
class FunctionalAnalysisResult:
    key_center: str
    key_signature: str
    mode: Literal['major', 'minor', 'modal']
    chords: List[FunctionalChordAnalysis]
    cadences: List[Cadence]
    progression_type: ProgressionType
    confidence: float
    explanation: str
    chromatic_elements: List[ChromaticElement]
```

## Testing

The library includes comprehensive test coverage with over 1000 test cases:

```bash
# Run all tests
pytest

# Run specific test categories
pytest -m "modal"
pytest -m "functional"
pytest -m "chromatic"

# Run with coverage
pytest --cov=harmonic_analysis --cov-report=html
```

## Development

### Quick Development Setup

We provide comprehensive automation for development setup:

```bash
# One-command environment setup with quality automation
python scripts/setup_dev_env.py

# Or manual setup:
git clone https://github.com/sammywachtel/harmonic-analysis-py.git
cd harmonic-analysis-py
pip install -e ".[dev]"
pre-commit install
```

### Quality Automation System 🚀

This project includes a comprehensive quality automation system with:

- **🎨 Auto-formatting** with Black and isort on every commit
- **🛡️ Security scanning** with Bandit for vulnerability detection
- **📊 Type checking** with MyPy for robust code
- **⚠️ Warning-based edge case testing** - tests provide feedback without blocking CI/CD
- **🚀 Automated releases** triggered by version increments
- **📝 IDE integration** with setup for PyCharm and VS Code

### Interactive Quality Commands

```bash
# Comprehensive quality check with auto-fix and colorful reporting
python scripts/quality_check.py --fix

# Quick quality check without auto-fix
python scripts/quality_check.py

# Run quick tests only (faster feedback)
python scripts/quality_check.py --quick-tests

# Traditional individual commands
black src/ tests/ scripts/          # Auto-format code
isort src/ tests/ scripts/          # Sort imports
flake8 src/ tests/ scripts/         # Linting
mypy src/ --ignore-missing-imports  # Type checking
bandit -r src/ -f json              # Security scanning

# Pre-commit hooks (run automatically on commit)
pre-commit run --all-files
```

### Quality Process Features

#### 🎯 Pre-commit Automation
Pre-commit hooks automatically:
- Format code with Black (⚫)
- Sort imports with isort (📦)
- Run security scans with Bandit (🛡️)
- Check type annotations with MyPy (📊)
- Validate file structure and hygiene (🧹)

#### ⚠️ Warning-Based Testing
Edge case tests use a warning system instead of failures:
- **Pass with warnings** for edge cases to avoid blocking CI/CD
- **Colorful icons** (🟠⚠️📊💭🔍) highlight issues in logs
- **Educational feedback** explains edge case behavior
- **Behavioral validation** ensures appropriate graceful degradation

#### 🚀 Automated Release Pipeline
GitHub Actions automatically:
- Detect version increments in pull requests to main
- Validate CHANGELOG.md updates
- Run comprehensive test suite with security scanning
- Create GitHub releases with tags
- Publish to PyPI on successful validation

### Development Workflow

```bash
# 1. Setup development environment (one-time)
python scripts/setup_dev_env.py

# 2. Create feature branch
git checkout -b feature/your-feature

# 3. Develop with automatic quality checks
# (Pre-commit hooks run automatically on commit)
git add .
git commit -m "feat: add your feature"

# 4. Run comprehensive quality check before push
python scripts/quality_check.py --fix

# 5. Push and create PR
git push origin feature/your-feature

# 6. Automated CI/CD handles testing and release
# (On merge to main, if version incremented)
```

### IDE Integration

The setup script configures:

**PyCharm:**
- Black formatter on file save
- Import optimization with isort
- Code inspection with flake8
- MyPy type checking integration

**VS Code:**
- Python formatting and linting settings
- Pre-commit integration
- Test discovery and execution
- Debugging configuration

### Testing with Quality Automation

```bash
# Run tests with quality automation feedback
pytest                                    # Full test suite
pytest tests/test_edge_case_behavior.py  # Edge case warnings
pytest -m "not slow"                     # Quick tests only

# Generate comprehensive test reports
python scripts/quality_check.py --fix --quick-tests

# Specific test categories with quality validation
pytest -m "modal" -v                     # Modal analysis
pytest -m "functional" -v                # Functional harmony
pytest tests/test_comprehensive_multi_layer_validation.py -v
```

## Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Citation

If you use this library in academic work, please cite:

```bibtex
@software{harmonic_analysis,
  title = {Music Theory Analysis: A Comprehensive Python Library},
  author = {Wachtel, Sam},
  year = {2025},
  url = {https://github.com/sammywachtel/harmonic-analysis-py}
}
```

## Related Projects

This library was extracted from the [Music Modes App](https://github.com/sammywachtel/music_modes_app), a comprehensive music theory toolkit with React frontend and FastAPI backend.
