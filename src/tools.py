import os
import pandas as pd


# ---------------------------------------------------------------------------
# Tool 1 — CSV loader and validator
# ---------------------------------------------------------------------------
def load_csv(file_path: str) -> pd.DataFrame:
    """
    Loads and validates a CSV file from the given path.

    Validation steps (in order):
        1. Check that the file exists on disk.
        2. Parse the file with pandas.read_csv().
        3. Check that the resulting DataFrame is not empty.

    Args:
        file_path: Path to the CSV file on disk.

    Returns:
        A pandas DataFrame containing the parsed CSV data.

    Raises:
        FileNotFoundError: If the file does not exist at the given path.
        ValueError: If the file is empty or contains no data rows.

    Note:
        Exceptions are raised (not returned as strings) because the CLI
        entry point catches them specifically to re-prompt the user.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    try:
        df = pd.read_csv(file_path)
    except pd.errors.EmptyDataError:
        raise ValueError("The CSV file is empty.")
    except pd.errors.ParserError as e:
        raise ValueError(f"The CSV file could not be parsed: {e}")

    if df.empty:
        raise ValueError("The CSV file is empty.")

    return df


# ---------------------------------------------------------------------------
# Tool 2 — Statistical analysis
# ---------------------------------------------------------------------------
def calculate_statistics(df: pd.DataFrame, question: str) -> str:
    """
    Performs statistical analysis on the DataFrame based on keywords found
    in the user's question.

    Supported operations:
        - mean / average
        - sum / total
        - max / highest / largest
        - min / lowest / smallest
        - count / how many
        - describe (default fallback when no keyword is matched)

    Args:
        df: The pandas DataFrame loaded by load_csv().
        question: The user's natural language question.

    Returns:
        A formatted string containing the analysis result. Errors are
        returned as user-friendly strings rather than raised, so the
        agent orchestrator can pass them straight to Claude.
    """
    try:
        question_lower = question.lower()
        numeric_cols = df.select_dtypes(include="number").columns.tolist()

        if not numeric_cols:
            return "No numeric columns found in the CSV file."

        results = []

        for col in numeric_cols:
            if "average" in question_lower or "mean" in question_lower:
                results.append(f"Average of '{col}': {df[col].mean():.2f}")
            elif "sum" in question_lower or "total" in question_lower:
                results.append(f"Sum of '{col}': {df[col].sum():.2f}")
            elif (
                "max" in question_lower
                or "highest" in question_lower
                or "largest" in question_lower
            ):
                results.append(f"Max of '{col}': {df[col].max():.2f}")
            elif (
                "min" in question_lower
                or "lowest" in question_lower
                or "smallest" in question_lower
            ):
                results.append(f"Min of '{col}': {df[col].min():.2f}")
            elif "count" in question_lower or "how many" in question_lower:
                results.append(f"Count of '{col}': {df[col].count()}")

        if not results:
            # No keyword matched — return a general describe() summary
            summary = df[numeric_cols].describe().to_string()
            return f"General statistics:\n{summary}"

        return "\n".join(results)

    except KeyError as e:
        return f"Error: column {e} not found in the CSV."
    except Exception as e:
        return f"Error during analysis: {str(e)}"


# ---------------------------------------------------------------------------
# Tool 3 — DataFrame metadata helper
# ---------------------------------------------------------------------------
def get_dataframe_info(df: pd.DataFrame) -> str:
    """
    Returns a formatted string summary of the DataFrame structure.

    The summary lists:
        - Row count
        - Column count
        - Each column's name and inferred data type

    This metadata is sent to Claude on every question so the model can
    reason about the data correctly without seeing the full contents
    of the CSV.

    Args:
        df: The pandas DataFrame.

    Returns:
        A formatted multi-line string describing the DataFrame structure.
    """
    try:
        col_info = "\n".join(
            [f"  - {col} ({dtype})" for col, dtype in zip(df.columns, df.dtypes)]
        )
        return (
            f"The CSV file has {len(df)} rows and "
            f"{len(df.columns)} columns:\n{col_info}"
        )
    except Exception as e:
        return f"Error reading DataFrame structure: {str(e)}"


# ---------------------------------------------------------------------------
# Tool 4 — Session report writer
# ---------------------------------------------------------------------------
def save_report(session_log: list, output_path: str = "report.txt") -> str:
    """
    Serializes the session log (a list of question-answer dictionaries)
    to a plain text file.

    The output file contains:
        - A header line
        - Each question and answer separated by a divider
        - A consistent numbering scheme (Q1/A1, Q2/A2, ...)

    Args:
        session_log: List of dicts with 'question' and 'answer' keys.
        output_path: Destination path for the report (default: 'report.txt').

    Returns:
        A confirmation string with the saved file's path on success, or
        a user-friendly error message on failure.
    """
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("CSV DATA ANALYST AGENT - SESSION REPORT\n")
            f.write("=" * 50 + "\n\n")

            for i, entry in enumerate(session_log, start=1):
                question = entry.get("question", "(no question)")
                answer = entry.get("answer", "(no answer)")
                f.write(f"Q{i}: {question}\n")
                f.write(f"A{i}: {answer}\n")
                f.write("-" * 40 + "\n")

        return f"Report saved to: {output_path}"

    except PermissionError:
        return f"Error: permission denied when writing to {output_path}."
    except OSError as e:
        return f"Error saving report: {str(e)}"
    except Exception as e:
        return f"Unexpected error saving report: {str(e)}"
