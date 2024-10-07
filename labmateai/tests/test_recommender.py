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
            category='unknown',
            features=['unknown'],
            cost='unknown',
            description='unknown',
            url='unknown',
            language='unknown',
            platform='unknown'
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
    # Based on build_graph, only Scanpy shares features with Seurat
    expected_recommendations = ['Scanpy', 'RNAAnalyzer']

    assert recommended_names == expected_recommendations, \
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


def test_recommend_tools_in_category_valid(recommender_instance):
    """
    Test recommending tools for a valid category name.
    """
    recommendations = recommender_instance.recommend_tools_in_category(
        category_name='Genomics')
    recommended_names = [tool.name for tool in recommendations]
    expected_recommendations = ['GenomicsToolX', 'Bowtie']

    assert set(recommended_names) == set(expected_recommendations), \
        f"Expected recommendations {expected_recommendations}, got {recommended_names}."


def test_recommend_tools_in_category_invalid(recommender_instance):
    """
    Test recommending tools for an invalid (non-existent) category name.
    """
    with pytest.raises(ValueError) as exc_info:
        recommender_instance.recommend_tools_in_category(
            category_name='Proteomics')
    assert "Category 'Proteomics' not found." in str(exc_info.value), \
        "Expected ValueError for non-existent category name."


def test_search_and_recommend_valid_keyword(recommender_instance):
    """
    Test searching and recommending tools with a valid keyword.
    """
    recommendations = recommender_instance.search_and_recommend(keyword='RNA')
    recommended_names = [tool.name for tool in recommendations]
    expected_recommendations = ['Seurat', 'Scanpy', 'RNAAnalyzer']

    assert set(recommended_names) == set(expected_recommendations), \
        f"Expected recommendations {expected_recommendations}, got {recommended_names}."


def test_search_and_recommend_no_matches(recommender_instance):
    """
    Test searching and recommending tools with a keyword that yields no matches.
    """
    recommendations = recommender_instance.search_and_recommend(
        keyword='Proteomics')
    assert recommendations == [], "Expected no recommendations for a keyword with no matches."


def test_recommend_combined_parameters_tool_name(recommender_instance):
    """
    Test the recommend method with only tool_name provided.
    """
    recommendations = recommender_instance.recommend(
        tool_name='GenomicsToolX', num_recommendations=1)
    recommended_names = [tool.name for tool in recommendations]
    expected_recommendations = ['Bowtie']

    assert recommended_names == expected_recommendations, \
        f"Expected recommendation {expected_recommendations}, got {recommended_names}."


def test_recommend_combined_parameters_category_name(recommender_instance):
    """
    Test the recommend method with only category_name provided.
    """
    recommendations = recommender_instance.recommend(category_name='RNA')
    recommended_names = [tool.name for tool in recommendations]
    expected_recommendations = ['RNAAnalyzer']

    assert recommended_names == expected_recommendations, \
        f"Expected recommendation {expected_recommendations}, got {recommended_names}."


def test_recommend_combined_parameters_keyword(recommender_instance):
    """
    Test the recommend method with only keyword provided.
    """
    recommendations = recommender_instance.recommend(keyword='Clustering')
    recommended_names = [tool.name for tool in recommendations]
    expected_recommendations = ['Seurat']

    assert recommended_names == expected_recommendations, \
        f"Expected recommendation {expected_recommendations}, got {recommended_names}."


def test_recommend_no_parameters(recommender_instance):
    """
    Test the recommend method with no parameters provided.
    """
    with pytest.raises(ValueError) as exc_info:
        recommender_instance.recommend()
    assert "At least one of tool_name, category_name, or keyword must be provided." in str(exc_info.value), \
        "Expected ValueError when no parameters are provided to recommend."


def test_recommend_display_recommendations(capsys, recommender_instance):
    """
    Test the display_recommendations method to ensure correct output.
    """
    recommendations = recommender_instance.recommend_tools_in_category(
        category_name='RNA')
    recommender_instance.display_recommendations(recommendations)

    captured = capsys.readouterr()
    expected_output = "\nRecommended Tools:\n- RNAAnalyzer - A tool for analyzing RNA-Seq data and identifying differential gene expression. (Category: RNA, Cost: $0.0)"

    assert expected_output in captured.out, \
        f"Expected output to contain '{expected_output}', got '{captured.out}'."


def test_recommend_with_more_recommendations_than_available(recommender_instance):
    """
    Test requesting more recommendations than available tools.
    """
    recommendations = recommender_instance.recommend(
        category_name='RNA', num_recommendations=5)
    recommended_names = [tool.name for tool in recommendations]
    expected_recommendations = ['RNAAnalyzer']

    assert recommended_names == expected_recommendations, \
        f"Expected recommendations {expected_recommendations}, got {recommended_names}."


def test_recommend_same_tool_multiple_times(recommender_instance):
    """
    Test recommending similar tools for the same tool multiple times to ensure consistency.
    """
    recommendations_first = recommender_instance.recommend_similar_tools(
        tool_name='Scanpy', num_recommendations=1)
    recommendations_second = recommender_instance.recommend_similar_tools(
        tool_name='Scanpy', num_recommendations=1)

    recommended_names_first = [tool.name for tool in recommendations_first]
    recommended_names_second = [tool.name for tool in recommendations_second]
    expected_recommendations = ['Seurat']

    assert recommended_names_first == expected_recommendations, \
        f"First recommendation expected {expected_recommendations}, got {recommended_names_first}."
    assert recommended_names_second == expected_recommendations, \
        f"Second recommendation expected {expected_recommendations}, got {recommended_names_second}."


def test_recommend_tool_with_no_similar_tools(recommender_instance):
    """
    Test recommending similar tools for a tool with no similar tools.
    """
    # Assuming 'RNAAnalyzer' has no similar tools beyond itself
    recommendations = recommender_instance.recommend_similar_tools(
        tool_name='GenomicsToolY', num_recommendations=2)
    recommended_names = [tool.name for tool in recommendations]
    expected_recommendations = []  # No similar tools

    assert recommended_names == expected_recommendations, \
        f"Expected no recommendations for 'GenomicsToolY', got {recommended_names}."


def test_recommender_with_duplicate_tools():
    """
    Test initializing Recommender with duplicate tools to ensure proper handling.
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


def test_recommender_case_insensitive_tool_names(recommender_instance):
    """
    Test that the Recommender handles tool names in a case-insensitive manner.
    """
    recommendations_upper = recommender_instance.recommend_similar_tools(
        tool_name='SEURAT', num_recommendations=2)
    recommendations_mixed = recommender_instance.recommend_similar_tools(
        tool_name='sEuRat', num_recommendations=2)
    expected_recommendations = ['Scanpy', 'RNAAnalyzer']

    recommended_names_upper = [tool.name for tool in recommendations_upper]
    recommended_names_mixed = [tool.name for tool in recommendations_mixed]

    assert recommended_names_upper == expected_recommendations, \
        f"Expected recommendations {expected_recommendations}, got {recommended_names_upper}."
    assert recommended_names_mixed == expected_recommendations, \
        f"Expected recommendations {expected_recommendations}, got {recommended_names_mixed}."


def test_recommender_multiple_keywords_search(recommender_instance):
    """
    Test searching and recommending tools with multiple keywords.
    """
    # Assuming the search_tools method can handle multiple keywords separated by spaces
    # For example, searching 'RNA-seq' should match 'Seurat', 'Scanpy', 'RNAAnalyzer'
    recommendations = recommender_instance.search_and_recommend(
        keyword='RNA-seq')
    recommended_names = [tool.name for tool in recommendations]
    expected_recommendations = ['Seurat', 'Scanpy', 'RNAAnalyzer']

    assert set(recommended_names) == set(expected_recommendations), \
        f"Expected recommendations {expected_recommendations}, got {recommended_names}."


def test_recommender_display_recommendations_no_recommendations(capsys, recommender_instance):
    """
    Test the display_recommendations method when there are no recommendations.
    """
    recommendations = []
    recommender_instance.display_recommendations(recommendations)

    captured = capsys.readouterr()
    expected_output = "\nRecommended Tools:\nNo recommendations found."

    assert expected_output in captured.out, \
        f"Expected output to contain '{expected_output}', got '{captured.out}'."


def test_recommender_display_recommendations_with_recommendations(capsys, recommender_instance):
    """
    Test the display_recommendations method with actual recommendations.
    """
    recommendations = recommender_instance.recommend_tools_in_category(
        category_name='Genomics')
    recommender_instance.display_recommendations(recommendations)

    captured = capsys.readouterr()
    expected_output_lines = [
        "\nRecommended Tools:",
        "- GenomicsToolX - A tool for comprehensive genome assembly and variant calling. (Category: Genomics, Cost: $0.0)",
        "- Bowtie - A fast and memory-efficient tool for aligning sequencing reads to long reference sequences. (Category: Genomics, Cost: $0.0)"
    ]

    for line in expected_output_lines:
        assert line in captured.out, f"Expected line '{line}' to be in the output."


def test_recommender_search_tools_case_insensitivity(recommender_instance):
    """
    Test that the search is case-insensitive.
    """
    recommendations_lower = recommender_instance.search_and_recommend(
        keyword='rna-seq')
    recommendations_upper = recommender_instance.search_and_recommend(
        keyword='RNA-SEQ')
    recommendations_mixed = recommender_instance.search_and_recommend(
        keyword='RnA-sEq')
    expected_recommendations = ['Seurat', 'Scanpy', 'RNAAnalyzer']

    recommended_names_lower = [tool.name for tool in recommendations_lower]
    recommended_names_upper = [tool.name for tool in recommendations_upper]
    recommended_names_mixed = [tool.name for tool in recommendations_mixed]

    assert set(recommended_names_lower) == set(expected_recommendations), \
        f"Expected recommendations {expected_recommendations}, got {recommended_names_lower}."
    assert set(recommended_names_upper) == set(expected_recommendations), \
        f"Expected recommendations {expected_recommendations}, got {recommended_names_upper}."
    assert set(recommended_names_mixed) == set(expected_recommendations), \
        f"Expected recommendations {expected_recommendations}, got {recommended_names_mixed}."
