"""
Unit tests for the tool functions in tools.py.
Run from the project root with: pytest tests/
"""

import sys
import os
import pandas as pd
import pytest

# Add the src/ folder to the Python path so we can import tools.py
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from tools import (
    load_csv,
    calculate_statistics,
    get_dataframe_info,
    save_report,
)


# ---------------------------------------------------------------------------
# Scenario 1 — Loading a valid CSV file
# ---------------------------------------------------------------------------
def test_load_valid_csv(tmp_path):
    """A correctly formatted CSV should be loaded into a DataFrame."""
    csv_path = tmp_path / "sales.csv"
    csv_path.write_text(
        "product,region,revenue,date\n"
        "A,North,100,2025-01-01\n"
        "B,South,200,2025-01-02\n"
        "C,East,300,2025-01-03\n"
    )

    df = load_csv(str(csv_path))

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 3
    assert list(df.columns) == ["product", "region", "revenue", "date"]


# ---------------------------------------------------------------------------
# Scenario 2 — Loading a non-existent file
# ---------------------------------------------------------------------------
def test_load_non_existent_file():
    """Loading a file that does not exist should raise FileNotFoundError."""
    with pytest.raises(FileNotFoundError) as exc_info:
        load_csv("this_file_does_not_exist.csv")

    assert "File not found" in str(exc_info.value)


# ---------------------------------------------------------------------------
# Scenario 3 — Loading an empty CSV
# ---------------------------------------------------------------------------
def test_load_empty_csv(tmp_path):
    """An empty CSV file should raise either ValueError or pandas EmptyDataError."""
    csv_path = tmp_path / "empty.csv"
    csv_path.write_text("")

    with pytest.raises(Exception):
        # pandas raises EmptyDataError for completely empty files;
        # load_csv() raises ValueError for files with headers but no rows.
        load_csv(str(csv_path))


def test_load_csv_with_headers_but_no_rows(tmp_path):
    """A CSV with only a header row should raise ValueError."""
    csv_path = tmp_path / "headers_only.csv"
    csv_path.write_text("product,region,revenue\n")

    with pytest.raises(ValueError) as exc_info:
        load_csv(str(csv_path))

    assert "empty" in str(exc_info.value).lower()


# ---------------------------------------------------------------------------
# Scenario 4 — Calculating the average of a numeric column
# ---------------------------------------------------------------------------
def test_calculate_average():
    """The statistics tool should return the correct mean of a numeric column."""
    df = pd.DataFrame({"revenue": [100, 200, 300, 400, 500]})

    result = calculate_statistics(df, "What is the average revenue?")

    assert "Average" in result
    assert "300.00" in result  # mean of 100..500 is 300


def test_calculate_sum():
    """The statistics tool should return the correct sum."""
    df = pd.DataFrame({"revenue": [100, 200, 300]})

    result = calculate_statistics(df, "What is the total revenue?")

    assert "Sum" in result
    assert "600.00" in result


def test_calculate_max():
    """The statistics tool should return the correct maximum."""
    df = pd.DataFrame({"revenue": [10, 50, 30, 90, 70]})

    result = calculate_statistics(df, "What is the highest revenue?")

    assert "Max" in result
    assert "90.00" in result


# ---------------------------------------------------------------------------
# Scenario 5 — Asking about a non-numeric column
# ---------------------------------------------------------------------------
def test_no_numeric_columns():
    """When the DataFrame has only text columns, return a helpful message."""
    df = pd.DataFrame({"product": ["A", "B", "C"], "region": ["N", "S", "E"]})

    result = calculate_statistics(df, "What is the average?")

    assert "No numeric columns" in result


# ---------------------------------------------------------------------------
# Scenario 6 — Saving a session report
# ---------------------------------------------------------------------------
def test_save_report(tmp_path):
    """The report writer should save the session log to a .txt file."""
    session_log = [
        {"question": "What is the average revenue?", "answer": "The average is 300."},
        {"question": "Which region performed best?", "answer": "The East region."},
        {"question": "How many products?", "answer": "There are 3 products."},
    ]
    output_path = tmp_path / "report.txt"

    result = save_report(session_log, str(output_path))

    assert "Report saved" in result
    assert output_path.exists()

    content = output_path.read_text(encoding="utf-8")
    assert "What is the average revenue?" in content
    assert "The average is 300." in content
    assert "Which region performed best?" in content


def test_save_empty_report(tmp_path):
    """Saving an empty session log should still create a valid file."""
    output_path = tmp_path / "empty_report.txt"

    result = save_report([], str(output_path))

    assert "Report saved" in result
    assert output_path.exists()


# ---------------------------------------------------------------------------
# Bonus — Helper utility test
# ---------------------------------------------------------------------------
def test_get_dataframe_info():
    """The helper should return a formatted summary of the DataFrame."""
    df = pd.DataFrame({
        "product": ["A", "B"],
        "revenue": [100, 200],
    })

    info = get_dataframe_info(df)

    assert "2 rows" in info
    assert "2 columns" in info
    assert "product" in info
    assert "revenue" in info
