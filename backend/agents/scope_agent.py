def scope_agent(topic):
    return {
        "topic": topic,
        "scope": {
            "included": ["algorithms", "applications", "data"],
            "excluded": ["pure statistics"],
            "audience": "beginner",
            "constraints": ["time-limited", "no paid tools"],
            "assumptions": ["user has basic Python knowledge"],
            "prerequisites": ["Python basics", "Linear algebra basics"]
        }
    }
