import flet as ft


def format_rupiah(angka):
    """Mengubah angka menjadi format Rupiah."""
    return f"Rp {int(angka):,}".replace(",", ".")


def cari_menu(daftar_menu, menu_id):
    """Mencari informasi menu berdasarkan ID."""

    if isinstance(daftar_menu, dict):

        menu = daftar_menu.get(menu_id)

        if menu is None:
            menu = daftar_menu.get(str(menu_id))

        if menu is not None:
            menu = dict(menu)
            menu.setdefault("id", menu_id)
            return menu

        data_menu = daftar_menu.values()

    else:
        data_menu = daftar_menu

    for menu in data_menu:
        if str(menu.get("id", menu.get("menu_id"))) == str(menu_id):
            return menu

    return None


def tampilkan_keranjang(
    keranjang,
    daftar_menu,
    on_kembali=None,
    on_checkout=None
):
    """
    Menampilkan halaman keranjang pembeli.

    Parameters:
        keranjang: Dictionary {menu_id: jumlah}
        daftar_menu: Data seluruh menu
        on_kembali: Callback untuk kembali ke beranda
        on_checkout: Callback untuk melanjutkan checkout
    """

    root = ft.Container(
        expand=True,
        bgcolor="#F8F9FA",
        padding=20
    )

    def render():

        root.content = None

        daftar_item = []
        subtotal = 0
        jumlah_item = 0
        semua_menu_valid = True

        # Mengambil informasi setiap menu
        for menu_id, jumlah in list(keranjang.items()):

            try:
                jumlah = int(jumlah)
            except (ValueError, TypeError):
                jumlah = 0

            if jumlah <= 0:
                keranjang.pop(menu_id, None)
                continue

            menu = cari_menu(daftar_menu, menu_id)

            if menu is None:
                semua_menu_valid = False
                continue

            nama = menu.get(
                "nama",
                menu.get("nama_menu", menu.get("name", "Menu"))
            )

            harga = menu.get(
                "harga",
                menu.get("price", 0)
            )

            harga = int(
                str(harga).replace("Rp", "").replace(".", "").replace(",", "").strip()
                or 0
            )

            gambar = menu.get(
                "gambar",
                menu.get("image", menu.get("foto", ""))
            )

            total_item = harga * jumlah

            subtotal += total_item
            jumlah_item += jumlah

            daftar_item.append({
                "id": menu_id,
                "nama": nama,
                "harga": harga,
                "jumlah": jumlah,
                "total": total_item,
                "gambar": gambar
            })

        # Mengubah jumlah pesanan
        def ubah_jumlah(menu_id, perubahan):

            jumlah_sekarang = int(keranjang.get(menu_id, 0))
            jumlah_baru = jumlah_sekarang + perubahan

            if jumlah_baru <= 0:
                keranjang.pop(menu_id, None)
            else:
                keranjang[menu_id] = jumlah_baru

            render()

        # Menghapus menu
        def hapus_menu(menu_id):

            keranjang.pop(menu_id, None)

            render()

        # Membuat tampilan item
        item_controls = []

        for item in daftar_item:

            gambar = (
                ft.Image(
                    src=item["gambar"],
                    width=85,
                    height=85,
                    fit=ft.ImageFit.COVER
                )
                if item["gambar"]
                else ft.Container(
                    width=85,
                    height=85,
                    bgcolor="#E9ECEF",
                    border_radius=10,
                    content=ft.Text(
                        "Foto",
                        color="#6C757D"
                    ),
                    alignment=ft.Alignment.CENTER
                )
            )

            kartu = ft.Container(
                bgcolor="#FFFFFF",
                border_radius=12,
                padding=15,
                content=ft.Row(
                    controls=[
                        gambar,

                        ft.Column(
                            controls=[
                                ft.Text(
                                    item["nama"],
                                    size=16,
                                    weight=ft.FontWeight.BOLD
                                ),

                                ft.Text(
                                    format_rupiah(item["harga"]),
                                    color="#6C757D",
                                    size=13
                                ),

                                ft.Text(
                                    format_rupiah(item["total"]),
                                    color="#198754",
                                    weight=ft.FontWeight.BOLD
                                )
                            ],
                            expand=True,
                            spacing=5
                        ),

                        ft.Column(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.IconButton(
                                            icon=ft.Icons.REMOVE,
                                            disabled=item["jumlah"] <= 1,
                                            on_click=lambda e, mid=item["id"]:
                                                ubah_jumlah(mid, -1)
                                        ),

                                        ft.Text(
                                            str(item["jumlah"]),
                                            weight=ft.FontWeight.BOLD
                                        ),

                                        ft.IconButton(
                                            icon=ft.Icons.ADD,
                                            on_click=lambda e, mid=item["id"]:
                                                ubah_jumlah(mid, 1)
                                        )
                                    ],
                                    spacing=0
                                ),

                                ft.TextButton(
                                    "Hapus",
                                    on_click=lambda e, mid=item["id"]:
                                        hapus_menu(mid)
                                )
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=0
                        )
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                )
            )

            item_controls.append(kartu)

        # Header keranjang
        header = ft.Row(
            controls=[
                ft.TextButton(
                    "← Kembali",
                    on_click=lambda e: (
                        on_kembali() if on_kembali else None
                    )
                ),

                ft.Text(
                    "Keranjang Saya",
                    size=23,
                    weight=ft.FontWeight.BOLD
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

        # Jika keranjang kosong
        if not daftar_item:

            isi_keranjang = ft.Container(
                padding=40,
                alignment=ft.Alignment.CENTER,
                content=ft.Column(
                    controls=[
                        ft.Text(
                            "Keranjang masih kosong",
                            size=20,
                            weight=ft.FontWeight.BOLD
                        ),

                        ft.Text(
                            "Yuk, pilih makanan favoritmu terlebih dahulu!",
                            color="#6C757D"
                        ),

                        ft.ElevatedButton(
                            "Mulai Belanja",
                            on_click=lambda e: (
                                on_kembali() if on_kembali else None
                            )
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=15
                )
            )

        else:

            isi_keranjang = ft.Column(
                controls=item_controls,
                spacing=12,
                scroll=ft.ScrollMode.AUTO,
                expand=True
            )

        # Ringkasan pembayaran
        ringkasan = ft.Container(
            bgcolor="#FFFFFF",
            border_radius=12,
            padding=20,
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Ringkasan Pesanan",
                        size=18,
                        weight=ft.FontWeight.BOLD
                    ),

                    ft.Row(
                        controls=[
                            ft.Text("Jumlah Item"),

                            ft.Text(
                                str(jumlah_item),
                                weight=ft.FontWeight.BOLD
                            )
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),

                    ft.Divider(),

                    ft.Row(
                        controls=[
                            ft.Text(
                                "Subtotal",
                                size=16,
                                weight=ft.FontWeight.BOLD
                            ),

                            ft.Text(
                                format_rupiah(subtotal),
                                color="#198754",
                                size=18,
                                weight=ft.FontWeight.BOLD
                            )
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),

                    ft.ElevatedButton(
                        "Lanjut ke Checkout",
                        width=300,
                        disabled=(
                            not daftar_item
                            or not semua_menu_valid
                            or on_checkout is None
                        ),
                        on_click=lambda e: (
                            on_checkout(dict(keranjang))
                            if on_checkout else None
                        )
                    )
                ],
                spacing=12
            )
        )

        # Layout utama
        root.content = ft.Column(
            controls=[
                header,
                isi_keranjang,
                ringkasan
            ],
            spacing=20,
            expand=True
        )

    render()

    return root