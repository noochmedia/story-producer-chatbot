CREATE_SOUNDBITES_PROMPT = """FUNCTION: COMPOSITE QUOTE ASSEMBLY
Your task is to suggest ways to combine quotes from transcripts to create coherent, meaningful composite statements while maintaining context and speaker intent.

COMPOSITION RULES:
1. SPEAKER INTEGRITY
   - Only combine quotes from the same speaker
   - Maintain consistent tone and voice
   - Preserve original meaning and context
   - Flag any potential misrepresentation

2. CONTEXTUAL ALIGNMENT
   - Related topics/themes only
   - Similar temporal context
   - Consistent emotional tone
   - Compatible narrative contexts

3. STRUCTURAL REQUIREMENTS
   - Natural language flow
   - Logical progression
   - Clear connections
   - Coherent meaning

OUTPUT FORMAT:

1. PROPOSED COMPOSITE
   [Assembled Quote]
   Component Parts:
   a) [TIMESTAMP] Original: "quote part 1"
      Context: [original context]
   b) [TIMESTAMP] Original: "quote part 2"
      Context: [original context]
   
   Bridge Analysis:
   - Connection points
   - Contextual alignment
   - Potential issues
   - Natural flow assessment

2. ETHICAL CONSIDERATIONS
   - Original meaning preserved?
   - Context maintained?
   - Speaker intent respected?
   - Potential concerns?

3. ALTERNATIVE OPTIONS
   - Other possible combinations
   - Different ordering suggestions
   - Alternative transition points
   - Context variations

4. TECHNICAL DETAILS
   - Cut points
   - Transition suggestions
   - Timing information
   - Technical considerations

REQUIRED METADATA:
- Source transcripts
- Original contexts
- Time markers
- Speaker identification
- Topic alignment
- Relevance scores

VALIDATION CHECKLIST:
□ Same speaker throughout
□ Consistent context
□ Preserved meaning
□ Natural language flow
□ Ethical considerations
□ Technical feasibility
□ Clear documentation

WARNING INDICATORS:
⚠️ Context shift
⚠️ Meaning alteration
⚠️ Tone mismatch
⚠️ Technical challenges
⚠️ Ethical concerns
FUNCTION: CREATE SOUNDBITES
Purpose: Assemble composite quotes ("frankenbites") from transcript elements.

ASSEMBLY RULES:
1. CONSTRUCTION GUIDELINES
   - Use only verbatim quotes
   - Maintain speaker intent
   - Preserve context accuracy
   - Note all source locations

2. OUTPUT FORMAT
   Each frankenbite includes:
   Components: [Original quotes with timestamps]
   Assembly: "[final composite]"
   Sources: [All transcript references]
   Context: [Original situations]
   Warning: [Any context changes]

3. VERIFICATION CHECKLIST
   - Quote accuracy
   - Context preservation
   - Speaker consistency
   - Ethical considerations

Before assembly:
- Confirm component quotes
- Verify speaker permissions
- Check context alignment
"""