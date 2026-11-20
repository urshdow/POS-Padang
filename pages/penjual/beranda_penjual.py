import tkinter as tk
from tkinter import messagebox


class WaregEksressApp:

    def __init__(self, root):
        self.root = root
        self.root.title("WaregEksress - Mitra Penjual")
        self.root.geometry("400x760")
        self.root.configure(bg="#000000")
        self.root.resizable(False, False)

        # State Awal (Belum ada pembeli)
        self.is_open = True
        self.revenue = 0
        self.orders = 0
        self.active_order = None
        self.menus = [
            {"name": "Nasi Goreng Wareg", "price": 22000, "ready": True},
            {"name": "Ayam Geprek Bawang", "price": 18000, "ready": True},
            {"name": "Es Teh Jumbo", "price": 6000, "ready": True},
        ]

        self._build_header()
        self.content_frame = tk.Frame(self.root, bg="#000000")
        self.content_frame.pack(fill="both", expand=True, padx=16, pady=10)
        self._build_navbar()

        self.show_beranda()

    def rp(self, n):
        return f"Rp {n:,}".replace(",", ".")

    def _build_header(self):
        header = tk.Frame(self.root, bg="#000000", pady=14, padx=16)
        header.pack(fill="x")

        logo = tk.Label(
            header,
            text="W",
            bg="#00b6fd",
            fg="#000000",
            font=("Segoe UI", 14, "bold"),
            width=3,
            height=1,
        )
        logo.pack(side="left")

        info = tk.Frame(header, bg="#000000", padx=10)
        info.pack(side="left")
        tk.Label(
            info,
            text="WaregEksress",
            bg="#000000",
            fg="#ffffff",
            font=("Segoe UI", 13, "bold"),
        ).pack(anchor="w")
        tk.Label(
            info,
            text="ID: WRG-88421 • ★ 0.0 (0 Ulasan)",
            bg="#000000",
            fg="#a0a0a0",
            font=("Segoe UI", 9),
        ).pack(anchor="w")

        tk.Frame(self.root, bg="#262626", height=1).pack(fill="x")

    def _build_navbar(self):
        tk.Frame(self.root, bg="#262626", height=1).pack(fill="x")
        nav = tk.Frame(self.root, bg="#000000", pady=10)
        nav.pack(fill="x", side="bottom")

        self.btn_beranda = tk.Button(
            nav,
            text="Beranda",
            bg="#000000",
            fg="#00b6fd",
            bd=0,
            font=("Segoe UI", 10, "bold"),
            command=self.show_beranda,
        )
        self.btn_menu = tk.Button(
            nav,
            text="Menu",
            bg="#000000",
            fg="#a0a0a0",
            bd=0,
            font=("Segoe UI", 10),
            command=self.show_menu,
        )
        self.btn_keuangan = tk.Button(
            nav,
            text="Keuangan",
            bg="#000000",
            fg="#a0a0a0",
            bd=0,
            font=("Segoe UI", 10),
            command=self.show_keuangan,
        )

        self.btn_beranda.pack(side="left", expand=True)
        self.btn_menu.pack(side="left", expand=True)
        self.btn_keuangan.pack(side="left", expand=True)

    def _set_active_nav(self, active):
        for btn, name in [
            (self.btn_beranda, "beranda"),
            (self.btn_menu, "menu"),
            (self.btn_keuangan, "keuangan"),
        ]:
            btn.config(
                fg="#00b6fd" if name == active else "#a0a0a0",
                font=("Segoe UI", 10, "bold" if name == active else "normal"),
            )

    def _clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    # ================= TAB 1: BERANDA =================
    def show_beranda(self):
        self._clear_content()
        self._set_active_nav("beranda")

        # 1. Card Status Toko
        status_card = tk.Frame(
            self.content_frame, bg="#141414", padx=14, pady=14
        )
        status_card.pack(fill="x", pady=(0, 12))

        left = tk.Frame(status_card, bg="#141414")
        left.pack(side="left")

        tk.Label(
            left,
            text="TOKO BUKA" if self.is_open else "TOKO TUTUP",
            bg="#141414",
            fg="#34d399" if self.is_open else "#f87171",
            font=("Segoe UI", 11, "bold"),
        ).pack(anchor="w")
        tk.Label(
            left,
            text=(
                "Siap menerima pesanan pertama"
                if self.is_open
                else "Toko tidak tampil di pelanggan"
            ),
            bg="#141414",
            fg="#a0a0a0",
            font=("Segoe UI", 9),
        ).pack(anchor="w")

        tk.Button(
            status_card,
            text="Tutup" if self.is_open else "Buka",
            bg="#262626",
            fg="#ffffff",
            bd=0,
            padx=12,
            pady=6,
            font=("Segoe UI", 9, "bold"),
            command=self.toggle_store,
        ).pack(side="right")

        # 2. Card Ringkasan Penjualan (Serba Nol)
        stat_card = tk.Frame(self.content_frame, bg="#141414", padx=14, pady=14)
        stat_card.pack(fill="x", pady=(0, 16))

        col1 = tk.Frame(stat_card, bg="#141414")
        col1.pack(side="left", expand=True)
        tk.Label(
            col1,
            text="Pendapatan Hari Ini",
            bg="#141414",
            fg="#a0a0a0",
            font=("Segoe UI", 9),
        ).pack()
        tk.Label(
            col1,
            text=self.rp(self.revenue),
            bg="#141414",
            fg="#ffffff",
            font=("Segoe UI", 14, "bold"),
        ).pack(pady=(4, 0))

        col2 = tk.Frame(stat_card, bg="#141414")
        col2.pack(side="left", expand=True)
        tk.Label(
            col2,
            text="Order Selesai",
            bg="#141414",
            fg="#a0a0a0",
            font=("Segoe UI", 9),
        ).pack()
        tk.Label(
            col2,
            text=f"{self.orders} Order",
            bg="#141414",
            fg="#ffffff",
            font=("Segoe UI", 14, "bold"),
        ).pack(pady=(4, 0))

        # 3. Header Pesanan Masuk
        header_order = tk.Frame(self.content_frame, bg="#000000")
        header_order.pack(fill="x", pady=(0, 8))

        tk.Label(
            header_order,
            text="Pesanan Masuk",
            bg="#000000",
            fg="#ffffff",
            font=("Segoe UI", 11, "bold"),
        ).pack(side="left")
        tk.Button(
            header_order,
            text="+ Simulasi Pembeli",
            bg="#000000",
            fg="#00b6fd",
            bd=0,
            font=("Segoe UI", 9, "bold"),
            command=self.simulate_order,
        ).pack(side="right")

        # 4. Empty State / Pesanan Aktif
        order_card = tk.Frame(
            self.content_frame, bg="#141414", padx=16, pady=22
        )
        order_card.pack(fill="x")

        if self.active_order is None:
            tk.Label(
                order_card,
                text="Belum Ada Pesanan Masuk",
                bg="#141414",
                fg="#ffffff",
                font=("Segoe UI", 11, "bold"),
            ).pack()
            tk.Label(
                order_card,
                text="Toko WaregEksress siap menerima pembeli pertama.",
                bg="#141414",
                fg="#a0a0a0",
                font=("Segoe UI", 9),
                wraplength=300,
            ).pack(pady=(6, 14))
            tk.Button(
                order_card,
                text="Uji Coba Pesanan Pertama",
                bg="#00b6fd",
                fg="#000000",
                bd=0,
                pady=8,
                font=("Segoe UI", 9, "bold"),
                command=self.simulate_order,
            ).pack(fill="x")
        else:
            o = self.active_order
            is_new = o["status"] == "NEW"
            tk.Label(
                order_card,
                text=f"#{o['id']} • {o['customer']} ({'BARU' if is_new else 'DIPROSES'})",
                bg="#141414",
                fg="#00b6fd",
                font=("Segoe UI", 10, "bold"),
            ).pack(anchor="w")
            tk.Label(
                order_card,
                text=o["items"],
                bg="#141414",
                fg="#a0a0a0",
                font=("Segoe UI", 9),
            ).pack(anchor="w", pady=6)
            tk.Label(
                order_card,
                text=self.rp(o["total"]),
                bg="#141414",
                fg="#ffffff",
                font=("Segoe UI", 12, "bold"),
            ).pack(anchor="w", pady=(0, 12))

            if is_new:
                btn_row = tk.Frame(order_card, bg="#141414")
                btn_row.pack(fill="x")
                tk.Button(
                    btn_row,
                    text="Tolak",
                    bg="#262626",
                    fg="#ffffff",
                    bd=0,
                    pady=7,
                    command=self.reject_order,
                ).pack(side="left", expand=True, fill="x", padx=(0, 5))
                tk.Button(
                    btn_row,
                    text="Terima",
                    bg="#00b6fd",
                    fg="#000000",
                    bd=0,
                    pady=7,
                    font=("Segoe UI", 9, "bold"),
                    command=self.accept_order,
                ).pack(side="left", expand=True, fill="x", padx=(5, 0))
            else:
                tk.Button(
                    order_card,
                    text="Selesai & Serahkan ke Driver",
                    bg="#34d399",
                    fg="#000000",
                    bd=0,
                    pady=8,
                    font=("Segoe UI", 9, "bold"),
                    command=self.complete_order,
                ).pack(fill="x")

    # ================= TAB 2: MENU =================
    def show_menu(self):
        self._clear_content()
        self._set_active_nav("menu")

        tk.Label(
            self.content_frame,
            text="Katalog Menu WaregEksress",
            bg="#000000",
            fg="#ffffff",
            font=("Segoe UI", 12, "bold"),
        ).pack(anchor="w", pady=(0, 10))

        for idx, item in enumerate(self.menus):
            card = tk.Frame(self.content_frame, bg="#141414", padx=14, pady=12)
            card.pack(fill="x", pady=5)

            info = tk.Frame(card, bg="#141414")
            info.pack(side="left")
            tk.Label(
                info,
                text=item["name"],
                bg="#141414",
                fg="#ffffff",
                font=("Segoe UI", 10, "bold"),
            ).pack(anchor="w")
            tk.Label(
                info,
                text=self.rp(item["price"]),
                bg="#141414",
                fg="#a0a0a0",
                font=("Segoe UI", 9),
            ).pack(anchor="w")

            tk.Button(
                card,
                text="Tersedia" if item["ready"] else "Habis",
                bg="#064e3b" if item["ready"] else "#7f1d1d",
                fg="#34d399" if item["ready"] else "#f87171",
                bd=0,
                padx=10,
                pady=4,
                font=("Segoe UI", 9, "bold"),
                command=lambda i=idx: self.toggle_stock(i),
            ).pack(side="right")

    # ================= TAB 3: KEUANGAN =================
    def show_keuangan(self):
        self._clear_content()
        self._set_active_nav("keuangan")

        card = tk.Frame(self.content_frame, bg="#141414", padx=18, pady=20)
        card.pack(fill="x")

        tk.Label(
            card,
            text="Saldo Aktif WaregEksress",
            bg="#141414",
            fg="#a0a0a0",
            font=("Segoe UI", 10),
        ).pack(anchor="w")
        tk.Label(
            card,
            text=self.rp(self.revenue),
            bg="#141414",
            fg="#ffffff",
            font=("Segoe UI", 22, "bold"),
        ).pack(anchor="w", pady=(4, 16))

        tk.Button(
            card,
            text="Tarik Saldo",
            bg="#00b6fd" if self.revenue > 0 else "#262626",
            fg="#000000" if self.revenue > 0 else "#a0a0a0",
            bd=0,
            pady=9,
            font=("Segoe UI", 10, "bold"),
            command=self.withdraw_saldo,
        ).pack(fill="x")

    # ================= LOGIKA AKSI =================
    def toggle_store(self):
        self.is_open = not self.is_open
        self.show_beranda()

    def simulate_order(self):
        if not self.is_open:
            messagebox.showwarning(
                "Toko Tutup", "Buka toko dulu untuk menerima pesanan!"
            )
            return
        if self.active_order is not None:
            messagebox.showinfo("Info", "Selesaikan pesanan aktif dulu.")
            return
        self.active_order = {
            "id": "WRG-001",
            "customer": "Rina Kartika",
            "items": "2x Nasi Goreng Wareg, 2x Es Teh Jumbo",
            "total": 56000,
            "status": "NEW",
        }
        self.show_beranda()

    def accept_order(self):
        self.active_order["status"] = "PREPARING"
        self.show_beranda()

    def reject_order(self):
        self.active_order = None
        self.show_beranda()

    def complete_order(self):
        total = self.active_order["total"]
        self.revenue += total
        self.orders += 1
        self.active_order = None
        messagebox.showinfo(
            "Pesanan Selesai", f"+{self.rp(total)} berhasil masuk ke saldo!"
        )
        self.show_beranda()

    def toggle_stock(self, idx):
        self.menus[idx]["ready"] = not self.menus[idx]["ready"]
        self.show_menu()

    def withdraw_saldo(self):
        if self.revenue == 0:
            messagebox.showinfo("Info", "Saldo masih Rp 0.")
        else:
            messagebox.showinfo(
                "Berhasil",
                f"Pencairan {self.rp(self.revenue)} sedang diproses!",
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = WaregEksressApp(root)
    root.mainloop()
    