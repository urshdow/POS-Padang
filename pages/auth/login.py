import flet as ft

def buat_halaman_login(on_login_success):
    input_user = ft.TextField(label="Email atau No. HP", width=320)
    input_pass = ft.TextField(
        label="Kata Sandi",
        password=True,
        can_reveal_password=True,
        width=320,
    )
    pilih_role = ft.Dropdown(
        label="Masuk Sebagai",
        width=320,
        value="user",
        options=[
            ft.dropdown.Option("user", "Pembeli (User)"),
            ft.dropdown.Option("penjual", "Restoran (Penjual)"),
            ft.dropdown.Option("driver", "Kurir (Driver)"),
        ],
    )
    pesan_error = ft.Text("", color="red", size=12)

    def klik_masuk(e):
        if not input_user.value:
            pesan_error.value = "Isi email atau nomor HP terlebih dahulu."
            pesan_error.update()
            return

        # Kirim role dan nama user ke main.py
        on_login_success(role=pilih_role.value, nama_user=input_user.value)

    return ft.Column(
        [
            ft.Icon(ft.Icons.DELIVERY_DINING, size=64, color="orange"),
            ft.Text("FoodExpress", size=28, weight=ft.FontWeight.BOLD),
            ft.Text("Silakan masuk sesuai akun Anda", color="grey"),
            ft.Container(height=10),
            input_user,
            input_pass,
            pilih_role,
            pesan_error,
            ft.Button(
                "Masuk",
                width=320,
                height=45,
                on_click=klik_masuk,
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True,
    )