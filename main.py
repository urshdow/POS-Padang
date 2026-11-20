import flet as ft
from pages.auth.login import buat_halaman_login
from pages.user.beranda_user import buat_beranda_user
from pages.penjual.beranda_penjual import buat_beranda_penjual
from pages.driver.beranda_driver import buat_beranda_driver

def main(page: ft.Page):
    page.title = "Wareg Express"
    page.window.width = 400
    page.window.height = 800
    page.theme_mode = ft.ThemeMode.SYSTEM

    def keluar_akun(e):
        tampilkan_login()

    def buka_detail_resto(data_resto):
        print("Restoran dipilih:", data_resto["nama"])

    def buka_beranda_role(role: str, nama_user: str):
        page.clean()

        if role == "user":
            page.appbar = ft.AppBar(
                title=ft.Text(f"Halo, {nama_user}", color="black"),
                bgcolor="#E3F2FD",
                actions=[
                    ft.IconButton(
                        ft.Icons.LOGOUT,
                        icon_color="black",
                        tooltip="Logout",
                        on_click=keluar_akun,
                    )
                ],
            )
            konten = buat_beranda_user(on_pilih_resto=buka_detail_resto)
            page.add(konten)
            return
        elif role == "penjual":
            page.appbar = ft.AppBar(
                title=ft.Text(f"Toko: {nama_user}", color="black"),
                    bgcolor="#FFF3E0",
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
        else:
            page.appbar = ft.AppBar(
                title=ft.Text(f"Driver: {nama_user}", color="black"),
                bgcolor="#E8F5E9",
                actions=[
                    ft.IconButton(
                        ft.Icons.LOGOUT,
                        icon_color="black",
                        tooltip="Logout",
                        on_click=keluar_akun,
                    )
                ],
            )
            konten = buat_beranda_driver(page=page)
            page.add(konten)
            return

        page.add(
            ft.Column(
                [
                    konten,
                    ft.Button("Logout", on_click=keluar_akun),
                ],
                spacing=20,
            )
        )

    def tampilkan_login():
        page.clean()
        page.appbar = None
        page.add(buat_halaman_login(on_login_success=buka_beranda_role))

    # Mulai dari halaman login
    tampilkan_login()

ft.run(main)