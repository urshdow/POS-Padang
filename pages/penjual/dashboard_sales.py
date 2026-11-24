import flet as ft
from . import (
    BG_CARD,
    BORDER_COLOR,
    PRIMARY,
    PRIMARY_HOVER,
    ACCENT_GOLD,
    ACCENT_GREEN,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    buat_header_halaman,
    buat_tag,
)


def buat_halaman_keuangan(on_back=None, on_export_excel=None):
    notif = ft.Text("", size=11, color=ACCENT_GREEN)

    def klik_export(e):
        if on_export_excel:
            on_export_excel()
        else:
            notif.value = "Siap dihubungkan ke fungsi openpyxl export Excel!"
            notif.update()

    return ft.Column(
        expand=True,
        spacing=0,
        controls=[
            buat_header_halaman("Keuangan & Analisis", on_back),
            ft.Container(
                expand=True,
                padding=12,
                content=ft.Column(
                    expand=True,
                    scroll=ft.ScrollMode.AUTO,
                    spacing=10,
                    controls=[
                        ft.Row(
                            spacing=8,
                            controls=[
                                ft.Container(
                                    expand=True,
                                    bgcolor=BG_CARD,
                                    border_radius=14,
                                    border=ft.Border.all(1, BORDER_COLOR),
                                    padding=12,
                                    content=ft.Column(
                                        spacing=3,
                                        controls=[
                                            ft.Text("Pendapatan Hari Ini", size=11, color=TEXT_SECONDARY),
                                            ft.Text("Rp 450,000", size=16, weight=ft.FontWeight.BOLD, color=PRIMARY),
                                        ],
                                    ),
                                ),
                                ft.Container(
                                    expand=True,
                                    bgcolor=BG_CARD,
                                    border_radius=14,
                                    border=ft.Border.all(1, BORDER_COLOR),
                                    padding=12,
                                    content=ft.Column(
                                        spacing=3,
                                        controls=[
                                            ft.Text("Pesanan Selesai", size=11, color=TEXT_SECONDARY),
                                            ft.Text("18 Order", size=16, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
                                        ],
                                    ),
                                ),
                            ],
                        ),
                        ft.Container(
                            bgcolor=BG_CARD,
                            border_radius=14,
                            border=ft.Border.all(1, BORDER_COLOR),
                            padding=12,
                            content=ft.Column(
                                spacing=8,
                                controls=[
                                    ft.Row(
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                        controls=[
                                            ft.Text("Analisis Penjualan", size=14, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
                                            buat_tag("Hari Ini", "#FEF3C7", "#B45309"),
                                        ],
                                    ),
                                    ft.Divider(height=1, color=BORDER_COLOR),
                                    ft.Row(
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                        controls=[
                                            ft.Text("Menu Terlaris", size=12, color=TEXT_SECONDARY),
                                            ft.Text("Paket Nasi Rendang", size=12, weight=ft.FontWeight.BOLD, color=ACCENT_GREEN),
                                        ],
                                    ),
                                    ft.Row(
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                        controls=[
                                            ft.Text("Rata-rata Order", size=12, color=TEXT_SECONDARY),
                                            ft.Text("Rp 25,000", size=12, weight=ft.FontWeight.BOLD, color=ACCENT_GOLD),
                                        ],
                                    ),
                                ],
                            ),
                        ),
                        ft.Container(
                            bgcolor=PRIMARY_HOVER,
                            border_radius=12,
                            padding=ft.Padding.symmetric(vertical=10, horizontal=12),
                            ink=True,
                            on_click=klik_export,
                            content=ft.Row(
                                alignment=ft.MainAxisAlignment.CENTER,
                                spacing=8,
                                controls=[
                                    ft.Icon(ft.Icons.DOWNLOAD, color=BG_CARD, size=18),
                                    ft.Text("Export Laporan Excel (.xlsx)", size=13, weight=ft.FontWeight.BOLD, color=BG_CARD),
                                ],
                            ),
                        ),
                        notif,
                    ],
                ),
            ),
        ],
    )