from setuptools import setup, find_packages

# Read the contents of your README file
with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='labmateai',  # Updated package name
    version='1.0.0',  # Incremented version number
    author='Terry Noblin',
    author_email='tnoblin@health.ucsd.edu',
    description='A recommendation system for laboratory tools and software.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    # Update if repository URL has changed
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
            'labmateai=labmateai.cli:main',  # Updated console script entry point
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6',
)
