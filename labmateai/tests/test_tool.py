# tests/test_tool.py

"""
Unit tests for the Tool class.
"""

import pytest
from labmateai.tool import Tool


@pytest.fixture
def sample_tool():
    """
    Fixture to provide a sample Tool instance.
    """
    return Tool(
        name='Seurat',
        category='Single-Cell Analysis',
        features=['Single-cell RNA-seq', 'Clustering'],
        cost='Free',
        description='An R package for single-cell RNA sequencing data.',
        url='https://satijalab.org/seurat/',
        language='R',
        platform='Cross-platform'
    )


@pytest.fixture
def another_tool():
    """
    Fixture to provide another sample Tool instance.
    """
    return Tool(
        name='GenomicsToolX',
        category='Genomics',
        features=['Genome Assembly', 'Variant Calling'],
        cost='Free',
        description='A tool for comprehensive genome assembly and variant calling.',
        url='https://genomicstoolx.com/',
        language='Python',
        platform='Cross-platform'
    )


@pytest.mark.parametrize("name, category, features, cost, description, url, language, platform", [
    ('Seurat', 'Single-Cell Analysis', ['Single-cell RNA-seq', 'Clustering'], 'Free',
     'An R package for single-cell RNA sequencing data.', 'https://satijalab.org/seurat/', 'R', 'Cross-platform'),
    ('Scanpy', 'Single-Cell Analysis', ['Single-cell RNA-seq', 'Visualization'], 'Free',
     'A scalable toolkit for analyzing single-cell gene expression data.', 'https://scanpy.readthedocs.io/', 'Python', 'Cross-platform'),
    ('GenomicsToolX', 'Genomics', ['Genome Assembly', 'Variant Calling'], 'Free',
     'A tool for comprehensive genome assembly and variant calling.', 'https://genomicstoolx.com/', 'Python', 'Cross-platform'),
    ('RNAAnalyzer', 'RNA', ['RNA-Seq Analysis', 'Differential Expression'], 'Free',
     'A tool for analyzing RNA-Seq data and identifying differential gene expression.', 'https://rnaanalyzer.example.com/', 'R', 'Cross-platform'),
])
def test_tool_initialization(name, category, features, cost, description, url, language, platform):
    """
    Test that a Tool instance is initialized correctly.

    Args:
        name (str): Tool name.
        category (str): Tool category.
        features (list): List of features.
        cost (str): Cost.
        description (str): Description.
        url (str): URL.
        language (str): Programming language.
        platform (str): Platform.
    """
    tool = Tool(
        name=name,
        category=category,
        features=features,
        cost=cost,
        description=description,
        url=url,
        language=language,
        platform=platform
    )

    assert tool.name == name, f"Expected name '{name}', got '{tool.name}'."
    assert tool.category == category, f"Expected category '{category}', got '{tool.category}'."
    assert tool.features == features, f"Expected features '{features}', got '{tool.features}'."
    assert tool.cost == cost, f"Expected cost '{cost}', got '{tool.cost}'."
    assert tool.description == description, f"Expected description '{description}', got '{tool.description}'."
    assert tool.url == url, f"Expected URL '{url}', got '{tool.url}'."
    assert tool.language == language, f"Expected language '{language}', got '{tool.language}'."
    assert tool.platform == platform, f"Expected platform '{platform}', got '{tool.platform}'."


def test_tool_equality_same_name(sample_tool):
    """
    Test that two Tool instances with the same name (case-insensitive) are equal.

    Args:
        sample_tool (Tool): A sample Tool instance.
    """
    tool_duplicate = Tool(
        name='seurat',  # different case
        category='Bioinformatics',
        features=['Feature1'],
        cost='Free',
        description='Another description.',
        url='https://anotherurl.com/',
        language='Python',
        platform='Linux'
    )

    assert sample_tool == tool_duplicate, "Tools with the same name (case-insensitive) should be equal."


def test_tool_equality_different_name(sample_tool, another_tool):
    """
    Test that two Tool instances with different names are not equal.

    Args:
        sample_tool (Tool): A sample Tool instance.
        another_tool (Tool): Another sample Tool instance with a different name.
    """
    assert sample_tool != another_tool, "Tools with different names should not be equal."


@pytest.mark.parametrize("name1, name2, expected", [
    ('Seurat', 'seurat', True),
    ('Seurat', 'SEURAT', True),
    ('Seurat', 'Scanpy', False),
    ('ToolA', 'ToolB', False),
])
def test_tool_equality(name1, name2, expected):
    """
    Parametrized test for Tool equality based on names.

    Args:
        name1 (str): Name of the first tool.
        name2 (str): Name of the second tool.
        expected (bool): Expected equality result.
    """
    tool1 = Tool(
        name=name1,
        category='Category1',
        features=['Feature1'],
        cost='Free',
        description='Description1',
        url='http://tool1.com',
        language='Python',
        platform='Cross-platform'
    )
    tool2 = Tool(
        name=name2,
        category='Category2',
        features=['Feature2'],
        cost='Free',
        description='Description2',
        url='http://tool2.com',
        language='R',
        platform='Cross-platform'
    )

    assert (
        tool1 == tool2) == expected, f"Equality test failed for '{name1}' and '{name2}'."


@pytest.mark.parametrize("name, expected_hash", [
    ('Seurat', hash('seurat')),
    ('Scanpy', hash('scanpy')),
    ('GenomicsToolX', hash('genomicstoolx')),
    ('RNAAnalyzer', hash('rnaanalyzer')),
])
def test_tool_hash(name, expected_hash):
    """
    Test that the hash of a Tool instance is based on the lowercased name.

    Args:
        name (str): Name of the tool.
        expected_hash (int): Expected hash value.
    """
    tool = Tool(
        name=name,
        category='Category',
        features=['Feature1'],
        cost='Free',
        description='Description',
        url='http://tool.com',
        language='Python',
        platform='Cross-platform'
    )
    assert hash(
        tool) == expected_hash, f"Hash for tool '{name}' should be '{expected_hash}', got '{hash(tool)}'."


@pytest.mark.parametrize("name, expected_repr", [
    ('Seurat', "Tool(name='Seurat')"),
    ('Scanpy', "Tool(name='Scanpy')"),
    ('GenomicsToolX', "Tool(name='GenomicsToolX')"),
])
def test_tool_repr(name, expected_repr):
    """
    Test the string representation (__repr__) of the Tool instance.

    Args:
        name (str): Name of the tool.
        expected_repr (str): Expected string representation.
    """
    tool = Tool(
        name=name,
        category='Category',
        features=['Feature1'],
        cost='Free',
        description='Description',
        url='http://tool.com',
        language='Python',
        platform='Cross-platform'
    )
    assert repr(
        tool) == expected_repr, f"__repr__ for tool '{name}' should be '{expected_repr}', got '{repr(tool)}'."


@pytest.mark.parametrize("name, category, features, cost, description, url, language, platform", [
    ('', 'Category', ['Feature1'], 'Free', 'Description',
     'http://tool.com', 'Python', 'Cross-platform'),
    ('ToolWithNoFeatures', 'Category', [], 'Free', 'Description',
     'http://tool.com', 'Python', 'Cross-platform'),
    ('ToolWithSpecialChars', 'Category', [
     'Feature@1', 'Feature#2'], 'Free', 'Description', 'http://tool.com', 'Python', 'Cross-platform'),
])
def test_tool_initialization_edge_cases(name, category, features, cost, description, url, language, platform):
    """
    Test the initialization of Tool instances with edge case inputs.

    Args:
        name (str): Name of the tool.
        category (str): Category of the tool.
        features (list): List of features.
        cost (str): Cost of the tool.
        description (str): Description of the tool.
        url (str): URL of the tool.
        language (str): Programming language.
        platform (str): Platform of the tool.
    """
    tool = Tool(
        name=name,
        category=category,
        features=features,
        cost=cost,
        description=description,
        url=url,
        language=language,
        platform=platform
    )

    assert tool.name == name, f"Expected name '{name}', got '{tool.name}'."
    assert tool.features == features, f"Expected features '{features}', got '{tool.features}'."
    # Additional assertions can be added as needed


def test_tool_equality_with_non_tool():
    """
    Test that Tool instances are not equal to objects of different types.
    """
    tool = Tool(
        name='Seurat',
        category='Single-Cell Analysis',
        features=['Single-cell RNA-seq', 'Clustering'],
        cost='Free',
        description='An R package for single-cell RNA sequencing data.',
        url='https://satijalab.org/seurat/',
        language='R',
        platform='Cross-platform'
    )

    assert tool != "Seurat", "Tool instance should not be equal to a string."


def test_tool_hash_uniqueness():
    """
    Test that different Tool instances have unique hash values based on their names.
    """
    tool1 = Tool(
        name='ToolA',
        category='Category1',
        features=['Feature1'],
        cost='Free',
        description='Description A',
        url='http://toola.com',
        language='Python',
        platform='Cross-platform'
    )

    tool2 = Tool(
        name='ToolB',
        category='Category2',
        features=['Feature2'],
        cost='Free',
        description='Description B',
        url='http://toolb.com',
        language='R',
        platform='Cross-platform'
    )

    tool3 = Tool(
        name='ToolA',  # Same name as tool1 but different case
        category='Category3',
        features=['Feature3'],
        cost='Free',
        description='Description C',
        url='http://toolc.com',
        language='Java',
        platform='Cross-platform'
    )

    assert hash(tool1) == hash(
        tool3), "Tools with the same name (case-insensitive) should have the same hash."
    assert hash(tool1) != hash(
        tool2), "Tools with different names should have different hashes."
