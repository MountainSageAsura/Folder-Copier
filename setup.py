"""
Setup script for Enhanced Folder Copier
"""

from setuptools import setup, find_packages
import os

# Read README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="enhanced-folder-copier",
    version="3.0.0",
    author="Enhanced Folder Copier Contributors",
    author_email="",
    description="A modern GUI application for copying folders with network support",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/enhanced-folder-copier",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: System :: Archiving :: Backup",
        "Topic :: Desktop Environment :: File Managers",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "folder-copier=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.ico", "*.png", "*.jpg"],
    },
    keywords="folder copier, file manager, backup, network copy, gui",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/enhanced-folder-copier/issues",
        "Source": "https://github.com/yourusername/enhanced-folder-copier",
        "Documentation": "https://github.com/yourusername/enhanced-folder-copier/blob/main/README.md",
    },
)