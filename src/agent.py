import anthropic
import pandas as pd

from tool_module import (
    calculate_statistics,
    get_dataframe_info,
    save_report,
)


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
MODEL_NAME = "claude-opus-4-6"
MAX_TOKENS = 1024

SYSTEM_PROMPT = """You are a helpful data analyst assistant.
You have access to a CSV file loaded by the user.

When the user asks a question about the data, you will receive:
  1. A description of the CSV structure (columns, types, row count).
  2. The user's question in plain English.
  3. The result of a statistical analysis tool run on the data.

Your job is to explain the analysis result clearly and concisely in
plain English. Never perform calculations yourself — always trust the
tool result. If the question is unclear or the tool result is empty,
ask the user for clarification rather than guessing."""


# ---------------------------------------------------------------------------
# Client initialisation
# ---------------------------------------------------------------------------
# The anthropic client reads ANTHROPIC_API_KEY from the environment.
# The key is loaded by python-dotenv in the CLI entry point before this
# module is used.
client = anthropic.Anthropic()


# ---------------------------------------------------------------------------
# Prompt construction
# ---------------------------------------------------------------------------
def build_user_message(question: str, df: pd.DataFrame, analysis_result: str) -> str:
    """
    Builds the single user message that is sent to the Claude API on every
    question. Combines the DataFrame metadata, the original question, and
    the result of the local statistical analysis.
    """
    data_info = get_dataframe_info(df)

    return (
        f"The user has loaded a CSV file with the following structure:\n"
        f"{data_info}\n\n"
        f"The user asks: \"{question}\"\n\n"
        f"Here is the result from the statistical analysis tool:\n"
        f"{analysis_result}\n\n"
        f"Please explain this result clearly to the user in plain English."
    )


# ---------------------------------------------------------------------------
# Claude API call with error handling
# ---------------------------------------------------------------------------
def call_claude_api(user_message: str) -> str:
    """
    Sends a single request to the Claude API and returns the plain text
    answer extracted from the JSON response. Translates any API exception
    into a user-friendly error string so the CLI never sees a stack trace.
    """
    try:
        response = client.messages.create(
            model=MODEL_NAME,
            max_tokens=MAX_TOKENS,
            system=SYSTEM_PROMPT,
            messages=[
                {"role": "user", "content": user_message},
            ],
        )

        # The response is a structured JSON object. We only need the text
        # of the first content block. All other fields (id, model, usage,
        # stop_reason) are metadata and are discarded.
        return response.content[0].text

    except anthropic.APIConnectionError:
        return (
            "Error: Could not connect to the Claude API. "
            "Please check your internet connection and try again."
        )
    except anthropic.AuthenticationError:
        return (
            "Error: The Anthropic API key is invalid or missing. "
            "Please check your .env file."
        )
    except anthropic.RateLimitError:
        return (
            "Error: The Claude API rate limit has been reached. "
            "Please wait a moment and try again."
        )
    except anthropic.APIStatusError as e:
        return f"Error: The Claude API returned an error (status {e.status_code})."
    except Exception as e:
        return f"Unexpected error during API call: {str(e)}"


# ---------------------------------------------------------------------------
# Public interface — called by the CLI entry point
# ---------------------------------------------------------------------------
def ask_agent(question: str, df: pd.DataFrame, session_log: list) -> str:
    """
    Main agent function. Executes the full six-step agent loop:
        1. Extract DataFrame metadata.
        2. Run local statistical analysis on the question.
        3. Build the prompt.
        4. Call the Claude API.
        5. Extract the plain text answer.
        6. Append the question and answer to the session log.

    Returns the answer string to be displayed by the CLI.
    """
    # Step 1 & 2 — Metadata is added inside build_user_message;
    # analysis is performed by the tool module.
    analysis_result = calculate_statistics(df, question)

    # Step 3 — Construct the prompt for Claude.
    user_message = build_user_message(question, df, analysis_result)

    # Step 4 & 5 — Call the API and extract the answer.
    answer = call_claude_api(user_message)

    # Step 6 — Maintain the in-memory session log.
    session_log.append({"question": question, "answer": answer})

    return answer


def handle_save_report(session_log: list) -> str:
    """
    Delegates to the tool module's report writer. Returns a confirmation
    message to be displayed by the CLI, or a message if there is nothing
    to save.
    """
    if not session_log:
        return "No questions have been asked yet. Nothing to save."

    return save_report(session_log){analysis_result}

Please explain this result clearly to the user in plain English."""

        # Call the Claude API
        response = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=[
                {"role": "user", "content": user_message}
            ]
        )

        answer = response.content[0].text

        # Log the question and answer for the session report
        session_log.append({"question": question, "answer": answer})

        return answer

    except anthropic.APIConnectionError:
        return "Error: Could not connect to the Claude API. Please check your internet connection."
    except anthropic.AuthenticationError:
        return "Error: Invalid API key. Please check your .env file."
    except Exception as e:
        return f"Unexpected error: {str(e)}"


def handle_save_report(session_log: list) -> str:
    """
    Triggers the report writer tool to save the session log.
    """
    if not session_log:
        return "No questions have been asked yet. Nothing to save."
    return save_report(session_log)
