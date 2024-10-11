# tests/test_recommender.py

"""
Unit tests for the Recommender class in LabMateAI.
"""

import pytest
from labmateai.recommender import Recommender
from labmateai.tool import Tool


@pytest.fixture
def sample_tools():
    """
    Fixture to provide a list of Tool instances with specified tool_ids for testing.
    """
    return [
        Tool(
            tool_id=119,
            name='Seurat',
            category='Single-Cell Analysis',
            features=['Single-cell RNA-seq', 'Clustering'],
            cost=0.0,
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
            cost=0.0,
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
            cost=0.0,
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
            cost=0.0,
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
            cost=0.0,
            description='A tool for analyzing RNA-Seq data and identifying differential gene expression.',
            url='https://rnaanalyzer.example.com/',
            language='R',
            platform='Cross-platform'
        ),
        Tool(
            tool_id=361,
            name='GenomicsToolY',
            category='Unknown',
            features=['Unknown'],
            cost='Unknown',
            description='Unknown',
            url='Unknown',
            language='Unknown',
            platform='Unknown'
        )
    ]


@pytest.fixture
def recommender_instance(sample_tools):
    """
    Fixture to provide a Recommender instance initialized with the sample tools.
    """
    return Recommender(tools=sample_tools)


def test_recommender_initialization(recommender_instance, sample_tools):
    """
    Test that the Recommender initializes correctly with the provided tools.
    """
    assert recommender_instance.tools == sample_tools, "Recommender should store the provided tools."
    assert recommender_instance.graph.graph.number_of_nodes() == len(sample_tools), \
        "Graph should contain all provided tools as nodes."
    assert recommender_instance.tree.tools == sample_tools, "ToolTree should contain all provided tools."


def test_recommend_similar_tools_valid(recommender_instance):
    """
    Test recommending similar tools for a valid tool name.
    """
    recommendations = recommender_instance.recommend_similar_tools(
        tool_name='Seurat', num_recommendations=2)
    recommended_names = [tool.name for tool in recommendations]

    # Since Seurat and Scanpy have similar features, Scanpy should be recommended.
    expected_recommendations = ['Scanpy', 'RNAAnalyzer']

    assert set(recommended_names) == set(expected_recommendations), \
        f"Expected recommendations {expected_recommendations}, got {recommended_names}."


def test_recommend_similar_tools_invalid(recommender_instance):
    """
    Test recommending similar tools for an invalid (non-existent) tool name.
    """
    with pytest.raises(ValueError) as exc_info:
        recommender_instance.recommend_similar_tools(
            tool_name='NonExistentTool', num_recommendations=2)
    assert "Tool 'NonExistentTool' not found in the dataset." in str(exc_info.value), \
        "Expected ValueError for non-existent tool name."


def test_get_recommendation_scores_valid_tool(recommender_instance):
    """
    Test getting recommendation scores for a valid tool.
    """
    scores = recommender_instance.get_recommendation_scores(tool_name='Seurat')
    assert isinstance(
        scores, dict), "Recommendation scores should be returned as a dictionary."
    assert len(scores) == len(recommender_instance.tools) - \
        1, "Recommendation scores should be calculated for all tools except the given one."
    assert 337 in scores, "Expected Scanpy to have a recommendation score for Seurat."
    assert scores[337] > 0, "Expected a positive score for Scanpy as it shares features with Seurat."


def test_get_recommendation_scores_invalid_tool(recommender_instance):
    """
    Test getting recommendation scores for an invalid tool.
    """
    with pytest.raises(ValueError) as exc_info:
        recommender_instance.get_recommendation_scores(
            tool_name='NonExistentTool')
    assert "Tool 'NonExistentTool' not found in the dataset." in str(exc_info.value), \
        "Expected ValueError for non-existent tool name."


def test_recommend_with_tool_name(recommender_instance):
    """
    Test the recommend method using a tool name for recommendations.
    """
    recommendations = recommender_instance.recommend(
        tool_name='Seurat', num_recommendations=2)
    recommended_names = [tool.name for tool in recommendations]
    expected_recommendations = ['Scanpy', 'RNAAnalyzer']

    assert set(recommended_names) == set(expected_recommendations), \
        f"Expected recommendations {expected_recommendations}, got {recommended_names}."


def test_recommend_with_category_name(recommender_instance):
    """
    Test the recommend method using a category name for recommendations.
    """
    recommendations = recommender_instance.recommend(
        category_name='Genomics', num_recommendations=2)
    recommended_names = [tool.name for tool in recommendations]
    expected_recommendations = ['GenomicsToolX', 'Bowtie']

    assert set(recommended_names) == set(expected_recommendations), \
        f"Expected recommendations {expected_recommendations}, got {recommended_names}."


def test_recommend_with_keyword(recommender_instance):
    """
    Test the recommend method using a keyword for recommendations.
    """
    recommendations = recommender_instance.recommend(
        keyword='RNA', num_recommendations=3)
    recommended_names = [tool.name for tool in recommendations]
    expected_recommendations = ['Seurat', 'Scanpy', 'RNAAnalyzer']

    assert set(recommended_names) == set(expected_recommendations), \
        f"Expected recommendations {expected_recommendations}, got {recommended_names}."


def test_recommend_with_no_parameters(recommender_instance):
    """
    Test the recommend method with no parameters provided.
    """
    with pytest.raises(ValueError) as exc_info:
        recommender_instance.recommend()
    assert "At least one of tool_name, category_name, or keyword must be provided." in str(exc_info.value), \
        "Expected ValueError when no parameters are provided to recommend."


def test_recommendation_scores_case_insensitivity(recommender_instance):
    """
    Test that the Recommender handles tool names in a case-insensitive manner for recommendation scores.
    """
    scores_lower = recommender_instance.get_recommendation_scores(
        tool_name='seurat')
    scores_mixed = recommender_instance.get_recommendation_scores(
        tool_name='SeUrAt')
    assert scores_lower == scores_mixed, "Expected the same recommendation scores regardless of tool name case."


def test_recommend_similar_tools_case_insensitivity(recommender_instance):
    """
    Test that the Recommender handles tool names in a case-insensitive manner for similar tool recommendations.
    """
    recommendations_lower = recommender_instance.recommend_similar_tools(
        tool_name='seurat', num_recommendations=2)
    recommendations_mixed = recommender_instance.recommend_similar_tools(
        tool_name='SeUrAt', num_recommendations=2)
    recommended_names_lower = [tool.name for tool in recommendations_lower]
    recommended_names_mixed = [tool.name for tool in recommendations_mixed]
    expected_recommendations = ['Scanpy', 'RNAAnalyzer']

    assert set(recommended_names_lower) == set(expected_recommendations), \
        f"Expected recommendations {expected_recommendations}, got {recommended_names_lower}."
    assert set(recommended_names_mixed) == set(expected_recommendations), \
        f"Expected recommendations {expected_recommendations}, got {recommended_names_mixed}."


def test_recommender_duplicate_tool_initialization():
    """
    Test initializing Recommender with duplicate tools.
    """
    duplicate_tool = Tool(
        tool_id=119,
        name='Seurat',
        category='Single-Cell Analysis',
        features=['Single-cell RNA-seq', 'Clustering'],
        cost=0.0,
        description='Duplicate Seurat tool.',
        url='https://satijalab.org/seurat/',
        language='R',
        platform='Cross-platform'
    )
    sample_tools = [
        Tool(
            tool_id=119,
            name='Seurat',
            category='Single-Cell Analysis',
            features=['Single-cell RNA-seq', 'Clustering'],
            cost=0.0,
            description='An R package for single-cell RNA sequencing data.',
            url='https://satijalab.org/seurat/',
            language='R',
            platform='Cross-platform'
        ),
        duplicate_tool
    ]

    with pytest.raises(ValueError) as exc_info:
        Recommender(tools=sample_tools)

    assert "Tool 'Seurat' already exists in the graph." in str(exc_info.value), \
        "Expected ValueError when initializing Recommender with duplicate tools."
