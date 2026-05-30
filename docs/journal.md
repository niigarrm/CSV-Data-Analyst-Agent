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
---

### List and Explanation of Test Scenarios

The test scenarios were chosen to cover both the **happy path** (typical
use by the target users described in Step 1) and **edge cases** that real
non-technical users are likely to trigger.

**Scenario 1 — Loading a valid CSV file**  
Input: Path to `sales.csv` with columns `product`, `region`, `revenue`, `date`.  
Expected result: A `pandas` DataFrame with 4 columns is returned.  
Verifies: `load_csv()` works correctly under normal conditions.

**Scenario 2 — Loading a non-existent file**  
Input: A path that does not exist on the filesystem.  
Expected result: `FileNotFoundError` raised with the message `"File not found: <path>"`.  
Verifies: Input validation prevents the system from crashing when a user
mistypes a file path.

**Scenario 3 — Loading an empty CSV**  
Input: A valid path pointing to an empty CSV file.  
Expected result: `ValueError` raised with the message `"The CSV file is empty."`.  
Verifies: The system handles edge cases where the file exists but contains
no usable data.

**Scenario 4 — Calculating the average of a numeric column**  
Input: A DataFrame with a `revenue` column and the question
*"What is the average revenue?"*.  
Expected result: A string containing the correctly calculated mean
(e.g. `"Average of 'revenue': 45200.00"`).  
Verifies: The statistical analysis tool produces mathematically accurate
results — directly enforcing the project's promise that the AI never
performs the maths itself.

**Scenario 5 — Asking about a non-numeric column**  
Input: A DataFrame with only string columns and the question
*"What is the average?"*.  
Expected result: The string `"No numeric columns found in the CSV file."`.  
Verifies: The tool handles edge cases gracefully and provides helpful
feedback rather than crashing.

**Scenario 6 — Saving a session report**  
Input: A list of three question-answer pairs and the output path `report.txt`.  
Expected result: A `.txt` file is created with all questions and answers
formatted correctly, and the function returns `"Report saved to: report.txt"`.  
Verifies: The report writer tool functions correctly and provides the
session record promised in the project goal.

**Scenario 7 — End-to-end functional test**  
Input: A real `sales.csv` file loaded through `main.py`, with the user
asking the worked example question: *"Which region brought in the most
money last quarter?"*.  
Expected result: The agent calls `calculate_statistics()`, receives the
result, and returns a clear natural-language answer through the Claude API.  
Verifies: The full agent loop (the six-step decision process described in
Step 2) works correctly end-to-end.

---

### Deployment Preparation

The system is designed as a **local command-line tool**, which is the
most appropriate deployment model for the target users (students, small
business owners, researchers, and junior analysts). It avoids the
complexity of hosting a web service while still being installable on any
machine with Python 3.10 or higher.

Another user can install and run the system by following these steps:

1. **Clone the repository** from GitHub
2. **Install dependencies**: `pip install -r requirements.txt`
3. **Configure the API key**: copy `.env.example` to `.env` and replace
   the placeholder with a valid Anthropic API key
4. **Run the program**: `python src/main.py`

All dependencies (`anthropic`, `pandas`, `python-dotenv`, `pytest`) are
listed in `requirements.txt`. The API key is loaded from the `.env` file
using `python-dotenv` so that no sensitive credentials are hardcoded into
the source code. The `.gitignore` file excludes the `.env` file from
version control, preventing accidental key leaks.

For future production deployment, this system could be packaged as:

- A **PyPI package** for easier installation via `pip install csv-analyst-agent`
- A **Docker container** for fully reproducible environments
- A **web service** using FastAPI if multiple users need simultaneous access,
  although this would require additional work on session management and
  authentication

A **staged release** approach is recommended: internal testing with
sample CSVs first, then a limited release to a small group of target
users for feedback, and finally a wider public release once edge cases
discovered during real use have been addressed.

---

### Data Conversion and Porting

The system handles data conversion at four points to ensure correctness
and consistency between components. Each conversion step corresponds to
a boundary between the tools described in Step 2.

**1. CSV file → `pandas` DataFrame**  
The input data starts as a raw CSV file on disk in standard tabular format
with a header row. The `load_csv()` function uses `pandas.read_csv()` to
parse the file into a structured DataFrame, which becomes the unified
internal data format used by all other tools. `pandas` automatically
infers column data types (numeric, string, date, boolean) so subsequent
tools can rely on consistent typing.

**2. DataFrame → analysis result string**  
When the statistical analysis tool runs, it converts numeric DataFrame
results into formatted strings (e.g. `f"Average of 'revenue': {value:.2f}"`)
so they can be embedded into the prompt sent to the Claude API as plain
text. This conversion is necessary because the Claude API only accepts
text input, not raw `pandas` objects.

**3. Claude API JSON response → final user output**  
The Claude API returns responses as structured JSON objects (as shown in
the tools section of Step 1). The agent extracts the `.content[0].text`
field to obtain a clean string, which is then displayed in the terminal.
The other fields in the response (`id`, `model`, `usage`, `stop_reason`)
are metadata and are discarded for user-facing output.

**4. Session log (list of dicts) → text report file**  
At the end of a session, the in-memory list of question-answer
dictionaries accumulated in `agent.py` is converted into formatted plain
text by `save_report()` and written to a `.txt` file using Python's
built-in `open()` function.

At each conversion step, data integrity is preserved through type
validation and error handling. For example, if a numeric column contains
unexpected non-numeric values, `pandas` handles the conversion safely
and the tool reports the issue rather than crashing. This consistent
approach to data conversion is what allows the system to deliver the
accurate, reliable insights promised in Step 1.


## Final Submission – 22.05

**Date:** 22.05.2025  
**Status:** Project complete

### Final System Description and Goal

The completed system is the **CSV Data Analyst Agent** — a Python-based 
command-line application that allows non-technical users to load a CSV 
file and ask natural language questions about its contents. The system 
combines the natural language understanding of the Anthropic Claude API 
with the deterministic numerical accuracy of `pandas`, ensuring that the 
AI never performs calculations itself but instead paraphrases verified 
results from local tools.

The final implementation meets the original project goal: any user can 
receive an accurate, human-readable answer about their CSV data within 
seconds, with zero programming knowledge required. The scope was 
deliberately kept to small and medium-sized CSV files (up to 10 MB, 
100,000 rows, and 50 columns) so the entire dataset can be held in 
memory and analysed quickly.

### Final Explanation of Programming Concepts and Their Usage

The final implementation uses eight programming concepts, each applied 
to a specific part of the system:

- **Modular project structure** — four clearly separated modules: 
  `cli_entry_point.py`, `ai_orchestrator.py`, `tool_module.py`, and 
  `config_manager.py`. Each module has a single, well-defined 
  responsibility, which made testing and debugging significantly easier 
  during development.
- **CSV parsing and data manipulation** — handled entirely by `pandas`, 
  which performs all numerical work (mean, sum, max, min, count, 
  describe, groupby) inside `tool_module.py`.
- **API integration** — handled by the `anthropic` SDK in 
  `ai_orchestrator.py`, with all calls wrapped in error handlers for 
  network, authentication, and rate-limit failures.
- **Tool-calling pattern** — implemented as the six-step agent loop 
  in `ask_agent()`, which coordinates metadata extraction, local 
  analysis, prompt construction, API call, response extraction, and 
  session logging.
- **Input validation** — applied at three boundaries: file path 
  validation in `cli_entry_point.py`, file existence and emptiness 
  checks in `load_csv()`, and numeric-column checks in 
  `calculate_statistics()`.
- **Error handling** — every external interaction (file I/O, API calls, 
  pandas parsing) is wrapped in `try`/`except` blocks that convert 
  exceptions into user-friendly strings instead of stack traces.
- **Environment variable management** — centralised in 
  `config_manager.py`, which uses `python-dotenv` to load the API key 
  from `.env` and validates its presence at startup.
- **Unit testing** — `pytest` is used in `tests/test_tools.py` to verify 
  each tool function independently with controlled input data.

### Final Description of Tools and Their Role

The final system uses four tools, all coordinated by the agent loop:

1. **File Reader (`load_csv`)** — Loads and validates the CSV file, 
   returning a `pandas.DataFrame` that all other tools operate on. 
   Enforces the project scope (file size, row count, column count) at 
   load time.
2. **Statistical Analysis Module (`calculate_statistics`)** — Performs 
   all numerical operations using `pandas` and returns results as 
   formatted strings ready for inclusion in the Claude prompt.
3. **DataFrame Metadata Helper (`get_dataframe_info`)** — Produces the 
   structural summary of the loaded data (columns, types, row count) 
   that is sent to Claude on every question so the model can reason 
   about the data without seeing the full contents.
4. **Report Writer (`save_report`)** — Serialises the session log to a 
   plain text file on demand, allowing the user to keep a permanent 
   record of the analysis.

In addition, the **Claude API** acts as the reasoning engine that 
interprets questions, coordinates the tool calls, and explains the 
results in plain English.

### Final Testing Results and Conclusions

The full test suite in `tests/test_tools.py` was executed before 
submission. All **11 unit tests pass** in under one second, covering:

- Valid CSV loading (1 test)
- File not found and empty CSV handling (3 tests)
- Statistical calculations: average, sum, max (3 tests)
- Edge cases: no numeric columns (1 test)
- Session report saving (2 tests)
- DataFrame metadata helper (1 test)

**Functional testing** of the end-to-end workflow was performed 
manually with several sample CSV files (a sales dataset, a student 
grades dataset, and a small inventory file). In every case, the agent 
correctly identified the intent of the question, called the appropriate 
tool, and returned a coherent natural language answer.

**Conclusions:**

- The separation between deterministic tools and the AI reasoning layer 
  proved to be the most valuable design decision. It made testing 
  straightforward (the tools can be tested without any API calls) and 
  guaranteed mathematical accuracy.
- Keyword-based intent matching in `calculate_statistics()` works well 
  for the common cases targeted by the project but could be extended 
  in the future with a more sophisticated tool-use mechanism (e.g. the 
  Anthropic SDK's native tool-use API).
- Error handling consistently prevented crashes during testing — every 
  invalid input produced a clear message instead of a traceback.
- The local CLI delivery model proved to be the right choice for the 
  target users: simple to install, fast to run, and requiring no 
  hosting infrastructure.

### Final Deployment Preparation

The project is fully prepared for controlled deployment by another 
user. The repository contains:

- `requirements.txt` listing all four dependencies (`anthropic`, 
  `pandas`, `python-dotenv`, `pytest`)
- `.env.example` showing the required environment variable
- `.gitignore` preventing the real `.env` file from being committed
- `README.md` with complete installation and usage instructions

A new user can run the system in four steps:

1. `git clone <repository-url>`
2. `pip install -r requirements.txt`
3. `cp .env.example .env` and add a valid Anthropic API key
4. `python src/cli_entry_point.py`

### Chosen Deployment Strategy

The chosen deployment strategy is a **local command-line tool with 
staged release**. This was selected over a hosted web service for 
three reasons:

1. **User profile** — the target users (students, small business 
   owners, junior analysts) work with their own private data and 
   prefer not to upload it to third-party servers.
2. **Simplicity** — a local tool requires no hosting, no 
   authentication system, no database, and no scaling considerations.
3. **Cost** — each user pays only for their own Claude API usage 
   through their own key, avoiding centralised cost management.

For future production deployment, a staged approach is recommended:

- **Stage 1** — Internal testing with a small set of sample CSVs 
  (already complete via `pytest`).
- **Stage 2** — Limited release to a small group of target users for 
  real-world feedback on edge cases the test suite did not catch.
- **Stage 3** — Public release on PyPI as `pip install csv-analyst-agent`, 
  with optional packaging as a Docker container for users in 
  controlled environments.

A web service deployment using FastAPI was considered but rejected at 
this stage, as it would introduce session management, authentication, 
and data privacy complexity disproportionate to the project's current 
scope.
