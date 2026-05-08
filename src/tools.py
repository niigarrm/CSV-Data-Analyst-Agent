import pandas as pd
import os


def load_csv(file_path: str) -> pd.DataFrame:
    """
    Loads and validates a CSV file from the given path.
    Returns a pandas DataFrame if successful.
    Raises an error if the file does not exist or is empty.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    df = pd.read_csv(file_path)

    if df.empty:
        raise ValueError("The CSV file is empty.")

    return df


def calculate_statistics(df: pd.DataFrame, question: str) -> str:
    """
    Performs statistical analysis on the DataFrame based on the question.
    Supports: mean, sum, max, min, count, groupby-style summaries.
    Returns a formatted string with the result.
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
            elif "max" in question_lower or "highest" in question_lower or "largest" in question_lower:
                results.append(f"Max of '{col}': {df[col].max():.2f}")
            elif "min" in question_lower or "lowest" in question_lower or "smallest" in question_lower:
                results.append(f"Min of '{col}': {df[col].min():.2f}")
            elif "count" in question_lower or "how many" in question_lower:
                results.append(f"Count of '{col}': {df[col].count()}")

        if not results:
            # Default: return a general summary of all numeric columns
            summary = df[numeric_cols].describe().to_string()
            return f"General statistics:\n{summary}"

        return "\n".join(results)

    except Exception as e:
        return f"Error during analysis: {str(e)}"


def get_dataframe_info(df: pd.DataFrame) -> str:
    """
    Returns a summary of the DataFrame structure:
    column names, data types, and row count.
    Useful for giving the agent context about the data.
    """
    col_info = "\n".join(
        [f"  - {col} ({dtype})" for col, dtype in zip(df.columns, df.dtypes)]
    )
    return (
        f"The CSV file has {len(df)} rows and {len(df.columns)} columns:\n{col_info}"
    )


def save_report(session_log: list, output_path: str = "report.txt") -> str:
    """
    Saves the session question-answer log to a .txt file.
    Returns a confirmation message with the file path.
    """
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("CSV DATA ANALYST AGENT - SESSION REPORT\n")
            f.write("=" * 50 + "\n\n")
            for i, entry in enumerate(session_log, 1):
                f.write(f"Q{i}: {entry['question']}\n")
                f.write(f"A{i}: {entry['answer']}\n")
                f.write("-" * 40 + "\n")
        return f"Report saved to: {output_path}"
    except Exception as e:
        return f"Error saving report: {str(e)}"
