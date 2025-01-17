from crewai import Crew, Agent, Task
from yaml import safe_load
from crewai_tools import DirectoryReadTool, FileReadTool, FileWriterTool


with open("config/agents.yml", "r") as agents_file, open("config/tasks.yml", "r") as tasks_file:
    agents_config = safe_load(agents_file)
    tasks_config = safe_load(tasks_file)


analyzer_directory_tool = DirectoryReadTool(directory="./notebooks")
refactorer_directory_tool = DirectoryReadTool(directory="./modularized_notebooks")
validator_directory_tool = DirectoryReadTool(directory="./modularized_notebooks")
file_read_tool = FileReadTool()
file_writer_tool = FileWriterTool()


analyzer_agent = Agent(
    config=agents_config['notebook_analyzer_agent'],
    tools=[analyzer_directory_tool, file_read_tool]
)
refactorer_agent = Agent(
    config=agents_config['code_refactorer_agent'],
    tools=[refactorer_directory_tool, file_writer_tool]
)
validator_agent = Agent(
    config=agents_config['code_validator_agent'],
    tools=[validator_directory_tool, file_read_tool]
)


analyze_task = Task(config=tasks_config['analyze_notebooks'], agent=analyzer_agent)
report_task = Task(config=tasks_config['generate_report'], agent=analyzer_agent, context=[analyze_task])
refactor_task = Task(config=tasks_config['refactor_code'], agent=refactorer_agent, context=[report_task])
validate_task = Task(config=tasks_config['validate_code'], agent=validator_agent, context=[refactor_task])


notebook_modularization_crew = Crew(
    agents=[analyzer_agent, refactorer_agent, validator_agent],
    tasks=[analyze_task, report_task, refactor_task, validate_task],
    verbose=True
)
