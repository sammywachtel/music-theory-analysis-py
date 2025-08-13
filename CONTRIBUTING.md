# Contributing to Music Theory Analysis

We welcome contributions to the Music Theory Analysis library! This document provides guidelines for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Contributing Process](#contributing-process)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Submitting Changes](#submitting-changes)

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to sammywachtel@gmail.com.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Basic understanding of music theory concepts

### Areas for Contribution

We welcome contributions in the following areas:

1. **Algorithm Improvements**: Enhance existing analysis algorithms
2. **New Features**: Add support for additional music theory concepts
3. **Performance Optimization**: Improve speed and memory usage
4. **Documentation**: Improve examples, tutorials, and API documentation
5. **Testing**: Add test cases and improve coverage
6. **Bug Fixes**: Fix issues and edge cases

## Development Setup

1. **Fork the repository** on GitHub

2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/yourusername/music-theory-analysis-py.git
   cd music-theory-analysis-py
   ```

3. **Set up the development environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e ".[dev,test]"
   ```

4. **Install pre-commit hooks**:
   ```bash
   pre-commit install
   ```

5. **Verify the setup**:
   ```bash
   pytest
   mypy src/
   black --check src/ tests/
   flake8 src/ tests/
   ```

## Contributing Process

1. **Create a feature branch** from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following our coding standards

3. **Write or update tests** for your changes

4. **Update documentation** if necessary

5. **Run the full test suite**:
   ```bash
   pytest
   ```

6. **Run quality checks**:
   ```bash
   pre-commit run --all-files
   ```

7. **Commit your changes** with descriptive messages:
   ```bash
   git add .
   git commit -m "feat: add support for augmented sixth chords"
   ```

8. **Push to your fork** and **create a pull request**

## Coding Standards

### Python Style

We follow PEP 8 with some modifications:

- **Line length**: 88 characters (Black default)
- **Imports**: Organized with isort, grouped by standard library, third-party, local
- **Type hints**: Required for all public functions and methods
- **Docstrings**: Google-style docstrings for all public APIs

### Code Quality Tools

We use several tools to maintain code quality:

- **Black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting
- **mypy**: Type checking
- **pre-commit**: Git hooks for quality checks

### Naming Conventions

- **Functions and variables**: `snake_case`
- **Classes**: `PascalCase`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private methods**: `_leading_underscore`
- **Files and modules**: `snake_case`

### Example Code Style

```python
from typing import List, Optional, Tuple
from dataclasses import dataclass

from .types import ChordFunction


@dataclass
class FunctionalChordAnalysis:
    """Analysis result for a single chord in functional harmony context.
    
    Args:
        chord_symbol: The chord symbol (e.g., "Cm7")
        roman_numeral: Roman numeral analysis (e.g., "ii7")
        function: Harmonic function of the chord
        confidence: Analysis confidence (0.0 to 1.0)
    """
    chord_symbol: str
    roman_numeral: str
    function: ChordFunction
    confidence: float
    
    def is_high_confidence(self) -> bool:
        """Check if analysis confidence is above threshold.
        
        Returns:
            True if confidence >= 0.7, False otherwise
        """
        return self.confidence >= 0.7


def analyze_chord_function(
    chord_symbol: str,
    key_center: str,
    mode: str = "major"
) -> FunctionalChordAnalysis:
    """Analyze the harmonic function of a chord in context.
    
    Args:
        chord_symbol: Chord to analyze (e.g., "Dm7")
        key_center: Tonal center (e.g., "C")
        mode: Mode context ("major" or "minor")
        
    Returns:
        Functional analysis result with Roman numeral and function
        
    Raises:
        ValueError: If chord_symbol or key_center is invalid
    """
    if not chord_symbol.strip():
        raise ValueError("Chord symbol cannot be empty")
        
    # Implementation details...
    return FunctionalChordAnalysis(
        chord_symbol=chord_symbol,
        roman_numeral="ii7",
        function=ChordFunction.PREDOMINANT,
        confidence=0.85
    )
```

## Testing

### Test Structure

We organize tests by category and scope:

```
tests/
├── unit/           # Unit tests for individual components
├── integration/    # Integration tests for component interaction
├── functional/     # End-to-end functional tests
├── generated/      # Generated test cases from scripts
└── fixtures/       # Test data and fixtures
```

### Test Categories

Use pytest markers to categorize tests:

```python
import pytest

@pytest.mark.unit
def test_chord_parsing():
    """Unit test for chord parsing logic."""
    pass

@pytest.mark.modal
def test_modal_detection():
    """Test modal analysis specifically."""
    pass

@pytest.mark.slow
def test_comprehensive_analysis():
    """Long-running comprehensive test."""
    pass
```

### Writing Good Tests

1. **Descriptive names**: Test function names should describe what is being tested
2. **Arrange, Act, Assert**: Structure tests clearly
3. **Test edge cases**: Include boundary conditions and error cases
4. **Use fixtures**: Share test data and setup code
5. **Parameterize**: Use `pytest.mark.parametrize` for multiple similar test cases

### Example Test

```python
import pytest
from music_theory_analysis import ComprehensiveAnalysisEngine

class TestFunctionalAnalysis:
    
    @pytest.fixture
    def analyzer(self):
        """Fixture providing a configured analysis engine."""
        return ComprehensiveAnalysisEngine()
    
    @pytest.mark.parametrize("progression,expected_key", [
        ("C F G C", "C major"),
        ("Am Dm G Am", "A minor"),
        ("G C D G", "G major"),
    ])
    def test_key_detection(self, analyzer, progression, expected_key):
        """Test key center detection for common progressions."""
        result = analyzer.analyze_comprehensively(progression)
        assert result.functional.key_center == expected_key
        assert result.confidence > 0.7
    
    def test_invalid_progression_raises_error(self, analyzer):
        """Test that invalid input raises appropriate error."""
        with pytest.raises(ValueError, match="empty progression"):
            analyzer.analyze_comprehensively("")
```

## Documentation

### API Documentation

- Use Google-style docstrings for all public functions and classes
- Include examples in docstrings where helpful
- Document parameter types and return values
- Note any exceptions that may be raised

### Code Comments

- Use comments sparingly, prefer self-documenting code
- Explain **why** something is done, not **what** is done
- Comment complex algorithms or non-obvious business logic
- Keep comments up-to-date with code changes

### Examples and Tutorials

When adding new features, consider adding:

- Usage examples in docstrings
- Tutorial notebooks in `docs/examples/`
- Updates to the main README if it affects the public API

## Submitting Changes

### Pull Request Process

1. **Update documentation** for any user-facing changes
2. **Add tests** that cover your changes
3. **Ensure all tests pass** and quality checks pass
4. **Write a clear PR description** explaining:
   - What changes were made
   - Why they were made  
   - Any breaking changes
   - How to test the changes

### Commit Message Format

We follow conventional commits format:

```
type(scope): description

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Adding or updating tests
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `chore`: Maintenance tasks

**Examples:**
- `feat(modal): add Lydian mode detection`
- `fix(parsing): handle enharmonic chord symbols`
- `docs(api): update functional analysis examples`

### Review Process

All submissions require review before merging:

1. **Automated checks** must pass (CI, tests, quality checks)
2. **Code review** by at least one maintainer
3. **Discussion** of any design decisions or concerns
4. **Final approval** and merge by maintainer

### After Your PR is Merged

1. **Delete your feature branch**
2. **Pull the latest main** to stay up-to-date
3. **Consider contributing** to related areas

## Getting Help

If you need help with contributing:

1. **Check existing issues** and discussions
2. **Read the documentation** and examples
3. **Ask questions** in GitHub discussions
4. **Contact maintainers** at sammywachtel@gmail.com

Thank you for contributing to Music Theory Analysis!