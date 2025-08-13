#!/usr/bin/env python3
"""
Comprehensive Modal Test Case Generator

Algorithmically generates ALL possible modal test scenarios
to ensure complete coverage without manual test case definition.

This Python script generates exactly the same test data as the TypeScript version
to ensure behavioral parity between implementations.
"""

import json
import csv
import os
import re
from datetime import datetime
from typing import List, Dict, Optional, Set, Any
from dataclasses import dataclass


@dataclass
class TestCase:
    """Test case data structure"""
    id: str
    chords: List[str]
    parent_key: Optional[str]
    expected_modal: bool
    expected_mode: Optional[str]
    description: str
    category: str
    theoretical_basis: str


@dataclass
class Mode:
    """Mode definition"""
    name: str
    degree: int
    characteristic: str


@dataclass
class Progression:
    """Chord progression with metadata"""
    variant: str
    chords: List[str]
    pattern: str
    reasoning: str


class ComprehensiveTestGenerator:
    """Comprehensive test case generator matching TypeScript behavior"""
    
    def __init__(self):
        self.test_cases: List[TestCase] = []
        self.case_id = 1
        
        # Pitch-class helpers for correct enharmonic handling
        self.NOTE_TO_INDEX = {
            'C': 0, 'B#': 0,
            'C#': 1, 'Db': 1,
            'D': 2,
            'D#': 3, 'Eb': 3,
            'E': 4, 'Fb': 4,
            'E#': 5, 'F': 5,
            'F#': 6, 'Gb': 6,
            'G': 7,
            'G#': 8, 'Ab': 8,
            'A': 9,
            'A#': 10, 'Bb': 10,
            'B': 11, 'Cb': 11
        }
        
        self.INDEX_TO_SHARPS = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        self.INDEX_TO_FLATS = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
        
        # Conventional major-key spellings for parent keys (avoid A# major, etc.)
        self.MAJOR_KEY_NAME_BY_INDEX = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']
        self.FLAT_MAJOR_ROOTS = {'F', 'Bb', 'Eb', 'Ab', 'Db', 'Gb', 'Cb'}
        
        # Core musical data for systematic generation
        self.ROOTS = self.MAJOR_KEY_NAME_BY_INDEX.copy()
        self.MAJOR_KEYS = [f"{root} major" for root in self.ROOTS]
        self.MINOR_KEYS = [f"{root} minor" for root in self.ROOTS]
        
        self.MODES = [
            Mode('Ionian', 1, 'major_seventh'),
            Mode('Dorian', 2, 'minor_with_major_sixth'),
            Mode('Phrygian', 3, 'minor_with_flat_second'),
            Mode('Lydian', 4, 'major_with_sharp_fourth'),
            Mode('Mixolydian', 5, 'major_with_flat_seventh'),
            Mode('Aeolian', 6, 'natural_minor'),
            Mode('Locrian', 7, 'diminished_with_flat_second')
        ]
    
    def unicode_to_ascii(self, s: str) -> str:
        """Convert unicode music symbols to ASCII"""
        return s.replace('♭', 'b').replace('♯', '#')
    
    def parse_root_name(self, s: str) -> str:
        """Extract root note name from chord symbol"""
        ascii_s = self.unicode_to_ascii(s)
        match = re.match(r'^[A-G](?:#|b)?', ascii_s)
        return match.group(0) if match else ascii_s
    
    def prefers_flats_from_root(self, root: str) -> bool:
        """Determine if root prefers flat notation"""
        r = self.parse_root_name(root)
        if 'b' in r:
            return True
        if '#' in r:
            return False
        idx = self.NOTE_TO_INDEX.get(r)
        if idx is None:
            return False
        return self.MAJOR_KEY_NAME_BY_INDEX[idx] in self.FLAT_MAJOR_ROOTS
    
    def get_note_at_interval(self, root: str, semitones: int, 
                           prefer: str = 'auto', for_key_name_major: bool = False) -> str:
        """Get note at specified interval from root"""
        base = self.parse_root_name(root)
        base_idx = self.NOTE_TO_INDEX.get(base)
        if base_idx is None:
            return root  # unknown symbol; fail soft
        
        target_idx = (base_idx + (semitones % 12) + 12) % 12
        
        if for_key_name_major:
            return self.MAJOR_KEY_NAME_BY_INDEX[target_idx]
        
        if prefer == 'flats':
            use_flats = True
        elif prefer == 'sharps':
            use_flats = False
        else:
            use_flats = self.prefers_flats_from_root(root)
        
        return self.INDEX_TO_FLATS[target_idx] if use_flats else self.INDEX_TO_SHARPS[target_idx]
    
    def get_parent_key(self, modal_root: str, mode_name: str) -> str:
        """Get parent key for a given modal root and mode"""
        mode_to_parent_offsets = {
            'Ionian': 0,
            'Dorian': 10,
            'Phrygian': 8,
            'Lydian': 7,
            'Mixolydian': 5,
            'Aeolian': 3,
            'Locrian': 1
        }
        
        offset = mode_to_parent_offsets[mode_name]
        # Compute the parent root using conventional major-key names first
        parent_root = self.get_note_at_interval(modal_root, offset, for_key_name_major=True)
        
        # If the modal root prefers flats (e.g., Ab, Eb), respell F# as Gb for the parent major key
        prefer_flats = self.prefers_flats_from_root(modal_root)
        if prefer_flats and parent_root == 'F#':
            parent_root = 'Gb'
        
        return f"{parent_root} major"
    
    def get_modal_root(self, parent_root: str, mode_name: str) -> str:
        """Get modal root from parent key and mode"""
        parent_to_modal_offsets = {
            'Ionian': 0,     # C major -> C Ionian
            'Dorian': 2,     # C major -> D Dorian
            'Phrygian': 4,   # C major -> E Phrygian
            'Lydian': 5,     # C major -> F Lydian
            'Mixolydian': 7, # C major -> G Mixolydian
            'Aeolian': 9,    # C major -> A Aeolian
            'Locrian': 11    # C major -> B Locrian
        }
        
        offset = parent_to_modal_offsets[mode_name]
        return self.get_note_at_interval(parent_root, offset)
    
    def get_characteristic_progressions(self, root: str, mode_name: str, parent_key: Optional[str]) -> List[Progression]:
        """Get characteristic progressions for a mode"""
        # Decide accidental preference by context: parent key first, then modal root
        prefer = 'auto'
        pk = parent_key or ''
        pk_root = self.parse_root_name(pk) if pk else ''
        
        if pk_root and pk_root in self.FLAT_MAJOR_ROOTS:
            prefer = 'flats'
        elif '#' in pk:
            prefer = 'sharps'
        elif 'b' in self.parse_root_name(root):
            prefer = 'flats'
        elif '#' in self.parse_root_name(root):
            prefer = 'sharps'
        
        # Optional notational refinement: in strongly flat parents, respell certain naturals diatonically
        def adjust_by_parent_key(n: str) -> str:
            if not parent_key:
                return n
            r = pk_root
            if r in self.FLAT_MAJOR_ROOTS:
                # In Gb/Db/Cb families, prefer Cb over B for certain degrees (e.g., bVII of Db)
                if r in ['Gb', 'Db', 'Cb'] and n == 'B':
                    return 'Cb'
                # Very rare, but if Cb major contexts appear and we hit E, prefer Fb
                if r == 'Cb' and n == 'E':
                    return 'Fb'
            return n
        
        def deg(semitones: int) -> str:
            return adjust_by_parent_key(self.get_note_at_interval(root, semitones, prefer))
        
        if mode_name == 'Mixolydian':
            return [
                Progression('long', [root, deg(10), deg(5), root], 'I-bVII-IV-I', 'bVII and IV emphasize modal dominant-less cadence'),
                Progression('short', [root, deg(10), root], 'I-bVII-I', 'bVII-I cadence is a core Mixolydian marker'),
                Progression('seventh', [f"{root}7", deg(5), f"{root}7"], 'I7-IV-I7', 'dominant-quality tonic is idiomatic in Mixolydian'),
                Progression('vamp', [root, deg(5)], 'I-IV (vamp)', 'sustained modal color without functional V'),
                Progression('foil', [root, deg(7), root], 'I-V-I (foil)', 'leading-tone V implies functional major over modal')
            ]
        elif mode_name == 'Dorian':
            return [
                Progression('long', [f"{root}m", deg(5), deg(10), f"{root}m"], 'i-IV-bVII-i', 'major IV and bVII with minor tonic'),
                Progression('short', [f"{root}m", deg(5), f"{root}m"], 'i-IV-i', 'major IV against minor tonic defines Dorian'),
                Progression('seventh', [f"{root}m7", f"{deg(5)}maj7", f"{root}m7"], 'i7-IVmaj7-i7', 'seventh-quality voicings, modal color intact'),
                Progression('vamp', [f"{root}m", deg(5)], 'i-IV (vamp)', 'two-chord Dorian vamp'),
                Progression('foil', [f"{root}m", f"{deg(5)}m", f"{root}m"], 'i-iv-i (foil)', 'minor iv pulls toward Aeolian')
            ]
        elif mode_name == 'Phrygian':
            return [
                Progression('long', [f"{root}m", deg(1), deg(10), f"{root}m"], 'i-bII-bVII-i', 'bII with bVII underscores Phrygian'),
                Progression('short', [f"{root}m", deg(1), f"{root}m"], 'i-bII-i', 'flat second is the signature degree'),
                Progression('seventh', [f"{root}m7", deg(1), f"{root}m7"], 'i7-bII-i7', 'seventh voicing maintains Phrygian color'),
                Progression('vamp', [f"{root}m", deg(1)], 'i-bII (vamp)', 'pedal vamp on tonic and bII'),
                Progression('foil', [f"{root}m", deg(2), f"{root}m"], 'i-II-i (foil)', 'natural 2 undermines Phrygian')
            ]
        elif mode_name == 'Lydian':
            return [
                Progression('long', [root, deg(2), deg(7), root], 'I-II-V-I', 'raised 4th via II; keeps functional V at bay contextually'),
                Progression('long_nov', [root, deg(2), root, deg(2)], 'I-II-I-II', 'strict Lydian motion emphasizing #4, avoids V'),
                Progression('short', [root, deg(2), root], 'I-II-I', 'II (diatonic) emphasizes #4 over IV'),
                Progression('seventh', [f"{root}maj7", deg(2), f"{root}maj7"], 'Imaj7-II-Imaj7', 'Imaj7 with implied #11 color'),
                Progression('vamp', [root, deg(2)], 'I-II (vamp)', 'two-chord Lydian vamp'),
                Progression('foil', [root, deg(7), root], 'I-V-I (foil)', 'authentic cadence reduces Lydian feel')
            ]
        elif mode_name == 'Aeolian':
            return [
                Progression('long', [f"{root}m", deg(8), deg(10), f"{root}m"], 'i-bVI-bVII-i', 'natural minor hallmark bVI, bVII'),
                Progression('short', [f"{root}m", deg(10), f"{root}m"], 'i-bVII-i', 'Aeolian cadence without leading tone'),
                Progression('seventh', [f"{root}m7", deg(8), deg(10), f"{root}m7"], 'i7-bVI-bVII-i7', 'seventh voicings in Aeolian'),
                Progression('vamp', [f"{root}m", deg(10)], 'i-bVII (vamp)', 'two-chord Aeolian vamp'),
                Progression('foil', [f"{root}m", f"{deg(7)}7", f"{root}m"], 'i-V7-i (foil)', 'leading-tone dominant suggests harmonic minor')
            ]
        elif mode_name == 'Locrian':
            return [
                Progression('long', [f"{root}dim", deg(1), f"{deg(6)}m", f"{root}dim"], 'i°-bII-v-i°', 'Locrian with bII and minor v (no true V)'),
                Progression('short', [f"{root}dim", deg(1), f"{root}dim"], 'i°-bII-i°', 'diminished tonic and Neapolitan color'),
                Progression('seventh', [f"{root}m7b5", deg(1), f"{root}m7b5"], 'iø7-bII-iø7', 'half-diminished tonic is idiomatic for Locrian'),
                Progression('vamp', [f"{root}dim", deg(1)], 'i°-bII (vamp)', 'two-chord Locrian vamp'),
                Progression('foil', [f"{root}dim", f"{deg(7)}7", f"{root}dim"], 'i°-V7-i° (foil)', 'true V7 contradicts Locrian')
            ]
        else:  # Ionian
            return [
                Progression('short', [root, deg(5), root], 'I-IV-I', 'plagal movement as modal color'),
                Progression('seventh', [f"{root}maj7", f"{deg(5)}maj7", f"{root}maj7"], 'Imaj7-IVmaj7-Imaj7', 'Ionian color with 7ths'),
                Progression('vamp', [root, deg(5)], 'I-IV (vamp)', 'sustained Ionian color'),
                Progression('foil', [root, deg(7), root], 'I-V-I (foil)', 'authentic cadence is functional, not modal')
            ]
    
    def has_definitive_modal_characteristics(self, chords: List[str], mode_name: str) -> bool:
        """Check if a progression has definitive modal characteristics"""
        # Analyze progression for definitive modal indicators
        if mode_name == 'Mixolydian':
            # Look for bVII chord (the smoking gun for Mixolydian)
            return self.progression_contains_bVII(chords)
        elif mode_name == 'Dorian':
            # Look for natural VI in minor context
            return self.progression_contains_natural_VI(chords)
        elif mode_name == 'Phrygian':
            # Look for bII chord
            return self.progression_contains_bII(chords)
        # Add other modal characteristics as needed
        return False
    
    def progression_contains_bVII(self, chords: List[str]) -> bool:
        """Check if progression contains bVII chord (definitive Mixolydian indicator)"""
        # Remove everything except letter name and 'b' for flats
        chord_symbols = [re.sub(r'[^A-Gb]', '', c) for c in chords]
        
        # Simple heuristic: if we see a progression that looks like I-bVII
        # For C major context: C followed by Bb
        for i in range(len(chord_symbols) - 1):
            current = chord_symbols[i]
            next_chord = chord_symbols[i + 1]
            
            # Check for semitone descending from tonic (I-bVII)
            if self.is_likely_I_bVII_motion(current, next_chord):
                return True
        
        # Also check if the progression contains Bb specifically when tonic is C
        if 'C' in chord_symbols and 'Bb' in chord_symbols:
            return True
        
        return False
    
    def is_likely_I_bVII_motion(self, chord1: str, chord2: str) -> bool:
        """Simple heuristic to detect I-bVII motion"""
        # Common I-bVII patterns
        patterns = [
            ('C', 'Bb'), ('G', 'F'), ('D', 'C'), ('A', 'G'),
            ('E', 'D'), ('B', 'A'), ('F', 'Eb'), ('Bb', 'Ab'),
            ('Eb', 'Db'), ('Ab', 'Gb'), ('Db', 'Cb'), ('Gb', 'Fb')
        ]
        
        return (chord1, chord2) in patterns
    
    def progression_contains_natural_VI(self, chords: List[str]) -> bool:
        """Placeholder for Dorian natural VI detection"""
        # Implementation would analyze for natural VI in minor context
        return False
    
    def progression_contains_bII(self, chords: List[str]) -> bool:
        """Placeholder for Phrygian bII detection"""
        # Implementation would analyze for bII chord
        return False
    
    def convert_pattern_to_chords(self, root: str, mode: str, pattern: List[str]) -> List[str]:
        """Convert scale degree pattern to chord symbols"""
        scale = self.get_scale_notes(root, mode)
        return [scale[int(degree) - 1] if degree.isdigit() and int(degree) <= len(scale) else root
                for degree in pattern]
    
    def get_scale_notes(self, root: str, mode: str) -> List[str]:
        """Get scale notes for a given root and mode"""
        # Simplified - major scale degrees only (functional tests use major)
        prefer = 'flats' if self.prefers_flats_from_root(root) else 'sharps'
        major_scale = [self.get_note_at_interval(root, ivl, prefer) for ivl in [0, 2, 4, 5, 7, 9, 11]]
        return major_scale
    
    def add_test_case(self, **kwargs):
        """Add a test case to the collection"""
        test_case = TestCase(
            id=f"test-{self.case_id}",
            **kwargs
        )
        self.test_cases.append(test_case)
        self.case_id += 1
    
    def generate_all_test_cases(self) -> List[TestCase]:
        """Generate ALL possible modal test scenarios systematically"""
        print('🔄 Generating comprehensive modal test cases...')
        
        self.test_cases = []
        self.case_id = 1
        
        # 1. Generate characteristic modal progressions for every mode and root
        self.generate_modal_characteristic_cases()
        
        # 2. Generate clear functional progressions in every key
        self.generate_functional_cases()
        
        # 3. Generate ambiguous cases (modal vs functional boundaries)
        self.generate_ambiguous_cases()
        
        # 4. Generate edge cases and error conditions
        self.generate_edge_cases()
        
        # 5. Generate cross-modal comparison cases
        self.generate_cross_modal_cases()
        
        print(f'✅ Generated {len(self.test_cases)} comprehensive test cases')
        return self.test_cases
    
    def generate_modal_characteristic_cases(self):
        """1. MODAL CHARACTERISTIC CASES - Generate the defining progressions for each mode in every key"""
        print('  Generating modal characteristic cases...')
        
        for root in self.ROOTS:
            for mode in self.MODES:
                parent_key = self.get_parent_key(root, mode.name)
                
                # Generate characteristic progressions for this mode
                progressions = self.get_characteristic_progressions(root, mode.name, parent_key)
                
                # Add tagged variants for each progression
                for progression in progressions:
                    category = 'modal_characteristic'
                    expected_modal = True
                    if progression.variant == 'seventh':
                        category = 'modal_seventh_variant'
                    elif progression.variant == 'vamp':
                        category = 'modal_vamp'
                    elif progression.variant == 'foil':
                        category = 'modal_foil'
                        expected_modal = False
                    
                    self.add_test_case(
                        chords=progression.chords,
                        parent_key=parent_key,
                        expected_modal=expected_modal,
                        expected_mode=f"{root} {mode.name}" if expected_modal else None,
                        description=f"{root} {mode.name} {progression.pattern}",
                        category=category,
                        theoretical_basis=f"{mode.name} {progression.variant} — {progression.reasoning}"
                    )
                
                # Add an ambiguous duplicate (no parent key) for the 'long' variant to test context-free classification
                long_prog = next((p for p in progressions if p.variant == 'long'), None)
                if long_prog:
                    # Check if progression has definitive modal characteristics
                    has_modal_characteristics = self.has_definitive_modal_characteristics(long_prog.chords, mode.name)
                    
                    self.add_test_case(
                        chords=long_prog.chords,
                        parent_key=None,
                        expected_modal=has_modal_characteristics,
                        expected_mode=f"{root} {mode.name}" if has_modal_characteristics else None,
                        description=f"{root} {mode.name} {long_prog.pattern} (no parent key)",
                        category='ambiguous',
                        theoretical_basis=(
                            f"Characteristic {mode.name} features make modal analysis preferred even without parent key"
                            if has_modal_characteristics else
                            'Omit parent key to force boundary decision between modal and functional'
                        )
                    )
    
    def generate_functional_cases(self):
        """2. FUNCTIONAL CASES - Generate clear functional progressions that should NOT be detected as modal"""
        print('  Generating functional cases...')
        
        functional_patterns = [
            {'pattern': ['1', '4', '5', '1'], 'name': 'I-IV-V-I', 'description': 'Classic functional cadence'},
            {'pattern': ['1', '6', '4', '5'], 'name': 'I-vi-IV-V', 'description': 'Pop progression'},
            {'pattern': ['6', '4', '1', '5'], 'name': 'vi-IV-I-V', 'description': 'Pop progression starting on vi'},
            {'pattern': ['2', '5', '1'], 'name': 'ii-V-I', 'description': 'Jazz ii-V-I'},
            {'pattern': ['1', '5', '6', '4'], 'name': 'I-V-vi-IV', 'description': 'Pop ballad progression'}
        ]
        
        for root in self.ROOTS:
            major_key = f"{root} major"
            
            for functional_pattern in functional_patterns:
                chords = self.convert_pattern_to_chords(root, 'major', functional_pattern['pattern'])
                
                self.add_test_case(
                    chords=chords,
                    parent_key=major_key,
                    expected_modal=False,
                    expected_mode=None,
                    description=f"{root} major {functional_pattern['name']} functional",
                    category='functional_clear',
                    theoretical_basis=f"{functional_pattern['description']} - pure functional harmony"
                )
    
    def generate_ambiguous_cases(self):
        """3. AMBIGUOUS CASES - Generate cases that test decision boundaries between modal and functional"""
        print('  Generating ambiguous cases...')
        
        # Test cases without parent key context
        ambiguous_patterns = [
            {'chords': ['C', 'F', 'G', 'C'], 'description': 'Could be C major functional or C Ionian modal'},
            {'chords': ['Am', 'F', 'C', 'G'], 'description': 'Could be A Aeolian or vi-IV-I-V in C'},
            {'chords': ['D', 'G', 'A', 'D'], 'description': 'Could be D major or D Mixolydian in G'}
        ]
        
        for pattern in ambiguous_patterns:
            self.add_test_case(
                chords=pattern['chords'],
                parent_key=None,
                expected_modal=False,  # Default to functional when ambiguous
                expected_mode=None,
                description=f"Ambiguous: {pattern['description']}",
                category='ambiguous',
                theoretical_basis='Without parent key context, functional interpretation is more likely'
            )
        
        # Test cases with explicit modal resolution via parent key (spell chords by parent key)
        for root in ['C', 'G', 'D', 'A']:
            # Parent key a fourth up from the modal root (I-bVII-IV-I in Mixolydian)
            pk_root = self.get_note_at_interval(root, 5, for_key_name_major=True)
            if self.prefers_flats_from_root(root) and pk_root == 'F#':
                pk_root = 'Gb'
            parent_key = f"{pk_root} major"
            
            # Choose chord spelling preference based on the parent key accidental
            if 'b' in parent_key:
                prefer = 'flats'
            elif '#' in parent_key:
                prefer = 'sharps'
            else:
                prefer = 'auto'
            
            chords = [
                root,
                self.get_note_at_interval(root, 10, prefer),  # bVII
                self.get_note_at_interval(root, 5, prefer),   # IV
                root
            ]
            
            self.add_test_case(
                chords=chords,
                parent_key=parent_key,
                expected_modal=True,
                expected_mode=f"{root} Mixolydian",
                description=f"{root} Mixolydian with parent key context",
                category='ambiguous',
                theoretical_basis='Parent key context resolves modal vs functional ambiguity'
            )
    
    def generate_edge_cases(self):
        """4. EDGE CASES - Generate error conditions and boundary cases"""
        print('  Generating edge cases...')
        
        edge_cases = [
            {
                'chords': ['C'],
                'description': 'Single chord',
                'expected_modal': False,
                'reasoning': 'No harmonic progression'
            },
            {
                'chords': ['G', 'G', 'G'],
                'description': 'Repeated chord',
                'expected_modal': False,
                'reasoning': 'Static harmony'
            },
            {
                'chords': ['C', 'C#', 'D'],
                'description': 'Chromatic progression',
                'expected_modal': False,
                'reasoning': 'Non-diatonic movement'
            },
            {
                'chords': ['F#', 'Gb'],
                'description': 'Enharmonic equivalents',
                'expected_modal': False,
                'reasoning': 'Enharmonic handling test'
            },
            {
                'chords': ['C', 'F#', 'B', 'E'],
                'description': 'Wide interval jumps',
                'expected_modal': False,
                'reasoning': 'Non-functional movement'
            }
        ]
        
        for edge_case in edge_cases:
            self.add_test_case(
                chords=edge_case['chords'],
                parent_key=None,
                expected_modal=edge_case['expected_modal'],
                expected_mode=None,
                description=f"Edge case: {edge_case['description']}",
                category='edge_case',
                theoretical_basis=edge_case['reasoning']
            )
    
    def generate_cross_modal_cases(self):
        """5. CROSS-MODAL COMPARISON CASES - Generate cases that distinguish between different modes"""
        print('  Generating cross-modal comparison cases...')
        
        # For each parent root, generate progressions that could be multiple modes
        for root in ['C', 'G', 'D', 'A']:
            parent_key = f"{root} major"
            
            # Test mode distinctions within the same parent key
            modes = ['Ionian', 'Dorian', 'Phrygian', 'Lydian', 'Mixolydian', 'Aeolian', 'Locrian']
            
            for mode_name in modes:
                modal_root = self.get_modal_root(root, mode_name)
                progressions = self.get_characteristic_progressions(modal_root, mode_name, parent_key)
                
                for progression in progressions:
                    category = 'modal_characteristic'
                    expected_modal = True
                    
                    if progression.variant == 'seventh':
                        category = 'modal_seventh_variant'
                    elif progression.variant == 'vamp':
                        category = 'modal_vamp'
                    elif progression.variant == 'foil':
                        category = 'modal_foil'
                        expected_modal = False
                    
                    self.add_test_case(
                        chords=progression.chords,
                        parent_key=parent_key,
                        expected_modal=expected_modal,
                        expected_mode=f"{modal_root} {mode_name}" if expected_modal else None,
                        description=f"{modal_root} {mode_name} in {parent_key} context — {progression.pattern}",
                        category=category,
                        theoretical_basis=f"Distinguishes {mode_name} from other modes in same parent key; variant={progression.variant}"
                    )
                    
                    # Add an ambiguous duplicate for the long variant
                    if progression.variant == 'long':
                        # Check if progression has definitive modal characteristics
                        has_modal_characteristics = self.has_definitive_modal_characteristics(progression.chords, mode_name)
                        
                        self.add_test_case(
                            chords=progression.chords,
                            parent_key=None,
                            expected_modal=has_modal_characteristics,
                            expected_mode=f"{modal_root} {mode_name}" if has_modal_characteristics else None,
                            description=f"{modal_root} {mode_name} {progression.pattern} (no parent key)",
                            category='ambiguous',
                            theoretical_basis=(
                                f"Characteristic {mode_name} features make modal analysis preferred even without parent key"
                                if has_modal_characteristics else
                                'Boundary test without parent-key context'
                            )
                        )
    
    def export_to_json(self) -> str:
        """Export test cases to JSON for external analysis"""
        # Calculate categories
        categories = {}
        for category in ['modal_characteristic', 'modal_seventh_variant', 'modal_vamp', 
                        'modal_foil', 'functional_clear', 'ambiguous', 'edge_case']:
            categories[category] = len([t for t in self.test_cases if t.category == category])
        
        data = {
            "metadata": {
                "generated": datetime.now().isoformat() + "Z",
                "totalCases": len(self.test_cases),
                "categories": categories
            },
            "testCases": []
        }
        
        # Convert test cases to dict format
        for test_case in self.test_cases:
            case_dict = {
                "id": test_case.id,
                "chords": test_case.chords,
                "parentKey": test_case.parent_key,
                "expectedModal": test_case.expected_modal,
                "expectedMode": test_case.expected_mode,
                "description": test_case.description,
                "category": test_case.category,
                "theoreticalBasis": test_case.theoretical_basis
            }
            data["testCases"].append(case_dict)
        
        return json.dumps(data, indent=2)
    
    def export_to_csv(self) -> str:
        """Export test cases to CSV format for manual spreadsheet review"""
        # Define CSV headers
        headers = [
            'Test ID',
            'Description',
            'Chords',
            'Parent Key',
            'Expected Modal',
            'Expected Mode',
            'Category',
            'Theoretical Basis'
        ]
        
        # Convert test cases to CSV rows
        rows = []
        for test_case in self.test_cases:
            row = [
                test_case.id,
                f'"{test_case.description}"',  # Quote to handle commas in descriptions
                f'"{" ".join(test_case.chords)}"',  # Quote chord progressions
                test_case.parent_key or 'none',
                'TRUE' if test_case.expected_modal else 'FALSE',
                test_case.expected_mode or 'none',
                test_case.category,
                f'"{test_case.theoretical_basis}"'  # Quote theoretical explanations
            ]
            rows.append(row)
        
        # Combine headers and rows
        csv_content = '\n'.join([','.join(headers)] + [','.join(row) for row in rows])
        
        return csv_content


def generate_comprehensive_test_cases() -> List[TestCase]:
    """Generate and return comprehensive test cases"""
    generator = ComprehensiveTestGenerator()
    return generator.generate_all_test_cases()


def export_comprehensive_test_cases():
    """Export comprehensive test cases to JSON and CSV files"""
    generator = ComprehensiveTestGenerator()
    test_cases = generator.generate_all_test_cases()
    
    print('\n📊 COMPREHENSIVE TEST CASE GENERATION COMPLETE')
    print(f'Generated {len(test_cases)} test cases')
    
    json_output = generator.export_to_json()
    csv_output = generator.export_to_csv()
    
    # Create output directory
    os.makedirs('./tests/generated', exist_ok=True)
    
    # Save JSON file
    with open('./tests/generated/comprehensive-modal-test-cases.json', 'w') as f:
        f.write(json_output)
    print('💾 Test cases saved to ./tests/generated/comprehensive-modal-test-cases.json')
    
    # Save CSV file for manual spreadsheet review
    with open('./tests/generated/comprehensive-modal-test-cases.csv', 'w') as f:
        f.write(csv_output)
    print('📊 CSV export saved to ./tests/generated/comprehensive-modal-test-cases.csv for manual review')
    
    print('\n📋 Test Case Breakdown:')
    categories = {}
    for tc in test_cases:
        categories[tc.category] = categories.get(tc.category, 0) + 1
    
    for category, count in categories.items():
        print(f'  {category}: {count} cases')
    
    # Show a few examples
    print('\n🎯 Example Generated Test Cases:')
    
    # Find an A Aeolian characteristic case
    a_aeolian_case = next((tc for tc in test_cases 
                          if tc.expected_mode == 'A Aeolian' and 'i-bVI-bVII-i' in tc.description), None)
    
    if a_aeolian_case:
        print('\n  ✅ Found A Aeolian characteristic case:')
        print(f'     {a_aeolian_case.id}: {a_aeolian_case.description}')
        print(f'     Chords: {" ".join(a_aeolian_case.chords)}')
        print(f'     Parent Key: {a_aeolian_case.parent_key or "none"}')
        print(f'     Expected: {"MODAL" if a_aeolian_case.expected_modal else "FUNCTIONAL"} ({a_aeolian_case.expected_mode or "none"})')
    
    # Show a few more examples
    print('\n  📋 More examples:')
    for tc in test_cases[:5]:
        print(f'     {tc.id}: {tc.description}')
        print(f'       {" ".join(tc.chords)} ({tc.parent_key or "no parent"})')
    
    return test_cases


if __name__ == '__main__':
    export_comprehensive_test_cases()