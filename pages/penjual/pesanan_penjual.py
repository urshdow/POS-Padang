import flet as ft
from . import (
    BG_CARD,
    BORDER_COLOR,
    PRIMARY,
    ACCENT_GREEN,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    DATA_PESANAN_MASUK,
    buat_header_halaman,
    buat_kotak_gambar,
    buat_tag,
    warna_status_pesanan,
)

# Daftar sub-tab kondisi pesanan ala TikTok Shop & Shopee
TAB_KONDISI = [
    {"status": "Masuk", "label": "Masuk"},
    {"status": "Diproses", "label": "Diproses"},
    {"status": "Pesanan Selesai", "label": "Selesai"},
]


def buat_halaman_pesanan(on_back=None):
    tab_aktif = {"status": "Masuk"}
    baris_tab = ft.Row(spacing=0)
    daftar_kartu = ft.Column(spacing=10)

    def pindah_tab(status_baru):
        tab_aktif["status"] = status_baru
        render_tabs()
        render_pesanan()
        baris_tab.update()
        daftar_kartu.update()

    # =========================================================================
    # 1. BILAH SUB-TAB KONDISI PESANAN (Diterima | Diproses | Selesai)
    # =========================================================================
    def render_tabs():
        baris_tab.controls.clear()
        for t in TAB_KONDISI:
            aktif = tab_aktif["status"] == t["status"]
            jumlah = sum(1 for o in DATA_PESANAN_MASUK if o["status"] == t["status"])

            baris_tab.controls.append(
                ft.Container(
                    expand=True,
                    ink=True,
                    padding=ft.Padding.only(top=10, left=4, right=4),
                    on_click=lambda _, s=t["status"]: pindah_tab(s),
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                        spacing=8,
                        controls=[
                            ft.Text(
                                f"{t['label']} ({jumlah})",
                                size=12,
                                weight=ft.FontWeight.BOLD if aktif else ft.FontWeight.W_500,
                                color=PRIMARY if aktif else TEXT_SECONDARY,
                                text_align=ft.TextAlign.CENTER,
                                max_lines=1,
                            ),
                            # Garis indikator bawah tab aktif ala Shopee / TikTok Shop
                            ft.Container(
                                height=3,
                                bgcolor=PRIMARY if aktif else "transparent",
                                border_radius=2,
                            ),
                        ],
                    ),
                )
            )

    wadah_tab = ft.Container(
        bgcolor=BG_CARD,
        border=ft.Border.only(bottom=ft.BorderSide(1, BORDER_COLOR)),
        content=baris_tab,
    )

    # =========================================================================
    # 2. DAFTAR KARTU PESANAN SESUAI TAB AKTIF
    # =========================================================================
    def render_pesanan():
        daftar_kartu.controls.clear()
        pesanan_terfilter = [o for o in DATA_PESANAN_MASUK if o["status"] == tab_aktif["status"]]

        if not pesanan_terfilter:
            daftar_kartu.controls.append(
                ft.Container(
                    bgcolor=BG_CARD,
                    border_radius=14,
                    border=ft.Border.all(1, BORDER_COLOR),
                    padding=ft.Padding.symmetric(vertical=32, horizontal=16),
                    alignment=ft.Alignment(0, 0),
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=6,
                        controls=[
                            ft.Icon(ft.Icons.RECEIPT_LONG_OUTLINED, size=36, color=TEXT_SECONDARY),
                            ft.Text(
                                f"Belum ada pesanan berstatus {tab_aktif['status']}",
                                size=12,
                                color=TEXT_SECONDARY,
                                text_align=ft.TextAlign.CENTER,
                            ),
                        ],
                    ),
                )
            )
            return

        for order in pesanan_terfilter:
            status = order["status"]
            bg_st, fg_st = warna_status_pesanan(status)

            def lanjut_tahap(e, o=order):
                if o["status"] == "Masuk":
                    o["status"] = "Diproses"
                elif o["status"] == "Diproses":
                    o["status"] = "Pesanan Selesai"
                render_tabs()
                render_pesanan()
                baris_tab.update()
                daftar_kartu.update()

            if status == "Masuk":
                tombol_aksi = ft.Button(
                    "Proses Pesanan",
                    bgcolor=PRIMARY,
                    color=BG_CARD,
                    on_click=lanjut_tahap,
                )
            elif status == "Diproses":
                tombol_aksi = ft.Button(
                    "Selesaikan",
                    bgcolor=ACCENT_GREEN,
                    color=BG_CARD,
                    on_click=lanjut_tahap,
                )
            else:
                tombol_aksi = buat_tag("Selesai ✓", "#DCFCE7", ACCENT_GREEN)

            daftar_kartu.controls.append(
                ft.Container(
                    bgcolor=BG_CARD,
                    border_radius=14,
                    border=ft.Border.all(1, BORDER_COLOR),
                    padding=12,
                    content=ft.Column(
                        spacing=10,
                        controls=[
                            # Baris atas kartu: Kode Order + Badge Kondisi
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    buat_tag(order["kode"]),
                                    buat_tag(status, bg_st, fg_st),
                                ],
                            ),
                            # Baris tengah kartu: Gambar + Nama Pembeli & Rincian Menu
                            ft.Row(
                                vertical_alignment=ft.CrossAxisAlignment.START,
                                spacing=10,
                                controls=[
                                    buat_kotak_gambar(order["gambar"], ft.Icons.SOUP_KITCHEN_OUTLINED),
                                    ft.Column(
                                        expand=True,
                                        spacing=3,
                                        controls=[
                                            ft.Text(
                                                order["pembeli"],
                                                size=14,
                                                weight=ft.FontWeight.BOLD,
                                                color=TEXT_PRIMARY,
                                            ),
                                            ft.Text(order["item"], size=12, color=TEXT_SECONDARY),
                                        ],
                                    ),
                                ],
                            ),
                            ft.Divider(height=1, color=BORDER_COLOR),
                            # Baris bawah kartu: Total Harga + Tombol Aksi Tahap Berikutnya
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    ft.Column(
                                        spacing=0,
                                        controls=[
                                            ft.Text("Total Pembayaran", size=10, color=TEXT_SECONDARY),
                                            ft.Text(
                                                f"Rp {order['total']:,}",
                                                size=14,
                                                weight=ft.FontWeight.BOLD,
                                                color=TEXT_PRIMARY,
                                            ),
                                        ],
                                    ),
                                    tombol_aksi,
                                ],
                            ),
                        ],
                    ),
                )
            )

    render_tabs()
    render_pesanan()

    return ft.Column(
        expand=True,
        spacing=0,
        controls=[
            buat_header_halaman("Pesanan Masuk", on_back),
            wadah_tab,
            ft.Container(
                expand=True,
                padding=12,
                content=ft.Column(
                    expand=True,
                    scroll=ft.ScrollMode.AUTO,
                    spacing=10,
                    controls=[daftar_kartu],
                ),
            ),
        ],
    )