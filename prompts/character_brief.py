CHARACTER_BRIEF_PROMPT = """FUNCTION: CHARACTER ANALYSIS
Your role is to analyze and generate detailed character profiles from interview transcripts.

REQUIRED OUTPUT SECTIONS:
1. EXECUTIVE SUMMARY (2-3 sentences)
   - Core identity and role
   - Primary contribution to the story
   - Key relationships

2. BIOGRAPHICAL DETAILS
   - Full name and variations used
   - Relevant background information
   - Professional/personal roles mentioned

3. KEY RELATIONSHIPS
   - Family connections
   - Professional relationships
   - Important personal relationships
   - Conflicts or tensions

4. STORY INVOLVEMENT
   - First appearance/mention
   - Major events involving character
   - Important decisions or actions
   - Impact on story progression

5. NOTABLE QUOTES
   - Direct quotes showing character's voice
   - Important statements about the character
   - Context for each quote

6. ANALYSIS
   - Character development/arc
   - Recurring themes
   - Underlying motivations
   - Conflicting elements

FORMAT REQUIREMENTS:
- Use clear section headers
- Include transcript references
- Note any conflicting information
- Specify if information is implied vs. stated
- Use bullet points for clarity
- Keep focus on factual information
FUNCTION: CHARACTER BRIEF
Purpose: Generate detailed subject profiles from transcript content.

REQUIRED COMPONENTS:
1. SUBJECT IDENTIFICATION
   - Name and Role
   - Source Transcripts
   - Timeline of Appearances

2. PROFILE STRUCTURE
   - Executive Summary (2-3 sentences)
   - Key Narrative Role
   - Critical Moments (with timestamps)
   - Relationship Web
   - Story Impact

3. QUOTABLE MOMENTS
   Each quote includes:
   - Timestamp
   - Exact Quote
   - Context
   - Narrative Significance

4. STORY CONNECTIONS
   - Plot Points
   - Character Intersections
   - Theme Contributions

Before proceeding:
- Confirm subject name
- Verify transcript sources
- Note any special focus areas
"""