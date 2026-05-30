# CSV Data Analyst Agent

An AI-powered command-line tool that lets you ask questions about CSV
files in plain English — no programming required.

Built as a single intelligent agent that combines the natural language
understanding of the **Anthropic Claude API** with the deterministic
numerical accuracy of **pandas**. The AI interprets questions and
explains results, but never performs calculations itself: every number
the user sees comes directly from `pandas`.

---

## Features

- Ask questions about your CSV in plain English (e.g. *"Which region
  brought in the most money last quarter?"*)
- Automatic statistical analysis: mean, sum, max, min, count,
  groupby-style summaries, and full `describe()` fallback
- Session report writer — save your entire question/answer history
  to a `.txt` file
- Graceful error handling: missing files, empty CSVs, invalid API
  keys, and network failures all return clear messages instead of
  crashes

---

## Project Scope

Designed for small and medium-sized CSV files:

- Up to ~10 MB in size
- Up to ~100,000 rows
- Up to ~50 columns
- Standard tabular CSV with a header row
- Mixed data types supported (numeric, text, dates, boolean)

---

## Project Structure

```
csv-analyst-agent/
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
│
├── src/
│   ├── cli_entry_point.py     # Module 1 — CLI and command parsing
│   ├── ai_orchestrator.py     # Module 2 — Claude API integration
│   ├── tool_module.py         # Module 3 — pandas-based tools
│   └── config_manager.py      # Module 4 — environment configuration
│
├── tests/
│   └── test_tools.py          # Unit tests for the tool functions
│
└── docs/
    └── journal.md             # Development journal (all stages)
```

---

## Installation

### Prerequisites

- Python 3.10 or higher
- An Anthropic API key — get one at https://console.anthropic.com/

### Setup

```bash
# 1. Clone the repository
git clone <your-repository-url>
cd csv-analyst-agent

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure your API key
cp .env.example .env
# Then open .env and replace 'your-api-key-here' with your real key
```

---

## Usage

Run the program from the project root:

```bash
python src/cli_entry_point.py
```

You will be prompted for the path to your CSV file. Once it loads, you
can start asking questions:

```
==================================================
   CSV DATA ANALYST AGENT
==================================================
Ask questions about your CSV file in plain English.
Type 'save' to save a session report.
Type 'quit' to exit.

Enter the path to your CSV file: data/sales.csv

File loaded successfully! (1500 rows, 4 columns)
Columns: product, region, revenue, date

Ask a question about your data: What is the average revenue?

Analysing...

Answer: The average revenue across all 1,500 transactions is €312.47.
--------------------------------------------------
Ask a question about your data: save

Report saved to: report.txt
```

### Commands

| Command | What it does |
|---|---|
| Any question in plain English | Asks the agent to analyse your data |
| `save` | Saves the session history to `report.txt` |
| `quit` | Exits the program |

---

## Configuration

All configuration is handled through a single `.env` file in the
project root:

```
ANTHROPIC_API_KEY=your-api-key-here
```

The `.env` file is excluded from version control by `.gitignore` —
your API key will never be accidentally committed to GitHub.

---

## Running the Tests

```bash
pytest tests/
```

The test suite covers:

- Valid CSV loading
- File not found and empty CSV handling
- Statistical calculations (mean, sum, max)
- Edge cases (no numeric columns)
- Session report saving
- DataFrame metadata helper

---

## How It Works

The system uses a **single intelligent agent** that follows a six-step
reasoning loop on every question:

1. **Extract metadata** — column names, types, and row count are
   gathered from the loaded DataFrame.
2. **Run local analysis** — `pandas` computes the actual numbers
   (mean, sum, max, etc.).
3. **Build the prompt** — metadata, question, and analysis result are
   combined into a single message.
4. **Call the Claude API** — the message is sent to Claude with a
   system prompt instructing it to act as a data analyst.
5. **Extract the answer** — the natural language response is pulled
   from the API's JSON output.
6. **Log the session** — the question and answer are stored in memory
   for the optional report writer.

This design guarantees mathematical accuracy: the AI never calculates
anything itself, it only paraphrases verified results from `pandas`.

---

## Dependencies

| Library | Purpose |
|---|---|
| `anthropic` | Claude API client |
| `pandas` | CSV parsing and data manipulation |
| `python-dotenv` | Loads the API key from `.env` |
| `pytest` | Unit testing framework |

---

## Documentation

See `docs/journal.md` for the full development journal, including the
design decisions, testing scenarios, and deployment strategy.

---

## License

This project was developed as a university assignment. Use freely
for educational purposes.
