# tests/test_tool.py

"""
Unit tests for the Tool class in LabMateAI.
"""

import pytest
import dataclasses
from labmateai.tool import Tool


@pytest.fixture
def seurat_tool():
    """
    Fixture for the Seurat tool.
    """
    return Tool(
        tool_id=119,
        name='Seurat',
        category='Single-Cell Analysis',
        features=('Single-cell RNA-seq', 'Clustering'),
        cost="Free",
        description='An R package for single-cell RNA sequencing data.',
        url='https://satijalab.org/seurat/',
        language='R',
        platform='Cross-platform'
    )


@pytest.fixture
def scanpy_tool():
    """
    Fixture for the Scanpy tool.
    """
    return Tool(
        tool_id=337,
        name='Scanpy',
        category='Single-Cell Analysis',
        features=('Single-cell RNA-seq', 'Visualization'),
        cost="Free",
        description='A scalable toolkit for analyzing single-cell gene expression data.',
        url='https://scanpy.readthedocs.io/',
        language='Python',
        platform='Cross-platform'
    )


@pytest.fixture
def genomics_tool():
    """
    Fixture for the GenomicsToolX tool.
    """
    return Tool(
        tool_id=359,
        name='GenomicsToolX',
        category='Genomics',
        features=('Genome Assembly', 'Variant Calling'),
        cost="Free",
        description='A tool for comprehensive genome assembly and variant calling.',
        url='https://genomicstoolx.com/',
        language='Python',
        platform='Cross-platform'
    )


@pytest.fixture
def bowtie_tool():
    """
    Fixture for the Bowtie tool.
    """
    return Tool(
        tool_id=126,
        name='Bowtie',
        category='Genomics',
        features=('Sequence Alignment', 'Genome Mapping'),
        cost="Free",
        description='A fast and memory-efficient tool for aligning sequencing reads to long reference sequences.',
        url='https://bowtie-bio.sourceforge.net/index.shtml',
        language='C++',
        platform='Cross-platform'
    )


@pytest.fixture
def rna_analyzer_tool():
    """
    Fixture for the RNAAnalyzer tool.
    """
    return Tool(
        tool_id=360,
        name='RNAAnalyzer',
        category='RNA',
        features=('RNA-Seq Analysis', 'Differential Expression'),
        cost="Free",
        description='A tool for analyzing RNA-Seq data and identifying differential gene expression.',
        url='https://rnaanalyzer.example.com/',
        language='R',
        platform='Cross-platform'
    )


@pytest.mark.parametrize("tool1, tool2, expected_equality", [
    # Same name, different tool_id and attributes
    ('Seurat', 'Seurat', True),
    ('Seurat', 'seurat', True),  # Case-insensitive
    # Different names
    ('Seurat', 'Scanpy', False),
    ('GenomicsToolX', 'Bowtie', False),
    # Same name, different cases
    ('RNAAnalyzer', 'rnaanalyzer', True),
])
def test_tool_equality(tool1, tool2, expected_equality, seurat_tool, scanpy_tool, genomics_tool, bowtie_tool, rna_analyzer_tool):
    """
    Test the equality (__eq__) of Tool instances based on name (case-insensitive).
    """
    tools = {
        'Seurat': seurat_tool,
        'Scanpy': scanpy_tool,
        'GenomicsToolX': genomics_tool,
        'Bowtie': bowtie_tool,
        'RNAAnalyzer': rna_analyzer_tool
    }

    tool_obj1 = tools.get(tool1) if tool1 in tools else Tool(
        tool_id=999,
        name=tool1,
        category='Unknown',
        features=[],
        cost="Free",
        description='Unknown tool.',
        url='https://unknown.example.com/',
        language='Unknown',
        platform='Unknown'
    )

    tool_obj2 = tools.get(tool2) if tool2 in tools else Tool(
        tool_id=999,
        name=tool2,
        category='Unknown',
        features=[],
        cost="Free",
        description='Unknown tool.',
        url='https://unknown.example.com/',
        language='Unknown',
        platform='Unknown'
    )

    assert (tool_obj1 == tool_obj2) == expected_equality, \
        f"Equality test failed for '{tool1}' and '{tool2}'. Expected {expected_equality}, got {tool_obj1 == tool_obj2}."


@pytest.mark.parametrize("tool1, tool2, expected_hash_equality", [
    # Same name, different tool_id
    ('Seurat', 'Seurat', True),
    ('seurat', 'Seurat', True),  # Case-insensitive
    # Different names
    ('Seurat', 'Scanpy', False),
    ('GenomicsToolX', 'Bowtie', False),
    # Same name, different cases
    ('RNAAnalyzer', 'rnaanalyzer', True),
])
def test_tool_hash(tool1, tool2, expected_hash_equality, seurat_tool, scanpy_tool, genomics_tool, bowtie_tool, rna_analyzer_tool):
    """
    Test the hashing (__hash__) of Tool instances based on name (case-insensitive).
    """
    tools = {
        'Seurat': seurat_tool,
        'Scanpy': scanpy_tool,
        'GenomicsToolX': genomics_tool,
        'Bowtie': bowtie_tool,
        'RNAAnalyzer': rna_analyzer_tool
    }

    tool_obj1 = tools.get(tool1) if tool1 in tools else Tool(
        tool_id=999,
        name=tool1,
        category='Unknown',
        features=[],
        cost="Free",
        description='Unknown tool.',
        url='https://unknown.example.com/',
        language='Unknown',
        platform='Unknown'
    )

    tool_obj2 = tools.get(tool2) if tool2 in tools else Tool(
        tool_id=999,
        name=tool2,
        category='Unknown',
        features=[],
        cost="Free",
        description='Unknown tool.',
        url='https://unknown.example.com/',
        language='Unknown',
        platform='Unknown'
    )

    assert (hash(tool_obj1) == hash(tool_obj2)) == expected_hash_equality, \
        f"Hash equality test failed for '{tool1}' and '{tool2}'. Expected {expected_hash_equality}, got {hash(tool_obj1) == hash(tool_obj2)}."


def test_tool_initialization(seurat_tool, scanpy_tool, genomics_tool, bowtie_tool, rna_analyzer_tool):
    """
    Test the initialization of Tool instances with all attributes.
    """
    tools = [seurat_tool, scanpy_tool, genomics_tool,
             bowtie_tool, rna_analyzer_tool]

    for tool in tools:
        assert isinstance(
            tool.tool_id, int), f"Tool ID for '{tool.name}' should be an integer."
        assert isinstance(
            tool.name, str), f"Tool name for ID {tool.tool_id} should be a string."
        assert isinstance(
            tool.category, str), f"Tool category for ID {tool.tool_id} should be a string."
        assert isinstance(
            tool.features, tuple), f"Tool features for ID {tool.tool_id} should be a tuple."
        assert isinstance(
            tool.cost, str), f"Tool cost for ID {tool.tool_id} should be a string."
        assert isinstance(
            tool.description, str), f"Tool description for ID {tool.tool_id} should be a string."
        assert isinstance(
            tool.url, str), f"Tool URL for ID {tool.tool_id} should be a string."
        assert isinstance(
            tool.language, str), f"Tool language for ID {tool.tool_id} should be a string."
        assert isinstance(
            tool.platform, str), f"Tool platform for ID {tool.tool_id} should be a string."


def test_tool_immutability(seurat_tool):
    """
    Test that Tool instances are immutable (frozen dataclass).
    """
    with pytest.raises(dataclasses.FrozenInstanceError):
        seurat_tool.name = 'NewName'

    # Test reassignment of features, since tuples are immutable by default
    with pytest.raises(dataclasses.FrozenInstanceError):
        seurat_tool.features = ('New Feature',)


def test_tool_repr(seurat_tool):
    """
    Test the string representation (__repr__) of the Tool instance.
    """
    expected_repr = "Tool(tool_id=119, name='Seurat')"
    assert repr(seurat_tool) == expected_repr, \
        f"Expected repr '{expected_repr}', got '{repr(seurat_tool)}'."


def test_tool_equality_with_different_attributes(seurat_tool):
    """
    Test that two Tool instances with the same name but different attributes are equal.
    """
    duplicate_seurat = Tool(
        tool_id=999,
        name='Seurat',
        category='Genomics',
        features=['Genome Assembly'],
        cost="Free",
        description='Different description.',
        url='https://different-url.com/',
        language='Python',
        platform='Linux'
    )

    assert seurat_tool == duplicate_seurat, \
        "Tools with the same name should be equal, regardless of other attributes."


def test_tool_equality_with_different_names(seurat_tool):
    """
    Test that two Tool instances with different names are not equal, even if other attributes are the same.
    """
    different_tool = Tool(
        tool_id=119,
        name='SeuratPro',
        category='Single-Cell Analysis',
        features=['Single-cell RNA-seq', 'Clustering'],
        cost="Free",
        description='An advanced R package for single-cell RNA sequencing data.',
        url='https://satijalab.org/seuratpro/',
        language='R',
        platform='Cross-platform'
    )

    assert seurat_tool != different_tool, \
        "Tools with different names should not be equal, even if other attributes are identical."


def test_tool_hash_equality(seurat_tool):
    """
    Test that tools with the same name have the same hash.
    """
    duplicate_seurat = Tool(
        tool_id=999,
        name='Seurat',
        category='Genomics',
        features=['Genome Assembly'],
        cost="Free",
        description='Different description.',
        url='https://different-url.com/',
        language='Python',
        platform='Linux'
    )

    assert hash(seurat_tool) == hash(duplicate_seurat), \
        "Tools with the same name should have identical hash values."


def test_tool_hash_inequality(seurat_tool, scanpy_tool):
    """
    Test that tools with different names have different hash values.
    """
    assert hash(seurat_tool) != hash(scanpy_tool), \
        "Tools with different names should have different hash values."
