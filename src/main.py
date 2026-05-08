import os
from dotenv import load_dotenv
from tools import load_csv
from agent import ask_agent, handle_save_report

# Load environment variables from .env file
load_dotenv()


def main():
    """
    Main entry point for the CSV Data Analyst Agent.
    Handles the user input loop and coordinates agent responses.
    """
    print("=" * 50)
    print("   CSV DATA ANALYST AGENT")
    print("=" * 50)
    print("Type 'save' to save a report, or 'quit' to exit.\n")

    # Step 1: Ask user for CSV file path
    while True:
        file_path = input("Enter the path to your CSV file: ").strip()
        try:
            df = load_csv(file_path)
            print(f"\nFile loaded successfully! ({len(df)} rows, {len(df.columns)} columns)")
            print(f"Columns: {', '.join(df.columns.tolist())}\n")
            break
        except FileNotFoundError as e:
            print(f"Error: {e}. Please try again.")
        except ValueError as e:
            print(f"Error: {e}. Please try again.")
        except Exception as e:
            print(f"Unexpected error loading file: {e}. Please try again.")

    # Step 2: Start the question-answer loop
    session_log = []

    while True:
        question = input("Ask a question about your data: ").strip()

        if not question:
            print("Please enter a question.\n")
            continue

        if question.lower() == "quit":
            print("Goodbye!")
            break

        if question.lower() == "save":
            result = handle_save_report(session_log)
            print(f"\n{result}\n")
            continue

        # Send the question to the agent
        print("\nAnalysing...\n")
        answer = ask_agent(question, df, session_log)
        print(f"Answer: {answer}\n")
        print("-" * 50)


if __name__ == "__main__":
    # Check that the API key is set before starting
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY not found.")
        print("Please create a .env file with your API key.")
        print("Example: ANTHROPIC_API_KEY=your-key-here")
    else:
        main()
