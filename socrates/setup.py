"""
Setup script for Socrates package
"""

from setuptools import setup, find_packages
import os

# Read README for long description
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), '..', 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "AI-Powered Interview Assistant"

# Read requirements
def read_requirements():
    requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(requirements_path):
        with open(requirements_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return [
        'pyaudio>=0.2.11',
        'tkinter',  # Usually comes with Python
    ]

setup(
    name="socrates",
    version="1.0.0",
    author="Socrates Team",
    author_email="team@socrates.ai",
    description="AI-Powered Interview Assistant",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/socrates-team/socrates",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Multimedia :: Sound/Audio :: Capture/Recording",
        "Topic :: Communications :: Chat",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "socrates=socrates.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="ai, interview, assistant, audio, recording, real-time",
    project_urls={
        "Bug Reports": "https://github.com/socrates-team/socrates/issues",
        "Source": "https://github.com/socrates-team/socrates",
        "Documentation": "https://github.com/socrates-team/socrates/wiki",
    },
)
