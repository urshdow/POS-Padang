import flet as ft
from pages.auth.login import buat_halaman_login
from pages.user.beranda_user import RESTORAN_AKTIF, buat_beranda_user
from pages.user.keranjang_pembeli import tampilkan_keranjang
from pages.penjual.beranda_penjual import buat_beranda_penjual

def main(page: ft.Page):
    page.title = "Padang"
    page.window.width = 400
    page.window.height = 800
    page.bgcolor = "#faf6f0"

    def keluar_akun(e):
        tampilkan_login()

    def lanjut_checkout(keranjang: dict[str, int]):
        print("Pesanan dipilih:", keranjang)

    def tampilkan_beranda_user(keranjang=None):
        page.clean()
        page.add(
            buat_beranda_user(
                on_checkout=buka_keranjang,
                keranjang_awal=keranjang,
            )
        )

    def buka_keranjang(keranjang: dict[str, int]):
        page.clean()
        page.add(
            tampilkan_keranjang(
                keranjang,
                RESTORAN_AKTIF["menu"],
                on_kembali=lambda: tampilkan_beranda_user(keranjang),
                on_checkout=lanjut_checkout,
            )
        )

    def buka_beranda_role(role: str, nama_user: str):
        page.clean()

        if role == "user":
            page.appbar = ft.AppBar(
                title=ft.Text(f"Halo, {nama_user}", color="black"),
                bgcolor="#faf6f0",
                actions=[
                    ft.IconButton(
                        ft.Icons.LOGOUT,
                        icon_color="black",
                        tooltip="Logout",
                        on_click=keluar_akun,
                    )
                ],
            )
            tampilkan_beranda_user()
            return
        else:
            page.appbar = ft.AppBar(
                title=ft.Text(f"Toko: {nama_user}", color="black"),
                    bgcolor="#faf6f0",
                        actions=[
                            ft.IconButton(
                        ft.Icons.LOGOUT,
                        icon_color="black",
                        tooltip="Logout",
                        on_click=keluar_akun,
                    )
                ],
            )
            konten = buat_beranda_penjual()
            page.add(konten)
            return
        
    def tampilkan_login():
        page.clean()
        page.appbar = None
        page.add(buat_halaman_login(on_login_success=buka_beranda_role))

    # Mulai dari halaman login
    tampilkan_login()

ft.run(main, assets_dir="assets", view=ft.AppView.FLET_APP)