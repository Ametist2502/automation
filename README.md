# auto_comment

Script Python tao cot `comment` tu dong trong file CSV (flat file), huong toi nguoi dung non-tech.

## 1) Tao moi truong (da dung uv venv)

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
pip install -r requirements.txt
```

## 4) Chay chuong trinh

```bash
python main.py
```

Sau do chi can tra loi cac cau hoi tren man hinh:
- duong dan file CSV dau vao
- cot du lieu can dua vao de tao comment
- ten cot comment moi
- mau comment
- file CSV dau ra

## Vi du mau comment

Mau mac dinh:

```text
Dong {row_number}: da ghi nhan '{value}'.
```

Ban co the doi sang:

```text
Khach hang {value} da duoc lien he o dong {row_number}.
```

## Ket qua

Script se tao file moi (mac dinh: `<tenfile>_commented.csv`) voi cot `comment`.
