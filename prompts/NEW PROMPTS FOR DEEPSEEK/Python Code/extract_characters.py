
def get_extract_characters_prompt():
    """
    Provide the extract_characters prompt.

    Purpose:
    This function generates the corresponding prompt content from the extract_characters.

    Response Format:
    Specify structured outputs where applicable.

    Returns:
    A string containing the extract_characters prompt content.
    """
    return """
    EXTRACT_CHARACTERS_PROMPT = """
FUNCTION: EXTRACT CHARACTERS
Purpose: Identify and list all unique named individuals from transcript content.

INSTRUCTIONS:
1. Scan the provided transcript for all named individuals
2. Extract full names where available, otherwise use the most complete form mentioned
3. Include only real people (not mentions of historical/fictional figures)
4. Format output as a simple comma-separated list
5. Do not include titles unless they are part of how the person is consistently referenced
6. Exclude the interviewer unless they are a significant part of the narrative
7. If the same person is referred to by multiple names/variants, use their most complete name form

Example output format:
John Smith, Mary Johnson, Robert "Bob" Williams

CRITICAL NOTES:
- Focus on actual participants in the events/story
- Include people who are talked about significantly, even if not present
- Use the most formal/complete version of names when multiple versions appear
- The response should ONLY be the comma-separated list, no other text
"""
    """
