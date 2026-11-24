import flet as ft

# Palet Warna :root
BG_MAIN = "#FAF6F0"
BG_CARD = "#FFFFFF"
BG_SECONDARY = "#EFE7DC"
BORDER_COLOR = "#EADFD0"
PRIMARY = "#D95D39"
PRIMARY_HOVER = "#B84726"
ACCENT_GOLD = "#D49B35"
ACCENT_GREEN = "#2E7D32"
TEXT_PRIMARY = "#2D241E"
TEXT_SECONDARY = "#786B61"

# Tahapan kondisi pesanan
TAHAP_PESANAN = ["Masuk", "Diproses", "Pesanan Selesai"]

DATA_PESANAN_MASUK = [
    {
        "kode": "ORD-1025",
        "pembeli": "Siti Aminah",
        "item": "1x Paket Nasi Ayam Pop Komplit",
        "total": 30000,
        "status": "Masuk",
        "gambar": "",
    },
    {
        "kode": "ORD-1024",
        "pembeli": "Budi Santoso",
        "item": "2x Paket Nasi Rendang Spesial, 2x Es Teh Jumbo",
        "total": 68000,
        "status": "Diproses",
        "gambar": "",
    },
    {
        "kode": "ORD-1023",
        "pembeli": "Andi Pratama",
        "item": "1x Paket Nasi Rendang Spesial",
        "total": 32000,
        "status": "Pesanan Selesai",
        "gambar": "",
    },
]

# Isi field "gambar" dengan path lokal (misal: "assets/rendang.jpg") atau URL gambar
DATA_MENU_TOKO = [
    {
        "nama": "Paket Nasi Rendang Spesial",
        "kategori": "Paket Nasi",
        "tag": "★ Terlaris",
        "deskripsi": "Nasi putih pulen dengan rendang daging sapi empuk berbumbu pekat, gulai nangka, dan sambal ijo.",
        "harga": 32000,
        "stok": 25,
        "gambar": "",
    },
    {
        "nama": "Paket Nasi Ayam Pop Komplit",
        "kategori": "Paket Nasi",
        "tag": "★ Terlaris",
        "deskripsi": "Nasi putih hangat dengan ayam pop gurih khas Bukittinggi, sayur nangka, dan sambal tomat merah.",
        "harga": 30000,
        "stok": 15,
        "gambar": "",
    },
    {
        "nama": "Es Teh Jumbo",
        "kategori": "Minuman",
        "tag": "Segar",
        "deskripsi": "Teh melati seduh segar dengan gula asli dan es batu melimpah.",
        "harga": 5000,
        "stok": 40,
        "gambar": "",
    },
]


class FullLayarContainer(ft.Container):
    def did_mount(self):
        try:
            if self.page:
                self.page.padding = 0
                self.page.spacing = 0
                self.page.bgcolor = BG_MAIN
                if self.page.views:
                    self.page.views[-1].padding = 0
                    self.page.views[-1].spacing = 0
                self.page.update()
        except Exception:
            pass


def buat_header_halaman(judul, on_back=None):
    return ft.Container(
        bgcolor=BG_CARD,
        border=ft.Border.only(bottom=ft.BorderSide(1, BORDER_COLOR)),
        padding=ft.Padding.symmetric(horizontal=6, vertical=6),
        content=ft.Row(
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=4,
            controls=[
                ft.IconButton(
                    ft.Icons.ARROW_BACK,
                    icon_color=TEXT_PRIMARY,
                    tooltip="Kembali ke Beranda",
                    on_click=lambda _: on_back() if on_back else None,
                ),
                ft.Text(judul, size=16, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
            ],
        ),
    )


def buat_kotak_gambar(src="", ikon=ft.Icons.RESTAURANT_MENU, ukuran=64):
    isi = (
        ft.Image(src=src, width=ukuran, height=ukuran, border_radius=12)
        if src
        else ft.Icon(ikon, size=26, color=ACCENT_GOLD)
    )
    return ft.Container(
        width=ukuran,
        height=ukuran,
        bgcolor=BG_MAIN,
        border_radius=14,
        border=ft.Border.all(1, BORDER_COLOR),
        alignment=ft.Alignment(0, 0),
        content=isi,
    )


def buat_tag(teks, bg=BG_SECONDARY, warna=TEXT_SECONDARY):
    return ft.Container(
        bgcolor=bg,
        border_radius=10,
        padding=ft.Padding.symmetric(horizontal=7, vertical=2),
        content=ft.Text(teks, size=10, weight=ft.FontWeight.W_600, color=warna),
    )


def warna_status_pesanan(status):
    if status == "Masuk":
        return "#FEF3C7", "#B45309"
    if status == "Diproses":
        return "#FFEDD5", PRIMARY
    return "#DCFCE7", ACCENT_GREEN


from .beranda_penjual import buat_beranda_penjual

__all__ = ["buat_beranda_penjual"]