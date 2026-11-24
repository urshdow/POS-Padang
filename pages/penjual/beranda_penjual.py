import flet as ft

DATA_PESANAN_MASUK = [
    {
        "kode": "ORD-1024",
        "pembeli": "Budi Santoso",
        "item": "2x Paket Geprek Level 3, 2x Es Teh Jumbo",
        "total": 38000,
        "status": "Menunggu Konfirmasi",
    },
    {
        "kode": "ORD-1025",
        "pembeli": "Siti Aminah",
        "item": "1x Geprek Keju Lumer",
        "total": 19000,
        "status": "Sedang Dimasak",
    },
]

DATA_MENU_TOKO = [
    {"nama": "Paket Geprek Level 1-5", "harga": 15000, "stok": 25},
    {"nama": "Geprek Keju Lumer", "harga": 19000, "stok": 12},
    {"nama": "Es Teh Jumbo", "harga": 4000, "stok": 40},
]

FITUR_UTAMA = [
    {"key": "pesanan", "nama": "Pesanan", "icon": ft.Icons.SOUP_KITCHEN_OUTLINED},
    {"key": "menu", "nama": "Menu", "icon": ft.Icons.MENU_BOOK_OUTLINED},
    {"key": "kasir", "nama": "Kasir", "icon": ft.Icons.POINT_OF_SALE_OUTLINED, "badge": "Baru"},
    {"key": "keuangan", "nama": "Keuangan &\nAnalisis", "icon": ft.Icons.ACCOUNT_BALANCE_WALLET_OUTLINED},
]


def buat_beranda_penjual(on_export_excel=None):
    # Hirarki warna sesuai :root
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

    tab_aktif = {"key": "pesanan"}

    # 1. Status Toko (Buka / Tutup)
    lbl_toko = ft.Text("Toko Sedang BUKA", weight=ft.FontWeight.BOLD, color=ACCENT_GREEN)

    def ubah_status_toko(e):
        lbl_toko.value = "Toko Sedang BUKA" if e.control.value else "Toko TUTUP Sementara"
        lbl_toko.color = ACCENT_GREEN if e.control.value else PRIMARY
        lbl_toko.update()

    kartu_status = ft.Container(
        bgcolor=BG_CARD,
        border_radius=12,
        border=ft.Border.all(1, BORDER_COLOR),
        padding=12,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Row(
                    spacing=10,
                    controls=[ft.Icon(ft.Icons.STOREFRONT, color=PRIMARY, size=24), lbl_toko],
                ),
                ft.Switch(value=True, active_color=ACCENT_GREEN, on_change=ubah_status_toko),
            ],
        ),
    )

    # 2. Tampilan Masing-Masing Fitur
    def view_pesanan():
        items = []
        for order in DATA_PESANAN_MASUK:
            warna_awal = ACCENT_GREEN if order["status"] == "Siap Diambil Driver" else ACCENT_GOLD
            lbl_status = ft.Text(order["status"], size=12, color=warna_awal, weight=ft.FontWeight.BOLD)

            def proses(e, o=order, lbl=lbl_status):
                o["status"] = "Siap Diambil Driver"
                lbl.value, lbl.color = o["status"], ACCENT_GREEN
                e.control.disabled, e.control.text = True, "Sudah Diproses"
                lbl.update()
                e.control.update()

            items.append(
                ft.Container(
                    bgcolor=BG_CARD,
                    border_radius=12,
                    border=ft.Border.all(1, BORDER_COLOR),
                    padding=14,
                    content=ft.Column(
                        spacing=6,
                        controls=[
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Text(
                                        f"{order['kode']} • {order['pembeli']}",
                                        weight=ft.FontWeight.BOLD,
                                        color=TEXT_PRIMARY,
                                    ),
                                    lbl_status,
                                ],
                            ),
                            ft.Text(order["item"], size=13, color=TEXT_SECONDARY),
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Text(
                                        f"Total: Rp {order['total']:,}",
                                        weight=ft.FontWeight.BOLD,
                                        color=PRIMARY,
                                    ),
                                    ft.Button(
                                        "Terima & Siapkan",
                                        bgcolor=PRIMARY,
                                        color=BG_CARD,
                                        on_click=proses,
                                    ),
                                ],
                            ),
                        ],
                    ),
                )
            )
        return ft.Column(
            spacing=10,
            controls=[
                ft.Text("Pesanan Masuk", size=16, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
                *items,
            ],
        )

    def view_menu():
        items = []
        for m in DATA_MENU_TOKO:
            lbl_stok = ft.Text(
                f"Stok: {m['stok']}",
                size=13,
                color=ACCENT_GREEN if m["stok"] > 0 else PRIMARY,
                weight=ft.FontWeight.BOLD,
            )

            def edit_stok(e, menu=m, delta=1, lbl=lbl_stok):
                menu["stok"] = max(0, menu["stok"] + delta)
                lbl.value = f"Stok: {menu['stok']}"
                lbl.color = ACCENT_GREEN if menu["stok"] > 0 else PRIMARY
                lbl.update()

            items.append(
                ft.Container(
                    bgcolor=BG_CARD,
                    border_radius=10,
                    border=ft.Border.all(1, BORDER_COLOR),
                    padding=12,
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Column(
                                spacing=2,
                                controls=[
                                    ft.Text(m["nama"], weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
                                    ft.Text(f"Rp {m['harga']:,}", size=12, color=TEXT_SECONDARY),
                                ],
                            ),
                            ft.Row(
                                spacing=4,
                                controls=[
                                    ft.IconButton(
                                        icon=ft.Icons.REMOVE_CIRCLE_OUTLINE,
                                        icon_color=PRIMARY,
                                        icon_size=22,
                                        tooltip="Kurangi Stok",
                                        on_click=lambda e, menu=m, lbl=lbl_stok: edit_stok(e, menu, -1, lbl),
                                    ),
                                    lbl_stok,
                                    ft.IconButton(
                                        icon=ft.Icons.ADD_CIRCLE_OUTLINE,
                                        icon_color=ACCENT_GREEN,
                                        icon_size=22,
                                        tooltip="Tambah Stok",
                                        on_click=lambda e, menu=m, lbl=lbl_stok: edit_stok(e, menu, 1, lbl),
                                    ),
                                ],
                            ),
                        ],
                    ),
                )
            )
        return ft.Column(
            spacing=8,
            controls=[
                ft.Text("Daftar Menu & Edit Stok", size=16, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
                *items,
            ],
        )

    def view_kasir():
        keranjang = {i: 0 for i in range(len(DATA_MENU_TOKO))}
        txt_total = ft.Text("Rp 0", size=18, weight=ft.FontWeight.BOLD, color=PRIMARY)
        txt_info = ft.Text("0 item dipilih", size=12, color=TEXT_SECONDARY)
        list_kasir = ft.Column(spacing=10)

        def hitung_ulang():
            total_rp = sum(DATA_MENU_TOKO[i]["harga"] * qty for i, qty in keranjang.items())
            total_qty = sum(keranjang.values())
            txt_total.value = f"Rp {total_rp:,}"
            txt_info.value = f"{total_qty} item dipilih"
            txt_total.update()
            txt_info.update()

        def render_pilihan():
            list_kasir.controls.clear()
            for i, m in enumerate(DATA_MENU_TOKO):
                lbl_qty = ft.Text(
                    str(keranjang[i]),
                    size=14,
                    weight=ft.FontWeight.BOLD,
                    color=TEXT_PRIMARY,
                    width=22,
                    text_align=ft.TextAlign.CENTER,
                )

                def ubah_qty(e, idx=i, delta=1, lbl=lbl_qty):
                    baru = keranjang[idx] + delta
                    if 0 <= baru <= DATA_MENU_TOKO[idx]["stok"]:
                        keranjang[idx] = baru
                        lbl.value = str(baru)
                        lbl.color = PRIMARY if baru > 0 else TEXT_PRIMARY
                        lbl.update()
                        hitung_ulang()

                list_kasir.controls.append(
                    ft.Container(
                        bgcolor=BG_CARD,
                        border_radius=10,
                        border=ft.Border.all(1, BORDER_COLOR),
                        padding=12,
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Column(
                                    spacing=2,
                                    controls=[
                                        ft.Text(m["nama"], weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
                                        ft.Text(
                                            f"Rp {m['harga']:,} • Stok: {m['stok']}",
                                            size=12,
                                            color=TEXT_SECONDARY,
                                        ),
                                    ],
                                ),
                                ft.Row(
                                    spacing=4,
                                    controls=[
                                        ft.IconButton(
                                            icon=ft.Icons.REMOVE_CIRCLE_OUTLINE,
                                            icon_color=PRIMARY,
                                            icon_size=22,
                                            tooltip="Kurangi Item",
                                            on_click=lambda e, idx=i, lbl=lbl_qty: ubah_qty(e, idx, -1, lbl),
                                        ),
                                        lbl_qty,
                                        ft.IconButton(
                                            icon=ft.Icons.ADD_CIRCLE_OUTLINE,
                                            icon_color=ACCENT_GREEN,
                                            icon_size=22,
                                            tooltip="Tambah Item",
                                            on_click=lambda e, idx=i, lbl=lbl_qty: ubah_qty(e, idx, 1, lbl),
                                        ),
                                    ],
                                ),
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
                render_pilihan()
                list_kasir.update()
                txt_total.value = "Rp 0"
                txt_info.value = f"Transaksi Rp {total_rp:,} selesai! Stok terpotong."
                txt_info.color = ACCENT_GREEN
                txt_total.update()
                txt_info.update()

        render_pilihan()

        return ft.Column(
            spacing=10,
            controls=[
                ft.Text("Kasir Cepat", size=16, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
                list_kasir,
                ft.Container(
                    bgcolor=BG_SECONDARY,
                    border_radius=12,
                    border=ft.Border.all(1, BORDER_COLOR),
                    padding=14,
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Column(spacing=2, controls=[txt_info, txt_total]),
                            ft.Button(
                                "Bayar",
                                bgcolor=PRIMARY,
                                color=BG_CARD,
                                on_click=bayar,
                            ),
                        ],
                    ),
                ),
            ],
        )

    def view_keuangan_analisis():
        notif = ft.Text("", size=12, color=ACCENT_GREEN)

        def klik_export(e):
            if on_export_excel:
                on_export_excel()
            else:
                notif.value = "Siap dihubungkan ke fungsi openpyxl export Excel!"
                notif.update()

        return ft.Column(
            spacing=10,
            controls=[
                ft.Text("Keuangan & Analisis", size=16, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
                ft.Row(
                    spacing=10,
                    controls=[
                        ft.Container(
                            expand=True,
                            bgcolor=BG_CARD,
                            border_radius=12,
                            border=ft.Border.all(1, BORDER_COLOR),
                            padding=14,
                            content=ft.Column(
                                spacing=4,
                                controls=[
                                    ft.Text("Pendapatan Hari Ini", size=12, color=TEXT_SECONDARY),
                                    ft.Text("Rp 450,000", size=18, weight=ft.FontWeight.BOLD, color=PRIMARY),
                                ],
                            ),
                        ),
                        ft.Container(
                            expand=True,
                            bgcolor=BG_CARD,
                            border_radius=12,
                            border=ft.Border.all(1, BORDER_COLOR),
                            padding=14,
                            content=ft.Column(
                                spacing=4,
                                controls=[
                                    ft.Text("Pesanan Selesai", size=12, color=TEXT_SECONDARY),
                                    ft.Text("18 Order", size=18, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
                                ],
                            ),
                        ),
                    ],
                ),
                ft.Container(
                    bgcolor=BG_SECONDARY,
                    border_radius=12,
                    border=ft.Border.all(1, BORDER_COLOR),
                    padding=14,
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text("Menu Terlaris: Paket Geprek Level 1-5", size=13, color=TEXT_PRIMARY),
                            ft.Text(
                                "Rata-rata: Rp 25,000",
                                size=13,
                                weight=ft.FontWeight.BOLD,
                                color=ACCENT_GOLD,
                            ),
                        ],
                    ),
                ),
                ft.Button(
                    "Export Excel (.xlsx)",
                    icon=ft.Icons.DOWNLOAD,
                    bgcolor=PRIMARY_HOVER,
                    color=BG_CARD,
                    on_click=klik_export,
                ),
                notif,
            ],
        )

    # 3. Grid 4 Fitur Utama (Pesanan, Menu, Kasir, Keuangan & Analisis)
    grid_fitur = ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, spacing=8)
    konten_aktif = ft.Container(content=view_pesanan())

    def render_grid():
        grid_fitur.controls.clear()
        for f in FITUR_UTAMA:
            aktif = tab_aktif["key"] == f["key"]
            kotak = ft.Container(
                width=62,
                height=62,
                top=6,
                left=7,
                bgcolor=BG_CARD if aktif else BG_SECONDARY,
                border_radius=16,
                border=ft.Border.all(2 if aktif else 1, PRIMARY if aktif else BORDER_COLOR),
                alignment=ft.Alignment(0, 0),
                content=ft.Icon(f["icon"], size=28, color=PRIMARY if aktif else TEXT_PRIMARY),
            )
            lapisan = [kotak]
            if f.get("badge"):
                lapisan.append(
                    ft.Container(
                        top=0,
                        right=2,
                        bgcolor=ACCENT_GREEN,
                        border_radius=8,
                        padding=ft.Padding.symmetric(horizontal=6, vertical=1),
                        content=ft.Text(f["badge"], size=10, weight=ft.FontWeight.BOLD, color=BG_CARD),
                    )
                )
            grid_fitur.controls.append(
                ft.Container(
                    expand=True,
                    ink=True,
                    border_radius=12,
                    on_click=lambda _, k=f["key"]: pilih_fitur(k),
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=4,
                        controls=[
                            ft.Stack(width=76, height=70, controls=lapisan),
                            ft.Text(
                                f["nama"],
                                size=12,
                                color=PRIMARY if aktif else TEXT_PRIMARY,
                                weight=ft.FontWeight.BOLD if aktif else ft.FontWeight.W_500,
                                text_align=ft.TextAlign.CENTER,
                            ),
                        ],
                    ),
                )
            )

    def pilih_fitur(key):
        tab_aktif["key"] = key
        views = {
            "pesanan": view_pesanan,
            "menu": view_menu,
            "kasir": view_kasir,
            "keuangan": view_keuangan_analisis,
        }
        konten_aktif.content = views[key]()
        render_grid()
        grid_fitur.update()
        konten_aktif.update()

    render_grid()

    return ft.Container(
        expand=True,
        bgcolor=BG_MAIN,
        padding=14,
        content=ft.Column(
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            spacing=14,
            controls=[
                kartu_status,
                grid_fitur,
                konten_aktif,
            ],
        ),
    )