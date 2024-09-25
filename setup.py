from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README.md for the long description
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name='labmateai',
    version='1.0.0',
    author='Terry Noblin',  # Replace with your actual name
    author_email='tnoblin@health.ucsd.edu',  # Replace with your actual email
    description='An AI-powered recommendation system for laboratory tools and software.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/RLTree/LabMateAI',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'networkx>=2.5',
        'numpy>=1.18.0',
        'prompt_toolkit>=3.0.0',
    ],
    entry_points={
        'console_scripts': [
            'labmateai=labmateai.cli:main',
        ],
    },
    classifiers=[
        # Specify the Python version you're using
        'Programming Language :: Python :: 3.8',
        'Operating System :: OS Independent',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'License :: OSI Approved :: MIT License',
    ],
    license='MIT',  # Ensure this matches your LICENSE file
    python_requires='>=3.8',
    keywords=[
        'AI',
        'Recommendation System',
        'Laboratory Tools',
        'Scientific Software',
        'Bioinformatics',
    ],
    project_urls={  # Optional: Add additional URLs
        'Bug Reports': 'https://github.com/RLTree/LabMateAI/issues',
        'Source': 'https://github.com/RLTree/LabMateAI',
    },
    extras_require={  # Optional: Define additional groups of dependencies
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=3.0.0',
            'mock>=3.11.1',
            # Add other development dependencies here
        ],
        'docs': [
            'sphinx>=4.0.0',
            'furo>=2021.8.14',
            # Add other documentation dependencies here
        ],
    },
)
