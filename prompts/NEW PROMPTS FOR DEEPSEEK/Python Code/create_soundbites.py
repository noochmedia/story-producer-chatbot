
def get_create_soundbites_prompt():
    """
    Generate a prompt for creating soundbites.

    Purpose:
    Assemble composite quotes ("frankenbites") from transcript elements while maintaining speaker intent, context accuracy, and ethical considerations.

    Deliverables:
    - Composite quotes with original timestamps and contexts.
    - Validation for speaker consistency and context preservation.
    - Ethical considerations and documentation.

    Response Format:
    {
        "frankenbites": [
            {
                "final_composite": str,
                "components": [
                    {"timestamp": str, "original": str, "context": str}
                ],
                "sources": [str],
                "context": str,
                "warnings": [str]
            }
        ],
        "verification_checklist": {
            "quote_accuracy": bool,
            "context_preservation": bool,
            "speaker_consistency": bool,
            "ethical_considerations": bool
        },
        "alternative_options": [
            {"suggestion": str, "variation": str, "notes": str}
        ]
    }

    Returns:
    A string containing the structured prompt for creating soundbites.
    """
    return """
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
