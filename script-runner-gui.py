#!/usr/bin/env python3

import sys
import subprocess
import json
import os
import platform
import webbrowser
from pathlib import Path
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QHBoxLayout, 
                            QVBoxLayout, QWidget, QAction, QFileDialog, QInputDialog, 
                            QMenu, QStyle, QLabel, QLineEdit, QComboBox, QTextEdit,
                            QMessageBox, QSplitter, QListWidget, QListWidgetItem,
                            QGroupBox, QGridLayout, QScrollArea, QFrame, QSizePolicy)
from PyQt5.QtCore import Qt, QMimeData, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QPixmap, QPalette, QColor

class ScriptExecutionThread(QThread):
    output_ready = pyqtSignal(str)
    finished = pyqtSignal(int)
    
    def __init__(self, command, working_dir=None):
        super().__init__()
        self.command = command
        self.working_dir = working_dir
        
    def run(self):
        try:
            process = subprocess.Popen(
                self.command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                cwd=self.working_dir,
                shell=True
            )
            
            for line in iter(process.stdout.readline, ''):
                if line:
                    self.output_ready.emit(line.strip())
                    
            process.wait()
            self.finished.emit(process.returncode)
        except Exception as e:
            self.output_ready.emit(f"Error: {str(e)}")
            self.finished.emit(-1)

class ScriptRunnerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.script_data = {}  # Store script metadata
        self.current_script = None
        self.execution_thread = None
        self.is_windows = platform.system() == "Windows"
        self.initUI()
        self.load_scripts()

    def initUI(self):
        self.setWindowTitle("Script Runner Pro - Windows Edition")
        self.setGeometry(100, 100, 1000, 700)
        self.setAcceptDrops(True)
        
        # Set modern styling
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
            QPushButton:pressed {
                background-color: #005a9e;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
            QLineEdit {
                padding: 8px;
                border: 2px solid #ddd;
                border-radius: 4px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #0078d4;
            }
            QComboBox {
                padding: 8px;
                border: 2px solid #ddd;
                border-radius: 4px;
                background-color: white;
            }
            QTextEdit {
                border: 2px solid #ddd;
                border-radius: 4px;
                background-color: white;
                font-family: 'Consolas', 'Courier New', monospace;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #ddd;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)

        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # Create splitter for resizable panels
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)

        # Left panel - Script list
        left_panel = self.create_script_panel()
        splitter.addWidget(left_panel)

        # Right panel - Script details and output
        right_panel = self.create_details_panel()
        splitter.addWidget(right_panel)

        # Set splitter proportions
        splitter.setSizes([300, 700])

        # Create menu bar
        self.create_menu_bar()

        # Create status bar
        self.statusBar().showMessage("Ready")

    def create_script_panel(self):
        panel = QWidget()
        layout = QVBoxLayout(panel)

        # Search box
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Search:"))
        self.search_box = QLineEdit()
        self.search_box.textChanged.connect(self.filter_scripts)
        search_layout.addWidget(self.search_box)
        layout.addLayout(search_layout)

        # Script list
        self.script_list = QListWidget()
        self.script_list.itemClicked.connect(self.on_script_selected)
        layout.addWidget(self.script_list)

        # Add script button
        add_btn = QPushButton("Add New Script")
        add_btn.clicked.connect(self.add_script)
        layout.addWidget(add_btn)

        return panel

    def create_details_panel(self):
        panel = QWidget()
        layout = QVBoxLayout(panel)

        # Script info group
        info_group = QGroupBox("Script Information")
        info_layout = QGridLayout(info_group)

        info_layout.addWidget(QLabel("Name:"), 0, 0)
        self.name_edit = QLineEdit()
        self.name_edit.textChanged.connect(self.update_script_name)
        info_layout.addWidget(self.name_edit, 0, 1)

        info_layout.addWidget(QLabel("Path:"), 1, 0)
        self.path_edit = QLineEdit()
        self.path_edit.textChanged.connect(self.update_script_path)
        info_layout.addWidget(self.path_edit, 1, 1)

        info_layout.addWidget(QLabel("Type:"), 2, 0)
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Python", "PowerShell", "Batch", "CMD", "Other"])
        self.type_combo.currentTextChanged.connect(self.update_script_type)
        info_layout.addWidget(self.type_combo, 2, 1)

        info_layout.addWidget(QLabel("Category:"), 3, 0)
        self.category_edit = QLineEdit()
        self.category_edit.setPlaceholderText("e.g., Development, Automation, Tools")
        self.category_edit.textChanged.connect(self.update_script_category)
        info_layout.addWidget(self.category_edit, 3, 1)

        layout.addWidget(info_group)

        # Action buttons
        button_layout = QHBoxLayout()
        
        self.run_btn = QPushButton("▶ Run Script")
        self.run_btn.clicked.connect(self.run_script)
        self.run_btn.setEnabled(False)
        button_layout.addWidget(self.run_btn)

        self.edit_btn = QPushButton("✏ Edit")
        self.edit_btn.clicked.connect(self.edit_script)
        self.edit_btn.setEnabled(False)
        button_layout.addWidget(self.edit_btn)

        self.delete_btn = QPushButton("🗑 Delete")
        self.delete_btn.clicked.connect(self.delete_script)
        self.delete_btn.setEnabled(False)
        button_layout.addWidget(self.delete_btn)

        layout.addLayout(button_layout)

        # Output group
        output_group = QGroupBox("Output")
        output_layout = QVBoxLayout(output_group)
        
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setMaximumHeight(200)
        output_layout.addWidget(self.output_text)

        # Clear output button
        clear_btn = QPushButton("Clear Output")
        clear_btn.clicked.connect(self.clear_output)
        output_layout.addWidget(clear_btn)

        layout.addWidget(output_group)

        return panel

    def create_menu_bar(self):
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('File')
        
        add_action = QAction('Add Script', self)
        add_action.setShortcut('Ctrl+N')
        add_action.triggered.connect(self.add_script)
        file_menu.addAction(add_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Tools menu
        tools_menu = menubar.addMenu('Tools')
        
        settings_action = QAction('Settings', self)
        settings_action.triggered.connect(self.show_settings)
        tools_menu.addAction(settings_action)

        # Help menu
        help_menu = menubar.addMenu('Help')
        
        about_action = QAction('About', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            if url.isLocalFile():
                self.add_script_from_path(url.toLocalFile())

    def add_script_from_path(self, script_path):
        script_name = Path(script_path).stem
        script_name, ok = QInputDialog.getText(
            self, 'Add Script', 
            'Enter name for the script:', 
            text=script_name
        )
        if ok and script_name:
            # Determine script type based on extension
            ext = Path(script_path).suffix.lower()
            script_type = "Other"
            if ext == '.py':
                script_type = "Python"
            elif ext == '.ps1':
                script_type = "PowerShell"
            elif ext in ['.bat', '.cmd']:
                script_type = "Batch" if ext == '.bat' else "CMD"
            
            self.add_script_to_list(script_name, script_path, script_type, "")

    def add_script(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter(
            "All Scripts (*.py *.ps1 *.bat *.cmd *.sh);;"
            "Python (*.py);;"
            "PowerShell (*.ps1);;"
            "Batch (*.bat);;"
            "CMD (*.cmd);;"
            "Shell (*.sh)"
        )
        script_path, _ = file_dialog.getOpenFileName(
            self, "Select Script", "", 
            "All Scripts (*.py *.ps1 *.bat *.cmd *.sh)"
        )
        if script_path:
            self.add_script_from_path(script_path)

    def add_script_to_list(self, name, path, script_type="Other", category=""):
        # Add to script data
        self.script_data[name] = {
            'path': path,
            'type': script_type,
            'category': category
        }
        
        # Add to list widget
        item = QListWidgetItem(name)
        item.setData(Qt.UserRole, name)
        self.script_list.addItem(item)
        
        # Save to file
        self.save_scripts()

    def on_script_selected(self, item):
        script_name = item.data(Qt.UserRole)
        if script_name in self.script_data:
            self.current_script = script_name
            script_info = self.script_data[script_name]
            
            # Update detail panel
            self.name_edit.setText(script_name)
            self.path_edit.setText(script_info['path'])
            self.type_combo.setCurrentText(script_info['type'])
            self.category_edit.setText(script_info['category'])
            
            # Enable buttons
            self.run_btn.setEnabled(True)
            self.edit_btn.setEnabled(True)
            self.delete_btn.setEnabled(True)

    def update_script_name(self, new_name):
        if self.current_script and new_name != self.current_script:
            # Update the data
            script_info = self.script_data.pop(self.current_script)
            self.script_data[new_name] = script_info
            
            # Update the list item
            for i in range(self.script_list.count()):
                item = self.script_list.item(i)
                if item.data(Qt.UserRole) == self.current_script:
                    item.setText(new_name)
                    item.setData(Qt.UserRole, new_name)
                    break
            
            self.current_script = new_name
            self.save_scripts()

    def update_script_path(self, new_path):
        if self.current_script:
            self.script_data[self.current_script]['path'] = new_path
            self.save_scripts()

    def update_script_type(self, new_type):
        if self.current_script:
            self.script_data[self.current_script]['type'] = new_type
            self.save_scripts()

    def update_script_category(self, new_category):
        if self.current_script:
            self.script_data[self.current_script]['category'] = new_category
            self.save_scripts()

    def run_script(self):
        if not self.current_script or self.current_script not in self.script_data:
            return
        
        script_info = self.script_data[self.current_script]
        script_path = script_info['path']
        script_type = script_info['type']
        
        if not os.path.exists(script_path):
            QMessageBox.warning(self, "Error", f"Script file not found: {script_path}")
            return
        
        # Clear previous output
        self.clear_output()
        
        # Build command based on script type
        if script_type == "Python":
            command = f'python "{script_path}"'
        elif script_type == "PowerShell":
            command = f'powershell -ExecutionPolicy Bypass -File "{script_path}"'
        elif script_type == "Batch":
            command = f'"{script_path}"'
        elif script_type == "CMD":
            command = f'cmd /c "{script_path}"'
        else:
            # Try to run directly
            command = f'"{script_path}"'
        
        # Start execution thread
        self.execution_thread = ScriptExecutionThread(command, os.path.dirname(script_path))
        self.execution_thread.output_ready.connect(self.append_output)
        self.execution_thread.finished.connect(self.on_script_finished)
        self.execution_thread.start()
        
        self.run_btn.setEnabled(False)
        self.run_btn.setText("⏸ Running...")
        self.statusBar().showMessage(f"Running {self.current_script}...")

    def append_output(self, text):
        self.output_text.append(text)
        # Auto-scroll to bottom
        cursor = self.output_text.textCursor()
        cursor.movePosition(cursor.End)
        self.output_text.setTextCursor(cursor)

    def on_script_finished(self, exit_code):
        self.run_btn.setEnabled(True)
        self.run_btn.setText("▶ Run Script")
        
        if exit_code == 0:
            self.statusBar().showMessage(f"Script '{self.current_script}' completed successfully")
        else:
            self.statusBar().showMessage(f"Script '{self.current_script}' finished with exit code {exit_code}")
        
        self.append_output(f"\n--- Script finished with exit code: {exit_code} ---")

    def edit_script(self):
        if not self.current_script or self.current_script not in self.script_data:
            return
        
        script_path = self.script_data[self.current_script]['path']
        
        if not os.path.exists(script_path):
            QMessageBox.warning(self, "Error", f"Script file not found: {script_path}")
            return
        
        # Open with default editor
        try:
            if self.is_windows:
                os.startfile(script_path)
            else:
                subprocess.Popen(['xdg-open', script_path])
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Could not open script: {str(e)}")

    def delete_script(self):
        if not self.current_script:
            return
        
        reply = QMessageBox.question(
            self, 'Delete Script',
            f'Are you sure you want to delete "{self.current_script}"?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Remove from data
            if self.current_script in self.script_data:
                del self.script_data[self.current_script]
            
            # Remove from list
            for i in range(self.script_list.count()):
                item = self.script_list.item(i)
                if item.data(Qt.UserRole) == self.current_script:
                    self.script_list.takeItem(i)
                    break
            
            # Clear detail panel
            self.current_script = None
            self.name_edit.clear()
            self.path_edit.clear()
            self.category_edit.clear()
            self.run_btn.setEnabled(False)
            self.edit_btn.setEnabled(False)
            self.delete_btn.setEnabled(False)
            
            # Save changes
            self.save_scripts()

    def clear_output(self):
        self.output_text.clear()

    def filter_scripts(self, text):
        for i in range(self.script_list.count()):
            item = self.script_list.item(i)
            script_name = item.data(Qt.UserRole)
            if text.lower() in script_name.lower():
                item.setHidden(False)
            else:
                item.setHidden(True)

    def save_scripts(self):
        try:
            with open('scripts.json', 'w') as file:
                json.dump(self.script_data, file, indent=2)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Could not save scripts: {str(e)}")

    def load_scripts(self):
        try:
            with open('scripts.json', 'r') as file:
                self.script_data = json.load(file)
                
            # Populate list
            for name, info in self.script_data.items():
                item = QListWidgetItem(name)
                item.setData(Qt.UserRole, name)
                self.script_list.addItem(item)
                
        except FileNotFoundError:
            # Create empty file
            with open('scripts.json', 'w') as file:
                json.dump({}, file)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Could not load scripts: {str(e)}")

    def show_settings(self):
        QMessageBox.information(self, "Settings", "Settings dialog will be implemented in a future version.")

    def show_about(self):
        QMessageBox.about(self, "About Script Runner Pro", 
                         "Script Runner Pro - Windows Edition\n\n"
                         "A modern script management and execution tool.\n"
                         "Supports Python, PowerShell, Batch, and more.\n\n"
                         "Version 2.0")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("Script Runner Pro")
    app.setApplicationVersion("2.0")
    
    
    ex = ScriptRunnerGUI()
    ex.show()
    sys.exit(app.exec_())
