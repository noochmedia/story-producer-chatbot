
def get_relationship_mapping_prompt():
    """
    Provide the relationship_mapping prompt.

    Purpose:
    This function generates the corresponding prompt content from the relationship_mapping.

    Response Format:
    Specify structured outputs where applicable.

    Returns:
    A string containing the relationship_mapping prompt content.
    """
    return """
    def map_relationships(characters):
    """
    Map character connections and dynamics.
    Deliverables:
    - Direct Relationships: Explicit connections (e.g., familial, professional).
    - Implicit Connections: Inferred ties based on context or evidence.
    - Networks: Social or professional groupings.
    - Dynamics: Quality and nature of relationships.
    
    Output structured as:
    {
        "relationships": [
            {
                "character_a": str,
                "character_b": str,
                "connection_type": str,
                "evidence": List[str],
                "strength": float
            }
        ]
    }
    """
    return characters
    """
