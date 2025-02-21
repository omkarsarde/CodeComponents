from crewai.tools import BaseTool, tool
from typing import Dict, Any
import logging
import nbformat
import ast
from pathlib import Path
import atexit
import sys
from datetime import datetime

logger = logging.getLogger(__name__)

@tool
class NotebookAnalyzerTool(BaseTool):
    """Tool for analyzing Jupyter notebooks."""
    name: str = "notebook_analyzer"  # Tool name should be snake_case
    description: str = "Analyzes Jupyter notebooks to extract code structure and assess quality"
    
    def __init__(self):
        super().__init__()
    
    def _run(self, notebook_path: str) -> Dict[str, Any]:
        """Analyzes a Jupyter notebook to extract code structure and dependencies."""
        try:
            with open(notebook_path) as f:
                nb = nbformat.read(f, as_version=4)
            
            pipeline_info = {
                "imports": [],
                "functions": [],
                "data_processing": [],
                "model_training": [],
                "evaluation": []
            }
            
            for cell in nb.cells:
                if cell.cell_type == "code":
                    tree = ast.parse(cell.source)
                    for node in ast.walk(tree):
                        if isinstance(node, ast.Import):
                            pipeline_info["imports"].extend(n.name for n in node.names)
                        elif isinstance(node, ast.FunctionDef):
                            pipeline_info["functions"].append({
                                "name": node.name,
                                "args": [arg.arg for arg in node.args.args],
                                "docstring": ast.get_docstring(node),
                                "complexity": self._calculate_complexity(node)
                            })
            
            return pipeline_info
        except Exception as e:
            logger.error(f"Notebook analysis failed: {e}")
            return {"error": str(e)}

    def _calculate_complexity(self, node: ast.AST) -> int:
        """Calculate cyclomatic complexity of a function."""
        complexity = 1  # Base complexity
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.For, ast.While, ast.Try)):
                complexity += 1
        return complexity 