
def get_story_analysis_prompt():
    """
    Provide the story_analysis prompt.

    Purpose:
    This function generates the corresponding prompt content from the story_analysis.

    Response Format:
    Specify structured outputs where applicable.

    Returns:
    A string containing the story_analysis prompt content.
    """
    return """
    def analyze_story_elements(transcript):
    """
    Analyze the provided transcript for narrative elements.
    Deliverables:
    - Core Themes: Identify key motifs and recurring ideas.
    - Story Arcs: Map progressions and resolutions.
    - Turning Points: Highlight critical moments and their impact.
    - Character Development: Assess growth or change over time.
    - Underlying Meanings: Extract deeper implications or messages.
    
    Output structured as:
    {
        "themes": List[str],
        "arcs": [
            {
                "arc_id": str,
                "progression": List[dict],
                "resolution_status": str
            }
        ],
        "turning_points": List[dict],
        "character_progression": [
            {
                "character": str,
                "development": str
            }
        ],
        "meanings": List[str]
    }
    """
    return transcript
    """
