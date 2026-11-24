import flet as ft

def buat_halaman_login(on_login_success):
    input_user = ft.TextField(label="Email atau No. HP", width=320, color="#000000")
    input_pass = ft.TextField(
        label="Kata Sandi",
        password=True,
        can_reveal_password=True,
        width=320, color="#000000"
    )
    pilih_role = ft.Dropdown(
        label="Masuk Sebagai",
        width=320,
        value="user",
        options=[
            ft.dropdown.Option("user", "Pembeli (User)"),
            ft.dropdown.Option("penjual", "Restoran (Penjual)"),
            #ft.dropdown.Option("driver", "Kurir (Driver)"),
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
            ft.Container(
                width = 64, 
                height = 64,  
                content = ft.Image(src="assets/Desain Tanpa Judul (1).png"),),
            ft.Text("Padang", size=28, weight=ft.FontWeight.BOLD, color = '#232b20'),
            ft.Text("Silakan masuk sesuai akun Anda", color='#232b20'),
            ft.Container(height=10),
            input_user,
            input_pass,
            pilih_role,
            pesan_error,
            ft.Button(
                "Masuk",
                width=320,
                height=45,
                on_click=klik_masuk, color='#E8F5E9', bgcolor = '#6c4830'
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True,
    )