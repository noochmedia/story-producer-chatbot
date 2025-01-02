
def get_context_check_prompt():
    """
    Provide the context_check prompt.

    Purpose:
    This function generates the corresponding prompt content from the context_check.

    Response Format:
    Specify structured outputs where applicable.

    Returns:
    A string containing the context_check prompt content.
    """
    return """
    CONTEXT_CHECK_PROMPT = """FUNCTION: CONTEXT ANALYSIS
Your task is to analyze the conversation history and current query to maintain coherent context and provide relevant responses.

ANALYSIS PARAMETERS:

1. CONVERSATION TRACKING
   - Current topic/focus
   - Active characters
   - Recent references
   - Ongoing themes

2. QUERY ANALYSIS
   - Topic relevance
   - Context continuity
   - Reference resolution
   - Intent classification

3. CONTEXT ELEMENTS
   Current:
   - Active transcript
   - Focused character
   - Recent topics
   - Last action

   History:
   - Previous queries
   - Past responses
   - Topic progression
   - Character mentions

RESPONSE FORMAT:
{
    "context_status": {
        "topic_continuity": true/false,
        "character_focus": "name" or null,
        "reference_type": "direct/indirect/none",
        "context_shift": true/false
    },
    "references": {
        "characters": ["list", "of", "names"],
        "topics": ["list", "of", "topics"],
        "transcripts": ["list", "of", "ids"]
    },
    "suggested_action": {
        "prompt_type": "type",
        "focus": "specific focus",
        "include_history": true/false
    }
}

Return ONLY the JSON object, no additional text.
FUNCTION: CONTEXT CHECK
Purpose: Verify quote context and usage

Verify:
- Original Context
- Speaker Intent
- Related Quotes
- Timeline Placement
"""
    """
