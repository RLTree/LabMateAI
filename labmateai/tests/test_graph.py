# tests/test_graph.py

"""
Unit tests for the graph module in LabMateAI.
"""

import pytest
from labmateai.graph import Graph
from labmateai.tool import Tool


@pytest.fixture
def tools():
    """
    Fixture to provide a list of Tool instances with specified tool_ids for testing.
    """
    return [
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
def graph_instance(tools):
    """
    Fixture to provide a Graph instance built with the provided tools.
    """
    graph = Graph(tools)
    return graph


def test_graph_initialization_empty():
    """
    Test initializing an empty Graph and ensuring no tools are present.
    """
    empty_graph = Graph([])  # Pass an empty list to create an empty graph
    assert empty_graph.graph.number_of_nodes(
    ) == 0, "Expected empty graph upon initialization."


def test_build_graph_adds_all_tools(tools, graph_instance):
    """
    Test that build_graph correctly adds all tools as nodes in the graph.
    """
    assert graph_instance.graph.number_of_nodes() == len(tools), \
        f"Expected {len(tools)} nodes in the graph, got {graph_instance.graph.number_of_nodes()}."

    # Verify that all tools are present in the graph
    for tool in tools:
        assert graph_instance.graph.has_node(
            tool), f"Tool '{tool.name}' (ID: {tool.tool_id}) not found in the graph."


def test_build_graph_adds_correct_edges(tools, graph_instance):
    """
    Test that build_graph correctly adds edges based on similarity threshold.
    """
    # Since the similarity threshold is 0.2, and based on provided features,
    # we need to determine which tools should be connected.
    # For simplicity, let's assume:
    # - Seurat and Scanpy share 'Single-cell RNA-seq' -> similarity > 0.2
    # - Seurat and RNAAnalyzer share 'RNA' category -> similarity > 0.2
    # - GenomicsToolX and Bowtie share 'Genome' related features -> similarity > 0.2
    # - Other tool pairs have low similarity

    tool_dict = {tool.name: tool for tool in tools}

    # Check for edge between Seurat and Scanpy
    assert graph_instance.graph.has_edge(tool_dict['Seurat'], tool_dict['Scanpy']), \
        "Expected an edge between Seurat and Scanpy based on similiarity score."

    # Check for edge between Seurat and RNAAnalyzer
    assert graph_instance.graph.has_edge(tool_dict['Seurat'], tool_dict['RNAAnalyzer']), \
        "Expected an edge between Seurat and RNAAnalyzer based on similiarity score."

    # Check for edge between GenomicsToolX and Bowtie
    assert graph_instance.graph.has_edge(tool_dict['GenomicsToolX'], tool_dict['Bowtie']), \
        "Expected an edge between GenomicsToolX and Bowtie based on similiarity score."

    # Check that no other edges exist
    expected_edges = [
        (tool_dict['Seurat'], tool_dict['Scanpy']),
        (tool_dict['Seurat'], tool_dict['RNAAnalyzer']),
        (tool_dict['GenomicsToolX'], tool_dict['Bowtie'])
    ]
    actual_edges = list(graph_instance.graph.edges())
    assert len(actual_edges) == len(expected_edges), \
        f"Expected {len(expected_edges)} edges, got {len(actual_edges)}."
    for edge in expected_edges:
        assert edge in actual_edges or (edge[1], edge[0]) in actual_edges, \
            f"Expected edge {edge} to be present in the graph."


def test_add_node(graph_instance, tools):
    """
    Test adding a new tool to the graph.
    """
    new_tool = Tool(
        tool_id=361,
        name='BioToolY',
        category='Bioinformatics',
        features=['Data Analysis', 'Visualization'],
        cost='Free',
        description='A bioinformatics tool for data analysis.',
        url='https://biotooly.example.com/',
        language='Python',
        platform='Cross-platform'
    )

    # Add the new tool
    graph_instance.add_node(new_tool)
    assert graph_instance.graph.has_node(new_tool), \
        f"Tool '{new_tool.name}' was not added to the graph."

    # Attempt to add the same tool again should not raise an error
    graph_instance.add_node(new_tool)
    assert graph_instance.graph.number_of_nodes() == len(tools) + 1, \
        "Adding an existing tool should not duplicate it in the graph."


def test_add_edge(graph_instance, tools):
    """
    Test adding a new edge between two tools.
    """
    tool_dict = {tool.name: tool for tool in tools}
    tool1 = tool_dict['RNAAnalyzer']
    tool2 = tool_dict['GenomicsToolX']

    # Initially, no edge should exist between RNAAnalyzer and GenomicsToolX
    assert not graph_instance.graph.has_edge(tool1, tool2), \
        "Edge between RNAAnalyzer and GenomicsToolX should not exist initially."

    # Add the edge
    graph_instance.add_edge(tool1, tool2, similarity=0.4)
    assert graph_instance.graph.has_edge(tool1, tool2), \
        "Edge between RNAAnalyzer and GenomicsToolX was not added."

    # Verify the edge weight
    weight = graph_instance.graph[tool1][tool2]['weight']
    assert weight == 0.4, f"Expected edge weight 0.4, got {weight}."

    # Attempt to add the same edge again should not change the weight
    graph_instance.add_edge(tool1, tool2, similarity=0.6)
    weight_after = graph_instance.graph[tool1][tool2]['weight']
    assert weight_after == 0.4, "Duplicate edge addition should not alter existing edge weight."


def test_calculate_similarity(graph_instance, tools):
    """
    Test the similarity calculation between two tools.
    """
    tool_dict = {tool.name: tool for tool in tools}
    tool1 = tool_dict['Seurat']
    tool2 = tool_dict['Scanpy']
    tool3 = tool_dict['GenomicsToolX']

    # Calculate similarity between Seurat and Scanpy
    similarity_seurat_scanpy = graph_instance.calculate_similarity(
        tool1, tool2)
    # Expected similarity based on shared 'Single-cell RNA-seq', category, cost, and platform similarities
    expected_similarity_seurat_scanpy = 0.8619639341007327
    assert similarity_seurat_scanpy == expected_similarity_seurat_scanpy, \
        f"Expected similarity of {expected_similarity_seurat_scanpy} between Seurat and Scanpy, got {similarity_seurat_scanpy}."

    # Calculate similarity between Seurat and GenomicsToolX
    similarity_seurat_genomics = graph_instance.calculate_similarity(
        tool1, tool3)
    # Expected similarity based on different categories and no shared features
    expected_similarity_seurat_genomics = 0.06444444444444446
    assert similarity_seurat_genomics == expected_similarity_seurat_genomics, \
        f"Expected similarity of {expected_similarity_seurat_genomics} between Seurat and GenomicsToolX, got {similarity_seurat_genomics}."


def test_find_most_relevant_tools(graph_instance, tools):
    """
    Test finding the most relevant tools based on similarity.
    """
    tool_dict = {tool.tool_id: tool for tool in tools}
    start_tool = tool_dict[119]  # Seurat
    recommendations = graph_instance.find_most_relevant_tools(
        start_tool, num_recommendations=3)

    # Expected recommendations based on similarity:
    # 1. Scanpy (ID: 337) - similarity 0.86
    # 2. RNAAnalyzer (ID: 360) - similarity 0.2

    expected_order = ['Scanpy', 'RNAAnalyzer']  # Top 2
    recommended_names = [tool.name for tool in recommendations]
    assert recommended_names == expected_order, \
        f"Expected recommendations {expected_order}, got {recommended_names}."


def test_find_most_relevant_tools_exceeding_recommendations(graph_instance, tools):
    """
    Test finding more recommendations than available tools.
    """
    tool_dict = {tool.tool_id: tool for tool in tools}
    start_tool = tool_dict[360]  # RNAAnalyzer
    recommendations = graph_instance.find_most_relevant_tools(
        start_tool, num_recommendations=10)

    # Expected recommendations: All other tools sorted by similarity
    expected_order = ['Seurat']
    recommended_names = [tool.name for tool in recommendations]
    assert len(recommendations) == 1, \
        f"Expected 1 recommendations, got {len(recommendations)}."
    assert recommended_names == expected_order, \
        f"Expected recommendations {expected_order}, got {recommended_names}."


def test_calculate_similarity_no_shared_features(graph_instance, tools):
    """
    Test similarity calculation between tools with no shared features and different categories.
    """
    tool_dict = {tool.tool_id: tool for tool in tools}
    tool1 = tool_dict[359]  # GenomicsToolX
    tool2 = tool_dict[360]  # RNAAnalyzer

    similarity = graph_instance.calculate_similarity(tool1, tool2)
    # Expected similarity:
    expected_similarity = 0.06444444444444446
    assert similarity == expected_similarity, \
        f"Expected similarity of {expected_similarity}, got {similarity}."


def test_calculate_similarity_same_tool(graph_instance, tools):
    """
    Test similarity calculation when comparing a tool with itself.
    """
    tool_dict = {tool.tool_id: tool for tool in tools}
    tool = tool_dict[119]  # Seurat

    similarity = graph_instance.calculate_similarity(tool, tool)
    # Expected similarity when comparing a tool with itself
    expected_similarity = 1.028888888888889
    assert similarity == expected_similarity, \
        f"Expected similarity of {expected_similarity} when comparing a tool with itself, got {similarity}."


def test_find_most_relevant_tools_invalid_tool(graph_instance, tools):
    """
    Test recommending similar tools with an invalid tool name.
    """
    # Create a tool that does not exist in the graph
    non_existent_tool = Tool(
        tool_id=999,
        name='NonExistentTool',
        category='Unknown',
        features=[],
        cost='Free',
        description='A tool that does not exist in the graph.',
        url='https://nonexistent.example.com/',
        language='Python',
        platform='Cross-platform'
    )

    with pytest.raises(ValueError) as exc_info:
        graph_instance.find_most_relevant_tools(
            non_existent_tool, num_recommendations=3)
    assert f"Start tool '{non_existent_tool.name}' not found in the graph." in str(exc_info.value), \
        "Expected ValueError for non-existent start tool."


def test_graph_repr(graph_instance, tools):
    """
    Test the string representation (__repr__) of the Graph instance.
    """
    graph_repr = repr(graph_instance)
    # Check that each tool is represented with its neighbors and similarity scores
    for tool in tools:
        for neighbor in graph_instance.graph.neighbors(tool):
            weight = graph_instance.graph[tool][neighbor]['weight']
            expected_substring = f"{neighbor.name} (similarity: {weight:.2f})"
            assert expected_substring in graph_repr, \
                f"Expected '{expected_substring}' to be in graph representation."
