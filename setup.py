"""
A module for setting up the labmate package.
"""

from setuptools import setup, find_packages

# Read the contents of your README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="LabMate",  # Replace with your project name
    version="1.0.0",
    author="Terry A. Noblin",
    author_email="tnoblin@health.ucsd.edu",  # Replace with your email
    description="A scientific tool recommendation system for researchers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # Replace with your GitHub repository
    url="https://github.com/RLTree/LabMate",
    packages=find_packages(),  # Automatically finds your project packages
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "argparse==1.4.0",
        "collections-extended==1.0.3",
        "jsonlib-python3==1.6.1",
        "networkx==2.8.8",
        "unittest2==1.1.0",
        "pytest==7.4.0",
        "pytest-mock==3.11.1",
        "mock==5.0.2",
        "flake8==6.1.0",
        "pandas==2.0.3",
    ],
    entry_points={
        'console_scripts': [
            'labmate=cli:main',  # Maps the CLI to a console script called 'labmate'
        ],
    },
)
