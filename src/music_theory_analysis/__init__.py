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
from .enhanced_modal_analyzer import (
    EnhancedModalAnalyzer,
    ModalAnalysisResult,
    ModalEvidence,
    EvidenceType,
    PatternContext,
    ModalPattern,
    ChordAnalysis,
    analyze_modal_progression,
)

# Chromatic analysis
from .chromatic_analysis import (
    ChromaticAnalyzer,
    ChromaticAnalysisResult,
    SecondaryDominant,
    BorrowedChord,
    ChromaticMediant,
    ResolutionPattern,
    ResolutionType,
    analyze_chromatic_harmony,
)

# Chord logic and parsing
from .chord_parser import (
    ChordParser,
    ChordMatch,
    ChordTemplate,
    parse_chord_progression,
    find_chords_from_midi,
    parse_chord,
    NOTE_TO_PITCH_CLASS,
    NOTE_NAMES,
    NOTE_NAMES_SHARP,
    NOTE_NAMES_FLAT,
)

# Scale data and constants
from .scales import (
    ScaleData,
    MAJOR_SCALE_MODES,
    MODAL_PARENT_KEYS,
    PITCH_CLASS_NAMES,
)

# Multiple interpretation service
from .multiple_interpretation_service import (
    MultipleInterpretationService,
    MultipleInterpretationResult,
    InterpretationAnalysis,
    AlternativeAnalysis,
    AnalysisEvidence,
    EvidenceType,
    InterpretationType,
    PedagogicalLevel,
    analyze_progression_multiple,
    multiple_interpretation_service,
)

# Types and interfaces
from .types import (
    UserInputContext,
    AnalysisOptions,
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
    "EvidenceType",
    "PatternContext", 
    "ModalPattern",
    "ChordAnalysis",
    "analyze_modal_progression",
    
    # Chromatic analysis
    "ChromaticAnalyzer",
    "ChromaticAnalysisResult",
    "SecondaryDominant",
    "BorrowedChord",
    "ChromaticMediant",
    "ResolutionPattern",
    "ResolutionType",
    "analyze_chromatic_harmony",
    
    # Chord logic
    "ChordParser",
    "ChordMatch",
    "ChordTemplate",
    "parse_chord_progression",
    "find_chords_from_midi",
    "parse_chord",
    "NOTE_TO_PITCH_CLASS",
    "NOTE_NAMES",
    "NOTE_NAMES_SHARP",
    "NOTE_NAMES_FLAT",
    
    # Scale data
    "ScaleData",
    "MAJOR_SCALE_MODES",
    "MODAL_PARENT_KEYS",
    "PITCH_CLASS_NAMES",
    
    # Multiple interpretation service
    "MultipleInterpretationService",
    "InterpretationAnalysis",
    "AlternativeAnalysis", 
    "AnalysisEvidence",
    "EvidenceType",
    "InterpretationType",
    "PedagogicalLevel",
    "analyze_progression_multiple",
    "multiple_interpretation_service",
    
    # Types
    "UserInputContext",
    "AnalysisOptions",
]