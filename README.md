# auto_comment

A simple Python tool that adds Excel header comments from a flat file (`CSV` or `XLSX`).

It is designed for non-technical users: run one command, answer prompts, and get an output file.

## Important behavior

- `CSV` files cannot store hover comments.
- The output is always `.xlsx` so users can hover header cells to read comments.
- The tool does **not** create a new `comment` column.

## Features

- Supports input files: `.csv`, `.xlsx`
- Normalizes headers automatically:
  - trims spaces
  - lowercases text
  - removes internal spaces
  - example: ` Sales Amount ` -> `salesamount`
- Lets you define one header comment per column
- Writes output as `.xlsx` with Excel comments attached to header cells
- Logs execution details to a file

## 1) Create virtual environment

```bash
cd auto_comment
uv venv
```

## 2) Activate virtual environment

Linux/macOS:

```bash
source .venv/bin/activate
```

Windows (PowerShell):

```powershell
.venv\Scripts\Activate.ps1
```

## 3) Install dependencies

```bash
uv pip install --python .venv/bin/python -r requirements.txt
```

## 4) Run the app

```bash
python main.py
```

## How it works

1. Enter input file path (`.csv` or `.xlsx`).
2. The app normalizes headers.
3. Enter a header comment for each column.
4. The app writes an `.xlsx` output file.
5. Open output file and hover the header cells to read comments.

If you leave a comment blank for a column, that column is skipped.

## Logging

The app writes logs to `auto_comment.log` by default.

Log format:

```text
timestamp-log level: content
```

Actual pattern used:

```text
YYYY-MM-DD HH:MM:SS-LEVEL: message
```

Example:

```text
2026-04-22 15:10:44-INFO: Application started
```

### Custom log file path

Set environment variable `AUTO_COMMENT_LOG_FILE` before running:

```bash
AUTO_COMMENT_LOG_FILE=logs/run.log python main.py
```

## Run tests

```bash
pytest -q
```
