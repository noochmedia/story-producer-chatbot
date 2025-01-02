
def get_character_profiling_prompt():
    """
    Provide the character_profiling prompt.

    Purpose:
    This function generates the corresponding prompt content from the character_profiling.

    Response Format:
    Specify structured outputs where applicable.

    Returns:
    A string containing the character_profiling prompt content.
    """
    return """
    def analyze_character_profiling(transcript):
    """
    Analyze the provided transcript or notes and extract detailed profiles for each character.
    Deliverables:
    - Full Name and Role: (e.g., Steve Barfield, believer and investigator)
    - Core Motivations: Why does this person act or believe as they do?
    - Key Evidence or Beliefs: Summarize their evidence, beliefs, or statements.
    - Emotional Stakes: What drives their emotional investment in the story?
    - Relevant Interactions: Notable relationships or moments.
    - Quotes with Context: Key quotes with timestamps and their significance.
    
    Output in structured JSON:
    {
        "characters": [
            {
                "name": "full_name",
                "role": "role_description",
                "motivations": ["motivation1", "motivation2"],
                "evidence": ["evidence1", "evidence2"],
                "emotional_stakes": "emotional_description",
                "relationships": ["relationship1", "relationship2"],
                "quotes": [
                    {
                        "text": "exact_quote",
                        "timestamp": "hh:mm:ss",
                        "context": "quote_context"
                    }
                ]
            }
        ]
    }
    """
    return transcript
    """
