import flet as ft

RESTORAN_AKTIF = {
    "id": "R01",
    "nama": "Warung Padang Sederhana",
    "kategori": "Masakan Padang",
    "rating": "4.8",
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

# Palet warna menyesuaikan hierarki gambar pertama
WARNA_BG = "#f7f5f0"          # Latar belakang halaman (krem sangat terang)
WARNA_CARD = "#ffffff"        # Permukaan kartu putih bersih
WARNA_BORDER = "#e5e0d8"      # Garis tepi halus kartu
WARNA_PRIMARY = "#d95d39"     # Aksen utama terakota/oranye bata
WARNA_PRIMARY_SOFT = "#faece6"# Latar ikon/badge lembut
WARNA_TEXT_DARK = "#1c1917"   # Teks utama gelap
WARNA_TEXT_MUTED = "#78716c"  # Teks sekunder abu-abu hangat


def buat_beranda_user(on_checkout=None, keranjang_awal=None):
    kategori_aktif = "Semua"
    keranjang = keranjang_awal if keranjang_awal is not None else {}

    daftar_kartu_menu = ft.Column(spacing=10)
    baris_kategori = ft.Row(scroll=ft.ScrollMode.AUTO, spacing=8)

    teks_ringkasan = ft.Text(
        "0 item  •  Total: Rp 0",
        size=13,
        weight=ft.FontWeight.BOLD,
        color=WARNA_TEXT_DARK,
    )

    def hitung_ringkasan():
        total_item = sum(keranjang.values())
        subtotal = 0
        for item in RESTORAN_AKTIF["menu"]:
            jumlah = keranjang.get(item["id"], 0)
            subtotal += item["harga"] * jumlah

        total_bayar = subtotal if total_item > 0 else 0
        teks_ringkasan.value = (
            f"{total_item} item  •  Subtotal Rp {subtotal:,}\n"
            f"Total: Rp {total_bayar:,}"
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
                    bgcolor=WARNA_CARD,
                    border=ft.Border.all(1, WARNA_BORDER),
                    border_radius=14,
                    padding=14,
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Row(
                                spacing=12,
                                expand=True,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    ft.Container(
                                        width=46,
                                        height=46,
                                        bgcolor=WARNA_PRIMARY_SOFT,
                                        border_radius=12,
                                        alignment=ft.Alignment.CENTER,
                                        content=ft.Icon(
                                            ft.Icons.RESTAURANT,
                                            color=WARNA_PRIMARY,
                                            size=22,
                                        ),
                                    ),
                                    ft.Column(
                                        spacing=3,
                                        expand=True,
                                        controls=[
                                            ft.Container(
                                                bgcolor="#f3efe9",
                                                padding=ft.Padding.symmetric(horizontal=8, vertical=2),
                                                border_radius=6,
                                                content=ft.Text(
                                                    menu["kategori"],
                                                    size=10,
                                                    weight=ft.FontWeight.W_600,
                                                    color=WARNA_TEXT_MUTED,
                                                ),
                                            ),
                                            ft.Text(
                                                menu["nama"],
                                                size=15,
                                                weight=ft.FontWeight.BOLD,
                                                color=WARNA_TEXT_DARK,
                                            ),
                                            ft.Text(
                                                f"Rp {menu['harga']:,}",
                                                size=13,
                                                weight=ft.FontWeight.BOLD,
                                                color=WARNA_PRIMARY,
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                            ft.Row(
                                spacing=4,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    ft.IconButton(
                                        icon=ft.Icons.REMOVE_CIRCLE_OUTLINE,
                                        icon_color=WARNA_TEXT_MUTED if jumlah == 0 else WARNA_PRIMARY,
                                        disabled=jumlah == 0,
                                        on_click=lambda e, mid=menu_id: ubah_jumlah(mid, -1),
                                    ),
                                    ft.Text(
                                        str(jumlah),
                                        size=14,
                                        weight=ft.FontWeight.BOLD,
                                        color=WARNA_TEXT_DARK,
                                    ),
                                    ft.IconButton(
                                        icon=ft.Icons.ADD_CIRCLE_OUTLINE,
                                        icon_color=WARNA_PRIMARY,
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
                    color=WARNA_TEXT_MUTED,
                    italic=True,
                )
            )

    # Header informasi restoran
    header_resto = ft.Container(
        bgcolor=WARNA_CARD,
        border=ft.Border.all(1, WARNA_BORDER),
        border_radius=14,
        padding=14,
        content=ft.Row(
            spacing=12,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    width=50,
                    height=50,
                    bgcolor=WARNA_PRIMARY,
                    border_radius=12,
                    alignment=ft.Alignment.CENTER,
                    content=ft.Icon(
                        ft.Icons.STOREFRONT,
                        color="white",
                        size=26,
                    ),
                ),
                ft.Column(
                    spacing=3,
                    expand=True,
                    controls=[
                        ft.Text(
                            RESTORAN_AKTIF["nama"],
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color=WARNA_TEXT_DARK,
                        ),
                        ft.Row(
                            spacing=5,
                            controls=[
                                ft.Text(
                                    RESTORAN_AKTIF["kategori"],
                                    size=12,
                                    color=WARNA_TEXT_MUTED,
                                ),
                                ft.Text("•", size=12, color=WARNA_TEXT_MUTED),
                                ft.Icon(ft.Icons.STAR, color="#eab308", size=14),
                                ft.Text(
                                    f"{RESTORAN_AKTIF['rating']} • {RESTORAN_AKTIF['jarak']} • Ongkir Rp {RESTORAN_AKTIF['ongkir']:,}",
                                    size=12,
                                    weight=ft.FontWeight.W_500,
                                    color="#15803d",
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
        hint_style=ft.TextStyle(color=WARNA_TEXT_MUTED, size=14),
        prefix_icon=ft.Icons.SEARCH,
        border_radius=12,
        bgcolor=WARNA_CARD,
        border_color=WARNA_BORDER,
        focused_border_color=WARNA_PRIMARY,
        color=WARNA_TEXT_DARK,
        on_change=lambda e: (
            perbarui_daftar_menu(e.control.value),
            daftar_kartu_menu.update(),
        ),
    )

    # Filter kategori menu
    daftar_kategori = ["Semua", "Daging", "Ayam", "Ikan", "Telur", "Pelengkap"]

    def render_kategori():
        baris_kategori.controls = [
            ft.Button(
                kat,
                bgcolor=WARNA_PRIMARY if kat == kategori_aktif else WARNA_CARD,
                color="white" if kat == kategori_aktif else WARNA_TEXT_DARK,
                elevation=0,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=10),
                    side=ft.BorderSide(
                        1, WARNA_PRIMARY if kat == kategori_aktif else WARNA_BORDER
                    ),
                ),
                on_click=lambda e, k=kat: pilih_kategori(k),
            )
            for kat in daftar_kategori
        ]

    def pilih_kategori(kat):
        nonlocal kategori_aktif
        kategori_aktif = kat
        render_kategori()
        perbarui_daftar_menu(input_cari.value)
        baris_kategori.update()
        daftar_kartu_menu.update()

    # Bar ringkasan pesanan di bawah
    bar_pesanan = ft.Container(
        bgcolor=WARNA_CARD,
        border=ft.Border.all(1, WARNA_BORDER),
        border_radius=14,
        padding=14,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(expand=True, content=teks_ringkasan),
                ft.Button(
                    "Pesan",
                    bgcolor=WARNA_PRIMARY,
                    color="white",
                    elevation=0,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=10),
                        padding=ft.Padding.symmetric(horizontal=20, vertical=12),
                    ),
                    on_click=lambda e: on_checkout(keranjang) if on_checkout else None,
                ),
            ],
        ),
    )

    render_kategori()
    hitung_ringkasan()
    perbarui_daftar_menu()

    return ft.Container(
        expand=True,
        bgcolor=WARNA_BG,
        padding=14,
        content=ft.Column(
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
                    color=WARNA_TEXT_DARK,
                ),
                daftar_kartu_menu,
                bar_pesanan,
            ],
        ),
    )