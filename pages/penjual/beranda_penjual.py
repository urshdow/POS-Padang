import flet as ft

DATA_PESANAN_MASUK = [
    {
        "kode": "ORD-1024",
        "pembeli": "Budi Santoso",
        "item": "2x Paket Nasi Rendang Spesial, 2x Es Teh Jumbo",
        "total": 68000,
        "status": "Menunggu Konfirmasi",
    },
    {
        "kode": "ORD-1025",
        "pembeli": "Siti Aminah",
        "item": "1x Paket Nasi Ayam Pop Komplit",
        "total": 30000,
        "status": "Sedang Dimasak",
    },
]

# Isi field "gambar" dengan path file lokal (misal: "assets/rendang.jpg") atau URL gambar
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

FITUR_UTAMA = [
    {"key": "pesanan", "nama": "Pesanan"},
    {"key": "menu", "nama": "Menu"},
    {"key": "kasir", "nama": "Kasir"},
    {"key": "keuangan", "nama": "Keuangan"},
]


class FullLayarContainer(ft.Container):
    def did_mount(self):
        try:
            if self.page:
                self.page.padding = 0
                self.page.spacing = 0
                self.page.bgcolor = "#FAF6F0"
                if self.page.views:
                    self.page.views[-1].padding = 0
                    self.page.views[-1].spacing = 0
                self.page.update()
        except Exception:
            pass


def buat_beranda_penjual(on_export_excel=None):
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

    def buat_kotak_gambar(src_gambar):
        if src_gambar:
            konten = ft.Image(src=src_gambar, width=64, height=64, border_radius=12)
        else:
            konten = ft.Icon(ft.Icons.RESTAURANT_MENU, size=24, color=ACCENT_GOLD)

        return ft.Container(
            width=64,
            height=64,
            bgcolor=BG_MAIN,
            border_radius=12,
            border=ft.Border.all(1, BORDER_COLOR),
            alignment=ft.Alignment(0, 0),
            content=konten,
        )

    def buat_tag(teks, bg, warna_teks):
        return ft.Container(
            bgcolor=bg,
            border_radius=10,
            padding=ft.Padding.symmetric(horizontal=7, vertical=2),
            content=ft.Text(teks, size=10, weight=ft.FontWeight.W_600, color=warna_teks),
        )

    def buat_tombol_stepper(ikon, warna, on_klik):
        return ft.Container(
            width=28,
            height=28,
            bgcolor=BG_MAIN,
            border_radius=8,
            border=ft.Border.all(1, BORDER_COLOR),
            alignment=ft.Alignment(0, 0),
            ink=True,
            on_click=on_klik,
            content=ft.Icon(ikon, size=16, color=warna),
        )

    # =========================================================================
    # 1. HEADER ATAS RINGKAS (TANPA TOMBOL LAPORAN & PESANAN)
    # =========================================================================
    lbl_status_toko = ft.Text("Toko BUKA", size=11, weight=ft.FontWeight.BOLD, color=ACCENT_GREEN)

    def ubah_status_toko(e):
        lbl_status_toko.value = "Toko BUKA" if e.control.value else "Toko TUTUP"
        lbl_status_toko.color = ACCENT_GREEN if e.control.value else PRIMARY
        lbl_status_toko.update()

    header_atas = ft.Container(
        bgcolor=BG_CARD,
        border=ft.Border.only(bottom=ft.BorderSide(1, BORDER_COLOR)),
        padding=ft.Padding.symmetric(horizontal=12, vertical=10),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
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
                                ft.Text(
                                    "RM Padang Sinar Minang",
                                    size=14,
                                    weight=ft.FontWeight.BOLD,
                                    color=TEXT_PRIMARY,
                                    max_lines=1,
                                    overflow=ft.TextOverflow.ELLIPSIS,
                                ),
                                ft.Row(
                                    spacing=5,
                                    controls=[
                                        ft.Text("Panel Penjual •", size=11, color=TEXT_SECONDARY),
                                        lbl_status_toko,
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
                ft.Switch(
                    value=True,
                    active_color=ACCENT_GREEN,
                    scale=0.85,
                    on_change=ubah_status_toko,
                ),
            ],
        ),
    )

    # =========================================================================
    # 2. BILAH TAB SEGMENTED PILL (4 MENU)
    # =========================================================================
    baris_tab = ft.Row(spacing=3)

    def render_tabs():
        baris_tab.controls.clear()
        for f in FITUR_UTAMA:
            aktif = tab_aktif["key"] == f["key"]
            baris_tab.controls.append(
                ft.Container(
                    expand=True,
                    bgcolor=PRIMARY if aktif else "transparent",
                    border_radius=20,
                    padding=ft.Padding.symmetric(vertical=8, horizontal=2),
                    alignment=ft.Alignment(0, 0),
                    ink=True,
                    on_click=lambda _, k=f["key"]: pilih_fitur(k),
                    content=ft.Text(
                        f["nama"],
                        size=11,
                        weight=ft.FontWeight.BOLD if aktif else ft.FontWeight.W_600,
                        color=BG_CARD if aktif else TEXT_PRIMARY,
                        text_align=ft.TextAlign.CENTER,
                        max_lines=1,
                    ),
                )
            )

    wadah_tab = ft.Container(
        bgcolor=BG_SECONDARY,
        border_radius=22,
        padding=3,
        content=baris_tab,
    )

    # =========================================================================
    # 3. KONTEN TAB (PESANAN, MENU, KASIR, KEUANGAN & ANALISIS)
    # =========================================================================
    def view_pesanan():
        kartu_list = []
        for order in DATA_PESANAN_MASUK:
            selesai = order["status"] == "Siap Diambil Driver"
            lbl_status = ft.Text(
                order["status"],
                size=10,
                weight=ft.FontWeight.BOLD,
                color=ACCENT_GREEN if selesai else ACCENT_GOLD,
            )

            def proses_order(e, o=order, lbl=lbl_status):
                o["status"] = "Siap Diambil Driver"
                lbl.value = o["status"]
                lbl.color = ACCENT_GREEN
                e.control.disabled = True
                e.control.text = "Sudah Siap"
                lbl.update()
                e.control.update()

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
                                    buat_kotak_gambar(""),
                                    ft.Column(
                                        expand=True,
                                        spacing=4,
                                        controls=[
                                            ft.Row(
                                                wrap=True,
                                                spacing=5,
                                                run_spacing=4,
                                                controls=[
                                                    buat_tag(order["kode"], BG_SECONDARY, TEXT_SECONDARY),
                                                    ft.Container(
                                                        bgcolor="#FEF3C7" if not selesai else "#DCFCE7",
                                                        border_radius=10,
                                                        padding=ft.Padding.symmetric(horizontal=7, vertical=2),
                                                        content=lbl_status,
                                                    ),
                                                ],
                                            ),
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
                                    ft.Button(
                                        "Sudah Siap" if selesai else "Terima & Siapkan",
                                        bgcolor=PRIMARY,
                                        color=BG_CARD,
                                        disabled=selesai,
                                        on_click=proses_order,
                                    ),
                                ],
                            ),
                        ],
                    ),
                )
            )
        return ft.Column(spacing=10, controls=kartu_list)

    def view_menu():
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
                                                run_spacing=4,
                                                controls=[
                                                    buat_tag(m["kategori"], BG_SECONDARY, TEXT_SECONDARY),
                                                    buat_tag(m["tag"], "#FEF3C7", "#B45309"),
                                                ],
                                            ),
                                            ft.Text(
                                                m["nama"],
                                                size=14,
                                                weight=ft.FontWeight.BOLD,
                                                color=TEXT_PRIMARY,
                                            ),
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
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    ft.Column(
                                        spacing=0,
                                        controls=[
                                            ft.Text("Harga", size=10, color=TEXT_SECONDARY),
                                            ft.Text(
                                                f"Rp {m['harga']:,}",
                                                size=14,
                                                weight=ft.FontWeight.BOLD,
                                                color=TEXT_PRIMARY,
                                            ),
                                        ],
                                    ),
                                    ft.Row(
                                        spacing=8,
                                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                        controls=[
                                            buat_tombol_stepper(
                                                ft.Icons.REMOVE,
                                                PRIMARY,
                                                lambda e, menu=m, lbl=lbl_stok: edit_stok(e, menu, -1, lbl),
                                            ),
                                            lbl_stok,
                                            buat_tombol_stepper(
                                                ft.Icons.ADD,
                                                ACCENT_GREEN,
                                                lambda e, menu=m, lbl=lbl_stok: edit_stok(e, menu, 1, lbl),
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                )
            )
        return ft.Column(spacing=10, controls=kartu_list)

    def view_kasir():
        keranjang = {i: 0 for i in range(len(DATA_MENU_TOKO))}
        txt_total = ft.Text("Rp 0", size=16, weight=ft.FontWeight.BOLD, color=PRIMARY)
        txt_info = ft.Text("0 item dipilih", size=11, color=TEXT_SECONDARY)
        list_kasir = ft.Column(spacing=10)

        def hitung_ulang():
            total_rp = sum(DATA_MENU_TOKO[i]["harga"] * qty for i, qty in keranjang.items())
            total_qty = sum(keranjang.values())
            txt_total.value = f"Rp {total_rp:,}"
            txt_info.value = f"{total_qty} item dipilih"
            txt_info.color = TEXT_SECONDARY
            txt_total.update()
            txt_info.update()

        def render_kasir():
            list_kasir.controls.clear()
            for i, m in enumerate(DATA_MENU_TOKO):
                qty_skrg = keranjang[i]

                def ubah_qty(e, idx=i, delta=1):
                    baru = keranjang[idx] + delta
                    if 0 <= baru <= DATA_MENU_TOKO[idx]["stok"]:
                        keranjang[idx] = baru
                        render_kasir()
                        list_kasir.update()
                        hitung_ulang()

                if qty_skrg == 0:
                    kontrol_kanan = ft.Button(
                        "+ Tambah",
                        bgcolor=PRIMARY,
                        color=BG_CARD,
                        disabled=m["stok"] == 0,
                        on_click=lambda e, idx=i: ubah_qty(e, idx, 1),
                    )
                else:
                    kontrol_kanan = ft.Row(
                        spacing=8,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            buat_tombol_stepper(
                                ft.Icons.REMOVE,
                                PRIMARY,
                                lambda e, idx=i: ubah_qty(e, idx, -1),
                            ),
                            ft.Text(
                                str(qty_skrg),
                                size=13,
                                weight=ft.FontWeight.BOLD,
                                color=PRIMARY,
                                width=18,
                                text_align=ft.TextAlign.CENTER,
                            ),
                            buat_tombol_stepper(
                                ft.Icons.ADD,
                                ACCENT_GREEN,
                                lambda e, idx=i: ubah_qty(e, idx, 1),
                            ),
                        ],
                    )

                list_kasir.controls.append(
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
                                                    run_spacing=4,
                                                    controls=[
                                                        buat_tag(m["kategori"], BG_SECONDARY, TEXT_SECONDARY),
                                                        buat_tag(
                                                            f"Stok: {m['stok']}",
                                                            "#DCFCE7" if m["stok"] > 0 else "#FEE2E2",
                                                            ACCENT_GREEN if m["stok"] > 0 else PRIMARY,
                                                        ),
                                                    ],
                                                ),
                                                ft.Text(
                                                    m["nama"],
                                                    size=14,
                                                    weight=ft.FontWeight.BOLD,
                                                    color=TEXT_PRIMARY,
                                                ),
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
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    controls=[
                                        ft.Column(
                                            spacing=0,
                                            controls=[
                                                ft.Text("Harga", size=10, color=TEXT_SECONDARY),
                                                ft.Text(
                                                    f"Rp {m['harga']:,}",
                                                    size=14,
                                                    weight=ft.FontWeight.BOLD,
                                                    color=TEXT_PRIMARY,
                                                ),
                                            ],
                                        ),
                                        kontrol_kanan,
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
                render_kasir()
                list_kasir.update()
                txt_total.value = "Rp 0"
                txt_info.value = f"Transaksi Rp {total_rp:,} selesai! Stok terpotong."
                txt_info.color = ACCENT_GREEN
                txt_total.update()
                txt_info.update()

        render_kasir()

        return ft.Column(
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
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Column(expand=True, spacing=1, controls=[txt_info, txt_total]),
                            ft.Button("Bayar", bgcolor=PRIMARY, color=BG_CARD, on_click=bayar),
                        ],
                    ),
                ),
            ],
        )

    def view_keuangan_analisis():
        notif = ft.Text("", size=11, color=ACCENT_GREEN)

        def klik_export(e):
            if on_export_excel:
                on_export_excel()
            else:
                notif.value = "Siap dihubungkan ke fungsi openpyxl export Excel!"
                notif.update()

        return ft.Column(
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
                                    ft.Text(
                                        "Keuangan & Analisis",
                                        size=14,
                                        weight=ft.FontWeight.BOLD,
                                        color=TEXT_PRIMARY,
                                    ),
                                    buat_tag("Hari Ini", "#FEF3C7", "#B45309"),
                                ],
                            ),
                            ft.Divider(height=1, color=BORDER_COLOR),
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                spacing=8,
                                controls=[
                                    ft.Text("Menu Terlaris", size=12, color=TEXT_SECONDARY),
                                    ft.Text(
                                        "Paket Nasi Rendang",
                                        expand=True,
                                        size=12,
                                        weight=ft.FontWeight.BOLD,
                                        color=ACCENT_GREEN,
                                        text_align=ft.TextAlign.RIGHT,
                                        max_lines=1,
                                        overflow=ft.TextOverflow.ELLIPSIS,
                                    ),
                                ],
                            ),
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                spacing=8,
                                controls=[
                                    ft.Text("Rata-rata Order", size=12, color=TEXT_SECONDARY),
                                    ft.Text(
                                        "Rp 25,000",
                                        size=12,
                                        weight=ft.FontWeight.BOLD,
                                        color=ACCENT_GOLD,
                                    ),
                                ],
                            ),
                        ],
                    ),
                ),
                ft.Row(
                    controls=[
                        ft.Button(
                            "Export Laporan Excel (.xlsx)",
                            icon=ft.Icons.DOWNLOAD,
                            expand=True,
                            bgcolor=PRIMARY_HOVER,
                            color=BG_CARD,
                            on_click=klik_export,
                        ),
                    ]
                ),
                notif,
            ],
        )

    # =========================================================================
    # 4. PENGATURAN NAVIGASI & FULL-SCREEN MOBILE CONTAINER
    # =========================================================================
    konten_aktif = ft.Container(expand=True, content=view_pesanan())

    def pilih_fitur(key):
        tab_aktif["key"] = key
        views = {
            "pesanan": view_pesanan,
            "menu": view_menu,
            "kasir": view_kasir,
            "keuangan": view_keuangan_analisis,
        }
        konten_aktif.content = views[key]()
        render_tabs()
        wadah_tab.update()
        konten_aktif.update()

    render_tabs()

    return FullLayarContainer(
        expand=True,
        margin=0,
        padding=0,
        bgcolor=BG_MAIN,
        content=ft.Column(
            expand=True,
            spacing=0,
            controls=[
                header_atas,
                ft.Container(
                    expand=True,
                    padding=ft.Padding.symmetric(horizontal=12, vertical=10),
                    content=ft.Column(
                        expand=True,
                        scroll=ft.ScrollMode.AUTO,
                        spacing=10,
                        controls=[
                            wadah_tab,
                            konten_aktif,
                        ],
                    ),
                ),
            ],
        ),
    )


if __name__ == "__main__":
    def main(page: ft.Page):
        page.title = "Panel Penjual"
        page.padding = 0
        page.spacing = 0
        page.bgcolor = "#FAF6F0"
        page.window.width = 390
        page.window.height = 844
        page.add(buat_beranda_penjual())

    ft.app(target=main)