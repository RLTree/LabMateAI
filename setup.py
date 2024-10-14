from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README.md for the long description
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name='labmateai',
    version='1.1.0',
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
        'pandas>=1.5.3',
        'scikit-learn>=1.1.3',
        'matplotlib>=3.6.2',
        'flask>=2.2.2',
        'requests>=2.28.1',
        'scipy>=1.9.3',
        'jinja2>=3.1.2',
        'gunicorn>=20.1.0',
        'psycopg2>=2.9.0'
    ],
    entry_points={
        'console_scripts': [
            'labmateai=labmateai.cli:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'License :: OSI Approved :: MIT License',
    ],
    license='MIT',
    python_requires='>=3.8',
    keywords=[
        'AI',
        'Recommendation System',
        'Laboratory Tools',
        'Scientific Software',
        'Bioinformatics',
    ],
    project_urls={
        'Bug Reports': 'https://github.com/RLTree/LabMateAI/issues',
        'Source': 'https://github.com/RLTree/LabMateAI',
    },
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=3.0.0',
            'mock>=4.0.3',
            'flake8>=6.1.0'
        ],
        'docs': [
            'sphinx>=4.0.0',
            'furo>=2021.8.14',
        ],
    },
)
