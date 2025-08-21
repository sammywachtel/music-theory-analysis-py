# API Usage Guide

## Core API Usage Examples

### Basic Chord Progression Analysis
```python
from harmonic_analysis import analyze_progression_multiple
from harmonic_analysis.types import AnalysisOptions

# Simple analysis
result = await analyze_progression_multiple(['C', 'F', 'G', 'C'])
print(f"Primary: {result.primary_analysis.analysis}")
print(f"Confidence: {result.primary_analysis.confidence:.2f}")

# With options
options = AnalysisOptions(
    parent_key="C major",
    pedagogical_level="intermediate",
    confidence_threshold=0.6,
    max_alternatives=2
)
result = await analyze_progression_multiple(['Am', 'F', 'C', 'G'], options)
```

### Multiple Interpretation Results
```python
# Access primary analysis
primary = result.primary_analysis
print(f"Type: {primary.type}")           # FUNCTIONAL, MODAL, or CHROMATIC
print(f"Analysis: {primary.analysis}")   # Human-readable description
print(f"Roman: {primary.roman_numerals}")# I vi IV V
print(f"Key: {primary.key_signature}")   # C major

# Access alternatives
for alt in result.alternative_analyses:
    print(f"Alternative: {alt.analysis} (confidence: {alt.confidence:.2f})")
    print(f"Relationship: {alt.relationship_to_primary}")
```

### Evidence and Reasoning Access
```python
# Examine analytical evidence
for evidence in result.primary_analysis.evidence:
    print(f"Evidence: {evidence.description}")
    print(f"Strength: {evidence.strength:.2f}")
    print(f"Type: {evidence.type}")
    print(f"Basis: {evidence.musical_basis}")
```

## Integration Patterns

### FastAPI Backend Integration
The library is designed for seamless FastAPI integration:

```python
from fastapi import FastAPI
from harmonic_analysis import analyze_progression_multiple

app = FastAPI()

@app.post("/analyze-chord-progression/")
async def analyze_progression(progression: List[str]):
    result = await analyze_progression_multiple(progression)
    return {
        "primary_analysis": result.primary_analysis,
        "alternatives": result.alternative_analyses,
        "metadata": result.metadata
    }
```

### Frontend Integration Pattern
The library provides structured output for frontend consumption:

```typescript
// TypeScript interface for frontend consumption
interface AnalysisResult {
  primary_analysis: {
    type: "functional" | "modal" | "chromatic";
    analysis: string;
    confidence: number;
    roman_numerals?: string;
    key_signature?: string;
    mode?: string;
    evidence: AnalysisEvidence[];
  };
  alternative_analyses: AlternativeAnalysis[];
  metadata: {
    total_interpretations_considered: number;
    show_alternatives: boolean;
    analysis_time_ms: number;
  };
}
```

## Library Purpose and Intended Usage

### Primary Use Case
This library serves as the **backend analysis engine** for a comprehensive harmonic analysis application. It analyzes chord progressions to provide:

1. **Multiple Analytical Perspectives**: Functional harmony, modal analysis, and chromatic harmony
2. **Educational Context**: Explanations suitable for different pedagogical levels (beginner/intermediate/advanced)
3. **Confidence-Based Results**: Analytical certainty scores to guide user experience
4. **Evidence-Based Reasoning**: Detailed justification for analytical conclusions

### Integration Pattern
The library is designed to be consumed by:
- **FastAPI Backend**: REST endpoints for harmonic progression analysis
- **Frontend Applications**: React/TypeScript harmonic analysis tools
- **Educational Software**: Music theory and harmonic analysis learning applications
- **Analysis Tools**: Standalone harmonic analysis utilities
