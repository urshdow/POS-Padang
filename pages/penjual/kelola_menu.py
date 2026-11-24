import flet as ft
from . import (
    BG_CARD,
    BG_SECONDARY,
    BORDER_COLOR,
    PRIMARY,
    ACCENT_GREEN,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    DATA_MENU_TOKO,
    buat_header_halaman,
    buat_kotak_gambar,
    buat_tag,
)


def buat_halaman_menu(on_back=None):
    kartu_list = []
    for m in DATA_MENU_TOKO:
        lbl_stok = ft.Text(
            f"Stok: {m['stok']}",
            size=12,
            weight=ft.FontWeight.BOLD,
            color=ACCENT_GREEN if m["stok"] > 0 else PRIMARY,
        )

        def edit_stok(e, menu=m, delta=1, lbl=lbl_stok):
            menu["stok"] = max(0, menu["stok"] + delta)
            lbl.value = f"Stok: {menu['stok']}"
            lbl.color = ACCENT_GREEN if menu["stok"] > 0 else PRIMARY
            lbl.update()

        kartu_list.append(
            ft.Container(
                bgcolor=BG_CARD,
                border_radius=14,
                border=ft.Border.all(1, BORDER_COLOR),
                padding=12,
                content=ft.Column(
                    spacing=10,
                    controls=[
                        ft.Row(
                            vertical_alignment=ft.CrossAxisAlignment.START,
                            spacing=10,
                            controls=[
                                buat_kotak_gambar(m["gambar"]),
                                ft.Column(
                                    expand=True,
                                    spacing=4,
                                    controls=[
                                        ft.Row(
                                            wrap=True,
                                            spacing=5,
                                            controls=[
                                                buat_tag(m["kategori"], BG_SECONDARY, TEXT_SECONDARY),
                                                buat_tag(m["tag"], "#FEF3C7", "#B45309"),
                                            ],
                                        ),
                                        ft.Text(m["nama"], size=14, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
                                        ft.Text(
                                            m["deskripsi"],
                                            size=11,
                                            color=TEXT_SECONDARY,
                                            max_lines=2,
                                            overflow=ft.TextOverflow.ELLIPSIS,
                                        ),
                                    ],
                                ),
                            ],
                        ),
                        ft.Divider(height=1, color=BORDER_COLOR),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Column(
                                    spacing=0,
                                    controls=[
                                        ft.Text("Harga", size=10, color=TEXT_SECONDARY),
                                        ft.Text(f"Rp {m['harga']:,}", size=14, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
                                    ],
                                ),
                                ft.Row(
                                    spacing=0,
                                    controls=[
                                        ft.IconButton(ft.Icons.REMOVE_CIRCLE_OUTLINE, icon_color=PRIMARY, on_click=lambda e, menu=m, lbl=lbl_stok: edit_stok(e, menu, -1, lbl)),
                                        lbl_stok,
                                        ft.IconButton(ft.Icons.ADD_CIRCLE_OUTLINE, icon_color=ACCENT_GREEN, on_click=lambda e, menu=m, lbl=lbl_stok: edit_stok(e, menu, 1, lbl)),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
            )
        )

    return ft.Column(
        expand=True,
        spacing=0,
        controls=[
            buat_header_halaman("Kelola Menu & Stok", on_back),
            ft.Container(
                expand=True,
                padding=12,
                content=ft.Column(expand=True, scroll=ft.ScrollMode.AUTO, spacing=10, controls=kartu_list),
            ),
        ],
    )