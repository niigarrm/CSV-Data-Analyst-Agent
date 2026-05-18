# Project Journal

## Step 1 – 24.04

**Date:** 24.04.2025  
**Status:** Planning phase begun

### What I planned today

I decided to build a CSV Data Analyst Agent as my project. The system will allow non-technical users to upload a CSV file and ask natural language questions about the data. The agent will use the Claude API to interpret questions, call the appropriate analysis tools, and return a structured answer.

### Why I chose this idea

I chose this project because it clearly satisfies all task requirements — it has a real user problem, uses an AI agent, requires multiple tools, and has testable, measurable outcomes. It is also practical enough to fully implement within the given timeline.

### AI approach decision

I decided to use a single-agent approach rather than a multi-agent system. For this problem, one agent coordinating multiple tools is simpler, easier to test, and sufficient to demonstrate agent-based logic.

### Tools I plan to use

- **File Reader** — to load and validate CSV files
- **Statistical Analysis Module** — to perform calculations using `pandas`
- **Report Writer** — to save results to a `.txt` file
- **Claude API** — to interpret user questions and coordinate tool calls

### Programming concepts I will need

- Modular Python project structure
- CSV parsing and data manipulation with `pandas`
- Claude API integration and tool-calling logic
- Input validation and error handling
- Testing with `pytest`
- Environment variable management with `python-dotenv`

## Step 2 – 08.05

**Date:** 08.05.2025  
**Status:** Implementation in progress

### Updated Description of the System

The system is a command-line AI agent that allows users to load a CSV file 
and ask natural language questions about the data. Since Step 1, the 
description has been refined based on actual implementation progress.

The system is now structured into three clearly separated modules:

- `main.py` — entry point, handles user input and output loop
- `agent.py` — contains the Claude API integration and reasoning logic
- `tools.py` — contains all tool functions the agent can call

The user launches the program from the terminal, provides a path to a CSV 
file, and then types questions in plain English. The agent processes each 
question, selects the appropriate tool, executes it, and returns the result. 
A final summary report can be saved to a `.txt` file at the end of the session.

---

### Refined List of Programming Concepts Actually Used

- **Modular project structure** — the project is split into `main.py`, 
  `agent.py`, and `tools.py` with clear responsibilities
- **CSV parsing with `pandas`** — used to load, validate, and query 
  tabular data
- **API integration** — the Anthropic Claude API is called via HTTP 
  using the `anthropic` Python library
- **Tool-calling / function-calling pattern** — the agent decides which 
  tool function to invoke based on the user's question
- **Input validation** — the system checks whether the uploaded file 
  exists, is a valid CSV, and is non-empty before processing
- **Error handling with try/except** — all tool calls and API calls are 
  wrapped in error handlers to prevent crashes
- **Environment variables** — the Claude API key is stored in a `.env` 
  file and loaded with `python-dotenv`
- **File I/O** — the report writer saves analysis results to a `.txt` 
  file using Python's built-in `open()` function
- **Unit testing with `pytest`** — individual tool functions are tested 
  with sample CSV data to verify correct output

---

### How These Concepts Are Applied in the Project

**Modular structure** keeps each part of the system independent. For 
example, `tools.py` can be tested on its own without needing the agent 
or the API to be running.

**Pandas** is used inside the analysis tool functions. When the user asks 
"What is the average value of column X?", the agent calls the 
`calculate_statistics()` function, which uses `pandas` to compute and 
return the result.

**Tool-calling logic** works by passing the user's question to the Claude 
API along with a description of available tools. The model returns which 
tool to call and with what parameters. The agent then executes that tool 
locally and passes the result back to the model for formatting.

**Error handling** is applied at two levels — if a tool fails (e.g. the 
column name does not exist in the CSV), the agent catches the error and 
returns a helpful message to the user instead of crashing.

**Environment variables** ensure the API key is never hardcoded in the 
source files, which is important for safe GitHub usage.

---

### How Tools Are Integrated into the System

The system currently uses four tools, all defined in `tools.py`:

**1. File Reader**  
- Triggered at startup when the user provides a CSV file path  
- Uses `pandas.read_csv()` to load the file  
- Validates that the file exists and contains data  
- Returns a `pandas` DataFrame passed to all other tools  

**2. Statistical Analysis Module**  
- Triggered when the agent identifies a calculation-type question  
- Accepts the DataFrame and a column name as input  
- Performs operations such as mean, sum, max, min, and groupby  
- Returns a formatted string result to the agent  

**3. Report Writer**  
- Triggered at the end of the session when the user requests a summary  
- Accepts a list of question-answer pairs from the session  
- Writes them to a `.txt` file using Python's `open()` function  
- Returns a confirmation message with the file path  

**4. Claude API**  
- Called in `agent.py` on every user question  
- Receives the user's question and the list of available tools  
- Returns a tool selection decision or a direct text response  
- All calls are wrapped in error handling with retry logic


## Step 3 – 17.05

**Date:** 17.05.2025  
**Status:** Testing and deployment preparation

### Description of the Testing Process

As stated in the project requirements, testing was performed in parallel
with implementation rather than at the end of the project. As each tool
function was added to `tools.py` during Step 2, a corresponding unit test
was written in `tests/test_tools.py` using the `pytest` framework.

The testing process covers three layers, each mapping to a specific part
of the architecture defined in Step 2:

1. **Unit testing** — each tool function (`load_csv`, `calculate_statistics`,
   `get_dataframe_info`, `save_report`) is tested independently with
   controlled input data. This isolates the deterministic logic from the
   non-deterministic Claude API responses.
2. **Input validation testing** — invalid inputs such as missing files,
   empty CSVs, and unsupported question types are tested to confirm the
   system fails gracefully, as promised in the error handling design.
3. **Functional testing** — the full workflow (`main.py` → `agent.py` →
   `tools.py`) is tested manually with sample CSV files within the defined
   project scope (up to 10 MB, 100,000 rows, 50 columns) to confirm the
   end-to-end user experience works as intended.

All automated tests run from the project root with:
