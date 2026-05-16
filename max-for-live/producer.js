/**
 * Producer — Max for Live Node.js Script
 * Calls the Claude API to generate MIDI patterns and session suggestions.
 * Place this file next to your .amxd patch file.
 */

const Max = require('max-api');
const https = require('https');

const MODEL = 'claude-sonnet-4-5';
let apiKey = '';
let sessionContext = {};

// ─────────────────────────────────────────
// RECEIVE FROM MAX PATCH
// ─────────────────────────────────────────

Max.addHandler('set_api_key', (key) => {
  apiKey = key;
  Max.outlet('status', 'API key saved');
});

Max.addHandler('set_context', (...args) => {
  // Receives: bpm, key, trackName, trackType, devices, clipLength
  const [bpm, key, trackName, trackType, devices, clipLength] = args;
  sessionContext = { bpm, key, trackName, trackType, devices, clipLength };
  Max.outlet('status', `Context: ${trackName} @ ${bpm}BPM`);
});

Max.addHandler('get_suggestions', () => {
  if (!apiKey) { Max.outlet('status', 'No API key set'); return; }
  getSuggestions();
});

Max.addHandler('generate_drum_pattern', (clipLength) => {
  if (!apiKey) { Max.outlet('status', 'No API key set'); return; }
  generateDrumPattern(clipLength || sessionContext.clipLength || 8);
});

Max.addHandler('generate_melodic_pattern', (clipLength, scaleHint) => {
  if (!apiKey) { Max.outlet('status', 'No API key set'); return; }
  generateMelodicPattern(clipLength || 8, scaleHint || '');
});

Max.addHandler('generate_chord_pattern', (clipLength) => {
  if (!apiKey) { Max.outlet('status', 'No API key set'); return; }
  generateChordPattern(clipLength || 8);
});

// ─────────────────────────────────────────
// CLAUDE API CALL
// ─────────────────────────────────────────

function callClaude(systemPrompt, userPrompt, onComplete) {
  Max.outlet('status', 'Thinking...');

  const body = JSON.stringify({
    model: MODEL,
    max_tokens: 2048,
    system: systemPrompt,
    messages: [{ role: 'user', content: userPrompt }]
  });

  const options = {
    hostname: 'api.anthropic.com',
    path: '/v1/messages',
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-api-key': apiKey,
      'anthropic-version': '2023-06-01',
      'Content-Length': Buffer.byteLength(body)
    }
  };

  const req = https.request(options, (res) => {
    let data = '';
    res.on('data', chunk => data += chunk);
    res.on('end', () => {
      try {
        const parsed = JSON.parse(data);
        if (parsed.error) {
          Max.outlet('status', 'Error: ' + parsed.error.message);
          return;
        }
        const text = parsed.content?.find(b => b.type === 'text')?.text || '';
        onComplete(text);
      } catch (e) {
        Max.outlet('status', 'Parse error: ' + e.message);
      }
    });
  });

  req.on('error', (e) => {
    Max.outlet('status', 'Network error: ' + e.message);
  });

  req.write(body);
  req.end();
}

// ─────────────────────────────────────────
// SUGGESTIONS
// ─────────────────────────────────────────

function getSuggestions() {
  const { bpm, key, trackName, trackType, devices } = sessionContext;

  const system = `You are a music production assistant for a minimal/tech house producer named Mina. 
Be concise. Return exactly 4 short suggestions (max 8 words each) as a JSON array of strings.
Example: ["Add a driving 16th hi-hat pattern", "Write a dark bass melody in D minor", "Create a percussive offbeat groove", "Layer a chord stab on the 3"]
Return ONLY the JSON array, nothing else.`;

  const user = `Session: ${bpm} BPM, Key: ${key || 'unknown'}, Track: "${trackName}" (${trackType}), Devices: ${devices || 'none'}
Give 4 context-aware production suggestions for this track.`;

  callClaude(system, user, (text) => {
    try {
      const clean = text.replace(/```json|```/g, '').trim();
      const suggestions = JSON.parse(clean);
      if (Array.isArray(suggestions)) {
        Max.outlet('suggestions', JSON.stringify(suggestions));
        Max.outlet('status', 'Suggestions ready');
      }
    } catch (e) {
      Max.outlet('status', 'Could not parse suggestions');
    }
  });
}

// ─────────────────────────────────────────
// DRUM PATTERN GENERATION
// ─────────────────────────────────────────

function generateDrumPattern(bars) {
  const { bpm, devices } = sessionContext;
  const steps = bars * 16; // 16th note resolution

  const system = `You are an expert drum programmer for minimal and tech house music.
Generate a ${bars}-bar drum pattern at ${bpm} BPM using 16th note grid (${steps} steps total, step 0 = beat 1).

RULES:
- Return ONLY a JSON object, no explanation, no markdown
- Use MIDI note numbers matching standard drum rack layout:
  36 = Kick, 38 = Snare, 42 = Closed HH, 46 = Open HH, 39 = Clap, 37 = Sidestick, 49 = Crash, 51 = Ride
- For tech house: driving kick on every beat, tight hats, snare on 2&4 or 3, subtle percussion variation
- Velocity range: 60-127 (use variation, not all at 100)
- Duration: use 0.25 for hats, 0.5 for kick/snare (in beats)

Return this exact format:
{
  "notes": [
    {"pitch": 36, "step": 0, "velocity": 110, "duration": 0.5},
    {"pitch": 42, "step": 0, "velocity": 80, "duration": 0.25}
  ],
  "bars": ${bars},
  "description": "one line description of the groove"
}`;

  const user = `Generate a ${bars}-bar minimal tech house drum pattern at ${bpm} BPM.
Loaded drum samples context: ${devices || 'standard drum rack'}.
Make it groove. Subtle variation, not robotic.`;

  callClaude(system, user, (text) => {
    try {
      const clean = text.replace(/```json|```/g, '').trim();
      const pattern = JSON.parse(clean);
      if (pattern.notes && Array.isArray(pattern.notes)) {
        Max.outlet('midi_pattern', JSON.stringify(pattern));
        Max.outlet('status', pattern.description || `${bars}-bar drum pattern ready`);
      }
    } catch (e) {
      Max.outlet('status', 'Pattern parse error — try again');
    }
  });
}

// ─────────────────────────────────────────
// MELODIC PATTERN GENERATION
// ─────────────────────────────────────────

function generateMelodicPattern(bars, scaleHint) {
  const { bpm, key } = sessionContext;
  const musicalKey = key || scaleHint || 'A minor';

  const system = `You are an expert melodic programmer for minimal and tech house music.
Generate a ${bars}-bar melodic bass or lead line in ${musicalKey} at ${bpm} BPM.

RULES:
- Return ONLY a JSON object, no explanation, no markdown  
- Use MIDI note numbers (A3=57, B3=59, C4=60, D4=62, E4=64, F4=65, G4=67, A4=69 etc)
- For minimal/tech house: sparse, hypnotic, repetitive with subtle variation
- Notes should breathe — not every 16th step filled
- Velocity range 70-110, longer notes for held tones
- Duration in beats (0.25 = 16th, 0.5 = 8th, 1.0 = quarter, 2.0 = half)

Return this exact format:
{
  "notes": [
    {"pitch": 57, "step": 0, "velocity": 95, "duration": 0.5},
    {"pitch": 60, "step": 4, "velocity": 85, "duration": 0.25}
  ],
  "bars": ${bars},
  "key": "${musicalKey}",
  "description": "one line description"
}`;

  const user = `Generate a ${bars}-bar minimal tech house melodic line in ${musicalKey} at ${bpm} BPM.
Hypnotic and driving. Think Underground Resistance meets Defected.`;

  callClaude(system, user, (text) => {
    try {
      const clean = text.replace(/```json|```/g, '').trim();
      const pattern = JSON.parse(clean);
      if (pattern.notes && Array.isArray(pattern.notes)) {
        Max.outlet('midi_pattern', JSON.stringify(pattern));
        Max.outlet('status', pattern.description || `${bars}-bar melodic pattern ready`);
      }
    } catch (e) {
      Max.outlet('status', 'Melodic parse error — try again');
    }
  });
}

// ─────────────────────────────────────────
// CHORD PATTERN GENERATION
// ─────────────────────────────────────────

function generateChordPattern(bars) {
  const { bpm, key } = sessionContext;
  const musicalKey = key || 'A minor';

  const system = `You are an expert chord programmer for minimal and tech house music.
Generate a ${bars}-bar chord progression in ${musicalKey} at ${bpm} BPM.

RULES:
- Return ONLY a JSON object, no explanation, no markdown
- Each chord = multiple notes with same step
- For tech house: stabs, offbeat hits, use inversions, keep it dark and hypnotic
- MIDI note numbers standard (C4=60)
- Velocity range 70-100, duration 0.25-0.5 for stabs, up to 1.0 for pads

Return this exact format:
{
  "notes": [
    {"pitch": 57, "step": 2, "velocity": 85, "duration": 0.25},
    {"pitch": 60, "step": 2, "velocity": 80, "duration": 0.25},
    {"pitch": 64, "step": 2, "velocity": 75, "duration": 0.25}
  ],
  "bars": ${bars},
  "key": "${musicalKey}",
  "description": "one line description"
}`;

  const user = `Generate a ${bars}-bar tech house chord stab pattern in ${musicalKey} at ${bpm} BPM.
Offbeat hits, dark voicings. Defected / Innervisions feel.`;

  callClaude(system, user, (text) => {
    try {
      const clean = text.replace(/```json|```/g, '').trim();
      const pattern = JSON.parse(clean);
      if (pattern.notes && Array.isArray(pattern.notes)) {
        Max.outlet('midi_pattern', JSON.stringify(pattern));
        Max.outlet('status', pattern.description || `${bars}-bar chord pattern ready`);
      }
    } catch (e) {
      Max.outlet('status', 'Chord parse error — try again');
    }
  });
}

Max.post('Producer script loaded');
Max.outlet('status', 'Ready');
