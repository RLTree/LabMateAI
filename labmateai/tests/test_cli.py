# tests/test_cli.py

"""
Unit tests for the CLI class.
"""

from unittest.mock import patch
import pytest
from labmateai.recommender import Recommender
from labmateai.tool import Tool
from labmateai.cli import CLI


# Define sample tools for testing with tool_id
SAMPLE_TOOLS = [
    Tool(
        tool_id=119,
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
        tool_id=337,
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
        tool_id=359,
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
        tool_id=126,
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
        tool_id=360,
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
def mock_cli():
    """
    Fixture to provide a mock CLI instance.
    """
    with patch('labmateai.recommender.Recommender') as MockRecommender:
        mock_recommender_instance = MockRecommender.return_value

        # Mocking the recommend methods to return controlled outputs
        mock_recommender_instance.recommend_similar_tools.side_effect = lambda tool_name, num_recommendations: (
            [SAMPLE_TOOLS[1]] if tool_name.lower() == 'seurat' else []
        )
        mock_recommender_instance.recommend_tools_in_category.side_effect = lambda category_name: (
            [SAMPLE_TOOLS[2], SAMPLE_TOOLS[3]
             ] if category_name.lower() == 'genomics' else []
        )
        mock_recommender_instance.search_and_recommend.side_effect = lambda keyword: (
            [SAMPLE_TOOLS[0], SAMPLE_TOOLS[1], SAMPLE_TOOLS[4]
             ] if keyword.lower() == 'rna' else []
        )

        cli = CLI(recommender=mock_recommender_instance, tools=SAMPLE_TOOLS)
        yield cli


@pytest.mark.parametrize("input_sequence, expected_output_checks", [
    # Test Case 1: Recommend similar tools to 'Seurat'
    (
        ['1', 'Seurat', '4'],
        ['Recommendations:', '- Scanpy (ID: 337):']
    ),
    # Test Case 2: Recommend tools in 'Genomics' category
    (
        ['2', 'Genomics', '4'],
        ['Recommendations:',
            '- GenomicsToolX (ID: 359):', '- Bowtie (ID: 126):']
    ),
    # Test Case 3: Search tools by keyword 'RNA'
    (
        ['3', 'RNA', '4'],
        ['Recommendations:',
            '- Seurat (ID: 119):', '- Scanpy (ID: 337):', '- RNAAnalyzer (ID: 360):']
    )
])
def test_cli_interactive_modes(mock_cli, input_sequence, expected_output_checks, capsys):
    """
    Test the interactive mode of the CLI with valid inputs.

    Args:
        mock_cli: Instance of the mock CLI class.
        input_sequence: List of user inputs to simulate.
        expected_output_checks: List of substrings expected to be in the output.
        capsys: Pytest fixture to capture stdout and stderr.
    """
    # Patch 'sys.argv' to simulate no command-line arguments (interactive mode)
    with patch('sys.argv', ['cli.py']):
        # Patch 'input' to simulate user inputs
        with patch('builtins.input', side_effect=input_sequence):
            mock_cli.start()

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
        "No tools found for category 'NonExistentCategory'."
    ),
    # Test Case 6: Search tools by a non-existent keyword
    (
        ['3', 'NonExistentKeyword', '4'],
        "No tools found matching keyword 'NonExistentKeyword'."
    ),
    # Test Case 7: Enter an invalid choice
    (
        ['5', '4'],
        "Invalid choice. Please enter a number between 1 and 4."
    )
])
def test_cli_invalid_inputs(mock_cli, input_sequence, expected_output, capsys):
    """
    Test the interactive mode of the CLI with invalid inputs.

    Args:
        mock_cli: Instance of the mock CLI class.
        input_sequence: List of user inputs to simulate.
        expected_output: Substring expected to be in the output.
        capsys: Pytest fixture to capture stdout and stderr.
    """
    # Patch 'sys.argv' to simulate no command-line arguments (interactive mode)
    with patch('sys.argv', ['cli.py']):
        # Patch 'input' to simulate user inputs
        with patch('builtins.input', side_effect=input_sequence):
            mock_cli.start()

    # Capture the output
    captured = capsys.readouterr()
    stdout = captured.out

    # Check for the expected substring in the output
    assert expected_output in stdout, f"Expected '{expected_output}' to be in the output."
