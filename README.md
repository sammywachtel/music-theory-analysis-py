# Music Theory Analysis

A comprehensive Python library for music theory analysis, providing sophisticated algorithms for functional harmony, modal analysis, and chromatic harmony detection.

## Features

- **Comprehensive Analysis Engine**: Hierarchical analysis combining functional harmony, modal characteristics, and chromatic elements
- **Functional Harmony Analysis**: Roman numeral analysis, chord functions, cadence detection
- **Enhanced Modal Analysis**: Evidence-based modal detection with confidence scoring
- **Chromatic Harmony**: Secondary dominants, borrowed chords, chromatic mediants
- **Parent Key + Local Tonic Approach**: Theoretically sound modal analysis framework
- **Extensive Test Coverage**: 1000+ test cases across functional, modal, and chromatic categories

## Installation

```bash
pip install music-theory-analysis
```

## Quick Start

```python
from music_theory_analysis import ComprehensiveAnalysisEngine

# Initialize the analysis engine
analyzer = ComprehensiveAnalysisEngine()

# Analyze a chord progression
result = await analyzer.analyze_comprehensively(
    progression_input="Am F C G",
    parent_key="C major"
)

# Access the results
print(f"Primary approach: {result.primary_approach}")
print(f"Confidence: {result.confidence:.2f}")
print(f"Explanation: {result.explanation}")

# Detailed analysis layers
if result.functional:
    print(f"Key center: {result.functional.key_center}")
    print(f"Roman numerals: {[chord.roman_numeral for chord in result.functional.chords]}")

if result.modal:
    print(f"Modal characteristics: {result.modal.modal_characteristics}")

if result.chromatic:
    print(f"Secondary dominants: {len(result.chromatic.secondary_dominants)}")
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
pytest --cov=music_theory_analysis --cov-report=html
```

## Development

### Setting up for development

```bash
git clone https://github.com/sammywachtel/music-theory-analysis-py.git
cd music-theory-analysis-py
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
@software{music_theory_analysis,
  title = {Music Theory Analysis: A Comprehensive Python Library},
  author = {Wachtel, Sam},
  year = {2025},
  url = {https://github.com/sammywachtel/music-theory-analysis-py}
}
```

## Related Projects

This library was extracted from the [Music Modes App](https://github.com/sammywachtel/music_modes_app), a comprehensive music theory toolkit with React frontend and FastAPI backend.
