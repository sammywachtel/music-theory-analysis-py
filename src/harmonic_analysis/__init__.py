"""Music Theory Analysis Library.

A comprehensive Python library for music theory analysis, providing sophisticated
algorithms for functional harmony, modal analysis, and chromatic harmony detection.
"""

__version__ = "0.2.0rc2"

# Main user-facing analysis functions
from .analysis import analyze_chord_progression, analyze_melody, analyze_scale
from .core.chromatic_analysis import (
    BorrowedChord,
    ChromaticAnalysisResult,
    ChromaticAnalyzer,
    ChromaticMediant,
    ResolutionPattern,
    ResolutionType,
    SecondaryDominant,
    analyze_chromatic_harmony,
)

# Core analysis engines (for advanced users)
from .core.enhanced_modal_analyzer import (
    ChordAnalysis,
    EnhancedModalAnalyzer,
    EvidenceType,
    ModalAnalysisResult,
    ModalEvidence,
    ModalPattern,
    PatternContext,
    analyze_modal_progression,
)
from .core.functional_harmony import (
    Cadence,
    ChordFunction,
    ChromaticType,
    FunctionalAnalysisResult,
    FunctionalChordAnalysis,
    FunctionalHarmonyAnalyzer,
    ProgressionType,
)
from .scale_melody_analysis import (
    ScaleMelodyAnalysisResult,
    ScaleMelodyAnalyzer,
    analyze_scale_melody,
)

# Services
from .services.comprehensive_analysis import (
    ComprehensiveAnalysisEngine,
    ComprehensiveAnalysisResult,
    ModalEnhancementResult,
)
from .services.multiple_interpretation_service import (
    AlternativeAnalysis,
    AnalysisEvidence,
    InterpretationAnalysis,
    InterpretationType,
    MultipleInterpretationService,
    PedagogicalLevel,
    analyze_progression_multiple,
    multiple_interpretation_service,
)

# Core analysis types and results
from .types import AnalysisOptions, UserInputContext

# Utilities (for advanced users)
from .utils.chord_parser import (
    NOTE_NAMES,
    NOTE_NAMES_FLAT,
    NOTE_NAMES_SHARP,
    NOTE_TO_PITCH_CLASS,
    ChordMatch,
    ChordParser,
    ChordTemplate,
    find_chords_from_midi,
    parse_chord,
    parse_chord_progression,
)
from .utils.scales import (
    MAJOR_SCALE_MODES,
    MODAL_PARENT_KEYS,
    PITCH_CLASS_NAMES,
    ScaleData,
)

__all__ = [
    # Version
    "__version__",
    # Main API functions
    "analyze_chord_progression",
    "analyze_melody",
    "analyze_scale",
    # Core types
    "AnalysisOptions",
    "UserInputContext",
    # Multiple interpretation service
    "AlternativeAnalysis",
    "AnalysisEvidence",
    "InterpretationAnalysis",
    "InterpretationType",
    "MultipleInterpretationService",
    "PedagogicalLevel",
    "analyze_progression_multiple",
    "multiple_interpretation_service",
    # Scale/melody analysis
    "ScaleMelodyAnalysisResult",
    "ScaleMelodyAnalyzer",
    "analyze_scale_melody",
    # Core analysis engines
    "ChordAnalysis",
    "EnhancedModalAnalyzer",
    "EvidenceType",
    "ModalAnalysisResult",
    "ModalEvidence",
    "ModalPattern",
    "PatternContext",
    "analyze_modal_progression",
    "Cadence",
    "ChordFunction",
    "ChromaticType",
    "FunctionalAnalysisResult",
    "FunctionalChordAnalysis",
    "FunctionalHarmonyAnalyzer",
    "ProgressionType",
    "BorrowedChord",
    "ChromaticAnalysisResult",
    "ChromaticAnalyzer",
    "ChromaticMediant",
    "ResolutionPattern",
    "ResolutionType",
    "SecondaryDominant",
    "analyze_chromatic_harmony",
    # Services
    "ComprehensiveAnalysisEngine",
    "ComprehensiveAnalysisResult",
    "ModalEnhancementResult",
    # Utilities
    "ChordMatch",
    "ChordParser",
    "ChordTemplate",
    "parse_chord_progression",
    "find_chords_from_midi",
    "parse_chord",
    "NOTE_TO_PITCH_CLASS",
    "NOTE_NAMES",
    "NOTE_NAMES_SHARP",
    "NOTE_NAMES_FLAT",
    "ScaleData",
    "MAJOR_SCALE_MODES",
    "MODAL_PARENT_KEYS",
    "PITCH_CLASS_NAMES",
]
