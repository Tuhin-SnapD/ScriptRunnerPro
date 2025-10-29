"""
Script Runner Pro - Windows Edition
A modern script management and execution tool for Windows.
"""

__version__ = "2.0.0"
__author__ = "Script Runner Pro Team"

def main():
    """Entry point for the application."""
    import sys
    import os
    
    # Add the parent directory to the path so we can import the main module
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, parent_dir)
    
    from script_runner_gui import ScriptRunnerGUI
    from PyQt5.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    app.setApplicationName("Script Runner Pro")
    app.setApplicationVersion(__version__)
    
    ex = ScriptRunnerGUI()
    ex.show()
    sys.exit(app.exec_())

