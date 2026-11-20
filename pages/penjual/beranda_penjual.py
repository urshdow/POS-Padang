import flet as ft
from pages.penjual.dashboard_sales import buat_dashboard_sales
from pages.penjual.kelola_menu import buat_kelola_menu
from pages.penjual.pesanan_penjual import buat_pesanan_penjual


def buat_beranda_penjual(page: ft.Page, nama_toko: str):
    state = {"is_open": True}

    status_title = ft.Text(
        "TOKO BUKA", weight=ft.FontWeight.BOLD, color="#16A34A", size=15
    )
    status_sub = ft.Text(
        "Siap menerima pesanan pertama hari ini", size=12, color="#6B7280"
    )
    area_konten = ft.Container(expand=True)

    def toast(msg):
        page.snack_bar = ft.SnackBar(ft.Text(msg))
        page.snack_bar.open = True
        page.update()

    def toggle_store(e):
        state["is_open"] = e.control.value
        status_title.value = "TOKO BUKA" if state["is_open"] else "TOKO TUTUP"
        status_title.color = "#16A34A" if state["is_open"] else "#DC2626"
        status_sub.value = (
            "Siap menerima pesanan pertama hari ini"
            if state["is_open"]
            else "Toko tidak tampil di aplikasi pembeli"
        )
        toast("Toko dibuka!" if state["is_open"] else "Toko ditutup.")
        page.update()

    def tampilkan_ringkasan(e=None):
        area_konten.content = ft.Column(
            scroll=ft.ScrollMode.AUTO,
            spacing=14,
            controls=[
                # Card Status Toko
                ft.Container(
                    padding=16,
                    bgcolor="#FFF8F0",
                    border_radius=12,
                    border=ft.border.all(1, "#FED7AA"),
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Column([status_title, status_sub], spacing=2),
                            ft.Switch(
                                value=state["is_open"],
                                active_color="#EA580C",
                                on_change=toggle_store,
                            ),
                        ],
                    ),
                ),
                # Ringkasan Hari Ini (Empty State: Rp 0)
                ft.Container(
                    padding=16,
                    bgcolor="#FFFFFF",
                    border_radius=12,
                    border=ft.border.all(1, "#E5E7EB"),
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_AROUND,
                        controls=[
                            ft.Column(
                                [
                                    ft.Text(
                                        "Pendapatan Hari Ini",
                                        size=11,
                                        color="#6B7280",
                                    ),
                                    ft.Text(
                                        "Rp 0",
                                        size=18,
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                            ft.Column(
                                [
                                    ft.Text(
                                        "Order Selesai",
                                        size=11,
                                        color="#6B7280",
                                    ),
                                    ft.Text(
                                        "0 Order",
                                        size=18,
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                        ],
                    ),
                ),
                # Empty State Pesanan
                ft.Container(
                    padding=24,
                    bgcolor="#FFFFFF",
                    border_radius=12,
                    border=ft.border.all(1, "#E5E7EB"),
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Icon(
                                ft.Icons.STOREFRONT_OUTLINED,
                                size=42,
                                color="#EA580C",
                            ),
                            ft.Text(
                                "Belum Ada Pesanan Masuk",
                                weight=ft.FontWeight.BOLD,
                                size=15,
                            ),
                            ft.Text(
                                f"Toko {nama_toko} siap menerima pembeli pertama.",
                                size=12,
                                color="#6B7280",
                                text_align=ft.TextAlign.CENTER,
                            ),
                        ],
                    ),
                ),
            ],
        )
        page.update()

    def buka_sub_halaman(halaman: str):
        if halaman == "ringkasan":
            tampilkan_ringkasan()
        elif halaman == "menu":
            area_konten.content = buat_kelola_menu(page)
        elif halaman == "pesanan":
            area_konten.content = buat_pesanan_penjual(page)
        elif halaman == "sales":
            area_konten.content = buat_dashboard_sales(page, nama_toko)
        page.update()

    # Navigasi Menu Penjual (4 Sub-Halaman sesuai hierarki)
    nav_tabs = ft.Row(
        scroll=ft.ScrollMode.AUTO,
        controls=[
            ft.FilledTonalButton(
                "Beranda",
                icon=ft.Icons.HOME,
                on_click=lambda e: buka_sub_halaman("ringkasan"),
            ),
            ft.FilledTonalButton(
                "Kelola Menu",
                icon=ft.Icons.RESTAURANT_MENU,
                on_click=lambda e: buka_sub_halaman("menu"),
            ),
            ft.FilledTonalButton(
                "Pesanan",
                icon=ft.Icons.RECEIPT_LONG,
                on_click=lambda e: buka_sub_halaman("pesanan"),
            ),
            ft.FilledTonalButton(
                "Sales & Excel",
                icon=ft.Icons.BAR_CHART,
                on_click=lambda e: buka_sub_halaman("sales"),
            ),
        ],
    )

    tampilkan_ringkasan()

    return ft.Column(
        expand=True,
        spacing=12,
        controls=[nav_tabs, area_konten],
    )
