import React, {useCallback, useEffect, useMemo, useRef, useState} from 'react';
import './App.css';

function App() {
    const [analysisType, setAnalysisType] = useState('progression');
    const [inputValue, setInputValue] = useState('C Am F G');
    const [parentKey, setParentKey] = useState('C major');
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [backendAvailable, setBackendAvailable] = useState(true);
    const [showJsonModal, setShowJsonModal] = useState(false);
    const [userIsEditing, setUserIsEditing] = useState(false);

    const examples = {
        progression: [
            {input: 'C Am F G', key: 'C major', description: 'Classic I-vi-IV-V'},
            {input: 'G F G', key: 'C major', description: 'Modal Mixolydian'},
            {input: 'Dm G C', key: 'C major', description: 'Strong ii-V-I'},
            {input: 'Am F C G', key: 'C major', description: 'vi-IV-I-V'},
            {input: 'C F C', key: 'C major', description: 'Plagal motion'},
            {input: 'Em Am D G', key: 'G major', description: 'vi-ii-V-I in G major'},
            {input: 'A G A', key: 'D major', description: 'A Mixolydian'},
            {input: 'F Bb C F', key: 'F major', description: 'I-IV-V-I in F major'},
        ],
        scale: [
            {input: 'C major scale', key: '', description: 'Ionian mode'},
            {input: 'G Mixolydian', key: 'C major', description: 'Fifth mode of C major'},
            {input: 'A harmonic minor', key: '', description: 'Harmonic minor scale'},
            {input: 'D Dorian', key: 'C major', description: 'Second mode of C major'},
            {input: 'E Phrygian', key: 'C major', description: 'Third mode of C major'},
            {input: 'F# Locrian', key: 'G major', description: 'Seventh mode of G major'},
        ],
        melody: [
            {input: 'C D E F G A B C', key: 'C major', description: 'C major scale melody'},
            {input: 'E F# G A B C# D E', key: 'D major', description: 'E Dorian melody'},
            {input: 'G A Bb C D Eb F G', key: 'Bb major', description: 'G Dorian melody'},
            {input: 'A B C D E F G A', key: 'C major', description: 'A Aeolian melody'},
            {input: 'F G Ab Bb C Db Eb F', key: 'Db major', description: 'F Aeolian melody'},
        ]
    };

    const [currentExampleIndex, setCurrentExampleIndex] = useState(0);
    const currentExampleIndexRef = useRef(0);

    const analysisTypes = [
        {id: 'progression', label: 'Chord Progression', placeholder: 'Enter chord symbols (e.g., C Am F G)', icon: '🎵'},
        {
            id: 'scale',
            label: 'Scale Analysis',
            placeholder: 'Enter scale name (e.g., C major scale, G Mixolydian)',
            icon: '🎼'
        },
        {id: 'melody', label: 'Melody Analysis', placeholder: 'Enter note sequence (e.g., C D E F G A B C)', icon: '🎶'}
    ];

    const currentAnalysisType = analysisTypes.find(type => type.id === analysisType);
    const currentExamples = useMemo(() => examples[analysisType] || [], [analysisType]);


    // Check backend availability
    useEffect(() => {
        const checkBackend = async () => {
            try {
                const response = await fetch('http://localhost:8010/health');
                setBackendAvailable(response.ok);
            } catch (error) {
                setBackendAvailable(false);
            }
        };
        checkBackend();
    }, []);

    const analyzeInput = useCallback(async () => {
        if (!inputValue.trim()) return;

        // If backend not available, don't analyze - user will see connection message
        if (!backendAvailable) {
            return;
        }

        setLoading(true);

        try {
            const endpoint = analysisType === 'progression' ? '/api/analyze' :
                analysisType === 'scale' ? '/api/analyze-scale' : '/api/analyze-melody';

            let requestBody;
            if (analysisType === 'progression') {
                requestBody = {
                    chords: inputValue.split(/\s+/).filter(c => c.length > 0),
                    parent_key: parentKey,
                    pedagogical_level: 'intermediate',
                    confidence_threshold: 0.5,
                    max_alternatives: 3
                };
            } else if (analysisType === 'scale') {
                requestBody = {
                    scale: inputValue,
                    parent_key: parentKey,
                    analysis_depth: 'comprehensive'
                };
            } else { // melody
                requestBody = {
                    melody: inputValue.split(/\s+/).filter(n => n.length > 0),
                    parent_key: parentKey,
                    analysis_type: 'harmonic_implications'
                };
            }

            const response = await fetch(`http://localhost:8010${endpoint}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestBody),
            });

            if (response.ok) {
                const data = await response.json();
                setResult(data);
            } else {
                throw new Error('Backend analysis failed');
            }
        } catch (error) {
            console.error('Analysis failed:', error);
            setResult(null);
        }

        setLoading(false);
    }, [inputValue, analysisType, parentKey, backendAvailable]);

    const analyzeSpecificInput = async (specificInputValue, specificParentKey) => {
        if (!specificInputValue.trim()) return;

        // If backend not available, don't analyze - user will see connection message
        if (!backendAvailable) {
            return;
        }

        setLoading(true);

        try {
            const endpoint = analysisType === 'progression' ? '/api/analyze' :
                            analysisType === 'scale' ? '/api/analyze-scale' : '/api/analyze-melody';

            let requestBody;
            if (analysisType === 'progression') {
                requestBody = {
                    chords: specificInputValue.split(/\s+/).filter(c => c.length > 0),
                    parent_key: specificParentKey,
                    pedagogical_level: 'intermediate',
                    confidence_threshold: 0.5,
                    max_alternatives: 3
                };
            } else if (analysisType === 'scale') {
                requestBody = {
                    scale: specificInputValue,
                    parent_key: specificParentKey,
                    analysis_depth: 'comprehensive'
                };
            } else { // melody
                requestBody = {
                    melody: specificInputValue.split(/\s+/).filter(n => n.length > 0),
                    parent_key: specificParentKey,
                    analysis_type: 'harmonic_implications'
                };
            }

            const response = await fetch(`http://localhost:8010${endpoint}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestBody),
            });

            if (response.ok) {
                const data = await response.json();
                setResult(data);
            } else {
                throw new Error('Backend analysis failed');
            }
        } catch (error) {
            console.error('Analysis failed:', error);
            setResult(null);
        }

        setLoading(false);
    };

    // Handle keyboard events
    useEffect(() => {
        const handleKeyDown = (event) => {
            console.log('🔍 Key pressed:', event.key);
            if (event.key === 'Tab') {
                console.log('🔍 Tab detected - target:', event.target.tagName, 'class:', event.target.className);
                console.log('🔍 Current example index:', currentExampleIndex);
                console.log('🔍 Current examples length:', currentExamples.length);
                console.log('🔍 Event target matches input:', event.target.matches('input, textarea, select'));
                console.log('🔍 Shift key pressed:', event.shiftKey);

                // Tab cycling: work when not in input fields OR when Shift+Tab (forced cycling)
                const shouldCycle = !event.target.matches('input, textarea, select') || event.shiftKey;

                if (shouldCycle) {
                    console.log('🔍 Tab cycling triggered');
                    event.preventDefault();

                    // Blur any focused input to prevent interference
                    if (event.target.matches('input, textarea, select')) {
                        event.target.blur();
                    }

                    // Use functional update to get the current value
                    setCurrentExampleIndex(prevIndex => {
                        const nextIndex = (prevIndex + 1) % currentExamples.length;
                        console.log('🔍 Calculating next index:', prevIndex, '+1 =', nextIndex);
                        const nextExample = currentExamples[nextIndex];
                        console.log('🔍 Next example:', nextExample);

                        // Set the input values immediately with the new example
                        setInputValue(nextExample.input);
                        setParentKey(nextExample.key);
                        setUserIsEditing(false); // Clear editing flag when using Tab to cycle

                        // Auto-analyze after a brief delay
                        setTimeout(() => {
                            console.log('🔍 About to analyze with:', nextExample.input, nextExample.key);
                            analyzeSpecificInput(nextExample.input, nextExample.key);
                        }, 100);

                        return nextIndex;
                    });
                } else {
                    console.log('🔍 Tab cycling not triggered - input field focused, use Shift+Tab for forced cycling');
                }
            }
        };

        window.addEventListener('keydown', handleKeyDown);
        return () => window.removeEventListener('keydown', handleKeyDown);
    }, [currentExampleIndex, currentExamples, analyzeSpecificInput]);

    // Initial analysis and handle analysis type changes
    useEffect(() => {
        if (backendAvailable) {
            analyzeInput();
        }
    }, [backendAvailable, analyzeInput]);

    // Reset to first example when analysis type changes (only if user isn't actively editing)
    useEffect(() => {
        if (!userIsEditing) {
            setCurrentExampleIndex(0);
            if (currentExamples.length > 0) {
                setInputValue(currentExamples[0].input);
                setParentKey(currentExamples[0].key);
                // Auto-analyze when type changes
                setTimeout(() => analyzeInput(), 100);
            }
        }
        // Reset editing flag when analysis type changes
        setUserIsEditing(false);
    }, [analysisType]); // Only reset when analysis type changes, not when currentExamples changes

    const renderEvidence = (evidence) => {
        return (
            <div className="evidence-section">
                <h4>Evidence ({evidence.length} pieces)</h4>
                {evidence.map((ev, idx) => (
                    <div key={idx} className="evidence-item">
                        <div className="evidence-header">
                            <span className="evidence-type">{ev.type}</span>
                            <span className="evidence-strength">Strength: {ev.strength.toFixed(2)}</span>
                        </div>
                        <div className="evidence-description">{ev.description}</div>
                        <div className="evidence-basis">{ev.musical_basis}</div>
                    </div>
                ))}
            </div>
        );
    };

    return (
        <div className="App">
            <header className="app-header">
                <h1>🎵 Harmonic Analysis Demo</h1>
                <p className="subtitle">
                    Comprehensive harmonic analysis with multiple interpretations
                </p>
            </header>

            <div className="input-section">
                {/* Analysis Type Selector */}
                <div className="analysis-type-selector">
                    {analysisTypes.map(type => (
                        <button
                            key={type.id}
                            className={`type-tab ${analysisType === type.id ? 'active' : ''}`}
                            onClick={() => setAnalysisType(type.id)}
                        >
                            <span className="type-icon">{type.icon}</span>
                            <span className="type-label">{type.label}</span>
                        </button>
                    ))}
                </div>

                {/* Input Fields */}
                <div className="input-group">
                    <label htmlFor="input">{currentAnalysisType.label}:</label>
                    <input
                        id="input"
                        type="text"
                        value={inputValue}
                        onChange={(e) => {
                            setInputValue(e.target.value);
                            setUserIsEditing(true);
                        }}
                        onFocus={() => setUserIsEditing(true)}
                        onBlur={() => analyzeInput()}
                        placeholder={currentAnalysisType.placeholder}
                        className="main-input"
                        onKeyDown={(e) => {
                            if (e.key === 'Enter') {
                                analyzeInput();
                            }
                        }}
                    />
                    <button onClick={analyzeInput} disabled={loading} className="analyze-button">
                        {loading ? 'Analyzing...' : 'Analyze'}
                    </button>
                </div>

                <div className="input-group">
                    <label htmlFor="parentKey">Parent Key:</label>
                    <input
                        id="parentKey"
                        type="text"
                        value={parentKey}
                        onChange={(e) => {
                            setParentKey(e.target.value);
                            setUserIsEditing(true);
                            // Auto-analyze when key changes if not empty
                            if (e.target.value.trim()) {
                                setTimeout(() => analyzeInput(), 300);
                            }
                        }}
                        onFocus={() => setUserIsEditing(true)}
                        placeholder="e.g., C major, G minor (optional)"
                        className="key-input"
                    />
                </div>

                <div className="help-text">
                    <div>💡 <strong>Tab:</strong> Cycle through {analysisType} examples (click outside inputs first) | <strong>Shift+Tab:</strong> Works anywhere
                        | <strong>Enter:</strong> Analyze current input
                    </div>
                    <div>📝
                        Examples: {currentExamples.slice(0, 3).map(ex => `${ex.input} (${ex.description})`).join(' • ')}{currentExamples.length > 3 ? '...' : ''}</div>
                    <div>🎯 Try different {analysisType} inputs and parent keys to see how analysis changes!</div>
                </div>
            </div>

            {!backendAvailable ? (
                <div className="results-container">
                    <div className="section backend-connection-message">
                        <h3>🔧 Demo Backend Not Connected</h3>
                        <div className="connection-instructions">
                            <p><strong>The harmonic analysis backend is not running.</strong></p>
                            <p>To see live analysis results, please start the backend:</p>

                            <div className="code-block">
                                <code>cd demo</code><br/>
                                <code>npm start</code>
                            </div>

                            <p>This will start both the frontend and backend services.</p>

                            <div className="help-links">
                                <p>📖 <strong>For detailed setup instructions:</strong></p>
                                <p>Please read the <code>README.md</code> file in the <code>demo/</code> folder</p>
                            </div>

                            <div className="status-info">
                                <p><strong>Current Status:</strong></p>
                                <ul>
                                    <li>✅ Frontend running on <code>localhost:3010</code></li>
                                    <li>❌ Backend not available at <code>localhost:8010</code></li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            ) : result && result.primary_analysis ? (
                <div className="results-container">
                    {/* Input Display */}
                    <div className="section">
                        <h3>Input {currentAnalysisType.label}</h3>
                        <div className="input-display">
                            {analysisType === 'progression' && result.input_chords && result.input_chords.join(' - ')}
                            {analysisType === 'scale' && result.input_scale}
                            {analysisType === 'melody' && result.input_melody && result.input_melody.join(' - ')}
                        </div>
                    </div>

                    {/* Primary Analysis */}
                    <div className="section primary-analysis">
                        <h3>Primary Analysis</h3>
                        <div className="analysis-content">
                            <div className="analysis-header">
                                <span className="analysis-type">{result.primary_analysis.type}</span>
                                <span
                                    className="confidence">Confidence: {result.primary_analysis.confidence.toFixed(3)}</span>
                            </div>

                            <div className="analysis-text">{result.primary_analysis.analysis}</div>

                            {/* Render different fields based on analysis type */}
                            {analysisType === 'progression' && (
                                <>
                                    {result.primary_analysis.roman_numerals && result.primary_analysis.roman_numerals.length > 0 && (
                                        <div className="roman-numerals">
                                            <strong>Roman
                                                Numerals:</strong> {result.primary_analysis.roman_numerals.join(' - ')}
                                        </div>
                                    )}

                                    {result.primary_analysis.key_signature && (
                                        <div className="key-info">
                                            <strong>Key:</strong> {result.primary_analysis.key_signature}
                                            {result.primary_analysis.mode &&
                                                <span> ({result.primary_analysis.mode})</span>}
                                        </div>
                                    )}
                                </>
                            )}

                            {analysisType === 'scale' && (
                                <>
                                    {result.primary_analysis.scale_degrees && (
                                        <div className="scale-degrees">
                                            <strong>Scale
                                                Degrees:</strong> {result.primary_analysis.scale_degrees.join(' - ')}
                                        </div>
                                    )}

                                    {result.primary_analysis.parent_key && (
                                        <div className="key-info">
                                            <strong>Parent Key:</strong> {result.primary_analysis.parent_key}
                                            {result.primary_analysis.mode &&
                                                <span> ({result.primary_analysis.mode})</span>}
                                        </div>
                                    )}

                                    {result.primary_analysis.intervallic_analysis && (
                                        <div className="intervallic-analysis">
                                            <strong>Intervallic
                                                Pattern:</strong> {result.primary_analysis.intervallic_analysis}
                                        </div>
                                    )}

                                    {result.primary_analysis.characteristic_notes && (
                                        <div className="characteristic-notes">
                                            <strong>Characteristic
                                                Notes:</strong> {result.primary_analysis.characteristic_notes.join(', ')}
                                        </div>
                                    )}
                                </>
                            )}

                            {analysisType === 'melody' && (
                                <>
                                    {result.primary_analysis.melodic_contour && (
                                        <div className="melodic-contour">
                                            <strong>Melodic Contour:</strong> {result.primary_analysis.melodic_contour}
                                        </div>
                                    )}

                                    {result.primary_analysis.scale_context && (
                                        <div className="scale-context">
                                            <strong>Scale Context:</strong> {result.primary_analysis.scale_context}
                                        </div>
                                    )}

                                    {result.primary_analysis.modal_characteristics && (
                                        <div className="modal-characteristics">
                                            <strong>Modal
                                                Characteristics:</strong> {result.primary_analysis.modal_characteristics}
                                        </div>
                                    )}

                                    {result.primary_analysis.phrase_analysis && (
                                        <div className="phrase-analysis">
                                            <strong>Phrase Analysis:</strong> {result.primary_analysis.phrase_analysis}
                                        </div>
                                    )}

                                    {result.primary_analysis.harmonic_implications && (
                                        <div className="harmonic-implications">
                                            <strong>Harmonic
                                                Implications:</strong> {result.primary_analysis.harmonic_implications}
                                        </div>
                                    )}
                                </>
                            )}

                            {result.primary_analysis.reasoning && (
                                <div className="reasoning">
                                    <h4>Reasoning</h4>
                                    <div>{result.primary_analysis.reasoning}</div>
                                </div>
                            )}

                            {result.primary_analysis.theoretical_basis && (
                                <div className="theoretical-basis">
                                    <h4>Theoretical Basis</h4>
                                    <div>{result.primary_analysis.theoretical_basis}</div>
                                </div>
                            )}

                            {result.primary_analysis.evidence && result.primary_analysis.evidence.length > 0 &&
                                renderEvidence(result.primary_analysis.evidence)
                            }
                        </div>
                    </div>

                    {/* Alternative Analyses */}
                    {result.alternative_analyses && result.alternative_analyses.length > 0 && (
                        <div className="section">
                            <h3>Alternative Interpretations ({result.alternative_analyses.length})</h3>
                            {result.alternative_analyses.map((alt, index) => (
                                <div key={index} className="alternative-analysis">
                                    <div className="analysis-header">
                                        <span className="analysis-type">{alt.type}</span>
                                        <span className="confidence">Confidence: {alt.confidence.toFixed(3)}</span>
                                    </div>

                                    <div className="analysis-text">{alt.analysis}</div>

                                    {alt.roman_numerals && alt.roman_numerals.length > 0 && (
                                        <div className="roman-numerals">
                                            <strong>Roman Numerals:</strong> {alt.roman_numerals.join(' - ')}
                                        </div>
                                    )}

                                    {alt.key_signature && (
                                        <div className="key-info">
                                            <strong>Key:</strong> {alt.key_signature}
                                            {alt.mode && <span> ({alt.mode})</span>}
                                        </div>
                                    )}

                                    {alt.relationship_to_primary && (
                                        <div className="relationship">
                                            <strong>Relationship to Primary:</strong> {alt.relationship_to_primary}
                                        </div>
                                    )}

                                    {alt.evidence && alt.evidence.length > 0 && renderEvidence(alt.evidence)}
                                </div>
                            ))}
                        </div>
                    )}

                    {/* Additional Analysis Sections for Scale and Melody */}
                    {analysisType === 'scale' && result.harmonic_implications && (
                        <div className="section">
                            <h3>Harmonic Implications</h3>
                            <div className="implications-list">
                                {result.harmonic_implications.map((implication, idx) => (
                                    <div key={idx} className="implication-item">
                                        • {implication}
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}

                    {analysisType === 'melody' && result.intervallic_analysis && (
                        <div className="section">
                            <h3>Intervallic Analysis</h3>
                            <div className="intervallic-grid">
                                {result.intervallic_analysis.intervals && (
                                    <div className="intervallic-item">
                                        <strong>Intervals:</strong> {Array.isArray(result.intervallic_analysis.intervals) ? result.intervallic_analysis.intervals.join(', ') : result.intervallic_analysis.intervals}
                                    </div>
                                )}
                                {result.intervallic_analysis.largest_leap && (
                                    <div className="intervallic-item">
                                        <strong>Largest Leap:</strong> {result.intervallic_analysis.largest_leap}
                                    </div>
                                )}
                                {result.intervallic_analysis.melodic_range && (
                                    <div className="intervallic-item">
                                        <strong>Melodic Range:</strong> {result.intervallic_analysis.melodic_range}
                                    </div>
                                )}
                                {result.intervallic_analysis.directional_tendency && (
                                    <div className="intervallic-item">
                                        <strong>Direction:</strong> {result.intervallic_analysis.directional_tendency}
                                    </div>
                                )}
                            </div>
                        </div>
                    )}

                    {analysisType === 'melody' && result.phrase_structure && (
                        <div className="section">
                            <h3>Phrase Structure</h3>
                            <div className="phrase-grid">
                                {result.phrase_structure.phrase_length && (
                                    <div className="phrase-item">
                                        <strong>Phrase Length:</strong> {result.phrase_structure.phrase_length}
                                    </div>
                                )}
                                {result.phrase_structure.cadential_points && (
                                    <div className="phrase-item">
                                        <strong>Cadential
                                            Points:</strong> {Array.isArray(result.phrase_structure.cadential_points) ? result.phrase_structure.cadential_points.join(', ') : result.phrase_structure.cadential_points}
                                    </div>
                                )}
                                {result.phrase_structure.motivic_content && (
                                    <div className="phrase-item">
                                        <strong>Motivic Content:</strong> {result.phrase_structure.motivic_content}
                                    </div>
                                )}
                            </div>
                        </div>
                    )}

                    {/* Metadata */}
                    {result.metadata && (
                        <div className="section metadata">
                            <h3>Analysis Metadata</h3>
                            <div className="metadata-grid">
                                {result.metadata.total_interpretations_considered && (
                                    <div className="metadata-item">
                                        <strong>Total
                                            Interpretations:</strong> {result.metadata.total_interpretations_considered}
                                    </div>
                                )}
                                {result.metadata.confidence_threshold && (
                                    <div className="metadata-item">
                                        <strong>Confidence Threshold:</strong> {result.metadata.confidence_threshold}
                                    </div>
                                )}
                                {result.metadata.show_alternatives !== undefined && (
                                    <div className="metadata-item">
                                        <strong>Show
                                            Alternatives:</strong> {result.metadata.show_alternatives ? 'Yes' : 'No'}
                                    </div>
                                )}
                                {result.metadata.pedagogical_level && (
                                    <div className="metadata-item">
                                        <strong>Pedagogical Level:</strong> {result.metadata.pedagogical_level}
                                    </div>
                                )}
                                {result.metadata.analysis_time_ms && (
                                    <div className="metadata-item">
                                        <strong>Analysis Time:</strong> {result.metadata.analysis_time_ms}ms
                                    </div>
                                )}
                                {result.metadata.scale_type && (
                                    <div className="metadata-item">
                                        <strong>Scale Type:</strong> {result.metadata.scale_type}
                                    </div>
                                )}
                                {result.metadata.melody_type && (
                                    <div className="metadata-item">
                                        <strong>Melody Type:</strong> {result.metadata.melody_type}
                                    </div>
                                )}
                                {result.metadata.note_count && (
                                    <div className="metadata-item">
                                        <strong>Note Count:</strong> {result.metadata.note_count}
                                    </div>
                                )}
                            </div>
                        </div>
                    )}
                </div>
            ) : result ? (
                <div className="results-container">
                    <div className="loading-message">
                        <p>⏳ Processing {currentAnalysisType.label.toLowerCase()} analysis...</p>
                        <p>Please wait while we analyze your input.</p>
                    </div>
                </div>
            ) : null}

            {/* Floating View Response Button */}
            {result && backendAvailable && (
                <button
                    className="view-response-button"
                    onClick={() => setShowJsonModal(true)}
                    title="View complete JSON response"
                >
                    📄 View Response
                </button>
            )}

            {/* JSON Response Modal */}
            {showJsonModal && result && (
                <div className="modal-overlay" onClick={() => setShowJsonModal(false)}>
                    <div className="modal-content" onClick={(e) => e.stopPropagation()}>
                        <div className="modal-header">
                            <h3>Complete JSON Response</h3>
                            <button
                                className="modal-close"
                                onClick={() => setShowJsonModal(false)}
                            >
                                ✕
                            </button>
                        </div>
                        <div className="modal-body">
              <pre className="json-display">
                {JSON.stringify(result, null, 2)}
              </pre>
                        </div>
                        <div className="modal-footer">
                            <button
                                className="copy-button"
                                onClick={() => {
                                    navigator.clipboard.writeText(JSON.stringify(result, null, 2));
                                    alert('JSON copied to clipboard!');
                                }}
                            >
                                📋 Copy JSON
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}

export default App;
