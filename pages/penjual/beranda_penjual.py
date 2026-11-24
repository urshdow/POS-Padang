import flet as ft
from . import (
    BG_MAIN,
    BG_CARD,
    BG_SECONDARY,
    BORDER_COLOR,
    PRIMARY,
    ACCENT_GREEN,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    DATA_MENU_TOKO,
    DATA_PESANAN_MASUK,
    FullLayarContainer,
    buat_header_halaman,
    buat_kotak_gambar,
    buat_tag,
    warna_status_pesanan,
)
from .pesanan_penjual import buat_halaman_pesanan
from .kelola_menu import buat_halaman_menu
from .dashboard_sales import buat_halaman_keuangan

MENU_BERANDA = [
    {"key": "pesanan", "nama": "Pesanan", "icon": ft.Icons.SOUP_KITCHEN_OUTLINED, "gambar": ""},
    {"key": "menu", "nama": "Menu", "icon": ft.Icons.MENU_BOOK_OUTLINED, "gambar": ""},
    {"key": "kasir", "nama": "Kasir", "icon": ft.Icons.POINT_OF_SALE_OUTLINED, "gambar": "", "badge": "Baru"},
    {"key": "keuangan", "nama": "Keuangan", "icon": ft.Icons.ACCOUNT_BALANCE_WALLET_OUTLINED, "gambar": ""},
]


def buat_halaman_kasir(on_back=None):
    keranjang = {i: 0 for i in range(len(DATA_MENU_TOKO))}
    txt_total = ft.Text("Rp 0", size=16, weight=ft.FontWeight.BOLD, color=PRIMARY)
    txt_info = ft.Text("0 item dipilih", size=11, color=TEXT_SECONDARY)
    list_kasir = ft.Column(spacing=10)

    def hitung_ulang():
        total_rp = sum(DATA_MENU_TOKO[i]["harga"] * qty for i, qty in keranjang.items())
        txt_total.value = f"Rp {total_rp:,}"
        txt_info.value = f"{sum(keranjang.values())} item dipilih"
        txt_info.color = TEXT_SECONDARY
        txt_total.update()
        txt_info.update()

    def render_kasir():
        list_kasir.controls.clear()
        for i, m in enumerate(DATA_MENU_TOKO):
            qty = keranjang[i]

            def ubah_qty(e, idx=i, delta=1):
                baru = keranjang[idx] + delta
                if 0 <= baru <= DATA_MENU_TOKO[idx]["stok"]:
                    keranjang[idx] = baru
                    render_kasir()
                    list_kasir.update()
                    hitung_ulang()

            aksi = (
                ft.IconButton(
                    ft.Icons.ADD_SHOPPING_CART,
                    icon_color=BG_CARD,
                    bgcolor=PRIMARY,
                    disabled=m["stok"] == 0,
                    on_click=lambda e, idx=i: ubah_qty(e, idx, 1),
                )
                if qty == 0
                else ft.Row(
                    spacing=0,
                    controls=[
                        ft.IconButton(ft.Icons.REMOVE_CIRCLE_OUTLINE, icon_color=PRIMARY, on_click=lambda e, idx=i: ubah_qty(e, idx, -1)),
                        ft.Text(str(qty), size=13, weight=ft.FontWeight.BOLD, color=PRIMARY),
                        ft.IconButton(ft.Icons.ADD_CIRCLE_OUTLINE, icon_color=ACCENT_GREEN, on_click=lambda e, idx=i: ubah_qty(e, idx, 1)),
                    ],
                )
            )

            list_kasir.controls.append(
                ft.Container(
                    bgcolor=BG_CARD,
                    border_radius=14,
                    border=ft.Border.all(1, BORDER_COLOR),
                    padding=12,
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Row(
                                expand=True,
                                spacing=10,
                                controls=[
                                    buat_kotak_gambar(m["gambar"]),
                                    ft.Column(
                                        expand=True,
                                        spacing=3,
                                        controls=[
                                            buat_tag(
                                                f"Stok: {m['stok']}",
                                                "#DCFCE7" if m["stok"] > 0 else "#FEE2E2",
                                                ACCENT_GREEN if m["stok"] > 0 else PRIMARY,
                                            ),
                                            ft.Text(m["nama"], size=14, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY, max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
                                            ft.Text(f"Rp {m['harga']:,}", size=13, weight=ft.FontWeight.W_600, color=PRIMARY),
                                        ],
                                    ),
                                ],
                            ),
                            aksi,
                        ],
                    ),
                )
            )

    def bayar(e):
        total_rp = sum(DATA_MENU_TOKO[i]["harga"] * qty for i, qty in keranjang.items())
        if total_rp > 0:
            for i, qty in keranjang.items():
                DATA_MENU_TOKO[i]["stok"] = max(0, DATA_MENU_TOKO[i]["stok"] - qty)
                keranjang[i] = 0
            render_kasir()
            list_kasir.update()
            txt_total.value = "Rp 0"
            txt_info.value = f"Transaksi Rp {total_rp:,} selesai!"
            txt_info.color = ACCENT_GREEN
            txt_total.update()
            txt_info.update()

    render_kasir()

    return ft.Column(
        expand=True,
        spacing=0,
        controls=[
            buat_header_halaman("Kasir Cepat", on_back),
            ft.Container(
                expand=True,
                padding=12,
                content=ft.Column(
                    expand=True,
                    scroll=ft.ScrollMode.AUTO,
                    spacing=10,
                    controls=[
                        list_kasir,
                        ft.Container(
                            bgcolor=BG_CARD,
                            border_radius=14,
                            border=ft.Border.all(1.5, PRIMARY),
                            padding=12,
                            content=ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Column(expand=True, spacing=1, controls=[txt_info, txt_total]),
                                    ft.IconButton(ft.Icons.CHECK_CIRCLE, icon_color=BG_CARD, bgcolor=PRIMARY, tooltip="Bayar", on_click=bayar),
                                ],
                            ),
                        ),
                    ],
                ),
            ),
        ],
    )


def buat_beranda_penjual(on_export_excel=None):
    status_toko = {"buka": True}
    wadah_halaman = FullLayarContainer(expand=True, margin=0, padding=0, bgcolor=BG_MAIN)

    def tampilan_beranda():
        lbl_status = ft.Text(
            "Toko BUKA" if status_toko["buka"] else "Toko TUTUP",
            size=11,
            weight=ft.FontWeight.BOLD,
            color=ACCENT_GREEN if status_toko["buka"] else PRIMARY,
        )

        def ubah_status(e):
            status_toko["buka"] = e.control.value
            lbl_status.value = "Toko BUKA" if e.control.value else "Toko TUTUP"
            lbl_status.color = ACCENT_GREEN if e.control.value else PRIMARY
            lbl_status.update()

        header_toko = ft.Container(
            bgcolor=BG_CARD,
            border=ft.Border.only(bottom=ft.BorderSide(1, BORDER_COLOR)),
            padding=ft.Padding.symmetric(horizontal=12, vertical=10),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Row(
                        expand=True,
                        spacing=10,
                        controls=[
                            ft.Container(
                                width=38,
                                height=38,
                                bgcolor=PRIMARY,
                                border_radius=10,
                                alignment=ft.Alignment(0, 0),
                                content=ft.Icon(ft.Icons.STOREFRONT, color=BG_CARD, size=20),
                            ),
                            ft.Column(
                                expand=True,
                                spacing=1,
                                controls=[
                                    ft.Text("RM Padang Sinar Minang", size=14, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY, max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
                                    ft.Row(spacing=5, controls=[ft.Text("Panel Penjual •", size=11, color=TEXT_SECONDARY), lbl_status]),
                                ],
                            ),
                        ],
                    ),
                    ft.Switch(value=status_toko["buka"], active_color=ACCENT_GREEN, scale=0.85, on_change=ubah_status),
                ],
            ),
        )

        # 1. Grid 4 Tombol Ikon / Gambar Fitur
        tombol_fitur = []
        for item in MENU_BERANDA:
            isi_ikon = (
                ft.Image(src=item["gambar"], width=36, height=36, border_radius=10)
                if item["gambar"]
                else ft.Icon(item["icon"], size=28, color=PRIMARY)
            )
            kotak = ft.Container(
                width=62,
                height=62,
                top=6,
                left=6,
                bgcolor=BG_CARD,
                border_radius=16,
                border=ft.Border.all(1, BORDER_COLOR),
                alignment=ft.Alignment(0, 0),
                content=isi_ikon,
            )
            lapisan = [kotak]
            if item.get("badge"):
                lapisan.append(
                    ft.Container(
                        top=0,
                        right=0,
                        bgcolor=PRIMARY,
                        border_radius=8,
                        padding=ft.Padding.symmetric(horizontal=6, vertical=1),
                        content=ft.Text(item["badge"], size=9, weight=ft.FontWeight.BOLD, color=BG_CARD),
                    )
                )

            tombol_fitur.append(
                ft.Container(
                    expand=True,
                    ink=True,
                    border_radius=12,
                    on_click=lambda _, k=item["key"]: buka_page(k),
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=5,
                        controls=[
                            ft.Stack(width=74, height=70, controls=lapisan),
                            ft.Text(item["nama"], size=12, weight=ft.FontWeight.W_600, color=TEXT_PRIMARY, text_align=ft.TextAlign.CENTER),
                        ],
                    ),
                )
            )

        # 2. Shortcut Pesanan Masuk di Beranda
        jumlah_aktif = sum(1 for o in DATA_PESANAN_MASUK if o["status"] != "Pesanan Selesai")
        kartu_shortcut = []
        for order in DATA_PESANAN_MASUK:
            bg_st, fg_st = warna_status_pesanan(order["status"])
            kartu_shortcut.append(
                ft.Container(
                    bgcolor=BG_CARD,
                    border_radius=14,
                    border=ft.Border.all(1, BORDER_COLOR),
                    padding=12,
                    ink=True,
                    on_click=lambda _: buka_page("pesanan"),
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=10,
                        controls=[
                            buat_kotak_gambar(order["gambar"], ft.Icons.SOUP_KITCHEN_OUTLINED, ukuran=50),
                            ft.Column(
                                expand=True,
                                spacing=3,
                                controls=[
                                    ft.Row(
                                        spacing=6,
                                        controls=[
                                            buat_tag(order["kode"]),
                                            buat_tag(order["status"], bg_st, fg_st),
                                        ],
                                    ),
                                    ft.Text(order["pembeli"], size=13, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
                                    ft.Text(
                                        f"{order['item']} • Rp {order['total']:,}",
                                        size=11,
                                        color=TEXT_SECONDARY,
                                        max_lines=1,
                                        overflow=ft.TextOverflow.ELLIPSIS,
                                    ),
                                ],
                            ),
                            ft.Icon(ft.Icons.CHEVRON_RIGHT, size=20, color=TEXT_SECONDARY),
                        ],
                    ),
                )
            )

        bagian_shortcut = ft.Column(
            spacing=8,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Row(
                            spacing=6,
                            controls=[
                                ft.Text("Pesanan Masuk", size=14, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
                                buat_tag(f"{jumlah_aktif} Aktif", "#FFEDD5", PRIMARY),
                            ],
                        ),
                        ft.GestureDetector(
                            on_tap=lambda _: buka_page("pesanan"),
                            content=ft.Text("Lihat Semua", size=12, weight=ft.FontWeight.BOLD, color=PRIMARY),
                        ),
                    ],
                ),
                *kartu_shortcut,
            ],
        )

        return ft.Column(
            expand=True,
            spacing=0,
            controls=[
                header_toko,
                ft.Container(
                    expand=True,
                    padding=ft.Padding.symmetric(horizontal=12, vertical=14),
                    content=ft.Column(
                        expand=True,
                        scroll=ft.ScrollMode.AUTO,
                        spacing=16,
                        controls=[
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                vertical_alignment=ft.CrossAxisAlignment.START,
                                spacing=6,
                                controls=tombol_fitur,
                            ),
                            bagian_shortcut,
                        ],
                    ),
                ),
            ],
        )

    def kembali_ke_beranda():
        wadah_halaman.content = tampilan_beranda()
        wadah_halaman.update()

    def buka_page(key):
        halaman = {
            "pesanan": lambda: buat_halaman_pesanan(on_back=kembali_ke_beranda),
            "menu": lambda: buat_halaman_menu(on_back=kembali_ke_beranda),
            "kasir": lambda: buat_halaman_kasir(on_back=kembali_ke_beranda),
            "keuangan": lambda: buat_halaman_keuangan(on_back=kembali_ke_beranda, on_export_excel=on_export_excel),
        }
        wadah_halaman.content = halaman[key]()
        wadah_halaman.update()

    wadah_halaman.content = tampilan_beranda()
    return wadah_halaman