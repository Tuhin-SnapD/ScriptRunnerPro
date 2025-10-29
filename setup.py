# Script Runner Pro - Windows Edition

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "Script Runner Pro - A modern script management and execution tool for Windows"

setup(
    name="script-runner-pro",
    version="2.0.0",
    author="Script Runner Pro Team",
    description="A modern script management and execution tool for Windows",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/Tuhin-SnapD/ScriptRunnerPro",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Desktop Environment",
        "Topic :: System :: Systems Administration",
    ],
    python_requires=">=3.7",
    install_requires=[
        "PyQt5>=5.15.0",
    ],
    entry_points={
        "console_scripts": [
            "script-runner-pro=script_runner_gui:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.json"],
    },
)
