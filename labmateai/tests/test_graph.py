# tests/test_graph.py

"""
Unit tests for the graph module.
"""

from math import inf
import pytest
from ..graph import Graph
from ..tool import Tool


@pytest.fixture
def tools():
    """
    Fixture to provide a list of Tool instances for testing.
    """
    return [
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
            features=['Single-cell RNA-seq', 'Clustering'],
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
            features=['Genome Exploration', 'Visualization'],
            cost='Free',
            description='A tool for exploring and visualizing genomic data.',
            url='https://genomicsexplorer.com/',
            language='Python',
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
        )
    ]


@pytest.fixture
def graph_instance(tools):
    """
    Fixture to provide a Graph instance built with the provided tools.
    """
    graph = Graph()
    graph.build_graph(tools)
    return graph


def test_dijkstra_algorithm(graph_instance, tools):
    """
    Test Dijkstra's algorithm implementation.
    """
    tool_dict = {tool.name: tool for tool in tools}
    start_tool = tool_dict['Seurat']
    distances = graph_instance.dijkstra(start_tool)

    # Expected distances:
    # Seurat to Seurat: 0
    # Seurat to Scanpy: 0.0 (dissimilarity)
    # Seurat to GenomicsToolX: inf (no path)

    scanpy_neighbor = next(
        (weight for neighbor, weight in graph_instance.get_neighbors(start_tool) if neighbor.name == 'Scanpy'), inf)

    assert distances[
        start_tool] == 0, f"Distance to start tool should be 0, got {distances[start_tool]}"
    assert distances[tool_dict['Scanpy']
                     ] == scanpy_neighbor, f"Distance to Scanpy should be {scanpy_neighbor}, got {distances[tool_dict['Scanpy']]}"
    assert distances[tool_dict['GenomicsToolX']
                     ] == inf, f"Distance to GenomicsToolX should be infinity, got {distances[tool_dict['GenomicsToolX']]}"


def test_add_duplicate_edge(graph_instance, tools):
    """
    Test that adding a duplicate edge does not create redundant connections.
    """
    tool_dict = {tool.name: tool for tool in tools}
    tool1 = tool_dict['Seurat']
    tool2 = tool_dict['Scanpy']

    initial_neighbors = graph_instance.get_neighbors(tool1)
    initial_count = len(initial_neighbors)

    # Attempt to add a duplicate edge with different weight
    graph_instance.add_edge(tool1, tool2, weight=0.5)

    updated_neighbors = graph_instance.get_neighbors(tool1)
    updated_count = len(updated_neighbors)

    # Ensure that the edge was not added again
    assert updated_count == initial_count, "Duplicate edge was added, but it should have been prevented."

    # Verify that the existing edge's weight remains unchanged
    existing_weight = next(
        (weight for neighbor, weight in updated_neighbors if neighbor == tool2), None)
    assert existing_weight is not None, "Edge to Scanpy should still exist."
    assert existing_weight == 0.0, f"Edge weight was changed. Expected 0.0, got {existing_weight}."


def test_remove_edge(graph_instance, tools):
    """
    Test removing an existing edge between two tools.
    """
    tool_dict = {tool.name: tool for tool in tools}
    tool1 = tool_dict['GenomicsToolX']
    tool2 = tool_dict['GenomicsExplorer']

    # Ensure the edge exists
    neighbors_before = graph_instance.get_neighbors(tool1)
    assert any(neighbor.name == tool2.name for neighbor,
               _ in neighbors_before), "Edge should exist before removal."

    # Remove the edge
    graph_instance.remove_edge(tool1, tool2)

    neighbors_after = graph_instance.get_neighbors(tool1)
    assert not any(neighbor.name == tool2.name for neighbor,
                   _ in neighbors_after), "Edge was not removed."


def test_remove_nonexistent_edge(graph_instance, tools):
    """
    Test removing an edge that does not exist between two tools.
    """
    tool_dict = {tool.name: tool for tool in tools}
    tool1 = tool_dict['Seurat']
    tool2 = tool_dict['GenomicsExplorer']  # No existing edge

    # Ensure the edge does not exist
    neighbors_before = graph_instance.get_neighbors(tool1)
    assert not any(neighbor.name == tool2.name for neighbor,
                   _ in neighbors_before), "Edge should not exist before removal."

    # Attempt to remove the nonexistent edge
    with pytest.raises(ValueError) as exc_info:
        graph_instance.remove_edge(tool1, tool2)
    assert "No edge exists between 'Seurat' and 'GenomicsExplorer'." in str(
        exc_info.value), "Expected ValueError for removing nonexistent edge."


def test_remove_tool(graph_instance, tools):
    """
    Test removing a tool from the graph and ensuring all associated edges are removed.
    """
    tool_dict = {tool.name: tool for tool in tools}
    tool_to_remove = tool_dict['Bowtie']

    # Ensure the tool exists
    assert tool_to_remove in graph_instance.adj_list, f"Tool '{tool_to_remove.name}' should exist in the graph before removal."

    # Remove the tool
    graph_instance.remove_tool(tool_to_remove)

    # Ensure the tool is removed
    assert tool_to_remove not in graph_instance.adj_list, f"Tool '{tool_to_remove.name}' was not removed from the graph."

    # Ensure all edges associated with the tool are removed
    for tool in tools:
        if tool != tool_to_remove:
            neighbors = graph_instance.get_neighbors(tool)
            assert all(neighbor != tool_to_remove for neighbor,
                       _ in neighbors), f"Edge with '{tool_to_remove.name}' was not removed."


def test_calculate_simularity(graph_instance, tools):
    """
    Test the similarity calculation between two tools.
    """
    tool_dict = {tool.name: tool for tool in tools}
    tool1 = tool_dict['Seurat']
    tool2 = tool_dict['Scanpy']
    tool3 = tool_dict['GenomicsToolX']

    similarity_seurat_scanpy = graph_instance.calculate_simularity(
        tool1, tool2)
    # Expected similarity:
    # Same category: +1.0
    # Shared features: 2 / 2 * 2.0 = 2.0
    # Same cost: +0.2
    # Total: 1.0 + 2.0 + 0.2 = 3.2

    assert similarity_seurat_scanpy == 3.2, f"Expected similarity of 3.2, got {similarity_seurat_scanpy}."

    similarity_seurat_genomics = graph_instance.calculate_simularity(
        tool1, tool3)
    # Expected similarity:
    # Different category: 0
    # Shared features: 0 / 2 * 2.0 = 0.0
    # Same cost: +0.2
    # Total: 0 + 0 + 0.2 = 0.2

    assert similarity_seurat_genomics == 0.2, f"Expected similarity of 0.2, got {similarity_seurat_genomics}."


def test_find_most_relevant_tools_empty(graph_instance):
    """
    Test finding most relevant tools when starting tool is not in the graph.
    """
    non_existent_tool = Tool(
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


def test_find_most_relevant_tools(graph_instance, tools):
    """
    Test finding the most relevant tools based on similarity.
    """
    tool_dict = {tool.name: tool for tool in tools}
    start_tool = tool_dict['Seurat']
    recommendations = graph_instance.find_most_relevant_tools(
        start_tool, num_recommendations=3)

    # Expected recommendations: Scanpy, GenomicsToolX, GenomicsExplorer
    expected_names = ['Scanpy', 'GenomicsToolX', 'GenomicsExplorer']
    assert len(
        recommendations) == 3, f"Expected 3 recommendations, got {len(recommendations)}."
    recommended_names = [tool.name for tool in recommendations]
    assert recommended_names == expected_names, f"Expected recommendations {expected_names}, got {recommended_names}."


def test_find_most_relevant_tools_exceeding_recommendations(graph_instance, tools):
    """
    Test finding more recommendations than available tools.
    """
    tool_dict = {tool.name: tool for tool in tools}
    start_tool = tool_dict['RNAAnalyzer']
    recommendations = graph_instance.find_most_relevant_tools(
        start_tool, num_recommendations=10)

    # Expected recommendations: All other tools
    expected_names = ['Seurat', 'Scanpy',
                      'GenomicsToolX', 'GenomicsExplorer', 'Bowtie']
    assert len(
        recommendations) == 5, f"Expected 5 recommendations, got {len(recommendations)}."
    recommended_names = [tool.name for tool in recommendations]
    assert recommended_names == expected_names, f"Expected recommendations {expected_names}, got {recommended_names}."


def test_find_most_relevant_tools_no_recommendations(graph_instance, tools):
    """
    Test finding most relevant tools when there are no connections.
    """
    # Create a new tool with no connections
    isolated_tool = Tool(
        name='IsolatedTool',
        category='Isolation',
        features=['Unique Feature'],
        cost='Free',
        description='A tool with no connections.',
        url='https://isolated.example.com/',
        language='Python',
        platform='Cross-platform'
    )
    graph_instance.add_node(isolated_tool)

    recommendations = graph_instance.find_most_relevant_tools(
        isolated_tool, num_recommendations=3)

    # Expected recommendations: All other tools with inf distance, but since they're not connected, it's arbitrary
    # Depending on implementation, it might return the first N tools
    expected_names = ['Seurat', 'Scanpy', 'GenomicsToolX']
    assert len(
        recommendations) == 3, f"Expected 3 recommendations, got {len(recommendations)}."
    recommended_names = [tool.name for tool in recommendations]
    assert recommended_names == expected_names, f"Expected recommendations {expected_names}, got {recommended_names}."


def test_find_most_relevant_tools_with_multiple_paths(graph_instance, tools):
    """
    Test finding the most relevant tools when multiple paths exist.
    """
    tool_dict = {tool.name: tool for tool in tools}
    tool1 = tool_dict['GenomicsToolX']
    tool2 = tool_dict['Bowtie']
    tool3 = tool_dict['GenomicsExplorer']

    # Manually connect GenomicsToolX and Bowtie with a different weight
    graph_instance.add_edge(tool1, tool2, weight=0.6)

    recommendations = graph_instance.find_most_relevant_tools(
        tool1, num_recommendations=2)

    # Expected recommendations: GenomicsExplorer, Bowtie
    expected_names = ['GenomicsExplorer', 'Bowtie']
    assert len(
        recommendations) == 2, f"Expected 2 recommendations, got {len(recommendations)}."
    recommended_names = [tool.name for tool in recommendations]
    assert set(recommended_names) == set(
        expected_names), f"Expected recommendations {expected_names}, got {recommended_names}."
