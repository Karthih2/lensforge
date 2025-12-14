Agent 1 — Topic Analysis Agent

Input: Raw topic string
Output: Normalized scope + boundaries

Agent 2 — Concept Extraction Agent

Input: Scoped topic
Output: 8–12 foundational concepts with 1-line explanations

Agent 3 — Timeline Agent

Input: Topic + concepts
Output: Past → Present → Future

Agent 4 — Debate Agent

Input: Topic + current state
Output: 3–5 real debates

Agent 5 — Roadmap Agent

Input: Concepts + debates
Output: Skill roadmap (weeks/months)

Agent 6 — Resource Agent

Input: Concepts + roadmap
Output: Curated resources (books, papers, tools)

Agent 7 — Assembly / UI Agent

Input: All structured outputs
Output: Clean JSON → UI-friendly format

Schemas
A data contract is a formal promise between parts of your system.
Data contracts give you:
    Deterministic behavior
    Easy debugging
    Safe retries
    Replaceable agents
    UI that never breaks unexpectedly

Field name – what is this data?
Type – string, array, object, enum
Required vs optional
Constraints – min/max length, allowed values
Semantic meaning – what this field means

Data Flow & Contracts

In LensForge, every agent communicates using structured data rather than free text. This ensures clarity, reliability, and easy debugging.

Key Principles
Every agent must output valid JSON
    Each agent’s output strictly follows its defined schema.
    No loosely formatted text is allowed.

Orchestrator validates schema
    The orchestrator checks each agent’s output against its corresponding JSON schema.
    Only valid outputs are passed to downstream agents.

Invalid output → retry or fail
    If an agent produces invalid JSON, the orchestrator either retries the task or logs a failure.
    This prevents cascading errors and ensures deterministic system behavior.