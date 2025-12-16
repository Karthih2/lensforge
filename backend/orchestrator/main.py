import json
import os
import logging
from jsonschema import validate, ValidationError

from backend.agents.scope_agent import scope_agent
from backend.agents.concept_agent import concept_agent
from backend.agents.timeline_agent import timeline_agent
from backend.agents.debate_agent import debate_agent
from backend.agents.roadmap_agent import roadmap_agent
from backend.agents.resource_agent import resource_agent
from backend.agents.assembly_agent import assembly_agent


#LOGGING SETUP

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
LOG_DIR = os.path.join(PROJECT_ROOT, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(LOG_DIR, "orchestrator.log")),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("LensForge-Orchestrator")


#SCHEMA LOADING

def load_schema(filename):
    schema_dir = os.path.join(PROJECT_ROOT, "backend", "schemas")
    with open(os.path.join(schema_dir, filename)) as f:
        return json.load(f)

topic_scope_schema = load_schema("topic_scope.schema.json")
concepts_schema = load_schema("concepts.schema.json")
timeline_schema = load_schema("timeline.schema.json")
debates_schema = load_schema("debates.schema.json")
roadmap_schema = load_schema("roadmap.schema.json")
resources_schema = load_schema("resources.schema.json")
final_schema = load_schema("final_output.schema.json")


#ORCHESTRATOR

def run_pipeline(topic):
    try:
        logger.info("Starting Topic Analysis Agent")
        scope_output = scope_agent(topic)
        validate(scope_output, topic_scope_schema)
        logger.info("Topic Analysis Agent completed")

        logger.info("Starting Concept Extraction Agent")
        concepts_output = concept_agent(scope_output)
        validate(concepts_output, concepts_schema)
        logger.info("Concept Extraction Agent completed")

        logger.info("Starting Timeline Agent")
        timeline_output = timeline_agent(topic, concepts_output)
        validate(timeline_output, timeline_schema)
        logger.info("Timeline Agent completed")

        logger.info("Starting Debate Agent")
        debates_output = debate_agent(topic, timeline_output)
        validate(debates_output, debates_schema)
        logger.info("Debate Agent completed")

        logger.info("Starting Roadmap Agent")
        roadmap_output = roadmap_agent(concepts_output, debates_output)
        validate(roadmap_output, roadmap_schema)
        logger.info("Roadmap Agent completed")

        logger.info("Starting Resource Agent")
        resources_output = resource_agent(concepts_output, roadmap_output)
        validate(resources_output, resources_schema)
        logger.info("Resource Agent completed")

        logger.info("Assembling Final Output")
        final_output = assembly_agent(
            topic,
            scope_output,
            concepts_output,
            timeline_output,
            debates_output,
            roadmap_output,
            resources_output
        )
        validate(final_output, final_schema)
        logger.info("Pipeline completed successfully")

        return final_output

    except ValidationError as ve:
        logger.error("Schema validation failed", exc_info=True)
        raise

    except Exception as e:
        logger.critical("Pipeline crashed", exc_info=True)
        raise


#ENTRY POINT
if __name__ == "__main__":
    result = run_pipeline("Machine Learning")
    print(json.dumps(result, indent=2))
