import os
import sys
from dotenv import load_dotenv

from tool_module import load_csv
from ai_orchestrator import ask_agent, handle_save_report


# Constants

COMMAND_QUIT = "quit"
COMMAND_SAVE = "save"
BANNER_WIDTH = 50


# ---------------------------------------------------------------------------
# Startup helpers
# ---------------------------------------------------------------------------
def print_banner() -> None:
    """Prints the application banner and a short list of available commands."""
    print("=" * BANNER_WIDTH)
    print("   CSV DATA ANALYST AGENT")
    print("=" * BANNER_WIDTH)
    print("Ask questions about your CSV file in plain English.")
    print(f"Type '{COMMAND_SAVE}' to save a session report.")
    print(f"Type '{COMMAND_QUIT}' to exit.\n")


def verify_api_key() -> bool:
    """
    Checks that the ANTHROPIC_API_KEY environment variable is set.
    Returns True if the key is present, False otherwise.
    """
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY not found.")
        print("Please create a .env file in the project root with:")
        print("    ANTHROPIC_API_KEY=your-key-here")
        print("You can get your key from: https://console.anthropic.com/")
        return False
    return True


# ---------------------------------------------------------------------------
# Phase 2 — CSV ingestion
# ---------------------------------------------------------------------------
def prompt_for_csv():
    """
    Prompts the user for a CSV file path and attempts to load it.
    Re-prompts on any error until a valid CSV is supplied.
    Returns the loaded pandas DataFrame on success.
    """
    while True:
        file_path = input("Enter the path to your CSV file: ").strip()

        if not file_path:
            print("Please enter a file path.\n")
            continue

        try:
            df = load_csv(file_path)
            print(
                f"\nFile loaded successfully! "
                f"({len(df)} rows, {len(df.columns)} columns)"
            )
            print(f"Columns: {', '.join(df.columns.tolist())}\n")
            return df

        except FileNotFoundError as e:
            print(f"Error: {e}. Please try again.\n")
        except ValueError as e:
            print(f"Error: {e}. Please try again.\n")
        except Exception as e:
            print(f"Unexpected error loading file: {e}. Please try again.\n")


# ---------------------------------------------------------------------------
# Phase 3 — Interactive question loop
# ---------------------------------------------------------------------------
def route_command(user_input: str, df, session_log: list) -> bool:
    """
    Routes a single line of user input to the appropriate handler.

    Returns:
        True if the loop should continue, False if the user requested to quit.
    """
    command = user_input.strip()

    # Empty input — re-prompt
    if not command:
        print("Please enter a question.\n")
        return True

    # Quit command
    if command.lower() == COMMAND_QUIT:
        print("Goodbye!")
        return False

    # Save command
    if command.lower() == COMMAND_SAVE:
        result = handle_save_report(session_log)
        print(f"\n{result}\n")
        return True

    # Default — treat as a natural language question
    print("\nAnalysing...\n")
    answer = ask_agent(command, df, session_log)
    print(f"Answer: {answer}\n")
    print("-" * BANNER_WIDTH)
    return True


def run_interactive_loop(df) -> None:
    """
    Runs the main question-answer loop. Maintains an in-memory session log
    that is passed to the agent on every question and to the report writer
    on 'save'.
    """
    session_log = []

    while True:
        try:
            user_input = input("Ask a question about your data: ")
        except (EOFError, KeyboardInterrupt):
            # Allow Ctrl+C / Ctrl+D to exit cleanly
            print("\nGoodbye!")
            break

        should_continue = route_command(user_input, df, session_log)
        if not should_continue:
            break


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
def main() -> None:
    """Main entry point — coordinates the three phases of the application."""
    # Phase 1 — Startup and configuration
    load_dotenv()
    if not verify_api_key():
        sys.exit(1)

    print_banner()

    # Phase 2 — CSV ingestion
    df = prompt_for_csv()

    # Phase 3 — Interactive question loop
    run_interactive_loop(df)


if __name__ == "__main__":
    main()
    the process environment.

    This must be called once at application startup, before any other
    module attempts to read environment variables.

    If no .env file is found, python-dotenv fails silently — the function
    will not raise. In that case, any required variables must already be
    set in the actual process environment (e.g. via the shell), otherwise
    validate_api_key() will fail later.
    """
    load_dotenv()


# ---------------------------------------------------------------------------
# API key access
# ---------------------------------------------------------------------------
def get_api_key() -> Optional[str]:
    """
    Returns the ANTHROPIC_API_KEY value from the environment, or None if
    the variable is not set or is empty.

    Returns:
        The API key string, or None if the variable is missing or blank.
    """
    key = os.getenv(API_KEY_VAR)

    # Treat empty strings the same as missing keys
    if not key or not key.strip():
        return None

    return key


# ---------------------------------------------------------------------------
# Startup validation
# ---------------------------------------------------------------------------
def validate_api_key() -> bool:
    """
    Validates that the ANTHROPIC_API_KEY is set before the application
    attempts to call the Claude API.

    Prints a helpful setup message if the key is missing, so the user
    knows exactly what to do next.

    Returns:
        True if the key is present, False otherwise.
    """
    if get_api_key() is None:
        print(f"Error: {API_KEY_VAR} not found.")
        print("Please create a .env file in the project root with:")
        print(f"    {API_KEY_VAR}=your-key-here")
        print("You can get your key from: https://console.anthropic.com/")
        return False

    return True
