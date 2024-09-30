# tests/test_tree.py

"""
Unit tests for the ToolTree class using pytest.
"""

import pytest
from ..tree import ToolTree, TreeNode
from ..tool import Tool


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
def tool_tree():
    """
    Fixture to initialize the ToolTree with predefined sample tools.
    """
    tree = ToolTree()
    tree.build_tree(SAMPLE_TOOLS)
    return tree


@pytest.fixture(scope="module")
def tools():
    """
    Fixture to provide the list of sample tools.
    """
    return SAMPLE_TOOLS


@pytest.mark.parametrize("category_name, expected_tool_names", [
    ('Genomics', ['GenomicsToolX', 'GenomicsExplorer', 'Bowtie']),
    ('Single-Cell Analysis', ['Seurat', 'Scanpy']),
    ('RNA', ['RNAAnalyzer']),
    ('NonExistentCategory', []),
])
def test_get_tools_in_category(tool_tree, category_name, expected_tool_names):
    """
    Test retrieving tools in a category.

    Args:
        tool_tree: Instance of the ToolTree class.
        category_name (str): The name of the category to retrieve tools from.
        expected_tool_names (list): List of expected tool names.
    """
    if expected_tool_names:
        tools_in_category = tool_tree.get_tools_in_category(category_name)
        assert len(tools_in_category) == len(expected_tool_names), \
            f"Expected {len(expected_tool_names)} tools in category '{category_name}', got {len(tools_in_category)}."
        retrieved_names = sorted([tool.name.lower()
                                 for tool in tools_in_category])
        expected_sorted = sorted([name.lower()
                                 for name in expected_tool_names])
        assert retrieved_names == expected_sorted, \
            f"Expected tools {expected_sorted} in category '{category_name}', got {retrieved_names}."
        assert all(tool.category == category_name for tool in tools_in_category), \
            "All retrieved tools should belong to the specified category."
    else:
        with pytest.raises(ValueError) as exc_info:
            tool_tree.get_tools_in_category(category_name)
        assert f"Category '{category_name}' not found." in str(exc_info.value), \
            f"Expected ValueError for non-existent category '{category_name}'."


@pytest.mark.parametrize("keyword, expected_tool_names", [
    ('RNA', ['Seurat', 'Scanpy', 'RNAAnalyzer']),
    ('Genome', ['GenomicsToolX', 'GenomicsExplorer', 'Bowtie']),
    ('Clustering', ['Seurat']),
    ('Visualization', ['Scanpy', 'GenomicsExplorer']),
    ('NonExistentKeyword', []),
])
def test_search_tools(tool_tree, keyword, expected_tool_names):
    """
    Test searching for tools by keyword.

    Args:
        tool_tree: Instance of the ToolTree class.
        keyword (str): The keyword to search for.
        expected_tool_names (list): List of expected tool names.
    """
    results = tool_tree.search_tools(keyword)
    if expected_tool_names:
        retrieved_names = sorted([tool.name for tool in results])
        expected_sorted = sorted(expected_tool_names)
        for name in expected_tool_names:
            assert name in retrieved_names, f"Expected tool '{name}' to be in search results for keyword '{keyword}'."
        # Optionally, check that no unexpected tools are included
        assert len(results) >= len(expected_tool_names), \
            f"Expected at least {len(expected_tool_names)} tools in search results for keyword '{keyword}', got {len(results)}."
    else:
        assert len(
            results) == 0, f"Expected no search results for keyword '{keyword}', but got {len(results)}."


def test_get_all_categories(tool_tree):
    """
    Test retrieving all categories.

    Args:
        tool_tree: Instance of the ToolTree class.
    """
    categories = tool_tree.get_all_categories()
    expected_categories = ['Single-Cell Analysis', 'Genomics', 'RNA']
    for category in expected_categories:
        assert category in categories, f"Expected category '{category}' to be in the list of all categories."
    assert len(categories) == len(expected_categories), \
        f"Expected categories {expected_categories}, but got {categories}."


@pytest.mark.parametrize("category_name, expected_tool_count", [
    ('Single-Cell Analysis', 2),
    ('Genomics', 3),
    ('RNA', 1),
])
def test_category_tool_counts(tool_tree, category_name, expected_tool_count):
    """
    Test the number of tools in each category.

    Args:
        tool_tree: Instance of the ToolTree class.
        category_name (str): The name of the category.
        expected_tool_count (int): Expected number of tools in the category.
    """
    tools_in_category = tool_tree.get_tools_in_category(category_name)
    assert len(tools_in_category) == expected_tool_count, \
        f"Expected {expected_tool_count} tools in category '{category_name}', got {len(tools_in_category)}."


@pytest.mark.parametrize("keyword, expected_tool_names", [
    ('RNA', ['Seurat', 'Scanpy', 'RNAAnalyzer']),
    ('Genomics', ['GenomicsToolX', 'GenomicsExplorer', 'Bowtie']),
    ('Visualization', ['Scanpy', 'GenomicsExplorer']),
])
def test_search_tools_case_insensitivity(tool_tree, keyword, expected_tool_names):
    """
    Test that the search is case-insensitive.

    Args:
        tool_tree: Instance of the ToolTree class.
        keyword (str): The keyword to search for (mixed case).
        expected_tool_names (list): List of expected tool names.
    """
    mixed_case_keyword = ''.join(
        [char.upper() if i % 2 == 0 else char.lower() for i, char in enumerate(keyword)])
    results = tool_tree.search_tools(mixed_case_keyword)
    retrieved_names = sorted([tool.name for tool in results])
    expected_sorted = sorted(expected_tool_names)
    assert retrieved_names == expected_sorted, \
        f"Expected search results {expected_sorted} for keyword '{mixed_case_keyword}', got {retrieved_names}."


def test_add_tool_to_tree():
    """
    Test adding a new tool to the tree and ensuring it's correctly categorized.
    """
    # Initialize a new ToolTree
    tree = ToolTree()
    new_tool = Tool(
        name='BioToolY',
        category='Bioinformatics',
        features=['Feature1', 'Feature2'],
        cost='Free',
        description='A bioinformatics tool for data analysis.',
        url='https://biotooly.example.com/',
        language='Python',
        platform='Cross-platform'
    )
    tree.build_tree([new_tool])

    # Check that the category exists
    categories = tree.get_all_categories()
    assert 'Bioinformatics' in categories, "Category 'Bioinformatics' should be present after adding a new tool."

    # Retrieve tools in the new category
    tools_in_category = tree.get_tools_in_category('Bioinformatics')
    assert len(
        tools_in_category) == 1, "There should be one tool in the 'Bioinformatics' category."
    assert tools_in_category[0].name == 'BioToolY', "The tool in 'Bioinformatics' category should be 'BioToolY'."

    # Add another tool to the same category
    another_tool = Tool(
        name='BioToolZ',
        category='Bioinformatics',
        features=['Feature3'],
        cost='Free',
        description='Another bioinformatics tool.',
        url='https://biotoolz.example.com/',
        language='R',
        platform='Cross-platform'
    )
    tree.add_tool(another_tool)

    # Check that both tools are present in the category
    tools_in_category = tree.get_tools_in_category('Bioinformatics')
    assert len(
        tools_in_category) == 2, "There should be two tools in the 'Bioinformatics' category."
    tool_names = sorted([tool.name for tool in tools_in_category])
    assert tool_names == [
        'BioToolY', 'BioToolZ'], f"Expected tools ['BioToolY', 'BioToolZ'], got {tool_names}."


def test_search_tools_no_matches(tool_tree):
    """
    Test searching for tools with a keyword that has no matches.

    Args:
        tool_tree: Instance of the ToolTree class.
    """
    keyword = 'NonExistentFeature'
    results = tool_tree.search_tools(keyword)
    assert len(
        results) == 0, f"Expected no search results for keyword '{keyword}', but got {len(results)}."
