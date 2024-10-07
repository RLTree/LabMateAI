# tests/test_tool.py

"""
Unit tests for the Tool class in LabMateAI.
"""

import pytest
from labmateai.tool import Tool


@pytest.fixture
def sample_tool():
    """
    Fixture to provide a sample Tool instance for testing.
    """
    return Tool(
        tool_id=119,
        name='Seurat',
        category='Single-Cell Analysis',
        features=['Single-cell RNA-seq', 'Clustering'],
        cost="Free",
        description='An R package for single-cell RNA sequencing data.',
        url='https://satijalab.org/seurat/',
        language='R',
        platform='Cross-platform'
    )


def test_tool_initialization(sample_tool):
    """
    Test that the Tool instance is initialized correctly with all attributes.
    """
    assert sample_tool.tool_id == 119, "Tool ID does not match."
    assert sample_tool.name == 'Seurat', "Tool name does not match."
    assert sample_tool.category == 'Single-Cell Analysis', "Tool category does not match."
    assert sample_tool.features == [
        'Single-cell RNA-seq', 'Clustering'], "Tool features do not match."
    assert sample_tool.cost == "Free", "Tool cost does not match."
    assert sample_tool.description == 'An R package for single-cell RNA sequencing data.', "Tool description does not match."
    assert sample_tool.url == 'https://satijalab.org/seurat/', "Tool URL does not match."
    assert sample_tool.language == 'R', "Tool language does not match."
    assert sample_tool.platform == 'Cross-platform', "Tool platform does not match."


def test_tool_equality(sample_tool):
    """
    Test that two Tool instances with the same name (case-insensitive) are considered equal.
    """
    tool_duplicate = Tool(
        tool_id=120,
        name='seurat',  # Different case
        category='Single-Cell Analysis',
        features=['Single-cell RNA-seq', 'Clustering'],
        cost="Free",
        description='Duplicate Seurat tool.',
        url='https://duplicate.seurat.org/',
        language='R',
        platform='Cross-platform'
    )

    assert sample_tool == tool_duplicate, "Tools with the same name should be equal."


def test_tool_inequality(sample_tool):
    """
    Test that two Tool instances with different names are not considered equal.
    """
    tool_different = Tool(
        tool_id=121,
        name='Scanpy',
        category='Single-Cell Analysis',
        features=['Single-cell RNA-seq', 'Visualization'],
        cost="Free",
        description='A scalable toolkit for analyzing single-cell gene expression data.',
        url='https://scanpy.readthedocs.io/',
        language='Python',
        platform='Cross-platform'
    )

    assert sample_tool != tool_different, "Tools with different names should not be equal."


def test_tool_hashing(sample_tool):
    """
    Test that Tool instances can be hashed and used in sets or as dictionary keys.
    """
    tool_set = set()
    tool_set.add(sample_tool)

    tool_duplicate = Tool(
        tool_id=122,
        name='Seurat',  # Same name
        category='Single-Cell Analysis',
        features=['Single-cell RNA-seq', 'Clustering'],
        cost="Free",
        description='Another Seurat tool.',
        url='https://another.seurat.org/',
        language='R',
        platform='Cross-platform'
    )

    tool_set.add(tool_duplicate)

    assert len(tool_set) == 1, "Duplicate tools should not be added to the set."

    tool_dict = {sample_tool: 'Original'}
    tool_dict[tool_duplicate] = 'Duplicate'

    assert tool_dict[sample_tool] == 'Duplicate', "Dictionary should overwrite with duplicate tool key."


def test_tool_repr(sample_tool):
    """
    Test the string representation (__repr__) of the Tool instance.
    """
    expected_repr = "Tool(tool_id=119, name='Seurat')"
    assert repr(
        sample_tool) == expected_repr, f"Expected repr '{expected_repr}', got '{repr(sample_tool)}'."


def test_tool_immutability(sample_tool):
    """
    Test that the Tool instance is immutable (frozen).
    """
    with pytest.raises(AttributeError):
        sample_tool.name = 'ModifiedSeurat'

    with pytest.raises(AttributeError):
        sample_tool.features = ('New Feature')


def test_tool_invalid_equality():
    """
    Test that Tool instances are not equal to objects of different types.
    """
    tool = Tool(
        tool_id=123,
        name='Bowtie',
        category='Genomics',
        features=['Sequence Alignment', 'Genome Mapping'],
        cost="Free",
        description='A fast and memory-efficient tool for aligning sequencing reads.',
        url='https://bowtie-bio.sourceforge.net/index.shtml',
        language='C++',
        platform='Cross-platform'
    )

    assert tool != "Bowtie", "Tool should not be equal to a string."
    assert tool != 123, "Tool should not be equal to an integer."


def test_tool_feature_case_insensitivity():
    """
    Test that features are handled correctly regardless of case.
    """
    tool_upper_features = Tool(
        tool_id=124,
        name='RNAAnalyzer',
        category='RNA',
        features=['RNA-SEQ ANALYSIS', 'DIFFERENTIAL EXPRESSION'],
        cost="Free",
        description='A tool for analyzing RNA-Seq data.',
        url='https://rnaanalyzer.example.com/',
        language='R',
        platform='Cross-platform'
    )

    tool_lower_features = Tool(
        tool_id=125,
        name='RNAAnalyzer',
        category='RNA',
        features=['rna-seq analysis', 'differential expression'],
        cost="Free",
        description='Another tool for analyzing RNA-Seq data.',
        url='https://another.rnaanalyzer.example.com/',
        language='R',
        platform='Cross-platform'
    )

    assert tool_upper_features == tool_lower_features, "Tools with features differing only in case should be equal."


def test_tool_different_names_same_attributes():
    """
    Test that tools with different names but identical other attributes are not equal.
    """
    tool1 = Tool(
        tool_id=126,
        name='ToolA',
        category='Genomics',
        features=['Feature1', 'Feature2'],
        cost="Free",
        description='Description A.',
        url='https://toola.example.com/',
        language='Python',
        platform='Cross-platform'
    )

    tool2 = Tool(
        tool_id=127,
        name='ToolB',
        category='Genomics',
        features=['Feature1', 'Feature2'],
        cost="Free",
        description='Description A.',
        url='https://toolb.example.com/',
        language='Python',
        platform='Cross-platform'
    )

    assert tool1 != tool2, "Tools with different names should not be equal, even if other attributes match."
