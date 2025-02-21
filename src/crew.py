from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import DirectoryReadTool, FileReadTool, FileWriterTool, CodeInterpreterTool
from typing import Dict, Any, List
import logging
from pathlib import Path
from datetime import datetime
from yaml import safe_load
from langchain_openai import ChatOpenAI
import os
from utils.env_loader import load_env
from tools.notebook_analyzer import NotebookAnalyzerTool
from tools.component_tester import ComponentTestTool
from tools.quality_validator import QualityValidatorTool

# Load and validate environment variables
env_config = load_env()

# Configure logging
logger = logging.getLogger(__name__)

@CrewBase
class NotebookModularizationCrew:
    """Crew for analyzing and modularizing Jupyter notebooks."""
    
    agents_config_path = 'src/config/agents.yaml'
    tasks_config_path = 'src/config/tasks.yaml'
    
    def __init__(self):
        """Initialize the crew with configurations and tools."""
        self._load_configurations()
        self._initialize_llm()
        logger.info("NotebookModularizationCrew initialized")

    def _initialize_llm(self):
        """Initialize the language model."""
        self.llm = ChatOpenAI(
            model=env_config['openai_model_name'],
            temperature=float(env_config['temperature'])
        )
        logger.info(f"Initialized LLM: {env_config['openai_model_name']}")

    def _load_configurations(self):
        """Load YAML configurations."""
        try:
            with open(self.agents_config_path, 'r') as f:
                self.agents_config = safe_load(f)
            with open(self.tasks_config_path, 'r') as f:
                self.tasks_config = safe_load(f)
            logger.info("Configurations loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load configurations: {e}")
            raise

    @agent
    def notebook_analyzer(self) -> Agent:
        """Creates the notebook analyzer agent."""
        config = self.agents_config['notebook_analyzer']
        return Agent(
            role=config['role'],
            goal=config['goal'],
            backstory=config['backstory'],
            tools=[
                NotebookAnalyzerTool(),
                DirectoryReadTool(),
                FileReadTool()
            ],
            llm=self.llm,
            verbose=True
        )

    @agent
    def code_refactorer(self) -> Agent:
        """Creates the code refactorer agent."""
        config = self.agents_config['code_refactorer']
        return Agent(
            role=config['role'],
            goal=config['goal'],
            backstory=config['backstory'],
            tools=[
                FileWriterTool(),
                CodeInterpreterTool(),
                ComponentTestTool()
            ],
            llm=self.llm,
            verbose=True
        )

    @agent
    def code_validator(self) -> Agent:
        """Creates the code validator agent."""
        config = self.agents_config['code_validator']
        return Agent(
            role=config['role'],
            goal=config['goal'],
            backstory=config['backstory'],
            tools=[
                QualityValidatorTool(),
                ComponentTestTool(),
                FileReadTool()
            ],
            llm=self.llm,
            verbose=True
        )

    @task
    def analyze_task(self) -> Task:
        """Creates the notebook analysis task."""
        config = self.tasks_config['analyze']
        return Task(
            description=config['description'],
            expected_output=config['expected_output'],
            agent=self.notebook_analyzer,
            context=config['context']
        )

    @task
    def refactor_task(self) -> Task:
        """Creates the code refactoring task."""
        config = self.tasks_config['refactor']
        return Task(
            description=config['description'],
            expected_output=config['expected_output'],
            agent=self.code_refactorer,
            context=config['context'],
            depends_on=[self.analyze_task]
        )

    @task
    def validate_task(self) -> Task:
        """Creates the code validation task."""
        config = self.tasks_config['validate']
        return Task(
            description=config['description'],
            expected_output=config['expected_output'],
            agent=self.code_validator,
            context=config['context'],
            depends_on=[self.refactor_task]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the notebook modularization crew."""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        ) 