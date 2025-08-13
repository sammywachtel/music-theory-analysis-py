"""
Multiple Interpretation Analysis Service

Provides comprehensive harmonic analysis with multiple valid interpretations,
confidence scoring, and evidence-based reasoning. Transforms the binary
modal/functional approach into a nuanced system that reflects real music
theory practice.

Architecture:
- Orchestrates existing analyzers (functional, modal, chromatic)
- Applies confidence scoring based on harmonic evidence
- Returns multiple valid interpretations ranked by theoretical certainty
- Supports adaptive disclosure for different pedagogical levels
"""

import asyncio
import json
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Union

from .enhanced_modal_analyzer import EnhancedModalAnalyzer, ModalAnalysisResult
from .functional_harmony import FunctionalAnalysisResult, FunctionalHarmonyAnalyzer
from .types import AnalysisOptions


class EvidenceType(Enum):
    """Types of analytical evidence"""

    HARMONIC = "harmonic"
    STRUCTURAL = "structural"
    CADENTIAL = "cadential"
    INTERVALLIC = "intervallic"
    CONTEXTUAL = "contextual"


class InterpretationType(Enum):
    """Types of harmonic interpretation"""

    FUNCTIONAL = "functional"
    MODAL = "modal"
    CHROMATIC = "chromatic"


class PedagogicalLevel(Enum):
    """Pedagogical levels for adaptive disclosure"""

    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


@dataclass
class AnalysisEvidence:
    """Evidence supporting an analytical interpretation"""

    type: EvidenceType
    strength: float  # 0.0 to 1.0
    description: str
    supported_interpretations: List[InterpretationType]
    musical_basis: str  # Theoretical explanation


@dataclass
class InterpretationAnalysis:
    """A single analytical interpretation with confidence"""

    type: InterpretationType
    confidence: float  # 0.0 to 1.0
    analysis: str
    roman_numerals: Optional[str] = None
    key_signature: Optional[str] = None
    mode: Optional[str] = None
    evidence: List[AnalysisEvidence] = field(default_factory=list)
    reasoning: str = ""
    theoretical_basis: str = ""


@dataclass
class AlternativeAnalysis(InterpretationAnalysis):
    """Alternative analysis with relationship to primary"""

    relationship_to_primary: str = ""


@dataclass
class MultipleInterpretationMetadata:
    """Metadata about the interpretation analysis"""

    total_interpretations_considered: int
    confidence_threshold: float
    show_alternatives: bool
    pedagogical_level: PedagogicalLevel
    analysis_time_ms: float


@dataclass
class MultipleInterpretationResult:
    """Complete result of multiple interpretation analysis"""

    primary_analysis: InterpretationAnalysis
    alternative_analyses: List[AlternativeAnalysis]
    metadata: MultipleInterpretationMetadata
    input_chords: List[str]
    input_options: Optional[AnalysisOptions] = None


# Confidence framework based on music theory expert guidance
CONFIDENCE_LEVELS = {
    "definitive": {
        "min": 0.85,
        "max": 1.0,
        "description": "Unambiguous harmonic markers present",
    },
    "strong": {
        "min": 0.65,
        "max": 0.84,
        "description": "Clear evidence with minimal ambiguity",
    },
    "moderate": {
        "min": 0.45,
        "max": 0.64,
        "description": "Valid interpretation with competing possibilities",
    },
    "weak": {
        "min": 0.25,
        "max": 0.44,
        "description": "Theoretically possible but lacks context",
    },
    "insufficient": {
        "min": 0.0,
        "max": 0.24,
        "description": "Requires significant assumptions",
    },
}

# Evidence weighting based on theoretical importance
EVIDENCE_WEIGHTS = {
    EvidenceType.CADENTIAL: 0.4,  # bVII-I, V-I, bII-I patterns
    EvidenceType.STRUCTURAL: 0.25,  # First/last chord relationships
    EvidenceType.INTERVALLIC: 0.2,  # Distinctive scale degrees (bVII, bII, etc.)
    EvidenceType.HARMONIC: 0.15,  # Key signature, chord qualities
    EvidenceType.CONTEXTUAL: 0.15,  # Overall context
}


class AnalysisCache:
    """Simple cache for performance optimization"""

    def __init__(self, max_size: int = 100, ttl_minutes: int = 5):
        self.cache: Dict[str, MultipleInterpretationResult] = {}
        self.timestamps: Dict[str, datetime] = {}
        self.max_size = max_size
        self.ttl = timedelta(minutes=ttl_minutes)

    def get(self, key: str) -> Optional[MultipleInterpretationResult]:
        """Get cached result if still valid"""
        if key not in self.cache:
            return None

        # Check TTL
        if datetime.now() - self.timestamps[key] > self.ttl:
            del self.cache[key]
            del self.timestamps[key]
            return None

        return self.cache[key]

    def set(self, key: str, result: MultipleInterpretationResult) -> None:
        """Cache result with LRU eviction"""
        # Implement LRU by clearing oldest entries
        if len(self.cache) >= self.max_size:
            oldest_key = min(self.timestamps.keys(), key=lambda k: self.timestamps[k])
            del self.cache[oldest_key]
            del self.timestamps[oldest_key]

        self.cache[key] = result
        self.timestamps[key] = datetime.now()

    def get_cache_key(
        self, chords: List[str], options: Optional[AnalysisOptions] = None
    ) -> str:
        """Generate cache key from input"""
        options_str = json.dumps(options.__dict__ if options else {}, sort_keys=True)
        return f"{'_'.join(chords)}_{hash(options_str)}"


class MultipleInterpretationService:
    """Service for multiple interpretation analysis"""

    def __init__(self):
        self.cache = AnalysisCache()
        self.functional_analyzer = FunctionalHarmonyAnalyzer()
        self.modal_analyzer = EnhancedModalAnalyzer()

    async def analyze_progression(
        self, chords: List[str], options: Optional[AnalysisOptions] = None
    ) -> MultipleInterpretationResult:
        """
        Main entry point for multiple interpretation analysis

        Args:
            chords: List of chord symbols
            options: Analysis options

        Returns:
            Complete multiple interpretation analysis result
        """
        if not chords:
            raise ValueError("Empty chord progression provided")

        start_time = time.time()

        if options is None:
            options = AnalysisOptions()

        cache_key = self.cache.get_cache_key(chords, options)

        # Check cache first
        cached = self.cache.get(cache_key)
        if cached:
            return cached

        try:
            # Set defaults
            pedagogical_level = (
                PedagogicalLevel(options.pedagogical_level)
                if options.pedagogical_level
                else PedagogicalLevel.INTERMEDIATE
            )
            confidence_threshold = (
                options.confidence_threshold
                if options.confidence_threshold is not None
                else 0.5
            )
            max_alternatives = (
                options.max_alternatives if options.max_alternatives is not None else 3
            )

            # Run parallel analysis
            functional_result, modal_result = await asyncio.gather(
                self._run_functional_analysis(chords, options),
                self._run_modal_analysis(chords, options),
                return_exceptions=True,
            )

            # Handle exceptions
            if isinstance(functional_result, Exception):
                functional_result = None
            if isinstance(modal_result, Exception):
                modal_result = None

            # Calculate interpretations with confidence scoring
            interpretations = await self._calculate_interpretations(
                chords, functional_result, modal_result, options
            )

            # Rank and filter interpretations
            ranked_interpretations = self._rank_interpretations(interpretations)
            filtered_alternatives = self._filter_alternatives(
                ranked_interpretations, confidence_threshold, max_alternatives
            )

            # Create result
            analysis_time_ms = (time.time() - start_time) * 1000

            result = MultipleInterpretationResult(
                primary_analysis=(
                    ranked_interpretations[0]
                    if ranked_interpretations
                    else self._create_fallback_interpretation(chords)
                ),
                alternative_analyses=filtered_alternatives,
                metadata=MultipleInterpretationMetadata(
                    total_interpretations_considered=len(interpretations),
                    confidence_threshold=confidence_threshold,
                    show_alternatives=self._should_show_alternatives(
                        ranked_interpretations,
                        pedagogical_level,
                        options.force_multiple_interpretations or False,
                    ),
                    pedagogical_level=pedagogical_level,
                    analysis_time_ms=analysis_time_ms,
                ),
                input_chords=chords,
                input_options=options,
            )

            # Cache result
            self.cache.set(cache_key, result)

            return result

        except Exception as error:
            raise Exception(f"Multiple interpretation analysis failed: {str(error)}")

    async def _run_functional_analysis(
        self, chords: List[str], options: AnalysisOptions
    ) -> Optional[FunctionalAnalysisResult]:
        """Run functional harmony analysis"""
        try:
            return await self.functional_analyzer.analyze_functionally(
                chords, options.parent_key
            )
        except Exception as e:
            print(f"Warning: Functional analysis failed: {e}")
            return None

    async def _run_modal_analysis(
        self, chords: List[str], options: AnalysisOptions
    ) -> Optional[ModalAnalysisResult]:
        """Run modal analysis"""
        try:
            return self.modal_analyzer.analyze_modal_characteristics(
                chords, options.parent_key
            )
        except Exception as e:
            print(f"Warning: Modal analysis failed: {e}")
            return None

    async def _calculate_interpretations(
        self,
        chords: List[str],
        functional_result: Optional[FunctionalAnalysisResult],
        modal_result: Optional[ModalAnalysisResult],
        options: AnalysisOptions,
    ) -> List[InterpretationAnalysis]:
        """Calculate all possible interpretations with confidence scores"""
        interpretations: List[InterpretationAnalysis] = []

        # Functional interpretation
        if functional_result:
            functional_interp = self._create_functional_interpretation(
                chords, functional_result, options
            )
            if functional_interp:
                interpretations.append(functional_interp)

        # Modal interpretation
        if modal_result:
            modal_interp = self._create_modal_interpretation(
                chords, modal_result, options
            )
            if modal_interp:
                interpretations.append(modal_interp)

        return interpretations

    def _create_functional_interpretation(
        self,
        chords: List[str],
        functional_result: FunctionalAnalysisResult,
        options: AnalysisOptions,
    ) -> Optional[InterpretationAnalysis]:
        """Create functional interpretation with confidence scoring"""
        try:
            evidence = self._collect_functional_evidence(chords, functional_result)
            confidence = self._calculate_confidence(evidence)

            return InterpretationAnalysis(
                type=InterpretationType.FUNCTIONAL,
                confidence=confidence,
                analysis=functional_result.explanation or "Functional progression",
                roman_numerals=" ".join(
                    [chord.roman_numeral for chord in functional_result.chords]
                ),
                key_signature=functional_result.key_center or options.parent_key,
                evidence=evidence,
                reasoning=self._generate_functional_reasoning(
                    functional_result, evidence
                ),
                theoretical_basis="Functional tonal harmony analysis based on Roman numeral progressions",
            )
        except Exception as e:
            print(f"Warning: Failed to create functional interpretation: {e}")
            return None

    def _create_modal_interpretation(
        self,
        chords: List[str],
        modal_result: ModalAnalysisResult,
        options: AnalysisOptions,
    ) -> Optional[InterpretationAnalysis]:
        """Create modal interpretation with confidence scoring"""
        try:
            evidence = self._collect_modal_evidence(chords, modal_result)
            confidence = self._calculate_confidence(evidence)

            return InterpretationAnalysis(
                type=InterpretationType.MODAL,
                confidence=confidence,
                analysis=f"{modal_result.mode_name} modal progression",
                mode=modal_result.mode_name,
                key_signature=modal_result.parent_key_signature,
                evidence=evidence,
                reasoning=self._generate_modal_reasoning(modal_result, evidence),
                theoretical_basis="Modal analysis based on characteristic scale degrees and harmonic patterns",
            )
        except Exception as e:
            print(f"Warning: Failed to create modal interpretation: {e}")
            return None

    def _collect_functional_evidence(
        self, chords: List[str], functional_result: FunctionalAnalysisResult
    ) -> List[AnalysisEvidence]:
        """Collect evidence for functional analysis"""
        evidence: List[AnalysisEvidence] = []

        # Cadential evidence
        if functional_result.cadences:
            cadence = functional_result.cadences[0]
            cadence_name = getattr(
                cadence, "name", getattr(cadence, "type", "authentic")
            )
            evidence.append(
                AnalysisEvidence(
                    type=EvidenceType.CADENTIAL,
                    strength=0.9,
                    description="Clear cadential progression identified",
                    supported_interpretations=[InterpretationType.FUNCTIONAL],
                    musical_basis=f"{cadence_name} cadence provides tonal resolution",
                )
            )

        # Structural framing
        if len(chords) >= 3 and chords[0] == chords[-1]:
            evidence.append(
                AnalysisEvidence(
                    type=EvidenceType.STRUCTURAL,
                    strength=0.7,
                    description="Strong tonic framing",
                    supported_interpretations=[
                        InterpretationType.FUNCTIONAL,
                        InterpretationType.MODAL,
                    ],
                    musical_basis="First and last chords establish tonic center",
                )
            )

        # Roman numeral clarity
        if functional_result.confidence >= 0.5:
            evidence.append(
                AnalysisEvidence(
                    type=EvidenceType.HARMONIC,
                    strength=functional_result.confidence,
                    description="Clear functional harmonic progression",
                    supported_interpretations=[InterpretationType.FUNCTIONAL],
                    musical_basis="Roman numeral analysis shows clear tonal relationships",
                )
            )

        # Strong Roman numeral progression (I-vi-IV-V type progressions)
        if len(functional_result.chords) >= 3:
            roman_numerals = [chord.roman_numeral for chord in functional_result.chords]
            if any(rn in ["I", "i"] for rn in roman_numerals):
                evidence.append(
                    AnalysisEvidence(
                        type=EvidenceType.STRUCTURAL,
                        strength=0.8,
                        description="Strong tonal center establishment",
                        supported_interpretations=[InterpretationType.FUNCTIONAL],
                        musical_basis="Roman numeral progression shows clear tonic-based functional relationships",
                    )
                )

        return evidence

    def _collect_modal_evidence(
        self, chords: List[str], modal_result: ModalAnalysisResult
    ) -> List[AnalysisEvidence]:
        """Collect evidence for modal analysis"""
        evidence: List[AnalysisEvidence] = []

        # Modal characteristics
        for modal_evidence in modal_result.evidence:
            chord_info = getattr(
                modal_evidence,
                "chord",
                getattr(modal_evidence, "pattern", str(modal_evidence)),
            )
            evidence.append(
                AnalysisEvidence(
                    type=EvidenceType.INTERVALLIC,
                    strength=0.85,
                    description=f"{chord_info} indicates {modal_result.mode_name} characteristics",
                    supported_interpretations=[InterpretationType.MODAL],
                    musical_basis=f"{chord_info} is characteristic of {modal_result.mode_name} mode",
                )
            )

        # Overall modal confidence
        evidence.append(
            AnalysisEvidence(
                type=EvidenceType.CONTEXTUAL,
                strength=modal_result.confidence,
                description="Overall modal characteristics present",
                supported_interpretations=[InterpretationType.MODAL],
                musical_basis="Combined modal features suggest modal interpretation",
            )
        )

        return evidence

    def _calculate_confidence(self, evidence: List[AnalysisEvidence]) -> float:
        """Calculate overall confidence based on evidence"""
        if not evidence:
            return 0.2

        # Weighted average based on evidence types
        total_weight = 0.0
        weighted_sum = 0.0

        for ev in evidence:
            weight = EVIDENCE_WEIGHTS.get(ev.type, 0.1)
            total_weight += weight
            weighted_sum += ev.strength * weight

        base_confidence = weighted_sum / total_weight if total_weight > 0 else 0.2

        # Bonus for multiple evidence types
        evidence_types = {ev.type for ev in evidence}
        diversity_bonus = 0.1 if len(evidence_types) > 1 else 0

        return min(1.0, base_confidence + diversity_bonus)

    def _generate_functional_reasoning(
        self,
        functional_result: FunctionalAnalysisResult,
        evidence: List[AnalysisEvidence],
    ) -> str:
        """Generate reasoning for functional interpretation"""
        reasons = []

        if functional_result.cadences:
            cadence = functional_result.cadences[0]
            cadence_name = getattr(
                cadence, "name", getattr(cadence, "type", "authentic")
            )
            reasons.append(
                f"Strong {cadence_name} cadence establishes functional tonality"
            )

        if functional_result.chords:
            reasons.append(
                "Clear Roman numeral progression supports functional analysis"
            )

        if any(
            e.type == EvidenceType.STRUCTURAL and e.strength > 0.6 for e in evidence
        ):
            reasons.append("Tonic framing reinforces key center")

        return (
            "; ".join(reasons)
            if reasons
            else "Functional harmonic progression with clear tonal relationships"
        )

    def _generate_modal_reasoning(
        self, modal_result: ModalAnalysisResult, evidence: List[AnalysisEvidence]
    ) -> str:
        """Generate reasoning for modal interpretation"""
        reasons = []

        if modal_result.evidence:
            first_evidence = modal_result.evidence[0]
            chord_info = getattr(
                first_evidence,
                "chord",
                getattr(first_evidence, "pattern", str(first_evidence)),
            )
            reasons.append(
                f"{chord_info} is characteristic of {modal_result.mode_name} mode"
            )

        if any(e.type == EvidenceType.INTERVALLIC for e in evidence):
            reasons.append("Distinctive modal scale degrees present")

        return (
            "; ".join(reasons)
            if reasons
            else f"Modal characteristics suggest {modal_result.mode_name} interpretation"
        )

    def _rank_interpretations(
        self, interpretations: List[InterpretationAnalysis]
    ) -> List[InterpretationAnalysis]:
        """Rank interpretations by confidence"""
        return sorted(
            [interp for interp in interpretations if interp.confidence > 0.2],
            key=lambda x: x.confidence,
            reverse=True,
        )

    def _filter_alternatives(
        self,
        ranked_interpretations: List[InterpretationAnalysis],
        confidence_threshold: float,
        max_alternatives: int,
    ) -> List[AlternativeAnalysis]:
        """Filter alternatives based on confidence and limits"""
        if len(ranked_interpretations) <= 1:
            return []

        primary = ranked_interpretations[0]
        alternatives = ranked_interpretations[1 : max_alternatives + 1]

        filtered_alternatives = []
        for alt in alternatives:
            if alt.confidence >= confidence_threshold:
                alt_analysis = AlternativeAnalysis(
                    type=alt.type,
                    confidence=alt.confidence,
                    analysis=alt.analysis,
                    roman_numerals=alt.roman_numerals,
                    key_signature=alt.key_signature,
                    mode=alt.mode,
                    evidence=alt.evidence,
                    reasoning=alt.reasoning,
                    theoretical_basis=alt.theoretical_basis,
                    relationship_to_primary=self._generate_relationship_description(
                        primary, alt
                    ),
                )
                filtered_alternatives.append(alt_analysis)

        return filtered_alternatives

    def _generate_relationship_description(
        self, primary: InterpretationAnalysis, alternative: InterpretationAnalysis
    ) -> str:
        """Generate description of relationship between interpretations"""
        if (
            primary.type == InterpretationType.FUNCTIONAL
            and alternative.type == InterpretationType.MODAL
        ):
            return "Modal interpretation emphasizes scale degrees over functional harmonic relationships"
        elif (
            primary.type == InterpretationType.MODAL
            and alternative.type == InterpretationType.FUNCTIONAL
        ):
            return "Functional interpretation emphasizes tonal chord progressions over modal characteristics"
        else:
            return "Alternative analytical perspective on the same harmonic content"

    def _should_show_alternatives(
        self,
        interpretations: List[InterpretationAnalysis],
        pedagogical_level: PedagogicalLevel,
        force_multiple: bool,
    ) -> bool:
        """Determine whether to show alternatives"""
        if force_multiple:
            return True
        if len(interpretations) <= 1:
            return False

        primary = interpretations[0]
        best_alternative = interpretations[1] if len(interpretations) > 1 else None

        # Always show for advanced users
        if pedagogical_level == PedagogicalLevel.ADVANCED:
            return True

        # For beginners, only show if primary isn't highly confident
        if pedagogical_level == PedagogicalLevel.BEGINNER:
            return primary.confidence < 0.8

        # For intermediate, show if alternative is reasonably strong
        if best_alternative:
            return (primary.confidence - best_alternative.confidence) < 0.3

        return False

    def _create_fallback_interpretation(
        self, chords: List[str]
    ) -> InterpretationAnalysis:
        """Create fallback interpretation when analysis fails"""
        return InterpretationAnalysis(
            type=InterpretationType.FUNCTIONAL,
            confidence=0.3,
            analysis=f"Basic chord progression: {' - '.join(chords)}",
            reasoning="Analysis completed with limited harmonic information",
            theoretical_basis="Basic chord progression analysis",
        )


# Export singleton instance
multiple_interpretation_service = MultipleInterpretationService()


async def analyze_progression_multiple(
    chords: List[str], options: Optional[AnalysisOptions] = None
) -> MultipleInterpretationResult:
    """
    Convenience function for multiple interpretation analysis

    Args:
        chords: List of chord symbols
        options: Analysis options

    Returns:
        Complete multiple interpretation result
    """
    return await multiple_interpretation_service.analyze_progression(chords, options)
