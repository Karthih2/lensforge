def debate_agent(topic, timeline_output):
    return {
        "debates": [
            {
                "id": "debate1",
                "title": "Interpretability vs Performance",
                "description": "Should models prioritize explainability over accuracy?",
                "pro_arguments": ["Explainable models are safer", "Better for regulation"],
                "con_arguments": ["Accuracy is more important for predictions", "Black-box models are practical"],
                "status": "open",
                "created_at": "2025-12-14T12:00:00Z",
                "updated_at": "2025-12-14T12:00:00Z",
                "stakeholders": ["Data Scientists", "Regulators"],
                "impact_level": "high"
            }
        ]
    }
