import flet as ft

# Data contoh pesanan masuk & stok menu untuk tampilan awal penjual
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


def buat_beranda_penjual(on_export_excel=None):
    # 1. Sakelar Status Toko (Buka / Tutup)
    label_status_toko = ft.Text("Toko Sedang BUKA", weight=ft.FontWeight.BOLD, color="#4ADE80")

    def ubah_status_toko(e):
        if e.control.value:
            label_status_toko.value = "Toko Sedang BUKA"
            label_status_toko.color = "#4ADE80"
        else:
            label_status_toko.value = "Toko TUTUP Sementara"
            label_status_toko.color = "#F87171"
        label_status_toko.update()

    kartu_status_toko = ft.Container(
        bgcolor="#1E293B",
        border_radius=12,
        padding=14,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Row(
                    spacing=10,
                    controls=[
                        ft.Icon(ft.Icons.STOREFRONT, color="#FB923C", size=26),
                        label_status_toko,
                    ],
                ),
                ft.Switch(value=True, active_color="#4ADE80", on_change=ubah_status_toko),
            ],
        ),
    )

    # 2. Kartu Ringkasan Pendapatan & Order Hari Ini
    ringkasan_hari_ini = ft.Row(
        spacing=10,
        controls=[
            ft.Container(
                expand=True,
                bgcolor="#1E293B",
                border_radius=12,
                padding=14,
                content=ft.Column(
                    spacing=4,
                    controls=[
                        ft.Text("Pendapatan Hari Ini", size=12, color="#94A3B8"),
                        ft.Text("Rp 450,000", size=18, weight=ft.FontWeight.BOLD, color="#FB923C"),
                    ],
                ),
            ),
            ft.Container(
                expand=True,
                bgcolor="#1E293B",
                border_radius=12,
                padding=14,
                content=ft.Column(
                    spacing=4,
                    controls=[
                        ft.Text("Pesanan Selesai", size=12, color="#94A3B8"),
                        ft.Text("18 Order", size=18, weight=ft.FontWeight.BOLD, color="white"),
                    ],
                ),
            ),
        ],
    )

    # 3. Tombol Aksi Cepat (Export Laporan Excel & Tambah Menu)
    notifikasi_aksi = ft.Text("", size=12, color="#38BDF8")

    def klik_export(e):
        if on_export_excel:
            on_export_excel()
        else:
            notifikasi_aksi.value = "Siap dihubungkan ke fungsi openpyxl export Excel!"
            notifikasi_aksi.update()

    baris_aksi = ft.Row(
        spacing=10,
        controls=[
            ft.Button(
                "Export Excel (.xlsx)",
                icon=ft.Icons.DOWNLOAD,
                expand=True,
                on_click=klik_export,
            ),
        ],
    )

    # 4. Daftar Pesanan Masuk
    daftar_pesanan_col = ft.Column(spacing=10)

    def muat_pesanan():
        daftar_pesanan_col.controls.clear()
        for order in DATA_PESANAN_MASUK:
            teks_status = ft.Text(order["status"], size=12, color="#FACC15", weight=ft.FontWeight.BOLD)

            def proses_order(e, o=order, lbl=teks_status):
                o["status"] = "Siap Diambil Driver"
                lbl.value = o["status"]
                lbl.color = "#4ADE80"
                e.control.disabled = True
                e.control.text = "Sudah Diproses"
                lbl.update()
                e.control.update()

            kartu_order = ft.Container(
                bgcolor="#1E293B",
                border_radius=12,
                padding=14,
                content=ft.Column(
                    spacing=6,
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text(f"{order['kode']} • {order['pembeli']}", weight=ft.FontWeight.BOLD, color="white"),
                                teks_status,
                            ],
                        ),
                        ft.Text(order["item"], size=13, color="#CBD5E1"),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text(f"Total: Rp {order['total']:,}", weight=ft.FontWeight.BOLD, color="#FB923C"),
                                ft.Button("Terima & Siapkan", on_click=proses_order),
                            ],
                        ),
                    ],
                ),
            )
            daftar_pesanan_col.controls.append(kartu_order)

    # 5. Daftar Stok Menu Toko
    daftar_menu_col = ft.Column(spacing=8)
    for menu in DATA_MENU_TOKO:
        daftar_menu_col.controls.append(
            ft.Container(
                bgcolor="#1E293B",
                border_radius=10,
                padding=12,
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Column(
                            spacing=2,
                            controls=[
                                ft.Text(menu["nama"], weight=ft.FontWeight.BOLD, color="white"),
                                ft.Text(f"Rp {menu['harga']:,}", size=12, color="#94A3B8"),
                            ],
                        ),
                        ft.Text(f"Stok: {menu['stok']}", size=13, color="#4ADE80", weight=ft.FontWeight.BOLD),
                    ],
                ),
            )
        )

    muat_pesanan()

    return ft.Column(
        expand=True,
        scroll=ft.ScrollMode.AUTO,
        spacing=14,
        controls=[
            kartu_status_toko,
            ringkasan_hari_ini,
            baris_aksi,
            notifikasi_aksi,
            ft.Text("Pesanan Masuk", size=16, weight=ft.FontWeight.BOLD, color="white"),
            daftar_pesanan_col,
            ft.Text("Daftar Menu & Stok", size=16, weight=ft.FontWeight.BOLD, color="white"),
            daftar_menu_col,
        ],
    )