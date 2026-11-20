import flet as ft
from pages.auth.login import buat_halaman_login

def main(page: ft.Page):
    page.title = "Wareg Express"
    page.window.width = 400
    page.window.height = 800
    page.theme_animation_style = ft.AnimationStyle(duration = 500, curve = ft.AnimationCurve.EASE_IN_OUT)
    page.theme_mode = ft.ThemeMode.SYSTEM

    def keluar_akun(e):
        tampilkan_login()

    def buka_beranda_role(role: str, nama_user: str):
        page.clean()

        if role == "user":
            page.appbar = ft.AppBar(title=ft.Text(f"Halo, {nama_user}"), bgcolor="#E3F2FD")
            konten = ft.Text("Ini Beranda Pembeli: Daftar Restoran akan tampil di sini.")
        elif role == "penjual":
            page.appbar = ft.AppBar(title=ft.Text(f"Toko: {nama_user}"), bgcolor="#FFF3E0")
            konten = ft.Text("Ini Beranda Penjual: Menu Kelola Stok, Pesanan & Export Excel.")
        else:
            page.appbar = ft.AppBar(title=ft.Text(f"Driver: {nama_user}"), bgcolor="#E8F5E9")
            konten = ft.Text("Ini Beranda Driver: Switch Online/Offline & Order Masuk.")

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