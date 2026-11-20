# mabar-gofood

## Menjalankan aplikasi

Pastikan Python sudah terpasang, lalu jalankan perintah berikut dari folder proyek di PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

Jika PowerShell memblokir aktivasi virtual environment, jalankan perintah instalasi dan aplikasi melalui interpreter virtual environment secara langsung:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```