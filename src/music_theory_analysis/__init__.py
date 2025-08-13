"""
Music Theory Analysis Library

A comprehensive Python library for music theory analysis, providing sophisticated 
algorithms for functional harmony, modal analysis, and chromatic harmony detection.
"""

__version__ = "0.1.0"

# Core analysis engines
from .comprehensive_analysis import (
    ComprehensiveAnalysisEngine,
    ComprehensiveAnalysisResult,
    ModalEnhancementResult,
    ChromaticAnalysisResult,
)

# Functional harmony analysis
from .functional_harmony import (
    FunctionalHarmonyAnalyzer,
    FunctionalAnalysisResult,
    FunctionalChordAnalysis,
    ChordFunction,
    ChromaticType,
    ProgressionType,
    Cadence,
)

# Modal analysis
from .modal_analysis import (
    EnhancedModalAnalyzer,
    ModalAnalysisResult,
    ModalEvidence,
)

# Chord logic and parsing
from .chord_logic import (
    ChordParser,
    ChordMatch,
    parse_chord_progression,
)

# Scale data and constants
from .scales import (
    ScaleData,
    MAJOR_SCALE_MODES,
    MODAL_PARENT_KEYS,
    NOTE_TO_PITCH_CLASS,
    PITCH_CLASS_NAMES,
)

# Types and interfaces
from .types import (
    UserInputContext,
    AnalysisOptions,
    MultipleInterpretationResult,
)

__all__ = [
    # Version
    "__version__",
    
    # Core analysis
    "ComprehensiveAnalysisEngine",
    "ComprehensiveAnalysisResult",
    "ModalEnhancementResult", 
    "ChromaticAnalysisResult",
    
    # Functional harmony
    "FunctionalHarmonyAnalyzer",
    "FunctionalAnalysisResult",
    "FunctionalChordAnalysis",
    "ChordFunction",
    "ChromaticType",
    "ProgressionType",
    "Cadence",
    
    # Modal analysis
    "EnhancedModalAnalyzer",
    "ModalAnalysisResult",
    "ModalEvidence",
    
    # Chord logic
    "ChordParser",
    "ChordMatch",
    "parse_chord_progression",
    
    # Scale data
    "ScaleData",
    "MAJOR_SCALE_MODES",
    "MODAL_PARENT_KEYS", 
    "NOTE_TO_PITCH_CLASS",
    "PITCH_CLASS_NAMES",
    
    # Types
    "UserInputContext",
    "AnalysisOptions",
    "MultipleInterpretationResult",
]