# Notebook Modularization Project

This project uses CrewAI to analyze, refactor, and validate Jupyter notebooks, transforming them into modular Python components.

## Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd codeComponents
   ```

2. **Create virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the project root with:
   ```
   OPENAI_API_KEY=your_actual_openai_key_here
   OPENAI_MODEL_NAME=gpt-4
   TEMPERATURE=0.7
   ```

5. **Prepare directories**:
   The following directories will be created automatically, but you can create them manually:
   ```bash
   mkdir -p notebooks modularized_notebooks test_data logs reports
   ```

## Usage

1. **Add input data**:
   - Place your Jupyter notebooks in the `notebooks/` directory
   - Place any test data files (CSVs, etc.) in the `test_data/` directory

2. **Run the project**:
   ```bash
   python src/main.py
   ```

3. **Check outputs**:
   - Modularized code will be in `modularized_notebooks/`
   - Execution logs will be in `logs/`
   - Analysis reports will be in `reports/`

## Project Structure

```
codeComponents/
├── src/
│   ├── main.py           # Main entry point
│   ├── crew.py          # CrewAI configuration
│   ├── config/          # YAML configurations
│   │   ├── agents.yaml  # Agent definitions
│   │   └── tasks.yaml   # Task definitions
│   ├── tools/           # Custom tools
│   │   ├── notebook_analyzer.py
│   │   ├── component_tester.py
│   │   └── quality_validator.py
│   └── utils/           # Utility functions
│       └── env_loader.py
├── notebooks/           # Input notebooks
├── modularized_notebooks/ # Output modules
├── test_data/          # Test data files
├── logs/               # Execution logs
├── reports/            # Analysis reports
├── .env               # Environment variables
└── requirements.txt    # Project dependencies
```

## Workflow

1. **Analysis**: The notebook analyzer agent examines input notebooks for:
   - Code structure and dependencies
   - Quality metrics and complexity
   - Modularization opportunities
   - ML pipeline patterns

2. **Refactoring**: The code refactorer agent:
   - Creates separate modules
   - Implements error handling
   - Adds documentation
   - Follows ML best practices

3. **Validation**: The code validator agent:
   - Runs unit tests
   - Verifies ML functionality
   - Checks code quality
   - Ensures documentation completeness

## Requirements

- Python 3.8+
- OpenAI API key
- Input Jupyter notebooks
- Test data (for validation)