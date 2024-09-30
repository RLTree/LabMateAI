# tests/test_recommender.py

"""
Unit tests for the Recommender class using pytest.
"""

import pytest
from ..recommender import Recommender
from ..tool import Tool
from ..graph import Graph
from ..tree import ToolTree


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
        name='GenomicsExplorer',
        category='Genomics',
        features=['Genome Browsing', 'Data Visualization'],
        cost='Free',
        description='A tool for exploring and visualizing genomic data.',
        url='https://genomicsexplorer.com/',
        language='Java',
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
    # Add more tools as needed
]


@pytest.fixture(scope="module")
def recommender():
    """
    Fixture to initialize the Recommender with predefined sample tools.
    """
    # Initialize Graph and ToolTree if needed, or mock them if they have complex dependencies
    return Recommender(SAMPLE_TOOLS)


@pytest.mark.parametrize("tool_name, num_recommendations, expected_length", [
    ('Seurat', 3, 3),  # Only Scanpy is similar in category
    ('GenomicsToolX', 2, 2),  # GenomicsExplorer and Bowtie
    ('RNAAnalyzer', 3, 3),  # Assuming no similar tools in 'RNA' category
])
def test_recommend_similar_tools(recommender, tool_name, num_recommendations, expected_length):
    """
    Test recommending similar tools.

    Args:
        recommender: Instance of the Recommender class.
        tool_name (str): The name of the tool to find recommendations for.
        num_recommendations (int): Number of recommendations to request.
        expected_length (int): Expected number of recommendations.
    """
    recommendations = recommender.recommend_similar_tools(
        tool_name, num_recommendations)
    assert len(
        recommendations) == expected_length, f"Expected {expected_length} recommendations, got {len(recommendations)}."
    assert all(
        tool.name != tool_name for tool in recommendations), f"The tool '{tool_name}' should not be in its own recommendations."


@pytest.mark.parametrize("category_name, expected_tool_names", [
    ('Genomics', ['GenomicsToolX', 'GenomicsExplorer', 'Bowtie']),
    ('Single-Cell Analysis', ['Seurat', 'Scanpy']),
    ('RNA', ['RNAAnalyzer']),
    ('NonExistentCategory', []),
])
def test_recommend_tools_in_category(recommender, category_name, expected_tool_names):
    """
    Test recommending tools based on category.

    Args:
        recommender: Instance of the Recommender class.
        category_name (str): The category to recommend tools from.
        expected_tool_names (list): List of expected tool names.
    """
    if expected_tool_names:
        recommendations = recommender.recommend_tools_in_category(
            category_name)
        assert len(recommendations) == len(expected_tool_names), \
            f"Expected {len(expected_tool_names)} recommendations, got {len(recommendations)}."
        recommended_names = sorted([tool.name for tool in recommendations])
        expected_sorted = sorted(expected_tool_names)
        assert recommended_names == expected_sorted, \
            f"Expected recommendations {expected_sorted}, got {recommended_names}."
        assert all(
            tool.category.lower() == category_name.lower() for tool in recommendations), \
            "All recommended tools should belong to the specified category."
    else:
        with pytest.raises(ValueError) as exc_info:
            recommender.recommend_tools_in_category(category_name)
        assert f"Category '{category_name}' not found." in str(exc_info.value), \
            f"Expected ValueError for non-existent category '{category_name}'."


@pytest.mark.parametrize("keyword, expected_tool_names", [
    ('RNA', ['Seurat', 'Scanpy', 'RNAAnalyzer']),
    ('Genome', ['GenomicsToolX', 'GenomicsExplorer', 'Bowtie']),
    ('Clustering', ['Seurat']),
    ('NonExistentKeyword', []),
])
def test_search_and_recommend(recommender, keyword, expected_tool_names):
    """
    Test searching tools by keyword.

    Args:
        recommender: Instance of the Recommender class.
        keyword (str): The keyword to search for.
        expected_tool_names (list): List of expected tool names.
    """
    recommendations = recommender.search_and_recommend(keyword)
    if expected_tool_names:
        recommended_names = [tool.name for tool in recommendations]
        for name in expected_tool_names:
            assert name in recommended_names, f"Expected tool '{name}' to be in the recommendations."
    else:
        # Assuming that no recommendations should return an empty list
        assert len(
            recommendations) == 0, f"Expected no recommendations, but got {len(recommendations)}."


def test_recommend_similar_tools_invalid_tool(recommender):
    """
    Test recommending similar tools with an invalid tool name.

    Args:
        recommender: Instance of the Recommender class.
    """
    with pytest.raises(ValueError) as exc_info:
        recommender.recommend_similar_tools('NonExistentTool', 3)
    assert "Tool 'NonExistentTool' not found." in str(
        exc_info.value), "Expected ValueError for non-existent tool."


def test_recommend_tools_in_nonexistent_category(recommender):
    """
    Test recommending tools in a non-existent category.

    Args:
        recommender: Instance of the Recommender class.
    """
    with pytest.raises(ValueError) as exc_info:
        recommender.recommend_tools_in_category('NonExistentCategory')
    assert "Category 'NonExistentCategory' not found." in str(exc_info.value), \
        "Expected ValueError for non-existent category."


def test_search_and_recommend_no_matches(recommender):
    """
    Test searching tools with a keyword that has no matches.

    Args:
        recommender: Instance of the Recommender class.
    """
    recommendations = recommender.search_and_recommend('NonExistentKeyword')
    assert len(
        recommendations) == 0, f"Expected no recommendations for non-existent keyword, got {len(recommendations)}."
