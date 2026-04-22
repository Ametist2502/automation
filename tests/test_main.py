from __future__ import annotations

import re
from pathlib import Path

import pytest
from openpyxl import load_workbook

from main import load_flat_file, main, normalize_header, normalize_headers


def test_normalize_header() -> None:
    assert normalize_header("  Sales Amount ") == "salesamount"


def test_normalize_headers_duplicate_raises() -> None:
    with pytest.raises(ValueError):
        normalize_headers(["Sale Amount", "saleamount"])


def test_load_flat_file_csv_normalize_header(tmp_path: Path) -> None:
    csv_file = tmp_path / "input.csv"
    csv_file.write_text("  Region Name , Sales Amount\nHN,120\n", encoding="utf-8-sig")

    columns, rows, source_info = load_flat_file(csv_file)

    assert columns == ["regionname", "salesamount"]
    assert rows == [{"regionname": "HN", "salesamount": "120"}]
    assert source_info in {"utf-8-sig", "utf-8"}


def test_main_csv_creates_xlsx_with_header_comments_and_log(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    input_file = tmp_path / "input.csv"
    input_file.write_text(
        " Region , Sales Amount\nHN,120\nHCM,200\n",
        encoding="utf-8",
    )

    output_file = tmp_path / "output.xlsx"
    log_file = tmp_path / "run.log"
    monkeypatch.setenv("AUTO_COMMENT_LOG_FILE", str(log_file))

    answers = iter(
        [
            str(input_file),
            "Region business meaning",
            "Sales business meaning",
            str(output_file),
        ]
    )

    monkeypatch.setattr("builtins.input", lambda _prompt: next(answers))

    main()

    out = capsys.readouterr().out
    assert "Completed!" in out
    assert output_file.exists()
    assert log_file.exists()

    wb_out = load_workbook(output_file)
    ws_out = wb_out.active

    headers = [cell.value for cell in next(ws_out.iter_rows(min_row=1, max_row=1))]
    assert headers == ["region", "salesamount"]
    assert ws_out.cell(row=1, column=1).comment is not None
    assert ws_out.cell(row=1, column=1).comment.text == "Region business meaning"
    assert ws_out.cell(row=1, column=2).comment is not None
    assert ws_out.cell(row=1, column=2).comment.text == "Sales business meaning"

    log_text = log_file.read_text(encoding="utf-8")
    assert "-INFO: Application started" in log_text
    first_line = log_text.splitlines()[0]
    assert re.match(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}-[A-Z]+: .+", first_line)


def test_main_xlsx_creates_output_with_header_comments(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    input_file = tmp_path / "input.xlsx"
    output_file = tmp_path / "output.xlsx"

    from openpyxl import Workbook

    wb = Workbook()
    ws = wb.active
    ws.append([" Product Name ", "Qty Sold"])
    ws.append(["Pen", 10])
    ws.append(["Book", 5])
    wb.save(input_file)

    answers = iter(
        [
            str(input_file),
            "Product description",
            "Quantity description",
            str(output_file),
        ]
    )

    monkeypatch.setattr("builtins.input", lambda _prompt: next(answers))

    main()

    out = capsys.readouterr().out
    assert "Completed!" in out
    assert output_file.exists()

    wb_out = load_workbook(output_file)
    ws_out = wb_out.active

    headers = [cell.value for cell in next(ws_out.iter_rows(min_row=1, max_row=1))]
    assert headers == ["productname", "qtysold"]

    assert ws_out.cell(row=1, column=1).comment is not None
    assert ws_out.cell(row=1, column=1).comment.text == "Product description"
    assert ws_out.cell(row=1, column=2).comment is not None
    assert ws_out.cell(row=1, column=2).comment.text == "Quantity description"
