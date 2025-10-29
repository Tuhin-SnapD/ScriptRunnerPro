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
    from PyQt5.QtGui import QIcon
    
    app = QApplication(sys.argv)
    app.setApplicationName("Script Runner Pro")
    app.setApplicationVersion(__version__)
    
    # Set application icon if available
    icon_path = os.path.join(parent_dir, 'script-runner-icon.png')
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    
    ex = ScriptRunnerGUI()
    ex.show()
    sys.exit(app.exec_())

