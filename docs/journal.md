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
