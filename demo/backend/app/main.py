"""
FastAPI backend for harmonic analysis demo
Simple backend that wraps the harmonic analysis library
"""

import time
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Import the harmonic analysis library as external dependency
try:
    from harmonic_analysis.multiple_interpretation_service import (
        analyze_progression_multiple,
    )
    from harmonic_analysis.scales import (
        MAJOR_SCALE_MODES,
        MODAL_PARENT_KEYS,
        NOTE_TO_PITCH_CLASS,
        PITCH_CLASS_NAMES,
    )
    from harmonic_analysis.types import AnalysisOptions
    from harmonic_analysis.scale_melody_analysis import analyze_scale_melody

    LIBRARY_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Harmonic analysis library not available: {e}")
    print("   Run setup.sh to install the library, or use frontend-only mode")
    LIBRARY_AVAILABLE = False

app = FastAPI(title="Harmonic Analysis Demo API", version="1.0.0")


# Add this after creating the FastAPI app but before CORS middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(
        f"{request.method} {request.url} - {response.status_code} - {process_time:.4f}s"
    )
    return response


# ... rest of your CORS middleware setup ...
# Basic CORS setup for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3010"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def analyze_scale_notes(scale_notes: str, parent_key: Optional[str] = None) -> dict:
    """
    Analyze a sequence of scale notes using the sophisticated scale analysis library.

    Args:
        scale_notes: Space-separated note names (e.g., "E F G# A B C D")
        parent_key: Optional parent key context

    Returns:
        Scale analysis result dictionary with contextual classification
    """
    if not LIBRARY_AVAILABLE:
        raise RuntimeError("Harmonic analysis library not available")

    # Parse note names 
    notes = scale_notes.strip().split()

    if len(notes) < 3:
        return {
            "error": "Insufficient notes for scale analysis",
            "input_scale": scale_notes,
            "analysis": "Need at least 3 notes for meaningful scale analysis",
        }

    try:
        # Use the real library's sophisticated analysis
        result = analyze_scale_melody(notes, parent_key, melody=False)

        # Debug logging for parent key logic
        print(
            f"🎯 Scale analysis result: classification='{result.classification}', parent_scales={result.parent_scales}")
        print(f"🎯 Modal labels: {result.modal_labels}")
        print(f"🎯 Non-diatonic pitches: {result.non_diatonic_pitches}")

        # Convert to demo format while preserving sophisticated analysis
        root_note = notes[0]

        # Determine the most likely mode based on the root note
        mode_name = "Unknown"
        confidence = result.confidence or 0.8

        # Get modal label for the root note if available
        if root_note in result.modal_labels:
            mode_name = result.modal_labels[root_note]
        elif result.modal_labels:
            # Use the first available modal label if root not found
            mode_name = list(result.modal_labels.values())[0]

        # Generate scale degrees from the notes
        scale_degrees = _generate_scale_degrees(notes)

        # Create analysis text with contextual information
        analysis_parts = [f"{root_note} {mode_name}"]

        if result.classification == "modal_borrowing":
            analysis_parts.append("Modal borrowing from parent scale")
        elif result.classification == "modal_candidate":
            analysis_parts.append("Modal characteristics without clear parent key")
        elif result.classification == "diatonic":
            analysis_parts.append("Diatonic within provided key context")

        if result.non_diatonic_pitches:
            analysis_parts.append(
                f"Non-diatonic: {', '.join(result.non_diatonic_pitches)}")

        analysis_text = " - ".join(analysis_parts)

        # Generate harmonic implications based on classification
        harmonic_implications = _get_contextual_implications(result)

        return {
            "input_scale": scale_notes,
            "primary_analysis": {
                "type": "SCALE",
                "confidence": confidence,
                "analysis": analysis_text,
                "mode_name": mode_name,
                "parent_key": parent_key or "Not specified",
                "parent_scales": result.parent_scales,
                "classification": result.classification,
                "modal_labels": result.modal_labels,
                "non_diatonic_pitches": result.non_diatonic_pitches,
                "scale_degrees": scale_degrees,
                "intervallic_analysis": f"Notes analyzed for parent scale membership and modal relationships",
                "characteristic_notes": notes[:3] if len(notes) >= 3 else notes,
                "reasoning": result.rationale or f"Contextual analysis classified as {result.classification}",
                "theoretical_basis": "Sophisticated scale analysis with parent scale detection and contextual classification",
                "evidence": [
                    {
                        "type": "CONTEXTUAL",
                        "strength": confidence,
                        "description": f"Classification: {result.classification}",
                        "supported_interpretations": ["SCALE"],
                        "musical_basis": "Parent scale detection and contextual analysis",
                    }
                ],
            },
            "harmonic_implications": harmonic_implications,
            "metadata": {
                "scale_type": "contextual",
                "parent_scales": result.parent_scales,
                "classification": result.classification,
                "analysis_time_ms": 30,
                "analysis_depth": "comprehensive"
            },
            "alternative_analyses": []
        }

    except Exception as e:
        # Fallback to basic analysis if sophisticated analysis fails
        print(f"⚠️  Sophisticated analysis failed: {e}, falling back to basic analysis")
        return _basic_scale_analysis(scale_notes, parent_key)


def _generate_scale_degrees(notes: List[str]) -> List[str]:
    """Generate scale degree notation from note names."""
    if not notes:
        return []

    # Simple scale degree mapping from root
    try:
        root_pc = NOTE_TO_PITCH_CLASS[notes[0].replace("♯", "#").replace("♭", "b")]
        scale_degrees = []

        for note in notes:
            pc = NOTE_TO_PITCH_CLASS[note.replace("♯", "#").replace("♭", "b")]
            degree = (pc - root_pc) % 12

            degree_map = {
                0: "1", 1: "♭2", 2: "2", 3: "♭3", 4: "3", 5: "4",
                6: "#4/♭5", 7: "5", 8: "♭6", 9: "6", 10: "♭7", 11: "7"
            }
            scale_degrees.append(degree_map.get(degree, str(degree)))

        return scale_degrees
    except KeyError:
        return [str(i + 1) for i in range(len(notes))]


def _get_contextual_implications(result) -> List[str]:
    """Generate harmonic implications based on contextual analysis."""
    implications = []

    if result.classification == "diatonic":
        implications.extend([
            "Fits naturally within the provided key context",
            "Standard diatonic harmonic relationships apply",
            "Compatible with traditional harmony"
        ])
    elif result.classification == "modal_borrowing":
        implications.extend([
            "Uses notes from parent scale but with different tonal center",
            "Creates modal harmonic relationships",
            "Suggests modal interchange possibilities"
        ])
    elif result.classification == "modal_candidate":
        implications.extend([
            "Independent modal character without clear parent key",
            "Establishes own harmonic framework",
            "May suggest exotic or contemporary harmonic approaches"
        ])

    if result.non_diatonic_pitches:
        implications.append(
            f"Non-diatonic elements: {', '.join(result.non_diatonic_pitches)} create harmonic tension")

    if result.parent_scales:
        implications.append(
            f"Compatible with {', '.join(result.parent_scales)} harmonic frameworks")

    return implications


def _basic_scale_analysis(scale_notes: str, parent_key: Optional[str] = None) -> dict:
    """Fallback basic analysis if sophisticated analysis fails."""
    notes = scale_notes.strip().split()
    return {
        "input_scale": scale_notes,
        "primary_analysis": {
            "type": "SCALE",
            "confidence": 0.5,
            "analysis": f"Basic analysis of {len(notes)} notes",
            "mode_name": "Unknown",
            "parent_key": parent_key or "Not specified",
            "scale_degrees": [str(i + 1) for i in range(len(notes))],
            "reasoning": "Fallback analysis due to processing error",
            "theoretical_basis": "Basic note sequence analysis",
        },
        "harmonic_implications": ["Requires manual analysis"],
        "metadata": {"scale_type": "basic", "analysis_time_ms": 5},
        "alternative_analyses": []
    }


def _describe_intervals(intervals: list) -> str:
    """Convert interval list to descriptive pattern."""
    if not intervals or len(intervals) < 2:
        return "Insufficient intervals"

    steps = [(intervals[i + 1] - intervals[i]) % 12 for i in range(len(intervals) - 1)]
    step_names = []
    for step in steps:
        if step == 1:
            step_names.append("H")
        elif step == 2:
            step_names.append("W")
        elif step == 3:
            step_names.append("W+H")
        else:
            step_names.append(f"{step}hs")

    return "-".join(step_names)


def _get_characteristic_notes(scale_name: str, scale_degrees: list) -> list:
    """Get characteristic notes for a scale."""
    if "Phrygian Dominant" in scale_name:
        return ["1", "♭2", "3", "5"]  # Root, flat 2nd, major 3rd, perfect 5th
    elif "Dorian" in scale_name:
        return ["1", "♭3", "6"]  # Minor 3rd, natural 6th
    elif "Mixolydian" in scale_name:
        return ["1", "3", "♭7"]  # Major 3rd, flat 7th
    elif "Phrygian" in scale_name:
        return ["1", "♭2", "♭3"]  # Flat 2nd, minor 3rd
    else:
        return scale_degrees[:3] if len(scale_degrees) >= 3 else scale_degrees


def analyze_melody_notes(
        melody_notes: List[str], parent_key: Optional[str] = None
) -> dict:
    """
    Analyze a melody sequence to identify contour, scale context, and harmonic implications.

    Args:
        melody_notes: List of note names (e.g., ["C", "D", "E", "F", "G", "A", "B", "C"])
        parent_key: Optional parent key context

    Returns:
        Melody analysis result dictionary
    """
    if not LIBRARY_AVAILABLE:
        raise RuntimeError("Harmonic analysis library not available")

    if len(melody_notes) < 3:
        return {
            "error": "Insufficient notes for melody analysis",
            "input_melody": melody_notes,
            "analysis": "Need at least 3 notes for meaningful melody analysis",
        }

    try:
        # Parse note names to pitch classes
        pitch_classes = [
            NOTE_TO_PITCH_CLASS[note.replace("♯", "#").replace("♭", "b")]
            for note in melody_notes
        ]
    except KeyError as e:
        return {
            "error": f"Invalid note name: {e}",
            "input_melody": melody_notes,
            "analysis": "Unable to parse note names",
        }

    # Analyze melodic contour
    contour = []
    for i in range(1, len(pitch_classes)):
        prev = pitch_classes[i - 1]
        curr = pitch_classes[i]
        diff = (curr - prev) % 12
        if diff == 0:
            contour.append("R")  # Repeated
        elif diff <= 6:
            contour.append("U")  # Up
        else:
            contour.append("D")  # Down

    contour_description = _describe_contour(contour)

    # Calculate intervals between consecutive notes
    intervals = []
    for i in range(1, len(pitch_classes)):
        interval = (pitch_classes[i] - pitch_classes[i - 1]) % 12
        intervals.append(interval)

    # Determine melodic range
    min_pc = min(pitch_classes)
    max_pc = max(pitch_classes)
    melodic_range = (max_pc - min_pc) % 12

    # Find largest leap
    largest_leap = max(intervals) if intervals else 0
    if largest_leap > 6:
        largest_leap = 12 - largest_leap  # Convert to smaller interval

    # Determine directional tendency
    up_movements = contour.count("U")
    down_movements = contour.count("D")
    repeated_notes = contour.count("R")

    if up_movements > down_movements:
        direction = "Generally ascending"
    elif down_movements > up_movements:
        direction = "Generally descending"
    else:
        direction = "Balanced movement"

    # Analyze scale context using unique notes
    unique_notes = list(
        dict.fromkeys(melody_notes)
    )  # Preserve order, remove duplicates
    scale_analysis = analyze_scale_notes(" ".join(unique_notes), parent_key)

    # Determine harmonic implications
    if (
            "primary_analysis" in scale_analysis
            and "mode_name" in scale_analysis["primary_analysis"]
    ):
        scale_mode = scale_analysis["primary_analysis"]["mode_name"]
        harmonic_implications = f"Suggests {scale_mode} tonality based on note content"
    else:
        harmonic_implications = "Chromatic or atonal harmonic implications"

    # Analyze phrase structure
    phrase_length = len(melody_notes)
    if phrase_length <= 4:
        phrase_type = "Motif"
    elif phrase_length <= 8:
        phrase_type = "Short phrase"
    elif phrase_length <= 16:
        phrase_type = "Standard phrase"
    else:
        phrase_type = "Extended phrase"

    # Identify potential cadential points (large leaps or repeated notes at end)
    cadential_points = []
    if len(intervals) > 0:
        if intervals[-1] == 0:  # Ends on repeated note
            cadential_points.append("Final note repetition")
        elif abs(intervals[-1]) >= 7:  # Large leap at end
            cadential_points.append("Final large interval")
        if any(interval >= 7 for interval in intervals):
            cadential_points.append("Internal large leaps")

    return {
        "input_melody": melody_notes,
        "primary_analysis": {
            "type": "MELODY",
            "confidence": 0.8,
            "analysis": f"Melodic analysis of {len(melody_notes)}-note sequence with {contour_description}",
            "melodic_contour": contour_description,
            "scale_context": scale_analysis.get("primary_analysis", {}).get(
                "mode_name", "Undetermined"
            )
                             + " context",
            "modal_characteristics": f"Melody exhibits {direction.lower()} motion with {_get_stepwise_analysis(intervals)}",
            "phrase_analysis": f"{phrase_type} ({phrase_length} notes) with {direction.lower()}",
            "harmonic_implications": harmonic_implications,
            "reasoning": f"Melodic analysis reveals {phrase_length} notes with {contour_description} and {largest_leap}-semitone maximum interval.",
            "theoretical_basis": "Melodic analysis based on contour, intervallic content, scale membership, and phrase structure.",
            "evidence": [
                {
                    "type": "STRUCTURAL",
                    "strength": 0.8,
                    "description": f"Clear melodic direction and {phrase_type.lower()} structure",
                    "supported_interpretations": ["MELODY"],
                    "musical_basis": "Melodic contour and phrase structure analysis",
                }
            ],
        },
        "intervallic_analysis": {
            "intervals": [_interval_name(interval) for interval in intervals],
            "largest_leap": _interval_name(largest_leap),
            "melodic_range": f"{melodic_range} semitones",
            "directional_tendency": direction,
        },
        "phrase_structure": {
            "phrase_length": f"{phrase_length} notes",
            "cadential_points": (
                cadential_points if cadential_points else ["No strong cadential points"]
            ),
            "motivic_content": f"{'Stepwise' if all(i <= 2 for i in intervals) else 'Mixed stepwise and leaping'} motion pattern",
        },
        "metadata": {
            "melody_type": "stepwise" if all(i <= 2 for i in intervals) else "mixed",
            "note_count": phrase_length,
            "analysis_type": "harmonic_implications",
            "parent_key": parent_key,
            "analysis_time_ms": 30,
        },
    }


def _describe_contour(contour: list) -> str:
    """Describe melodic contour pattern."""
    if not contour:
        return "Static"

    up_count = contour.count("U")
    down_count = contour.count("D")
    repeat_count = contour.count("R")

    if up_count > down_count * 2:
        return "Strong ascending contour"
    elif down_count > up_count * 2:
        return "Strong descending contour"
    elif up_count == down_count:
        return "Balanced arch contour"
    elif repeat_count > len(contour) // 2:
        return "Static with repeated notes"
    else:
        return "Mixed directional contour"


def _get_stepwise_analysis(intervals: list) -> str:
    """Analyze stepwise vs. leaping motion."""
    if not intervals:
        return "no motion"

    stepwise = sum(1 for i in intervals if i <= 2)
    leaping = len(intervals) - stepwise

    if stepwise > leaping * 2:
        return "predominantly stepwise motion"
    elif leaping > stepwise:
        return "predominantly leaping motion"
    else:
        return "mixed stepwise and leaping motion"


def _interval_name(semitones: int) -> str:
    """Convert semitone count to interval name."""
    names = {
        0: "Unison",
        1: "Minor 2nd",
        2: "Major 2nd",
        3: "Minor 3rd",
        4: "Major 3rd",
        5: "Perfect 4th",
        6: "Tritone",
        7: "Perfect 5th",
        8: "Minor 6th",
        9: "Major 6th",
        10: "Minor 7th",
        11: "Major 7th",
    }
    return names.get(semitones, f"{semitones} semitones")


def _get_harmonic_implications(scale_name: str) -> list:
    """Get harmonic implications for a scale."""
    if "Phrygian Dominant" in scale_name:
        return [
            "Strong dominant character with exotic flavor",
            "Augmented 2nd creates harmonic tension",
            "Common in Middle Eastern and flamenco music",
            "Effective over dominant chords in minor keys",
        ]
    elif "Dorian" in scale_name:
        return [
            "Natural 6th creates brighter minor sound",
            "Popular in jazz and folk music",
            "Works well over minor 7th chords",
        ]
    elif "Mixolydian" in scale_name:
        return [
            "Dominant character with flat 7th",
            "Bluesy and rock applications",
            "Perfect over dominant 7th chords",
        ]
    else:
        return [
            "Modal harmonic character",
            "Distinctive intervallic relationships",
            "Specific harmonic context applications",
        ]


class AnalysisRequest(BaseModel):
    chords: List[str]
    parent_key: Optional[str] = None
    pedagogical_level: str = "intermediate"
    confidence_threshold: float = 0.5
    max_alternatives: int = 3


class ScaleAnalysisRequest(BaseModel):
    scale: str
    parent_key: Optional[str] = None
    analysis_depth: str = "comprehensive"


class MelodyAnalysisRequest(BaseModel):
    melody: List[str]
    parent_key: Optional[str] = None
    analysis_type: str = "harmonic_implications"


class AnalysisResponse(BaseModel):
    input_chords: List[str]
    primary_analysis: dict
    alternative_analyses: List[dict]
    metadata: dict


@app.get("/")
async def root():
    return {"message": "Harmonic Analysis Demo API", "status": "running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze_chord_progression(request: AnalysisRequest):
    """
    Analyze a chord progression and return multiple interpretations
    """
    if not LIBRARY_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="Harmonic analysis library not installed. Run setup.sh to install dependencies.",
        )

    try:
        # Create analysis options
        options = AnalysisOptions(
            parent_key=request.parent_key,
            pedagogical_level=request.pedagogical_level,
            confidence_threshold=request.confidence_threshold,
            max_alternatives=request.max_alternatives,


        # Run the analysis
        result = await analyze_progression_multiple(request.chords, options)

        # Convert the result to the expected format including enhanced fields
        response_data = {
            "input_chords": result.input_chords,
            "primary_analysis": {
                "type": result.primary_analysis.type.value,
                "confidence": result.primary_analysis.confidence,
                "analysis": result.primary_analysis.analysis,
                "roman_numerals": result.primary_analysis.roman_numerals or [],
                "key_signature": result.primary_analysis.key_signature,
                "mode": result.primary_analysis.mode,
                "reasoning": result.primary_analysis.reasoning,
                "theoretical_basis": result.primary_analysis.theoretical_basis,
                "evidence": [
                    {
                        "type": evidence.type.value,
                        "strength": evidence.strength,
                        "description": evidence.description,
                        "supported_interpretations": [
                            interp.value
                            for interp in evidence.supported_interpretations
                        ],
                        "musical_basis": evidence.musical_basis,
                    }
                    for evidence in result.primary_analysis.evidence
                ],
                # Enhanced analysis fields
                "modal_characteristics": getattr(result.primary_analysis,
                                                 'modal_characteristics', []),
                "parent_key_relationship": getattr(result.primary_analysis,
                                                   'parent_key_relationship', None),
                "secondary_dominants": getattr(result.primary_analysis,
                                               'secondary_dominants', []),
                "borrowed_chords": getattr(result.primary_analysis, 'borrowed_chords',
                                           []),
                "chromatic_mediants": getattr(result.primary_analysis,
                                              'chromatic_mediants', []),
                "cadences": getattr(result.primary_analysis, 'cadences', []),
                "chord_functions": getattr(result.primary_analysis, 'chord_functions',
                                           []),
                "contextual_classification": getattr(result.primary_analysis,
                                                     'contextual_classification', None),
                "functional_confidence": getattr(result.primary_analysis,
                                                 'functional_confidence', None),
                "modal_confidence": getattr(result.primary_analysis, 'modal_confidence',
                                            None),
                "chromatic_confidence": getattr(result.primary_analysis,
                                                'chromatic_confidence', None),
            },
            "alternative_analyses": [
                {
                    "type": alt.type.value,
                    "confidence": alt.confidence,
                    "analysis": alt.analysis,
                    "roman_numerals": alt.roman_numerals or [],
                    "key_signature": alt.key_signature,
                    "mode": alt.mode,
                    "reasoning": alt.reasoning,
                    "theoretical_basis": alt.theoretical_basis,
                    "relationship_to_primary": alt.relationship_to_primary,
                    "evidence": [
                        {
                            "type": evidence.type.value,
                            "strength": evidence.strength,
                            "description": evidence.description,
                            "supported_interpretations": [
                                interp.value
                                for interp in evidence.supported_interpretations
                            ],
                            "musical_basis": evidence.musical_basis,
                        }
                        for evidence in alt.evidence
                    ],
                    # Enhanced fields for alternatives too
                    "modal_characteristics": getattr(alt, 'modal_characteristics', []),
                    "parent_key_relationship": getattr(alt, 'parent_key_relationship',
                                                       None),
                    "secondary_dominants": getattr(alt, 'secondary_dominants', []),
                    "borrowed_chords": getattr(alt, 'borrowed_chords', []),
                    "chromatic_mediants": getattr(alt, 'chromatic_mediants', []),
                    "cadences": getattr(alt, 'cadences', []),
                    "chord_functions": getattr(alt, 'chord_functions', []),
                    "contextual_classification": getattr(alt,
                                                         'contextual_classification',
                                                         None),
                    "functional_confidence": getattr(alt, 'functional_confidence',
                                                     None),
                    "modal_confidence": getattr(alt, 'modal_confidence', None),
                    "chromatic_confidence": getattr(alt, 'chromatic_confidence', None),
                }
                for alt in result.alternative_analyses
            ],
            "metadata": {
                "total_interpretations_considered": result.metadata.total_interpretations_considered,
                "confidence_threshold": result.metadata.confidence_threshold,
                "show_alternatives": result.metadata.show_alternatives,
                "pedagogical_level": result.metadata.pedagogical_level.value,
                "analysis_time_ms": result.metadata.analysis_time_ms,
            },
        }

        return response_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.post("/api/analyze-scale")
async def analyze_scale(request: ScaleAnalysisRequest):
    """
    Analyze a scale and return modal and harmonic characteristics using the real harmonic analysis library
    """
    if not LIBRARY_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="Harmonic analysis library not installed. Run setup.sh to install dependencies.",
        )

    try:
        # Debug logging to see what we received
        print(
            f"🔍 Scale analysis request: scale='{request.scale}', parent_key='{request.parent_key}'")

        # Use the real scale analysis function
        result = analyze_scale_notes(request.scale, request.parent_key)

        # Add metadata safely
        if "metadata" not in result:
            result["metadata"] = {}
        result["metadata"]["analysis_depth"] = request.analysis_depth
        result["alternative_analyses"] = (
            []
        )  # For consistency with frontend expectations

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scale analysis failed: {str(e)}")


@app.post("/api/analyze-melody")
async def analyze_melody(request: MelodyAnalysisRequest):
    """
    Analyze a melody and return contour, harmonic implications, and modal characteristics using the real harmonic analysis library
    """
    if not LIBRARY_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="Harmonic analysis library not installed. Run setup.sh to install dependencies.",
        )

    try:
        # Use the real melody analysis function
        result = analyze_melody_notes(request.melody, request.parent_key)

        # Add metadata
        result["metadata"]["analysis_type"] = request.analysis_type
        result["alternative_analyses"] = (
            []
        )  # For consistency with frontend expectations

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Melody analysis failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8010, log_level="info")
