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

### Setting up for development

```bash
git clone https://github.com/sammywachtel/harmonic-analysis-py.git
cd harmonic-analysis-py
pip install -e ".[dev]"
pre-commit install
```

### Running quality checks

```bash
# Format code
black src/ tests/

# Type checking
mypy src/

# Linting
flake8 src/ tests/

# Run all checks
pre-commit run --all-files
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
