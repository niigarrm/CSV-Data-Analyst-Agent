import anthropic
import pandas as pd
from tools import calculate_statistics, get_dataframe_info, save_report

# Initialize the Anthropic client
client = anthropic.Anthropic()

# System prompt that instructs the agent how to behave
SYSTEM_PROMPT = """You are a helpful data analyst assistant. 
You have access to a CSV file loaded by the user.
When the user asks a question about the data, you will receive the 
result of a statistical analysis tool and must explain it clearly 
and concisely in plain English.
If the question is unclear, ask the user for clarification.
Always be concise and focus on what the data actually shows."""


def ask_agent(question: str, df: pd.DataFrame, session_log: list) -> str:
    """
    Sends the user's question to the Claude API along with relevant
    data context and tool results. Returns the agent's response.
    """
    try:
        # Get structural info about the dataframe
        data_info = get_dataframe_info(df)

        # Get statistical analysis result
        analysis_result = calculate_statistics(df, question)

        # Build the full message to send to Claude
        user_message = f"""The user has loaded a CSV file with the following structure:
{data_info}

The user asks: "{question}"

Here is the result from the statistical analysis tool:
{analysis_result}

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
