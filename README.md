# auto_comment

`auto_comment` is a simple Python CLI that reads a flat file (`.csv` or `.xlsx`) and writes an Excel file (`.xlsx`) with comments attached to header cells.

Users can open the output file in Excel and hover each header cell to read its comment.

## Key behavior

- Input: `.csv` or `.xlsx`
- Output: always `.xlsx`
- No extra `comment` column is created
- Header names are normalized before processing:
  - trim spaces
  - lowercase
  - remove internal spaces
  - example: ` Sales Amount ` -> `salesamount`

## Why output is always XLSX

CSV format does not support Excel-style cell comments. To support hover comments, the tool writes `.xlsx` output.

## Setup

```bash
cd auto_comment
uv venv
source .venv/bin/activate
uv pip install --python .venv/bin/python -r requirements.txt
```

Windows (PowerShell):

```powershell
cd auto_comment
uv venv
.venv\Scripts\Activate.ps1
uv pip install --python .venv\Scripts\python.exe -r requirements.txt
```

## Run

```bash
python main.py
```

## Runtime flow

1. Enter input file path (`.csv` or `.xlsx`).
2. Review normalized headers shown by the app.
3. Enter header comment text for each column (leave blank to skip).
4. Enter output file path (`.xlsx`).
5. Open output in Excel and hover header cells.

## Logging

Default log file: `auto_comment.log`

Log format:

```text
timestamp-log level: content
```

Implemented pattern:

```text
YYYY-MM-DD HH:MM:SS-LEVEL: message
```

Example:

```text
2026-04-22 15:10:44-INFO: Application started
```

Use a custom log path:

```bash
AUTO_COMMENT_LOG_FILE=logs/run.log python main.py
```

## Run tests

```bash
pytest -q
```
