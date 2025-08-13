"""
Functional harmony analysis engine.

Implements comprehensive functional harmony analysis with complete Roman numeral
generation, chromatic chord detection, and figured bass notation.
"""

from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from .types import ChordFunction, ChromaticType, ProgressionType
from .chord_logic import ChordMatch, find_chord_matches, determine_chord_function
from .scales import NOTE_TO_PITCH_CLASS, PITCH_CLASS_NAMES


# Enhanced Roman numeral templates with chromatic chord support
FUNCTIONAL_ROMAN_NUMERALS = {
    'major': {
        'diatonic': ['I', 'ii', 'iii', 'IV', 'V', 'vi', 'vii°'],
        'chromatic': {
            # Secondary dominants (used as fallback for non-dominant quality chords at these intervals)
            2: 'V/V',     # D7 - Dominant of V (very common)
            4: 'V/vi',    # E7 - Dominant of vi
            9: 'V/ii',    # A7 - Dominant of ii
            11: 'V/iii',  # B7 - Dominant of iii
        }
    },
    'minor': {
        'diatonic': ['i', 'ii°', 'III', 'iv', 'v', 'VI', 'VII'],
        'chromatic': {
            # Secondary dominants
            2: 'V/III',   # Dominant of III
            5: 'V/iv',    # Dominant of iv
            7: 'V/v',     # Dominant of v
            9: 'V/VI',    # Dominant of VI
            11: 'V/VII',  # Dominant of VII
            
            # Common chromatic chords in minor keys
            4: '#iv°',    # Raised 4th diminished
        }
    }
}

# Chord function mapping based on Roman numeral degree
CHORD_FUNCTIONS: Dict[int, Dict[str, ChordFunction]] = {
    # Major key functions
    0: {'major': ChordFunction.TONIC, 'minor': ChordFunction.TONIC},        # I/i
    1: {'major': ChordFunction.CHROMATIC, 'minor': ChordFunction.CHROMATIC}, # Chromatic
    2: {'major': ChordFunction.PREDOMINANT, 'minor': ChordFunction.PREDOMINANT}, # ii/ii°
    3: {'major': ChordFunction.CHROMATIC, 'minor': ChordFunction.TONIC},    # iii/III - chromatic in major, tonic in minor
    4: {'major': ChordFunction.PREDOMINANT, 'minor': ChordFunction.PREDOMINANT}, # iii/III
    5: {'major': ChordFunction.SUBDOMINANT, 'minor': ChordFunction.SUBDOMINANT}, # IV/iv
    6: {'major': ChordFunction.CHROMATIC, 'minor': ChordFunction.CHROMATIC}, # Tritone
    7: {'major': ChordFunction.DOMINANT, 'minor': ChordFunction.DOMINANT},  # V/v
    8: {'major': ChordFunction.CHROMATIC, 'minor': ChordFunction.CHROMATIC}, # Chromatic
    9: {'major': ChordFunction.TONIC, 'minor': ChordFunction.SUBDOMINANT},  # vi/VI - relative minor/submediant
    10: {'major': ChordFunction.CHROMATIC, 'minor': ChordFunction.SUBDOMINANT}, # bVII - modal in major, natural in minor
    11: {'major': ChordFunction.LEADING_TONE, 'minor': ChordFunction.LEADING_TONE} # vii°/VII
}


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
    """Main functional harmony analyzer class with comprehensive Roman numeral generation."""
    
    def __init__(self):
        self.last_analysis_ambiguity: List[str] = []
    
    async def analyze_functionally(
        self,
        chord_symbols: List[str],
        parent_key: Optional[str] = None
    ) -> FunctionalAnalysisResult:
        """
        Analyze chord progression with functional harmony as primary framework.
        
        Args:
            chord_symbols: List of chord symbols to analyze
            parent_key: Optional parent key signature (e.g., "C major")
            
        Returns:
            Complete functional analysis result
        """
        if not chord_symbols:
            raise ValueError("Empty chord progression")
        
        # Step 1: Determine key center (use parent key if provided)
        key_analysis = self._determine_key_center(chord_symbols, parent_key)
        
        # Step 2: Analyze each chord functionally
        functional_chords = self._analyze_chords_in_key(chord_symbols, key_analysis)
        
        # Step 3: Identify cadences and progressions
        cadences = self._identify_cadences(functional_chords)
        progression_type = self._classify_progression(functional_chords, cadences)
        
        # Step 4: Detect chromatic elements
        chromatic_elements = self._detect_chromatic_elements(functional_chords, key_analysis)
        
        # Step 5: Calculate confidence and create explanation
        confidence = self._calculate_confidence(functional_chords, cadences, chromatic_elements)
        explanation = self._create_explanation(functional_chords, progression_type, chromatic_elements)
        
        return FunctionalAnalysisResult(
            key_center=key_analysis['key_center'],
            key_signature=key_analysis['key_signature'],
            mode=key_analysis['mode'],
            chords=functional_chords,
            cadences=cadences,
            progression_type=progression_type,
            confidence=confidence,
            explanation=explanation,
            chromatic_elements=chromatic_elements,
            ambiguity_factors=self.last_analysis_ambiguity if self.last_analysis_ambiguity else None
        )
    
    def _determine_key_center(
        self,
        chord_symbols: List[str],
        parent_key: Optional[str]
    ) -> Dict[str, Any]:
        """
        Determine the key center using multiple methods.
        
        Returns:
            Dictionary with key_center, key_signature, mode, root_pitch, is_minor
        """
        if parent_key:
            # Use provided parent key
            parsed = self._parse_key(parent_key)
            if parsed:
                return {
                    'key_center': f"{parsed['tonic']} {'Minor' if parsed['is_minor'] else 'Major'}",
                    'key_signature': self._get_key_signature(parsed['tonic'], parsed['is_minor']),
                    'mode': 'minor' if parsed['is_minor'] else 'major',
                    'root_pitch': NOTE_TO_PITCH_CLASS.get(parsed['tonic'], 0),
                    'is_minor': parsed['is_minor']
                }
        
        # Analyze first and last chords for tonal center
        first_chord = self._parse_chord_symbol(chord_symbols[0])
        last_chord = self._parse_chord_symbol(chord_symbols[-1])
        
        # Assume first/last chord suggests key (simple heuristic for now)
        suggested_root = first_chord['root'] if first_chord else 0
        is_minor = first_chord and ('m' in first_chord['chord_name'] and 'M' not in first_chord['chord_name'])
        root_name = next((name for name, pitch in NOTE_TO_PITCH_CLASS.items() 
                         if pitch == suggested_root), 'C')
        
        return {
            'key_center': f"{root_name} {'Minor' if is_minor else 'Major'}",
            'key_signature': self._get_key_signature(root_name, is_minor),
            'mode': 'minor' if is_minor else 'major',
            'root_pitch': suggested_root,
            'is_minor': is_minor
        }
    
    def _parse_key(self, key_str: str) -> Optional[Dict[str, Any]]:
        """Parse key string like 'C major' or 'A minor'."""
        parts = key_str.split()
        if len(parts) >= 2:
            tonic = parts[0]
            mode = parts[1].lower()
            if tonic in NOTE_TO_PITCH_CLASS:
                return {
                    'tonic': tonic,
                    'is_minor': 'minor' in mode or 'm' in mode.lower()
                }
        return None
    
    def _get_key_signature(self, tonic: str, is_minor: bool) -> str:
        """Get key signature for display."""
        return f"{tonic} {'minor' if is_minor else 'major'}"
    
    def _parse_chord_symbol(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Parse chord symbol into components."""
        try:
            from .chord_logic import ChordParser
            parser = ChordParser()
            chord_match = parser.parse_chord(symbol)
            return {
                'root': chord_match.root_pitch,
                'chord_name': symbol,
                'bass_note': chord_match.bass_pitch
            }
        except:
            # Fallback parsing
            if symbol and symbol[0] in NOTE_TO_PITCH_CLASS:
                return {
                    'root': NOTE_TO_PITCH_CLASS[symbol[0]],
                    'chord_name': symbol,
                    'bass_note': None
                }
            return None
    
    def _analyze_chords_in_key(
        self,
        chord_symbols: List[str],
        key_analysis: Dict[str, Any]
    ) -> List[FunctionalChordAnalysis]:
        """
        Analyze each chord within the established key with figured bass notation.
        """
        analyzed_chords = []
        
        for symbol in chord_symbols:
            chord_info = self._parse_chord_symbol(symbol)
            if not chord_info:
                analyzed_chords.append(self._create_empty_chord_analysis(symbol))
                continue
            
            # Calculate interval from key center
            interval_from_key = (chord_info['root'] - key_analysis['root_pitch'] + 12) % 12
            
            # Determine if chord is diatonic or chromatic
            is_diatonic = self._is_chord_diatonic(
                interval_from_key, 
                key_analysis['is_minor'], 
                chord_info['chord_name']
            )
            
            # Get Roman numeral and function
            roman_numeral = self._get_roman_numeral(
                interval_from_key,
                key_analysis['is_minor'],
                chord_info['chord_name'],
                not is_diatonic
            )
            
            chord_function = self._get_chord_function(
                interval_from_key,
                key_analysis['is_minor'],
                not is_diatonic
            )
            
            # Analyze inversion and figured bass
            inversion_analysis = self._analyze_inversion_and_figured_bass(chord_info, roman_numeral)
            
            # Determine chromatic type if applicable
            chromatic_type = None
            if not is_diatonic:
                chromatic_type = self._determine_chromatic_type(
                    interval_from_key,
                    key_analysis['is_minor'],
                    chord_info['chord_name']
                )
            
            analyzed_chords.append(FunctionalChordAnalysis(
                chord_symbol=symbol,
                root=chord_info['root'],
                chord_name=chord_info['chord_name'],
                roman_numeral=roman_numeral + inversion_analysis['figured_bass'],
                figured_bass=inversion_analysis['figured_bass'],
                inversion=inversion_analysis['inversion'],
                function=chord_function,
                is_chromatic=not is_diatonic,
                chromatic_type=chromatic_type,
                bass_note=chord_info['bass_note']
            ))
        
        return analyzed_chords
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