
import os
from utils import load_env
from crew import notebook_modularization_crew

load_env()
os.environ['OPENAI_MODEL_NAME'] = 'gpt-4o-mini'


def run():
    """
    Run the notebook modularization workflow.
    """
    inputs = {
        "directory": "notebooks/",
        "output_directory": "modularized_notebooks/"
    }

    print("## Welcome to Notebook Modularization Crew")
    print("------------------------------------------")
    print(f"Input directory: {inputs['directory']}")
    print(f"Output directory: {inputs['output_directory']}")

    try:
        result = notebook_modularization_crew.kickoff(inputs=inputs)
        print("\nWorkflow completed successfully.")
        print("\n########################")
        print("## Workflow Report")
        print("########################\n")
        print(result)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    run()
