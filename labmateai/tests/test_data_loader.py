# tests/test_data_loader.py

"""
Unit tests for the data_loader module.
"""

import json
import pytest
from labmateai.data_loader import load_tools_from_json, load_tools_from_csv
from labmateai.tool import Tool


# Define sample JSON data for testing
SAMPLE_JSON = json.dumps([
    {
        "name": "Seurat",
        "category": "Single-Cell Analysis",
        "features": ["Single-cell RNA-seq", "Clustering"],
        "cost": "Free",
        "description": "An R package for single-cell RNA sequencing data.",
        "url": "https://satijalab.org/seurat/",
        "platform": "Cross-platform",
        "language": "R"
    },
    {
        "name": "GenomicsToolX",
        "category": "Genomics",
        "features": ["Genome Assembly", "Variant Calling"],
        "cost": "Free",
        "description": "A tool for comprehensive genome assembly and variant calling.",
        "url": "https://genomicstoolx.com/",
        "platform": "Cross-platform",
        "language": "Python"
    },
    {
        "name": "RNAAnalyzer",
        "category": "RNA",
        "features": ["RNA-Seq Analysis", "Differential Expression"],
        "cost": "Free",
        "description": "A tool for analyzing RNA-Seq data and identifying differential gene expression.",
        "url": "https://rnaanalyzer.example.com/",
        "platform": "Cross-platform",
        "language": "R"
    }
])


# Define sample CSV data for testing
SAMPLE_CSV = """name,category,features,cost,description,url,platform,language
Seurat,Single-Cell Analysis,"Single-cell RNA-seq;Clustering",Free,"An R package for single-cell RNA sequencing data.","https://satijalab.org/seurat/","Cross-platform",R
GenomicsToolX,Genomics,"Genome Assembly;Variant Calling",Free,"A tool for comprehensive genome assembly and variant calling.","https://genomicstoolx.com/","Cross-platform",Python
RNAAnalyzer,RNA,"RNA-Seq Analysis;Differential Expression",Free,"A tool for analyzing RNA-Seq data and identifying differential gene expression.","https://rnaanalyzer.example.com/","Cross-platform",R
"""


@pytest.fixture
def sample_json_data():
    """
    Fixture to provide sample JSON data.
    """
    return SAMPLE_JSON


@pytest.fixture
def sample_csv_data():
    """
    Fixture to provide sample CSV data.
    """
    return SAMPLE_CSV


@pytest.fixture
def expected_tools():
    """
    Fixture to provide expected Tool instances from SAMPLE_JSON.
    """
    return [
        Tool(
            name="Seurat",
            category="Single-Cell Analysis",
            features=["Single-cell RNA-seq", "Clustering"],
            cost="Free",
            description="An R package for single-cell RNA sequencing data.",
            url="https://satijalab.org/seurat/",
            platform="Cross-platform",
            language="R"
        ),
        Tool(
            name="GenomicsToolX",
            category="Genomics",
            features=["Genome Assembly", "Variant Calling"],
            cost="Free",
            description="A tool for comprehensive genome assembly and variant calling.",
            url="https://genomicstoolx.com/",
            platform="Cross-platform",
            language="Python"
        ),
        Tool(
            name="RNAAnalyzer",
            category="RNA",
            features=["RNA-Seq Analysis", "Differential Expression"],
            cost="Free",
            description="A tool for analyzing RNA-Seq data and identifying differential gene expression.",
            url="https://rnaanalyzer.example.com/",
            platform="Cross-platform",
            language="R"
        )
    ]


def test_load_tools_from_json_success(expected_tools, sample_json_data, mocker):
    """
    Test successful loading of tools from JSON.

    Args:
        expected_tools (list): Expected list of Tool instances.
        sample_json_data (str): Sample JSON data.
        mocker: Pytest mocker fixture.
    """
    # Mock importlib.resources.open_text to return sample_json_data
    mock_file = mocker.mock_open(read_data=sample_json_data)
    mocker.patch('importlib.resources.open_text', mock_file)

    tools = load_tools_from_json()
    assert len(tools) == len(
        expected_tools), f"Expected {len(expected_tools)} tools, got {len(tools)}."

    for loaded_tool, expected_tool in zip(tools, expected_tools):
        assert loaded_tool.name == expected_tool.name, f"Expected tool name '{expected_tool.name}', got '{loaded_tool.name}'."
        assert loaded_tool.category == expected_tool.category, f"Expected category '{expected_tool.category}', got '{loaded_tool.category}'."
        assert loaded_tool.features == expected_tool.features, f"Expected features {expected_tool.features}, got {loaded_tool.features}."
        assert loaded_tool.cost == expected_tool.cost, f"Expected cost '{expected_tool.cost}', got '{loaded_tool.cost}'."
        assert loaded_tool.description == expected_tool.description, f"Expected description '{expected_tool.description}', got '{loaded_tool.description}'."
        assert loaded_tool.url == expected_tool.url, f"Expected URL '{expected_tool.url}', got '{loaded_tool.url}'."
        assert loaded_tool.platform == expected_tool.platform, f"Expected platform '{expected_tool.platform}', got '{loaded_tool.platform}'."
        assert loaded_tool.language == expected_tool.language, f"Expected language '{expected_tool.language}', got '{loaded_tool.language}'."


def test_load_tools_from_json_missing_required_fields(mocker):
    """
    Test loading tools from JSON with missing required fields.

    Args:
        mocker: Pytest mocker fixture.
    """
    # JSON with missing 'features' and 'language'
    incomplete_json = json.dumps([
        {
            "name": "IncompleteTool",
            "category": "Bioinformatics",
            "cost": "Free",
            "description": "A tool with missing required fields.",
            "url": "https://incomplete.example.com/",
            "platform": "Cross-platform"
            # 'features' and 'language' are missing
        }
    ])
    mock_file = mocker.mock_open(read_data=incomplete_json)
    mocker.patch('importlib.resources.open_text', mock_file)

    with pytest.raises(KeyError) as exc_info:
        load_tools_from_json()
    assert "'features'" in str(exc_info.value) or "'language'" in str(exc_info.value), \
        "Expected KeyError for missing 'features' or 'language' fields."


def test_load_tools_from_json_invalid_json(mocker):
    """
    Test loading tools from malformed JSON.

    Args:
        mocker: Pytest mocker fixture.
    """
    malformed_json = "{ this is not: valid JSON }"
    mock_file = mocker.mock_open(read_data=malformed_json)
    mocker.patch('importlib.resources.open_text', mock_file)

    with pytest.raises(json.JSONDecodeError):
        load_tools_from_json()


def test_load_tools_from_csv_success(expected_tools, sample_csv_data, tmp_path):
    """
    Test successful loading of tools from CSV.

    Args:
        expected_tools (list): Expected list of Tool instances.
        sample_csv_data (str): Sample CSV data.
        tmp_path: Pytest fixture for temporary directory.
    """
    # Create a temporary CSV file
    csv_file = tmp_path / "tools.csv"
    csv_file.write_text(sample_csv_data, encoding='utf-8')

    tools = load_tools_from_csv(str(csv_file))
    assert len(tools) == len(
        expected_tools), f"Expected {len(expected_tools)} tools, got {len(tools)}."

    for loaded_tool, expected_tool in zip(tools, expected_tools):
        assert loaded_tool.name == expected_tool.name, f"Expected tool name '{expected_tool.name}', got '{loaded_tool.name}'."
        assert loaded_tool.category == expected_tool.category, f"Expected category '{expected_tool.category}', got '{loaded_tool.category}'."
        assert loaded_tool.features == expected_tool.features, f"Expected features '{expected_tool.features}', got '{loaded_tool.features}'."
        assert loaded_tool.cost == expected_tool.cost, f"Expected cost '{expected_tool.cost}', got '{loaded_tool.cost}'."
        assert loaded_tool.description == expected_tool.description, f"Expected description '{expected_tool.description}', got '{loaded_tool.description}'."
        assert loaded_tool.url == expected_tool.url, f"Expected URL '{expected_tool.url}', got '{loaded_tool.url}'."
        assert loaded_tool.platform == expected_tool.platform, f"Expected platform '{expected_tool.platform}', got '{loaded_tool.platform}'."
        assert loaded_tool.language == expected_tool.language, f"Expected language '{expected_tool.language}', got '{loaded_tool.language}'."


@pytest.mark.parametrize("csv_data, expected_tool_count, expected_tool_names, expect_error", [
    # Valid CSV with two tools
    ("""name,category,features,cost,description,url,platform,language
ToolA,Bioinformatics,"Feature1;Feature2",Free,"Description A","http://toola.com","Cross-platform",Python
ToolB,Genomics,"Feature3;Feature4",Free,"Description B","http://toolb.com","Cross-platform",R
""",
     2,
     ["ToolA", "ToolB"],
     False),
    # CSV with missing 'language' field (empty)
    ("""name,category,features,cost,description,url,platform,language
ToolC,Genomics,"Feature5;Feature6",Free,"Description C","http://toolc.com","Cross-platform",
""",
     1,
     ["ToolC"],
     True),
    # CSV with empty 'features'
    ("""name,category,features,cost,description,url,platform,language
ToolD,Bioinformatics,"",Free,"Description D","http://toold.com","Cross-platform",Java
""",
     1,
     ["ToolD"],
     True),
])
def test_load_tools_from_csv_various_cases(csv_data, expected_tool_count, expected_tool_names, expect_error, tmp_path):
    """
    Test loading tools from CSV with various scenarios.

    Args:
        csv_data (str): CSV data as string.
        expected_tool_count (int): Expected number of Tool instances.
        expected_tool_names (list): Expected names of tools.
        expect_error (bool): Whether to expect an error.
        tmp_path: Pytest fixture for temporary directory.
    """
    # Create a temporary CSV file
    csv_file = tmp_path / "tools_various.csv"
    csv_file.write_text(csv_data, encoding='utf-8')

    if expect_error:
        with pytest.raises(KeyError):
            load_tools_from_csv(str(csv_file))
    else:
        tools = load_tools_from_csv(str(csv_file))
        assert len(
            tools) == expected_tool_count, f"Expected {expected_tool_count} tools, got {len(tools)}."

        retrieved_names = [tool.name for tool in tools]
        for name in expected_tool_names:
            assert name in retrieved_names, f"Expected tool '{name}' to be loaded from CSV."

        # Additional checks
        for tool in tools:
            if not tool.features:
                assert tool.features == [
                ], f"Expected empty features list, got {tool.features}."
            if not tool.language:
                # Since 'language' is required and non-empty, this should not happen
                pytest.fail(
                    "Tool has empty 'language' field, but it should have raised KeyError.")


def test_load_tools_from_csv_missing_required_fields(tmp_path):
    """
    Test loading tools from CSV with missing required fields.

    Args:
        tmp_path: Pytest fixture for temporary directory.
    """
    # CSV missing 'language' field in the second row
    malformed_csv = """name,category,features,cost,description,url,platform,language
ToolA,Bioinformatics,"Feature1;Feature2",Free,"Description A","http://toola.com","Cross-platform",Python
ToolB,Genomics,"Feature3;Feature4",Free,"Description B","http://toolb.com","Cross-platform",
"""
    csv_file = tmp_path / "malformed_columns.csv"
    csv_file.write_text(malformed_csv, encoding='utf-8')

    with pytest.raises(KeyError) as exc_info:
        load_tools_from_csv(str(csv_file))
    assert "'language'" in str(
        exc_info.value), "Expected KeyError for missing 'language' field."


def test_load_tools_from_csv_malformed_csv(tmp_path):
    """
    Test loading tools from a malformed CSV file.

    Args:
        tmp_path: Pytest fixture for temporary directory.
    """
    # Malformed CSV (uneven columns)
    malformed_csv = """name,category,features,cost,description,url,platform,language
ToolA,Bioinformatics,"Feature1;Feature2",Free,"Description A","http://toola.com","Cross-platform",Python
ToolB,Genomics,"Feature3;Feature4",Free,"Description B","http://toolb.com","Cross-platform"
"""
    csv_file = tmp_path / "malformed_columns.csv"
    csv_file.write_text(malformed_csv, encoding='utf-8')

    with pytest.raises(KeyError) as exc_info:
        load_tools_from_csv(str(csv_file))
    assert "'language'" in str(
        exc_info.value), "Expected KeyError for missing 'language' field."


def test_load_tools_from_csv_features_parsing(tmp_path):
    """
    Test that features are correctly parsed from semicolon-separated string.

    Args:
        tmp_path: Pytest fixture for temporary directory.
    """
    csv_data = """name,category,features,cost,description,url,platform,language
ToolE,Bioinformatics,"Feature1;Feature2;Feature3",Free,"Description E","http://toole.com","Cross-platform",C++
"""
    csv_file = tmp_path / "features_parsing.csv"
    csv_file.write_text(csv_data, encoding='utf-8')

    tools = load_tools_from_csv(str(csv_file))
    assert len(tools) == 1, f"Expected 1 tool, got {len(tools)}."

    tool = tools[0]
    expected_features = ["Feature1", "Feature2", "Feature3"]
    assert tool.features == expected_features, f"Expected features {expected_features}, got {tool.features}."


def test_load_tools_from_csv_extra_columns(tmp_path):
    """
    Test loading tools from CSV with extra columns that should be ignored.

    Args:
        tmp_path: Pytest fixture for temporary directory.
    """
    csv_data = """name,category,features,cost,description,url,platform,language,extra_column
ToolF,Bioinformatics,"Feature4;Feature5",Free,"Description F","http://toolf.com","Cross-platform",Ruby,ExtraValue
"""
    csv_file = tmp_path / "extra_columns.csv"
    csv_file.write_text(csv_data, encoding='utf-8')

    tools = load_tools_from_csv(str(csv_file))
    assert len(tools) == 1, f"Expected 1 tool, got {len(tools)}."

    tool = tools[0]
    assert tool.name == "ToolF", f"Expected tool name 'ToolF', got '{tool.name}'."
    assert tool.category == "Bioinformatics"
    assert tool.features == ["Feature4", "Feature5"]
    assert tool.language == "Ruby"
    # Extra column should be ignored since 'extra_column' is not used in Tool initialization
    # No assertion needed for 'extra_column'


def test_load_tools_from_csv_empty_file(tmp_path):
    """
    Test loading tools from an empty CSV file.

    Args:
        tmp_path: Pytest fixture for temporary directory.
    """
    empty_csv = ""
    csv_file = tmp_path / "empty.csv"
    csv_file.write_text(empty_csv, encoding='utf-8')

    with pytest.raises(KeyError) as exc_info:
        load_tools_from_csv(str(csv_file))
    assert "CSV file is missing header." in str(
        exc_info.value), "Expected KeyError for missing header."


def test_load_tools_from_csv_only_headers(tmp_path):
    """
    Test loading tools from a CSV file that contains only headers.

    Args:
        tmp_path: Pytest fixture for temporary directory.
    """
    headers_only_csv = """name,category,features,cost,description,url,platform,language
"""
    csv_file = tmp_path / "headers_only.csv"
    csv_file.write_text(headers_only_csv, encoding='utf-8')

    # Since headers are present but no data rows, it should not raise KeyError and return an empty list
    tools = load_tools_from_csv(str(csv_file))
    assert len(
        tools) == 0, f"Expected 0 tools from headers-only CSV, got {len(tools)}."
