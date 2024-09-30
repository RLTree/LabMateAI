# tests/test_cli.py

"""
Unit tests for the CLI class.
"""

import pytest
from unittest.mock import patch
from ..cli import CLI
from ..tool import Tool
from ..recommender import Recommender


# Define sample tools for testing
SAMPLE_TOOLS = [
    Tool(
        name='Seurat',
        category='Single-Cell Analysis',
        features=['Single-cell RNA-seq', 'Clustering'],
        cost='Free',
        description='An R package for single-cell RNA sequencing data.',
        url='https://satijalab.org/seurat/',
        language='R',
        platform='Cross-platform'
    ),
    Tool(
        name='Scanpy',
        category='Single-Cell Analysis',
        features=['Single-cell RNA-seq', 'Visualization'],
        cost='Free',
        description='A scalable toolkit for analyzing single-cell gene expression data.',
        url='https://scanpy.readthedocs.io/',
        language='Python',
        platform='Cross-platform'
    ),
    Tool(
        name='GenomicsToolX',
        category='Genomics',
        features=['Genome Assembly', 'Variant Calling'],
        cost='Free',
        description='A tool for comprehensive genome assembly and variant calling.',
        url='https://genomicstoolx.com/',
        language='Python',
        platform='Cross-platform'
    ),
    Tool(
        name='Bowtie',
        category='Genomics',
        features=['Sequence Alignment', 'Genome Mapping'],
        cost='Free',
        description='A fast and memory-efficient tool for aligning sequencing reads to long reference sequences.',
        url='https://bowtie-bio.sourceforge.net/index.shtml',
        language='C++',
        platform='Cross-platform'
    ),
    Tool(
        name='RNAAnalyzer',
        category='RNA',
        features=['RNA-Seq Analysis', 'Differential Expression'],
        cost='Free',
        description='A tool for analyzing RNA-Seq data and identifying differential gene expression.',
        url='https://rnaanalyzer.example.com/',
        language='R',
        platform='Cross-platform'
    )
]


@pytest.fixture
def mock_recommender():
    """
    Fixture to provide a mock Recommender instance.
    """
    recommender = Recommender(tools=SAMPLE_TOOLS)

    # Mock the methods to return controlled outputs
    with patch.object(recommender, 'recommend_similar_tools') as mock_recommend_similar:
        with patch.object(recommender, 'recommend_tools_in_category') as mock_recommend_category:
            with patch.object(recommender, 'search_and_recommend') as mock_search:
                # Define mock return values based on input
                def recommend_similar_tools_side_effect(tool_name, num_recommendations):
                    if tool_name.lower() == 'seurat':
                        return [SAMPLE_TOOLS[1]]  # Scanpy
                    else:
                        raise ValueError(f"Tool '{tool_name}' not found.")

                def recommend_tools_in_category_side_effect(category_name):
                    if category_name.lower() == 'genomics':
                        # GenomicsToolX, Bowtie
                        return [SAMPLE_TOOLS[2], SAMPLE_TOOLS[3]]
                    else:
                        return []

                def search_and_recommend_side_effect(keyword):
                    if keyword.lower() == 'rna':
                        # Seurat, Scanpy, RNAAnalyzer
                        return [SAMPLE_TOOLS[0], SAMPLE_TOOLS[1], SAMPLE_TOOLS[4]]
                    else:
                        return []

                mock_recommend_similar.side_effect = recommend_similar_tools_side_effect
                mock_recommend_category.side_effect = recommend_tools_in_category_side_effect
                mock_search.side_effect = search_and_recommend_side_effect

                yield recommender


@pytest.fixture
def cli_instance(mock_recommender):
    """
    Fixture to provide a CLI instance initialized with the mock Recommender.
    """
    return CLI(recommender=mock_recommender)


@pytest.mark.parametrize("input_sequence, expected_output_checks", [
    # Test Case 1: Recommend similar tools to 'Seurat'
    (
        ['1', 'Seurat', '4'],
        ['Recommendations:', '- Scanpy:']
    ),
    # Test Case 2: Recommend tools in 'Genomics' category
    (
        ['2', 'Genomics', '4'],
        ['Recommendations:', '- GenomicsToolX:', '- Bowtie:']
    ),
    # Test Case 3: Search tools by keyword 'RNA'
    (
        ['3', 'RNA', '4'],
        ['Recommendations:', '- Seurat:', '- Scanpy:', '- RNAAnalyzer:']
    )
])
def test_cli_interactive_modes(cli_instance, input_sequence, expected_output_checks, capsys):
    """
    Test the interactive mode of the CLI with valid inputs.

    Args:
        cli_instance: Instance of the CLI class.
        input_sequence: List of user inputs to simulate.
        expected_output_checks: List of substrings expected to be in the output.
        capsys: Pytest fixture to capture stdout and stderr.
    """
    # Patch 'sys.argv' to simulate no command-line arguments (interactive mode)
    with patch('sys.argv', ['cli.py']):
        # Patch 'input' to simulate user inputs
        with patch('builtins.input', side_effect=input_sequence):
            cli_instance.start()

    # Capture the output
    captured = capsys.readouterr()
    stdout = captured.out

    # Check for expected substrings in the output
    for expected_substring in expected_output_checks:
        assert expected_substring in stdout, f"Expected '{expected_substring}' to be in the output."


@pytest.mark.parametrize("input_sequence, expected_output", [
    # Test Case 4: Recommend similar tools to a non-existent tool
    (
        ['1', 'NonExistentTool', '4'],
        "Tool 'NonExistentTool' not found."
    ),
    # Test Case 5: Recommend tools in a non-existent category
    (
        ['2', 'NonExistentCategory', '4'],
        "No tools found in category 'NonExistentCategory'."
    ),
    # Test Case 6: Search tools by a non-existent keyword
    (
        ['3', 'NonExistentKeyword', '4'],
        "No tools found matching keyword 'NonExistentKeyword'."
    ),
    # Test Case 7: Enter an invalid choice
    (
        ['5', '4'],
        "Invalid choice. Please try again."
    )
])
def test_cli_invalid_inputs(cli_instance, input_sequence, expected_output, capsys):
    """
    Test the interactive mode of the CLI with invalid inputs.

    Args:
        cli_instance: Instance of the CLI class.
        input_sequence: List of user inputs to simulate.
        expected_output: Substring expected to be in the output.
        capsys: Pytest fixture to capture stdout and stderr.
    """
    # Patch 'sys.argv' to simulate no command-line arguments (interactive mode)
    with patch('sys.argv', ['cli.py']):
        # Patch 'input' to simulate user inputs
        with patch('builtins.input', side_effect=input_sequence):
            cli_instance.start()

    # Capture the output
    captured = capsys.readouterr()
    stdout = captured.out

    # Check for the expected substring in the output
    assert expected_output in stdout, f"Expected '{expected_output}' to be in the output."
