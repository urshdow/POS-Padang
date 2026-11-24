import flet as ft

# Data contoh restoran (sudah dilengkapi menu & koordinat untuk tahap berikutnya)
DATA_RESTORAN = [
    {
        "id": "R01",
        "nama": "Ayam Geprek Juara",
        "kategori": "Ayam & Bebek",
        "rating": "4.8",
        "jarak": "1.2 km",
        "ongkir": 5000,
        "koordinat": (-7.9797, 112.6304),
        "menu": [
            {"nama": "Paket Geprek Level 1-5", "harga": 15000},
            {"nama": "Geprek Keju Lumer", "harga": 19000},
            {"nama": "Es Teh Jumbo", "harga": 4000},
        ],
    },
    {
        "id": "R02",
        "nama": "Nasi Goreng Kambing Kebon",
        "kategori": "Nasi & Mie",
        "rating": "4.9",
        "jarak": "2.0 km",
        "ongkir": 7000,
        "koordinat": (-7.9750, 112.6340),
        "menu": [
            {"nama": "Nasi Goreng Kambing Spesial", "harga": 25000},
            {"nama": "Nasi Goreng Ayam Kampung", "harga": 18000},
            {"nama": "Jeruk Hangat", "harga": 5000},
        ],
    },
    {
        "id": "R03",
        "nama": "Mie Ayam Pangsit Cak Min",
        "kategori": "Nasi & Mie",
        "rating": "4.7",
        "jarak": "0.8 km",
        "ongkir": 4000,
        "koordinat": (-7.9820, 112.6280),
        "menu": [
            {"nama": "Mie Ayam Bakso Urat", "harga": 16000},
            {"nama": "Mie Ayam Pangsit Goreng", "harga": 14000},
            {"nama": "Es Campur", "harga": 8000},
        ],
    },
    {
        "id": "R04",
        "nama": "Kopi Kenangan Mantan",
        "kategori": "Minuman",
        "rating": "4.8",
        "jarak": "1.5 km",
        "ongkir": 6000,
        "koordinat": (-7.9775, 112.6255),
        "menu": [
            {"nama": "Es Kopi Susu Gula Aren", "harga": 18000},
            {"nama": "Matcha Latte", "harga": 22000},
            {"nama": "Roti Bakar Cokelat Keju", "harga": 15000},
        ],
    },
]


def buat_beranda_user(on_pilih_resto):
    kategori_aktif = "Semua"
    daftar_kartu_resto = ft.Column(spacing=12)

    # Fungsi untuk memperbarui tampilan daftar restoran sesuai pencarian & kategori
    def perbarui_daftar(kata_kunci=""):
        daftar_kartu_resto.controls.clear()
        kata_kunci = kata_kunci.lower().strip()

        for resto in DATA_RESTORAN:
            cocok_kategori = (
                kategori_aktif == "Semua" or resto["kategori"] == kategori_aktif
            )
            cocok_nama = kata_kunci in resto["nama"].lower()

            if cocok_kategori and cocok_nama:
                kartu = ft.Container(
                    bgcolor="#d95d39",
                    border_radius=12,
                    padding=14,
                    ink=True,
                    on_click=lambda e, r=resto: on_pilih_resto(r),
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Row(
                                spacing=12,
                                controls=[
                                    ft.Container(
                                        width=52,
                                        height=52,
                                        bgcolor="#FFFFFF",
                                        border_radius=10,
                                        alignment=ft.Alignment.CENTER,
                                        content=ft.Icon(
                                            ft.Icons.RESTAURANT,
                                            color="#d95d39",
                                            size=28,
                                        ),
                                    ),
                                    ft.Column(
                                        spacing=4,
                                        controls=[
                                            ft.Text(
                                                resto["nama"],
                                                size=15,
                                                weight=ft.FontWeight.BOLD,
                                                color="white",
                                            ),
                                            ft.Text(
                                                resto["kategori"],
                                                size=12,
                                                color="#ffffff",
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
                                                        f"{resto['rating']}  •  {resto['jarak']}  •  Ongkir Rp {resto['ongkir']:,}",
                                                        size=12,
                                                        color="#CBD5E1",
                                                    ),
                                                ],
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                            ft.Icon(
                                ft.Icons.CHEVRON_RIGHT,
                                color="#94A3B8",
                            ),
                        ],
                    ),
                )
                daftar_kartu_resto.controls.append(kartu)

        if not daftar_kartu_resto.controls:
            daftar_kartu_resto.controls.append(
                ft.Text(
                    "Restoran tidak ditemukan.",
                    color="#94A3B8",
                    italic=True,
                )
            )

    # Kotak pencarian
    input_cari = ft.TextField(
        hint_text="Cari nama restoran...",
        prefix_icon=ft.Icons.SEARCH,
        border_radius=12,
        bgcolor="#efe7dc",
        color="white",
        on_change=lambda e: (perbarui_daftar(e.control.value), daftar_kartu_resto.update()),
    )

    # Tombol filter kategori
    def pilih_kategori(kat):
        nonlocal kategori_aktif
        kategori_aktif = kat
        perbarui_daftar(input_cari.value)
        daftar_kartu_resto.update()

    daftar_kategori = ["Semua", "Ayam & Bebek", "Nasi & Mie", "Minuman"]
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

    # Muat daftar restoran pertama kali saat halaman dibuka
    perbarui_daftar()

    return ft.Column(
        expand=True,
        scroll=ft.ScrollMode.AUTO,
        spacing=14,
        controls=[
            input_cari,
            baris_kategori,
            ft.Text(
                "Rekomendasi Restoran Terdekat",
                size=16,
                weight=ft.FontWeight.BOLD,
                color="#2d241e",
            ),
            daftar_kartu_resto,
        ],
    )