
def route_prompt(user_query):
    """
    Route user queries to the appropriate analysis prompt.
    Parameters:
    - user_query: The user's input or transcript analysis request.
    Deliverables:
    - Identify the appropriate prompt or analysis function based on query keywords.
    
    Example Routing:
    - "character" → analyze_character_profiling
    - "story" → analyze_story_elements
    - "relationships" → map_relationships
    """
    if "character" in user_query.lower():
        return "analyze_character_profiling"
    elif "story" in user_query.lower():
        return "analyze_story_elements"
    elif "relationships" in user_query.lower():
        return "map_relationships"
    else:
        return "default_handler"
