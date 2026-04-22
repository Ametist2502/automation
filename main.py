from __future__ import annotations

import csv
from pathlib import Path


def read_csv_with_fallback(file_path: Path) -> tuple[list[str], list[dict[str, str]], str]:
    encodings = ["utf-8-sig", "utf-8", "cp1258", "latin-1"]

    last_error: Exception | None = None
    for encoding in encodings:
        try:
            with file_path.open("r", newline="", encoding=encoding) as f:
                reader = csv.DictReader(f)
                if not reader.fieldnames:
                    raise ValueError("Khong tim thay tieu de cot (header) trong file CSV.")

                rows = list(reader)
                return reader.fieldnames, rows, encoding
        except Exception as err:  # noqa: BLE001
            last_error = err

    raise RuntimeError(f"Khong doc duoc file CSV. Loi cuoi: {last_error}")


def ask_input(prompt: str, default: str | None = None) -> str:
    if default:
        raw = input(f"{prompt} [{default}]: ").strip()
        return raw or default

    return input(f"{prompt}: ").strip()


def choose_column(columns: list[str]) -> str:
    print("\nDanh sach cot hien co:")
    for idx, col in enumerate(columns, start=1):
        print(f"  {idx}. {col}")

    while True:
        selected = ask_input("Nhap so thu tu cot de tao comment", "1")
        if selected.isdigit():
            index = int(selected) - 1
            if 0 <= index < len(columns):
                return columns[index]

        print("Lua chon khong hop le. Vui long nhap lai.")


def build_comment(value: str, row_number: int, template: str) -> str:
    return template.format(value=value, row_number=row_number)


def main() -> None:
    print("=== AUTO COMMENT CSV ===")

    input_path_raw = ask_input("Nhap duong dan file CSV dau vao", "input.csv")
    input_path = Path(input_path_raw)

    if not input_path.exists() or not input_path.is_file():
        print(f"Khong tim thay file: {input_path}")
        return

    try:
        columns, rows, source_encoding = read_csv_with_fallback(input_path)
    except Exception as err:  # noqa: BLE001
        print(f"Loi khi doc file CSV: {err}")
        return

    if not rows:
        print("File CSV khong co dong du lieu nao.")
        return

    base_column = choose_column(columns)
    comment_column = ask_input("Ten cot comment moi", "comment")

    template = ask_input(
        "Mau comment (dung {value} cho gia tri cot, {row_number} cho so dong)",
        "Dong {row_number}: da ghi nhan '{value}'.",
    )

    default_output = f"{input_path.stem}_commented.csv"
    output_path = Path(ask_input("Duong dan file CSV dau ra", default_output))

    if comment_column not in columns:
        columns.append(comment_column)

    for i, row in enumerate(rows, start=1):
        value = (row.get(base_column) or "").strip()
        row[comment_column] = build_comment(value=value, row_number=i, template=template)

    try:
        with output_path.open("w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=columns)
            writer.writeheader()
            writer.writerows(rows)
    except Exception as err:  # noqa: BLE001
        print(f"Loi khi ghi file CSV: {err}")
        return

    print("\nHoan tat!")
    print(f"- Da doc: {input_path} (encoding: {source_encoding})")
    print(f"- Da ghi: {output_path}")
    print(f"- So dong da tao comment: {len(rows)}")


if __name__ == "__main__":
    main()
