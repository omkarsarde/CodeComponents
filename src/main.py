#!/usr/bin/env python
import os
import sys
import logging
from pathlib import Path
import json
from datetime import datetime
from crew import NotebookModularizationCrew

def setup_logging():
    """Set up logging configuration."""
    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = log_dir / f'notebook_modularization_{timestamp}.log'
    
    # Create a file handler
    file_handler = logging.FileHandler(str(log_file))
    file_handler.setLevel(logging.INFO)
    
    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Create a formatter
    formatter = logging.Formatter('%(asctime)s - %(process)d - %(filename)s-%(funcName)s:%(lineno)d - %(levelname)s: %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Get the root logger and set its level
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    
    # Remove any existing handlers
    root_logger.handlers = []
    
    # Add the handlers to the root logger
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    return file_handler  # Return the file handler for proper cleanup

def main():
    """Main execution function."""
    # Set up logging
    file_handler = setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("Starting notebook modularization process")
        crew = NotebookModularizationCrew()
        result = crew.crew().kickoff()
        logger.info("Notebook modularization completed successfully")
        return result
    except Exception as e:
        logger.critical(f"Application failed: {str(e)}", exc_info=True)
        raise
    finally:
        # Clean up logging handlers
        file_handler.close()
        logging.getLogger().removeHandler(file_handler)

if __name__ == "__main__":
    main()
