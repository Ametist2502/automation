# auto_comment

Script Python them cot `comment` tu dong cho flat file `CSV` hoac `XLSX`, huong toi nguoi dung non-tech.

## 1) Tao moi truong

```bash
cd auto_comment
uv venv
```

## 2) Kich hoat moi truong

Linux/macOS:
```bash
source .venv/bin/activate
```

Windows (PowerShell):
```powershell
.venv\Scripts\Activate.ps1
```

## 3) Cai dependency

```bash
uv pip install --python .venv/bin/python -r requirements.txt
```

## 4) Chay chuong trinh

```bash
python main.py
```

## Flow xu ly

1. Nhap file dau vao (`.csv` hoac `.xlsx`).
2. Script tu dong chuan hoa header:
- xoa khoang trang
- chuyen lowercase
- vi du: ` Sales Amount ` -> `salesamount`
3. Script hoi template comment cho tung cot:
- de trong neu khong muon comment cot do
- placeholder ho tro: `{column}`, `{value}`, `{row_number}`
4. Nhap ten cot comment va ky tu noi.
5. Script tao file dau ra cung dinh dang voi file dau vao.

## Vi du template

- Cot `salesamount`: `Sales={value}`
- Cot `region`: `Region={value}`

Ket qua 1 dong co the la:

```text
Sales=120 | Region=HN
```

## Chay test (pytest)

```bash
pytest -q
```
