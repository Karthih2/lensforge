def assembly_agent(
    topic: str,
    scope: dict,
    concepts: dict,
    timeline: dict,
    debates: dict,
    roadmap: dict,
    resources: dict
) -> dict:
    return {
        "topic": topic,
        "scope": scope.get("scope", scope),
        "concepts": concepts.get("concepts", concepts),
        "timeline": timeline,
        "debates": debates.get("debates", debates),
        "roadmap": roadmap,
        "resources": resources
    }
