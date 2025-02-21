from crewai.tools import BaseTool, tool
from typing import Dict, Any
import logging
import inspect
import importlib.util
import pandas as pd
from crewai_tools import CodeInterpreterTool

logger = logging.getLogger(__name__)

@tool
class ComponentTestTool(BaseTool):
    """Tool for testing refactored code components."""
    name: str = "component_tester"
    description: str = "Tests individual components of the refactored code"

    def _execute(self, component_path: str, test_data_path: str) -> str:
        """Run tests on a component using provided test data."""
        try:
            code_interpreter = CodeInterpreterTool()
            
            # Import the module dynamically
            spec = importlib.util.spec_from_file_location("module", component_path)
            if not spec or not spec.loader:
                raise ImportError(f"Could not load module from {component_path}")
            
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Generate and run tests
            test_code = self._generate_test_code(module, test_data_path)
            result = code_interpreter.execute(test_code)
            
            return f"Test Results:\n{result}"
        except Exception as e:
            logger.error(f"Component testing failed: {e}")
            return f"Test Failed: {str(e)}"

    def _generate_test_code(self, module: Any, test_data_path: str) -> str:
        """Generate test code for each function in the module."""
        module_functions = inspect.getmembers(module, inspect.isfunction)
        test_cases = []
        
        for func_name, func in module_functions:
            # Get function signature and docstring for better testing
            sig = inspect.signature(func)
            doc = inspect.getdoc(func) or ""
            
            test_cases.append(f"""
def test_{func_name}():
    \"\"\"Test {func_name} with sample data.
    
    Function Signature: {sig}
    Documentation: {doc}
    \"\"\"
    test_data = pd.read_csv('{test_data_path}')
    try:
        result = {func_name}(test_data)
        assert result is not None, "Function returned None"
        print(f"✓ Test passed for {func_name}")
        return result
    except Exception as e:
        print(f"✗ Test failed for {func_name}: {str(e)}")
        raise

print(f"Running tests for {func_name}...")
result = test_{func_name}()
print("-" * 50)
""")
        return "\n".join(test_cases) 