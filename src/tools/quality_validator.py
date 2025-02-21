from crewai.tools import BaseTool, tool
from typing import Dict, Any, ClassVar
import logging
import ast
from pathlib import Path

logger = logging.getLogger(__name__)

@tool
class QualityValidatorTool(BaseTool):
    """Tool for validating code quality."""
    name: str = "quality_validator"
    description: str = "Validates code quality metrics and best practices"

    # Quality thresholds as a ClassVar
    THRESHOLDS: ClassVar[Dict[str, float]] = {
        "complexity": 10,
        "lines_of_code": 200,
        "max_function_length": 50,
        "min_doc_coverage": 0.8
    }

    def _execute(self, module_path: str) -> Dict[str, Any]:
        """Analyze code quality metrics for a Python module."""
        try:
            with open(module_path, 'r') as f:
                code = f.read()
            
            tree = ast.parse(code)
            
            # Calculate metrics
            metrics = self._calculate_metrics(tree)
            
            # Generate suggestions based on metrics
            suggestions = self._generate_suggestions(metrics)
            
            return {
                "status": "completed",
                "metrics": metrics,
                "suggestions": suggestions,
                "needs_refactor": any(
                    metrics[key] > threshold
                    for key, threshold in self.THRESHOLDS.items()
                    if key in metrics
                )
            }
            
        except Exception as e:
            logger.error(f"Quality validation failed: {e}")
            return {
                "status": "failed",
                "error": str(e)
            }

    def _calculate_metrics(self, tree: ast.AST) -> Dict[str, Any]:
        """Calculate various code quality metrics."""
        metrics = {
            "complexity": 0,
            "functions": 0,
            "classes": 0,
            "documented": 0,
            "lines_of_code": len(tree.body),
            "imports": 0,
            "max_function_length": 0,
            "avg_function_length": 0,
            "doc_coverage": 0.0
        }
        
        function_lengths = []
        
        for node in ast.walk(tree):
            # Count basic elements
            if isinstance(node, ast.FunctionDef):
                metrics["functions"] += 1
                length = len(node.body)
                function_lengths.append(length)
                metrics["max_function_length"] = max(
                    metrics["max_function_length"],
                    length
                )
                if ast.get_docstring(node):
                    metrics["documented"] += 1
            elif isinstance(node, ast.ClassDef):
                metrics["classes"] += 1
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                metrics["imports"] += 1
            
            # Calculate complexity
            if isinstance(node, (ast.If, ast.For, ast.While, ast.Try)):
                metrics["complexity"] += 1
        
        # Calculate averages and ratios
        if metrics["functions"] > 0:
            metrics["avg_function_length"] = sum(function_lengths) / metrics["functions"]
            metrics["doc_coverage"] = metrics["documented"] / metrics["functions"]
        
        return metrics

    def _generate_suggestions(self, metrics: Dict[str, Any]) -> list:
        """Generate improvement suggestions based on metrics."""
        suggestions = []
        
        if metrics["complexity"] > self.THRESHOLDS["complexity"]:
            suggestions.append(
                "High complexity detected. Consider breaking down complex functions."
            )
        
        if metrics["lines_of_code"] > self.THRESHOLDS["lines_of_code"]:
            suggestions.append(
                "Module is too large. Consider splitting into smaller modules."
            )
        
        if metrics["max_function_length"] > self.THRESHOLDS["max_function_length"]:
            suggestions.append(
                "Some functions are too long. Consider breaking them into smaller functions."
            )
        
        if metrics["doc_coverage"] < self.THRESHOLDS["min_doc_coverage"]:
            suggestions.append(
                f"Documentation coverage is {metrics['doc_coverage']:.1%}. " 
                "Add docstrings to improve coverage."
            )
        
        return [s for s in suggestions if s is not None] 