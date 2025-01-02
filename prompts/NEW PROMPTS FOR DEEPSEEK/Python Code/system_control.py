
def get_system_control_prompt():
    """
    Provide the system_control prompt.

    Purpose:
    This function generates the corresponding prompt content from the system_control.

    Response Format:
    Specify structured outputs where applicable.

    Returns:
    A string containing the system_control prompt content.
    """
    return """
    def control_system_access(project_id, knowledge_toggle=False, search_authorized=False):
    """
    Control system behavior for project isolation and external integrations.
    Parameters:
    - Project Isolation:
      - Limit access to project-specific transcripts and context.
      - Enforce cross-project access restrictions.
    - External Knowledge Integration:
      - Enable access to domain expertise or broader knowledge bases.
      - Require clear source citation and context alignment.
    - Web Search Protocol:
      - Authorize relevant searches within defined parameters.
    
    Output structured as:
    {
        "project_scope": str,
        "external_knowledge": bool,
        "web_search": bool,
        "constraints": List[str]
    }
    """
    return {"project_scope": project_id, "external_knowledge": knowledge_toggle, "web_search": search_authorized}
    """
