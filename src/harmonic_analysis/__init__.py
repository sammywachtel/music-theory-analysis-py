"""
Music Theory Analysis Library

A comprehensive Python library for music theory analysis, providing sophisticated
algorithms for functional harmony, modal analysis, and chromatic harmony detection.
"""

__version__ = "0.1.0b1"

# Chord logic and parsing
from .chord_parser import (NOTE_NAMES, NOTE_NAMES_FLAT, NOTE_NAMES_SHARP,
                           NOTE_TO_PITCH_CLASS, ChordMatch, ChordParser,
                           ChordTemplate, find_chords_from_midi, parse_chord,
                           parse_chord_progression)
# Chromatic analysis
from .chromatic_analysis import (BorrowedChord, ChromaticAnalysisResult,
                                 ChromaticAnalyzer, ChromaticMediant,
                                 ResolutionPattern, ResolutionType,
                                 SecondaryDominant, analyze_chromatic_harmony)
# Core analysis engines
from .comprehensive_analysis import (ComprehensiveAnalysisEngine,
                                     ComprehensiveAnalysisResult,
                                     ModalEnhancementResult)
# Modal analysis
from .enhanced_modal_analyzer import (ChordAnalysis, EnhancedModalAnalyzer,
                                      EvidenceType, ModalAnalysisResult,
                                      ModalEvidence, ModalPattern,
                                      PatternContext,
                                      analyze_modal_progression)
# Functional harmony analysis
from .functional_harmony import (Cadence, ChordFunction, ChromaticType,
                                 FunctionalAnalysisResult,
                                 FunctionalChordAnalysis,
                                 FunctionalHarmonyAnalyzer, ProgressionType)
# Multiple interpretation service
from .multiple_interpretation_service import (AlternativeAnalysis,
                                              AnalysisEvidence,
                                              InterpretationAnalysis,
                                              InterpretationType,
                                              MultipleInterpretationService,
                                              PedagogicalLevel,
                                              analyze_progression_multiple,
                                              multiple_interpretation_service)
# Scale data and constants
from .scales import (MAJOR_SCALE_MODES, MODAL_PARENT_KEYS, PITCH_CLASS_NAMES,
                     ScaleData)
# Types and interfaces
from .types import AnalysisOptions, UserInputContext

__all__ = [
    # Version
    "__version__",
    # Core analysis
    "ComprehensiveAnalysisEngine",
    "ComprehensiveAnalysisResult",
    "ModalEnhancementResult",
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
    "InterpretationType",
    "PedagogicalLevel",
    "analyze_progression_multiple",
    "multiple_interpretation_service",
    # Types
    "UserInputContext",
    "AnalysisOptions",
]
