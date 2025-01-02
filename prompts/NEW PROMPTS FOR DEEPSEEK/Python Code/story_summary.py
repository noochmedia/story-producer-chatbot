
def get_story_summary_prompt():
    """
    Provide the story_summary prompt.

    Purpose:
    This function generates the corresponding prompt content from the story_summary.

    Response Format:
    Specify structured outputs where applicable.

    Returns:
    A string containing the story_summary prompt content.
    """
    return """
    STORY_SUMMARY_PROMPT = """FUNCTION: STORY ANALYSIS
Your task is to analyze interview transcripts and generate a comprehensive story summary.

OUTPUT STRUCTURE:

1. NARRATIVE OVERVIEW (2-3 paragraphs)
   - Core story elements
   - Main themes
   - Key conflicts or tensions
   - Central narrative arc

2. KEY PLOT POINTS (chronological order)
   - Major events and revelations
   - Critical decisions
   - Turning points
   - Resolution points

3. CHARACTER DYNAMICS
   - Primary characters and their roles
   - Key relationships
   - Power dynamics
   - Character arcs and development

4. THEMATIC ANALYSIS
   - Core themes
   - Recurring motifs
   - Underlying messages
   - Cultural/social context

5. NARRATIVE ELEMENTS
   - Setting and context
   - Time period/timeline
   - Important locations
   - Background events

6. SUPPORTING EVIDENCE
   - Direct quotes
   - Specific examples
   - Context for key moments
   - Source references

FORMATTING REQUIREMENTS:
- Use clear section headers
- Maintain chronological order where relevant
- Include transcript references
- Note any ambiguities or contradictions
- Use bullet points for clarity
- Distinguish between stated facts and interpretations

SPECIAL CONSIDERATIONS:
- Focus on factual information from transcripts
- Note when drawing connections or making interpretations
- Highlight any gaps or unclear elements
- Consider multiple perspectives
- Track narrative threads across multiple sources
FUNCTION: STORY SUMMARY
Purpose: Create comprehensive narrative overview from all transcripts.

DELIVERY FORMAT:
1. OVERVIEW
   - Core Story Elements
   - Key Players
   - Central Conflicts

2. NARRATIVE STRUCTURE
   - Beginning: Initial Setup
   - Middle: Developing Events
   - Current Status: Latest Developments

3. THEME ANALYSIS
   - Primary Themes
   - Supporting Evidence
   - Character Contributions

4. PLOT POINTS
   Each point includes:
   - Timestamp
   - Event Description
   - Impact on Story
   - Related Characters

5. STORY ARCS
   - Main Narrative Thread
   - Sub-plots
   - Character Journeys

Confirm before proceeding:
- Timeline range to cover
- Specific focus areas
- Key characters to highlight
"""
    """
