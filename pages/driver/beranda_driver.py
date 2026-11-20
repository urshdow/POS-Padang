<<<<<<< HEAD
import flet as ft

# Data contoh orderan yang siap diambil driver
DATA_ORDER_TERSEDIA = [
    {
        "kode": "ORD-1024",
        "resto": "Ayam Geprek Juara",
        "alamat_antar": "Jl. Veteran No. 12, Malang",
        "jarak": "1.2 km",
        "ongkir": 5000,
        "koordinat_tujuan": "-7.9839,112.6214",
    },
    {
        "kode": "ORD-1026",
        "resto": "Mie Ayam Pangsit Cak Min",
        "alamat_antar": "Jl. Soekarno Hatta Kav. 8",
        "jarak": "2.4 km",
        "ongkir": 8000,
        "koordinat_tujuan": "-7.9465,112.6156",
    },
]


def buat_beranda_driver(page: ft.Page = None):
    status_online = True
    order_aktif = None
    total_pendapatan = 45000
    jumlah_trip = 6

    # 1. Sakelar Status Driver (Online / Offline)
    label_status = ft.Text(
        "Status: ONLINE (Siap Terima Order)",
        weight=ft.FontWeight.BOLD,
        color="#4ADE80",
    )

    def ubah_status_driver(e):
        nonlocal status_online
        status_online = e.control.value
        if status_online:
            label_status.value = "Status: ONLINE (Siap Terima Order)"
            label_status.color = "#4ADE80"
        else:
            label_status.value = "Status: OFFLINE (Istirahat)"
            label_status.color = "#F87171"
        label_status.update()
        perbarui_tampilan_order()

    kartu_status = ft.Container(
        bgcolor="#1E293B",
        border_radius=12,
        padding=14,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Row(
                    spacing=10,
                    controls=[
                        ft.Icon(ft.Icons.TWO_WHEELER, color="#4ADE80", size=28),
                        label_status,
                    ],
                ),
                ft.Switch(value=True, active_color="#4ADE80", on_change=ubah_status_driver),
            ],
        ),
    )

    # 2. Kartu Ringkasan Pendapatan & Trip Hari Ini
    teks_pendapatan = ft.Text(
        f"Rp {total_pendapatan:,}",
        size=18,
        weight=ft.FontWeight.BOLD,
        color="#4ADE80",
    )
    teks_trip = ft.Text(
        f"{jumlah_trip} Trip",
        size=18,
        weight=ft.FontWeight.BOLD,
        color="white",
    )

    ringkasan_driver = ft.Row(
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
                        teks_pendapatan,
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
                        ft.Text("Pengantaran Selesai", size=12, color="#94A3B8"),
                        teks_trip,
                    ],
                ),
            ),
        ],
    )

    # 3. Wadah Order Aktif & Daftar Order Tersedia
    wadah_order_aktif = ft.Column(spacing=10)
    wadah_order_tersedia = ft.Column(spacing=10)

    def ambil_order(data_order):
        nonlocal order_aktif
        order_aktif = data_order
        DATA_ORDER_TERSEDIA.remove(data_order)
        perbarui_tampilan_order()

    def selesaikan_order(e):
        nonlocal order_aktif, total_pendapatan, jumlah_trip
        if order_aktif:
            total_pendapatan += order_aktif["ongkir"]
            jumlah_trip += 1
            teks_pendapatan.value = f"Rp {total_pendapatan:,}"
            teks_trip.value = f"{jumlah_trip} Trip"
            teks_pendapatan.update()
            teks_trip.update()
            order_aktif = None
            perbarui_tampilan_order()

    def buka_google_maps(koordinat):
        url = f"https://www.google.com/maps/dir/?api=1&destination={koordinat}"
        if page:
            page.launch_url(url)

    def perbarui_tampilan_order():
        wadah_order_aktif.controls.clear()
        wadah_order_tersedia.controls.clear()

        # Tampilkan kartu pengantaran jika driver sedang membawa orderan
        if order_aktif:
            wadah_order_aktif.controls.append(
                ft.Text("Sedang Diantar", size=16, weight=ft.FontWeight.BOLD, color="#38BDF8")
            )
            wadah_order_aktif.controls.append(
                ft.Container(
                    bgcolor="#0F2942",
                    border=ft.border.all(1, "#38BDF8"),
                    border_radius=12,
                    padding=14,
                    content=ft.Column(
                        spacing=8,
                        controls=[
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Text(
                                        f"Order {order_aktif['kode']}",
                                        weight=ft.FontWeight.BOLD,
                                        color="#38BDF8",
                                    ),
                                    ft.Text(
                                        f"+Rp {order_aktif['ongkir']:,}",
                                        weight=ft.FontWeight.BOLD,
                                        color="#4ADE80",
                                    ),
                                ],
                            ),
                            ft.Text(f"Ambil di: {order_aktif['resto']}", color="white", weight=ft.FontWeight.BOLD),
                            ft.Text(f"Antar ke: {order_aktif['alamat_antar']}", size=13, color="#CBD5E1"),
                            ft.Row(
                                spacing=8,
                                controls=[
                                    ft.Button(
                                        "Buka Maps",
                                        icon=ft.Icons.NAVIGATION,
                                        on_click=lambda e, k=order_aktif["koordinat_tujuan"]: buka_google_maps(k),
                                    ),
                                    ft.Button(
                                        "Selesai Antar",
                                        icon=ft.Icons.CHECK_CIRCLE,
                                        on_click=selesaikan_order,
                                    ),
                                ],
                            ),
                        ],
                    ),
                )
            )

        # Cek status Online/Offline untuk daftar order masuk
        if not status_online:
            wadah_order_tersedia.controls.append(
                ft.Text(
                    "Aktifkan status ONLINE di atas untuk mulai menerima orderan.",
                    color="#94A3B8",
                    italic=True,
                )
            )
        elif not DATA_ORDER_TERSEDIA:
            wadah_order_tersedia.controls.append(
                ft.Text("Belum ada orderan baru di sekitarmu.", color="#94A3B8", italic=True)
            )
        else:
            for item in DATA_ORDER_TERSEDIA:
                kartu = ft.Container(
                    bgcolor="#1E293B",
                    border_radius=12,
                    padding=14,
                    content=ft.Column(
                        spacing=6,
                        controls=[
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Text(item["resto"], weight=ft.FontWeight.BOLD, color="white"),
                                    ft.Text(
                                        f"Ongkir Rp {item['ongkir']:,}",
                                        weight=ft.FontWeight.BOLD,
                                        color="#4ADE80",
                                    ),
                                ],
                            ),
                            ft.Text(
                                f"Tujuan: {item['alamat_antar']} ({item['jarak']})",
                                size=12,
                                color="#CBD5E1",
                            ),
                            ft.Button(
                                "Ambil Order",
                                disabled=order_aktif is not None,
                                on_click=lambda e, o=item: ambil_order(o),
                            ),
                        ],
                    ),
                )
                wadah_order_tersedia.controls.append(kartu)

        wadah_order_aktif.update()
        wadah_order_tersedia.update()

    # Inisialisasi tampilan pertama kali (tanpa .update() sebelum masuk page)
    for item in DATA_ORDER_TERSEDIA:
        wadah_order_tersedia.controls.append(
            ft.Container(
                bgcolor="#1E293B",
                border_radius=12,
                padding=14,
                content=ft.Column(
                    spacing=6,
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text(item["resto"], weight=ft.FontWeight.BOLD, color="white"),
                                ft.Text(
                                    f"Ongkir Rp {item['ongkir']:,}",
                                    weight=ft.FontWeight.BOLD,
                                    color="#4ADE80",
                                ),
                            ],
                        ),
                        ft.Text(
                            f"Tujuan: {item['alamat_antar']} ({item['jarak']})",
                            size=12,
                            color="#CBD5E1",
                        ),
                        ft.Button(
                            "Ambil Order",
                            on_click=lambda e, o=item: ambil_order(o),
                        ),
                    ],
                ),
            )
        )

    return ft.Column(
        expand=True,
        scroll=ft.ScrollMode.AUTO,
        spacing=14,
        controls=[
            kartu_status,
            ringkasan_driver,
            wadah_order_aktif,
            ft.Text("Orderan Siap Jemput", size=16, weight=ft.FontWeight.BOLD, color="white"),
            wadah_order_tersedia,
        ],
    )

