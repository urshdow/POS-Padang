import flet as ft

RESTORAN_AKTIF = {
    "id": "R01",
    "nama": 'Warung Padang Sederhana',
    "kategori": "Masakan Padang",
    "rating": "4.8",
    "jarak": "1.2 km",
    "ongkir": 5000,
    "koordinat": (-7.9797, 112.6304),
    "menu": [
        {"id": "M01", "nama": "Rendang Daging", "kategori": "Daging", "harga": 22000},
        {"id": "M02", "nama": "Ayam Pop", "kategori": "Ayam", "harga": 20000},
        {"id": "M03", "nama": "Dendeng Balado", "kategori": "Daging", "harga": 21000},
        {"id": "M04", "nama": "Gulai Kepala Kakap", "kategori": "Ikan", "harga": 28000},
        {"id": "M05", "nama": "Telur Dadar Padang", "kategori": "Telur", "harga": 10000},
        {"id": "M06", "nama": "Daun Singkong & Sambal", "kategori": "Pelengkap", "harga": 6000},
    ],
}


def buat_beranda_user(on_checkout=None):
    kategori_aktif = "Semua"
    keranjang = {}  # {menu_id: jumlah}

    daftar_kartu_menu = ft.Column(spacing=12)
    teks_ringkasan = ft.Text(
        "0 item  •  Total: Rp 0",
        size=14,
        weight=ft.FontWeight.BOLD,
        color="white",
    )

    def hitung_ringkasan():
        total_item = sum(keranjang.values())
        subtotal = 0
        for item in RESTORAN_AKTIF["menu"]:
            jumlah = keranjang.get(item["id"], 0)
            subtotal += item["harga"] * jumlah

        total_bayar = subtotal + RESTORAN_AKTIF["ongkir"] if total_item > 0 else 0
        teks_ringkasan.value = (
            f"{total_item} item  •  Subtotal Rp {subtotal:,}  •  "
            f"Total (+Ongkir Rp {RESTORAN_AKTIF['ongkir']:,} jika ada): Rp {total_bayar:,}"
        )

    def ubah_jumlah(menu_id, delta):
        jumlah_baru = keranjang.get(menu_id, 0) + delta
        if jumlah_baru <= 0:
            keranjang.pop(menu_id, None)
        else:
            keranjang[menu_id] = jumlah_baru
        hitung_ringkasan()
        perbarui_daftar_menu(input_cari.value)
        daftar_kartu_menu.update()
        teks_ringkasan.update()

    def perbarui_daftar_menu(kata_kunci=""):
        daftar_kartu_menu.controls.clear()
        kata_kunci = kata_kunci.lower().strip()

        for menu in RESTORAN_AKTIF["menu"]:
            cocok_kategori = (
                kategori_aktif == "Semua" or menu["kategori"] == kategori_aktif
            )
            cocok_nama = (
                kata_kunci in menu["nama"].lower()
                or kata_kunci in menu["kategori"].lower()
            )

            if cocok_kategori and cocok_nama:
                menu_id = menu["id"]
                jumlah = keranjang.get(menu_id, 0)

                kartu = ft.Container(
                    bgcolor="#d95d39",
                    border_radius=12,
                    padding=14,
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Column(
                                spacing=4,
                                expand=True,
                                controls=[
                                    ft.Text(
                                        menu["nama"],
                                        size=15,
                                        weight=ft.FontWeight.BOLD,
                                        color="white",
                                    ),
                                    ft.Text(
                                        menu["kategori"],
                                        size=12,
                                        color="#FDE8E1",
                                    ),
                                    ft.Text(
                                        f"Rp {menu['harga']:,}",
                                        size=13,
                                        weight=ft.FontWeight.BOLD,
                                        color="#FACC15",
                                    ),
                                ],
                            ),
                            ft.Row(
                                spacing=8,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    ft.IconButton(
                                        icon=ft.Icons.REMOVE_CIRCLE_OUTLINE,
                                        icon_color="white",
                                        disabled=jumlah == 0,
                                        on_click=lambda e, mid=menu_id: ubah_jumlah(mid, -1),
                                    ),
                                    ft.Text(
                                        str(jumlah),
                                        size=14,
                                        weight=ft.FontWeight.BOLD,
                                        color="white",
                                    ),
                                    ft.IconButton(
                                        icon=ft.Icons.ADD_CIRCLE_OUTLINE,
                                        icon_color="white",
                                        on_click=lambda e, mid=menu_id: ubah_jumlah(mid, 1),
                                    ),
                                ],
                            ),
                        ],
                    ),
                )
                daftar_kartu_menu.controls.append(kartu)

        if not daftar_kartu_menu.controls:
            daftar_kartu_menu.controls.append(
                ft.Text(
                    "Menu tidak ditemukan.",
                    color="#94A3B8",
                    italic=True,
                )
            )

    # Header informasi satu restoran
    header_resto = ft.Container(
        bgcolor="#2d241e",
        border_radius=12,
        padding=14,
        content=ft.Row(
            spacing=12,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    width=52,
                    height=52,
                    bgcolor="#d95d39",
                    border_radius=10,
                    alignment=ft.Alignment.CENTER,
                    content=ft.Icon(
                        ft.Icons.RESTAURANT_MENU,
                        color="white",
                        size=28,
                    ),
                ),
                ft.Column(
                    spacing=4,
                    expand=True,
                    controls=[
                        ft.Text(
                            RESTORAN_AKTIF["nama"],
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color="white",
                        ),
                        ft.Text(
                            RESTORAN_AKTIF["kategori"],
                            size=12,
                            color="#E2E8F0",
                        ),
                        ft.Row(
                            spacing=6,
                            controls=[
                                ft.Icon(
                                    ft.Icons.STAR,
                                    color="#FACC15",
                                    size=14,
                                ),
                                ft.Text(
                                    f"{RESTORAN_AKTIF['rating']}  •  {RESTORAN_AKTIF['jarak']}  •  Ongkir Rp {RESTORAN_AKTIF['ongkir']:,}",
                                    size=12,
                                    color="#CBD5E1",
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        ),
    )

    # Kotak pencarian menu
    input_cari = ft.TextField(
        hint_text="Cari menu makanan...",
        prefix_icon=ft.Icons.SEARCH,
        border_radius=12,
        bgcolor="#efe7dc",
        color="#2d241e",
        on_change=lambda e: (
            perbarui_daftar_menu(e.control.value),
            daftar_kartu_menu.update(),
        ),
    )

    # Filter kategori menu
    def pilih_kategori(kat):
        nonlocal kategori_aktif
        kategori_aktif = kat
        perbarui_daftar_menu(input_cari.value)
        daftar_kartu_menu.update()

    daftar_kategori = ["Semua", "Daging", "Ayam", "Ikan", "Telur", "Pelengkap"]
    baris_kategori = ft.Row(
        scroll=ft.ScrollMode.AUTO,
        spacing=8,
        controls=[
            ft.Button(
                kat,
                bgcolor="#d95d39",
                color="white",
                on_click=lambda e, k=kat: pilih_kategori(k),
            )
            for kat in daftar_kategori
        ],
    )

    # Bar ringkasan pesanan di bawah
    bar_pesanan = ft.Container(
        bgcolor="#2d241e",
        border_radius=12,
        padding=14,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(expand=True, content=teks_ringkasan),
                ft.Button(
                    "Pesan",
                    bgcolor="#d95d39",
                    color="white",
                    on_click=lambda e: on_checkout(keranjang) if on_checkout else None,
                ),
            ],
        ),
    )

    hitung_ringkasan()
    perbarui_daftar_menu()

    return ft.Column(
        expand=True,
        scroll=ft.ScrollMode.AUTO,
        spacing=14,
        controls=[
            header_resto,
            input_cari,
            baris_kategori,
            ft.Text(
                "Daftar Menu",
                size=16,
                weight=ft.FontWeight.BOLD,
                color="#2d241e",
            ),
            daftar_kartu_menu,
            bar_pesanan,
        ],
    )