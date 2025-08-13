"""
Functional harmony analysis engine.
"""

from dataclasses import dataclass
from typing import List, Optional
from .types import ChordFunction, ChromaticType, ProgressionType
from .chord_logic import ChordMatch, find_chord_matches, determine_chord_function
from .scales import NOTE_TO_PITCH_CLASS, PITCH_CLASS_NAMES


@dataclass
class FunctionalChordAnalysis:
    """Analysis result for a single chord in functional harmony context."""
    chord_symbol: str
    root: int
    chord_name: str
    roman_numeral: str
    figured_bass: str
    inversion: int
    function: ChordFunction
    is_chromatic: bool
    chromatic_type: Optional[ChromaticType] = None
    bass_note: Optional[int] = None


@dataclass
class Cadence:
    """Cadence analysis result."""
    type: str  # 'authentic', 'plagal', 'deceptive', 'half'
    chords: List[FunctionalChordAnalysis]
    strength: float
    position: str  # 'phrase_ending' or 'mid_phrase'


@dataclass
class ChromaticElement:
    """Chromatic harmony element."""
    chord: FunctionalChordAnalysis
    type: ChromaticType
    resolution: Optional[FunctionalChordAnalysis]
    explanation: str


@dataclass
class FunctionalAnalysisResult:
    """Complete functional harmony analysis result."""
    key_center: str
    key_signature: str
    mode: str  # 'major', 'minor', 'modal'
    chords: List[FunctionalChordAnalysis]
    cadences: List[Cadence]
    progression_type: ProgressionType
    confidence: float
    explanation: str
    chromatic_elements: List[ChromaticElement]
    ambiguity_factors: Optional[List[str]] = None


class FunctionalHarmonyAnalyzer:
    """Analyzer for functional harmony progressions."""
    
    def __init__(self):
        # Roman numeral templates
        self.major_romans = ['I', 'ii', 'iii', 'IV', 'V', 'vi', 'vii°']
        self.minor_romans = ['i', 'ii°', 'III', 'iv', 'V', 'VI', 'VII']
        
        # Secondary dominant patterns
        self.secondary_dominants = {
            2: 'V/V',    # D7 in C major
            4: 'V/vi',   # E7 in C major
            7: 'V/ii',   # A7 in C major
            9: 'V/iii',  # B7 in C major
            11: 'V/IV'   # C7 in C major (rare)
        }
    
    async def analyze_functionally(
        self,
        chord_symbols: List[str],
        parent_key: Optional[str] = None
    ) -> FunctionalAnalysisResult:
        """
        Analyze chord progression using functional harmony principles.
        
        Args:
            chord_symbols: List of chord symbols to analyze
            parent_key: Optional key center hint
            
        Returns:
            Complete functional analysis result
        """
        if not chord_symbols:
            raise ValueError("Empty chord progression")
        
        # Parse chords
        chord_matches = find_chord_matches(chord_symbols)
        
        # Determine key center
        key_center, mode = self._determine_key_center(chord_matches, parent_key)
        
        # Analyze each chord
        analyzed_chords = []
        for chord_match in chord_matches:
            analysis = self._analyze_chord(chord_match, key_center, mode)
            analyzed_chords.append(analysis)
        
        # Detect cadences
        cadences = self._detect_cadences(analyzed_chords)
        
        # Identify chromatic elements
        chromatic_elements = self._identify_chromatic_elements(analyzed_chords, key_center, mode)
        
        # Determine progression type
        progression_type = self._determine_progression_type(analyzed_chords, cadences)
        
        # Calculate confidence
        confidence = self._calculate_confidence(analyzed_chords, cadences)
        
        # Generate explanation
        explanation = self._generate_explanation(analyzed_chords, key_center, mode)
        
        # Format key signature
        key_signature = f"{key_center} {mode}"
        
        return FunctionalAnalysisResult(
            key_center=key_center,
            key_signature=key_signature,
            mode=mode,
            chords=analyzed_chords,
            cadences=cadences,
            progression_type=progression_type,
            confidence=confidence,
            explanation=explanation,
            chromatic_elements=chromatic_elements
        )
    
    def _determine_key_center(
        self,
        chord_matches: List[ChordMatch],
        parent_key: Optional[str]
    ) -> tuple[str, str]:
        """Determine the key center and mode from chord progression."""
        if parent_key:
            # Parse parent key if provided
            parts = parent_key.split()
            if len(parts) >= 2:
                key_center = parts[0]
                mode = "minor" if "minor" in parts[1].lower() else "major"
                return key_center, mode
        
        # Simple key detection based on first and last chords
        if chord_matches:
            first_chord = chord_matches[0]
            last_chord = chord_matches[-1]
            
            # If first and last chords are the same, likely tonic
            if first_chord.root == last_chord.root:
                key_center = first_chord.root
                mode = "minor" if first_chord.quality == "minor" else "major"
                return key_center, mode
        
        # Default fallback
        return "C", "major"
    
    def _analyze_chord(
        self,
        chord_match: ChordMatch,
        key_center: str,
        mode: str
    ) -> FunctionalChordAnalysis:
        """Analyze a single chord in functional context."""
        # Calculate Roman numeral
        roman_numeral = self._calculate_roman_numeral(chord_match, key_center, mode)
        
        # Determine function
        function = determine_chord_function(chord_match, key_center, mode)
        
        # Check if chromatic
        is_chromatic = function == ChordFunction.CHROMATIC
        
        # Generate figured bass
        figured_bass = self._generate_figured_bass(chord_match)
        
        return FunctionalChordAnalysis(
            chord_symbol=chord_match.chord_symbol,
            root=chord_match.root_pitch,
            chord_name=f"{chord_match.root} {chord_match.quality}",
            roman_numeral=roman_numeral,
            figured_bass=figured_bass,
            inversion=chord_match.inversion,
            function=function,
            is_chromatic=is_chromatic,
            bass_note=chord_match.bass_pitch
        )
    
    def _calculate_roman_numeral(
        self,
        chord_match: ChordMatch,
        key_center: str,
        mode: str
    ) -> str:
        """Calculate Roman numeral for chord in key context."""
        key_pitch = NOTE_TO_PITCH_CLASS.get(key_center, 0)
        chord_pitch = chord_match.root_pitch
        
        scale_degree = (chord_pitch - key_pitch) % 12
        
        # Get basic Roman numeral
        if mode == "major":
            roman_map = {0: 'I', 2: 'ii', 4: 'iii', 5: 'IV', 7: 'V', 9: 'vi', 11: 'vii°'}
        else:
            roman_map = {0: 'i', 2: 'ii°', 3: 'III', 5: 'iv', 7: 'V', 8: 'VI', 10: 'VII'}
        
        roman = roman_map.get(scale_degree, 'X')  # X for unknown/chromatic
        
        # Adjust for chord quality if it doesn't match expected
        if roman == 'X':
            # Check for secondary dominants
            if scale_degree in self.secondary_dominants:
                roman = self.secondary_dominants[scale_degree]
            else:
                # Generic chromatic notation
                accidental = self._get_accidental_for_degree(scale_degree, key_center, mode)
                degree_roman = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII'][scale_degree // 2]
                roman = f"{accidental}{degree_roman}"
        
        return roman
    
    def _get_accidental_for_degree(self, scale_degree: int, key_center: str, mode: str) -> str:
        """Get accidental symbol for chromatic scale degree."""
        # Simplified - could be more sophisticated
        chromatic_degrees = {1: 'b', 3: 'b', 6: 'b', 8: 'b', 10: 'b'}
        return chromatic_degrees.get(scale_degree, '')
    
    def _generate_figured_bass(self, chord_match: ChordMatch) -> str:
        """Generate figured bass notation for chord."""
        if chord_match.inversion == 0:
            return ''  # Root position
        elif chord_match.inversion == 1:
            return '⁶'  # First inversion
        elif chord_match.inversion == 2:
            return '⁶₄'  # Second inversion
        else:
            return '⁷'  # Assume seventh chord
    
    def _detect_cadences(self, chords: List[FunctionalChordAnalysis]) -> List[Cadence]:
        """Detect cadential patterns in progression."""
        cadences = []
        
        for i in range(len(chords) - 1):
            current = chords[i]
            next_chord = chords[i + 1]
            
            # V-I authentic cadence
            if (current.function == ChordFunction.DOMINANT and 
                next_chord.function == ChordFunction.TONIC):
                cadences.append(Cadence(
                    type='authentic',
                    chords=[current, next_chord],
                    strength=0.9,
                    position='phrase_ending' if i == len(chords) - 2 else 'mid_phrase'
                ))
            
            # IV-I plagal cadence
            elif (current.function == ChordFunction.SUBDOMINANT and 
                  next_chord.function == ChordFunction.TONIC):
                cadences.append(Cadence(
                    type='plagal',
                    chords=[current, next_chord],
                    strength=0.7,
                    position='phrase_ending' if i == len(chords) - 2 else 'mid_phrase'
                ))
        
        return cadences
    
    def _identify_chromatic_elements(
        self,
        chords: List[FunctionalChordAnalysis],
        key_center: str,
        mode: str
    ) -> List[ChromaticElement]:
        """Identify chromatic harmony elements."""
        chromatic_elements = []
        
        for i, chord in enumerate(chords):
            if chord.is_chromatic:
                # Simple secondary dominant detection
                if 'V/' in chord.roman_numeral:
                    resolution = chords[i + 1] if i + 1 < len(chords) else None
                    chromatic_elements.append(ChromaticElement(
                        chord=chord,
                        type=ChromaticType.SECONDARY_DOMINANT,
                        resolution=resolution,
                        explanation=f"Secondary dominant {chord.roman_numeral}"
                    ))
        
        return chromatic_elements
    
    def _determine_progression_type(
        self,
        chords: List[FunctionalChordAnalysis],
        cadences: List[Cadence]
    ) -> ProgressionType:
        """Determine the overall progression type."""
        # Simple heuristics
        if any(c.type == 'authentic' for c in cadences):
            return ProgressionType.AUTHENTIC_CADENCE
        elif any(c.type == 'plagal' for c in cadences):
            return ProgressionType.PLAGAL_CADENCE
        else:
            return ProgressionType.OTHER
    
    def _calculate_confidence(
        self,
        chords: List[FunctionalChordAnalysis],
        cadences: List[Cadence]
    ) -> float:
        """Calculate analysis confidence score."""
        base_confidence = 0.5
        
        # Boost for strong cadences
        if cadences:
            base_confidence += 0.3
        
        # Boost for mostly diatonic chords
        diatonic_ratio = sum(1 for c in chords if not c.is_chromatic) / len(chords)
        base_confidence += diatonic_ratio * 0.2
        
        return min(base_confidence, 1.0)
    
    def _generate_explanation(
        self,
        chords: List[FunctionalChordAnalysis],
        key_center: str,
        mode: str
    ) -> str:
        """Generate human-readable explanation of analysis."""
        romans = ' - '.join(c.roman_numeral for c in chords)
        return f"Functional progression in {key_center} {mode}: {romans}"