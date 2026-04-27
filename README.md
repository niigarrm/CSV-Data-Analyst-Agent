# CSV Data Analyst Agent

## Project Description
The planned system is an AI-powered CSV Data Analyst Agent for non-technical users — such as students, analysts, and small business owners — who need to extract insights from tabular data without writing code. The user provides a CSV file and asks natural language questions such as "Which product category had the highest total revenue?" or "What is the average order value per month?". The agent analyses the data using Python-based tools and returns a structured, human-readable answer along with a generated summary report saved to a file.
The measurable goal of the system is to allow any user to receive accurate statistical insights from a CSV file within under 10 seconds, with zero programming knowledge required.

## AI / Agent Approach
The system uses a single intelligent agent powered by the Claude API (Anthropic). The agent follows a structured reasoning loop:

Parse intent — interpret the user's natural language question
Select tool — decide whether to use the file reader, statistical calculator, or report writer
Execute tool — run the selected tool and retrieve the result
Format output — return a clear, structured answer to the user

If a tool returns an error or the question is ambiguous, the agent asks the user for clarification rather than guessing.

## Tools Used
| Tool | Purpose |
|---|---|
| **File Reader** | Loads and validates the uploaded CSV file using `pandas` |
| **Statistical Analysis Module** | Performs calculations: mean, sum, max, min, groupby, trend detection |
| **Report Writer** | Saves a structured `.txt` summary of the analysis results |
| **Claude API** | Interprets questions, selects tools, and formats the final response |


## Programming Concepts

- Python project structuring and modular design
- File I/O and CSV parsing with `pandas`
- API integration and prompt engineering (Anthropic Claude API)
- Agent reasoning loop and tool-calling logic
- Input validation and error handling
- Unit and integration testing with `pytest`
- Environment variable management with `python-dotenv`
- Dependency management with `requirements.txt`
