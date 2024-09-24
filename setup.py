from setuptools import setup, find_packages

setup(
    name='labmateai',
    version='1.0.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='An AI-powered recommendation system for laboratory tools and software.',
    long_description=open('README.md', encoding='utf-8').read(),
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
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6',
)
