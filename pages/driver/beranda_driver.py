"""
Halaman Beranda Driver - Aplikasi Wareg Express
File: pages/driver/beranda_driver.py

Fitur:
- Desain responsif penuh (stretch ke layar laptop/desktop & adaptif di layar HP)
- Identitas visual Dark Mode Wareg Express (#000000 & #00b6fd)
- Semua tombol, modal, simulasi order, alur pengantaran, tarik saldo, & 5 tab navigasi aktif
- Kompatibel dengan Python 3.15 & Flet v0.80+ / v1.0 maupun Flet v0.2x
"""

import inspect
import random
from typing import Callable, Dict, List, Optional
import flet as ft

# ==============================================================================
# 1. LAPISAN KOMPATIBILITAS LINTAS VERSI FLET (v0.2x & v0.80+ / v1.0)
# ==============================================================================
Icons = getattr(ft, "Icons", getattr(ft, "icons", None))
Colors = getattr(ft, "Colors", getattr(ft, "colors", None))
PaddingCls = getattr(ft, "Padding", getattr(ft, "padding", None))
MarginCls = getattr(ft, "Margin", getattr(ft, "margin", None))
BorderCls = getattr(ft, "Border", getattr(ft, "border", None))
ButtonCls = getattr(ft, "Button", getattr(ft, "ElevatedButton", None))

ALIGN_CENTER = getattr(getattr(ft, "Alignment", None), "CENTER", None) or ft.Alignment(0, 0)
ALIGN_TOP_CENTER = getattr(getattr(ft, "Alignment", None), "TOP_CENTER", None) or ft.Alignment(0, -1)


def get_icon(*names: str):
    """Mengambil ikon Material secara aman di semua versi Flet."""
    for name in names:
        if Icons is not None and hasattr(Icons, name):
            return getattr(Icons, name)
    return getattr(Icons, "CIRCLE", None)


def make_switch(
    value: bool,
    on_change: Callable,
    active_color: str = "#22C55E",
    inactive_color: str = "#6B7280",
    label: Optional[str] = None,
) -> ft.Switch:
    """Membuat ft.Switch yang kompatibel dengan Flet v0.2x maupun v0.80+."""
    sig = inspect.signature(ft.Switch.__init__)
    params = sig.parameters
    kwargs = {"value": value, "on_change": on_change}

    if label is not None and "label" in params:
        kwargs["label"] = label

    if "active_thumb_color" in params:
        kwargs["active_thumb_color"] = "#FFFFFF"
        if "active_track_color" in params:
            kwargs["active_track_color"] = active_color
        if "inactive_thumb_color" in params:
            kwargs["inactive_thumb_color"] = "#D1D5DB"
        if "inactive_track_color" in params:
            kwargs["inactive_track_color"] = inactive_color
    elif "active_color" in params:
        kwargs["active_color"] = active_color
        if "inactive_track_color" in params:
            kwargs["inactive_track_color"] = inactive_color

    return ft.Switch(**kwargs)


def show_snackbar(page: ft.Page, message: str) -> None:
    """Menampilkan SnackBar notifikasi secara aman di berbagai versi Flet."""
    snack_behavior = getattr(getattr(ft, "SnackBarBehavior", None), "FLOATING", None)
    snack = ft.SnackBar(
        content=ft.Text(message, color="#FFFFFF", size=13, weight=ft.FontWeight.W_500),
        bgcolor="#202020",
        behavior=snack_behavior,
        duration=2200,
        shape=ft.RoundedRectangleBorder(radius=10),
    )
    if hasattr(page, "show_dialog"):
        page.show_dialog(snack)
    elif hasattr(page, "open"):
        page.open(snack)
    else:
        page.overlay.append(snack)
        snack.open = True
        page.update()


def open_modal(page: ft.Page, dialog: ft.AlertDialog) -> None:
    """Membuka AlertDialog secara aman di berbagai versi Flet."""
    if hasattr(page, "show_dialog"):
        page.show_dialog(dialog)
    elif hasattr(page, "open"):
        page.open(dialog)
    else:
        if dialog not in page.overlay:
            page.overlay.append(dialog)
        dialog.open = True
        page.update()


def close_modal(page: ft.Page, dialog: ft.AlertDialog) -> None:
    """Menutup AlertDialog secara aman di berbagai versi Flet."""
    if hasattr(page, "pop_dialog"):
        page.pop_dialog()
    elif hasattr(page, "close"):
        page.close(dialog)
    else:
        dialog.open = False
        page.update()


# ==============================================================================
# 2. KONSTANTA TEMA & WARNA WAREG EXPRESS
# ==============================================================================
class WaregTheme:
    BG_PRIMARY = "#000000"
    ACCENT = "#00b6fd"
    ACCENT_DARK = "#003B54"
    CARD_PRIMARY = "#171717"
    CARD_SECONDARY = "#202020"
    BORDER_SUBTLE = "#2B2B2B"
    TEXT_PRIMARY = "#FFFFFF"
    TEXT_SECONDARY = "#A0A0A0"
    STATUS_ONLINE = "#22C55E"
    STATUS_ONLINE_BG = "#0F2E1B"
    STATUS_OFFLINE = "#6B7280"
    STATUS_OFFLINE_BG = "#232529"
    WARNING = "#F59E0B"
    DANGER = "#EF4444"


def format_rupiah(nominal: int) -> str:
    """Memformat angka integer menjadi format mata uang Rupiah (Rp)."""
    return f"Rp {nominal:,.0f}".replace(",", ".")


# ==============================================================================
# 3. DATA DUMMY DRIVER & OPERASIONAL WAREG EXPRESS
# ==============================================================================
def get_default_driver_state() -> Dict:
    """Menyediakan data dummy lengkap untuk dashboard driver Wareg Express."""
    return {
        "driver": {
            "nama": "Budi Santoso",
            "id_driver": "DRV-WRG-2026089",
            "rating": 4.92,
            "plat_nomor": "L 4829 WRG",
            "kendaraan": "Honda Vario 160 • Hitam",
            "no_hp": "0812-3456-7890",
            "inisial": "BS",
        },
        "is_online": True,
        "pendapatan": {
            "hari_ini": 245000,
            "minggu_ini": 1680000,
            "saldo_dompet": 640000,
            "pesanan_selesai": 12,
            "bonus_insentif": 35000,
            "target_harian_order": 14,
            "bonus_target_nominal": 25000,
            "bonus_diklaim": False,
            "rincian_hari_ini": [
                {"judul": "Tarif Bersih Perjalanan (12 Order)", "nominal": 195000},
                {"judul": "Bonus Poin Harian", "nominal": 35000},
                {"judul": "Tip Pelanggan", "nominal": 15000},
            ],
            "riwayat_penarikan": [
                {"tanggal": "18 Nov 2026", "tujuan": "BCA •••• 8821", "nominal": 500000, "status": "Berhasil"},
                {"tanggal": "14 Nov 2026", "tujuan": "BCA •••• 8821", "nominal": 450000, "status": "Berhasil"},
            ],
        },
        "lokasi": {
            "alamat": "Jl. Basuki Rahmat No. 88, Surabaya",
            "koordinat": "-7.2657, 112.7418",
            "zona": "Zona Ramai • Pusat Kota",
            "pin_left": 180,
            "pin_top": 70,
            "sekitar": [
                {
                    "nama": "Tunjungan Plaza",
                    "alamat": "Jl. Jenderal Basuki Rachmat No.8-12",
                    "koordinat": "-7.2624, 112.7381",
                    "jarak": "450 m",
                    "permintaan": "Tinggi",
                    "pin_left": 70,
                    "pin_top": 35,
                },
                {
                    "nama": "Mie Gacoan Ambengan",
                    "alamat": "Jl. Ambengan No.51, Ketabang",
                    "koordinat": "-7.2589, 112.7485",
                    "jarak": "1,1 km",
                    "permintaan": "Sangat Tinggi",
                    "pin_left": 260,
                    "pin_top": 105,
                },
                {
                    "nama": "Stasiun Surabaya Gubeng",
                    "alamat": "Jl. Gubeng Masjid No.1, Pacar Keling",
                    "koordinat": "-7.2654, 112.7520",
                    "jarak": "1,8 km",
                    "permintaan": "Sedang",
                    "pin_left": 320,
                    "pin_top": 42,
                },
            ],
        },
        "statistik": {
            "total_order": 12,
            "total_jarak_km": 68.4,
            "durasi_online": "6j 25m",
            "rating_pelanggan": 4.92,
        },
        "layanan": [
            {
                "id": "ride",
                "nama": "Wareg Ride",
                "deskripsi": "Antar penumpang motor cepat",
                "ikon": get_icon("TWO_WHEELER", "DIRECTIONS_BIKE"),
                "aktif": True,
                "order": 5,
            },
            {
                "id": "car",
                "nama": "Wareg Car",
                "deskripsi": "Antar penumpang mobil nyaman",
                "ikon": get_icon("DIRECTIONS_CAR", "LOCAL_TAXI"),
                "aktif": False,
                "order": 0,
            },
            {
                "id": "food",
                "nama": "Wareg Food",
                "deskripsi": "Pesan antar kuliner & resto",
                "ikon": get_icon("RESTAURANT", "FASTFOOD_ROUNDED"),
                "aktif": True,
                "order": 5,
            },
            {
                "id": "send",
                "nama": "Wareg Send",
                "deskripsi": "Kirim paket instan dalam kota",
                "ikon": get_icon("LOCAL_SHIPPING", "INVENTORY_2_OUTLINED"),
                "aktif": True,
                "order": 2,
            },
        ],
        "pesanan_aktif": None,  # Menyimpan order aktif yang sedang dikerjakan driver
        "pesanan_terbaru": [
            {
                "id_order": "ORD-WRG-9941",
                "pelanggan": "Siti Rahmawati",
                "layanan": "Wareg Food",
                "jemput": "Mie Gacoan Ambengan, Surabaya",
                "tujuan": "Jl. Dharmahusada Indah No. 42",
                "status": "Selesai",
                "pendapatan": 18500,
                "jarak_km": 3.8,
                "waktu": "14 menit lalu",
                "catatan": "Titip di pos satpam blok B ya Pak",
            },
            {
                "id_order": "ORD-WRG-9938",
                "pelanggan": "Andi Wijaya",
                "layanan": "Wareg Ride",
                "jemput": "Stasiun Surabaya Gubeng",
                "tujuan": "Gedung Siola, Jl. Tunjungan",
                "status": "Selesai",
                "pendapatan": 14000,
                "jarak_km": 2.9,
                "waktu": "42 menit lalu",
                "catatan": "Tunggu di pintu keluar barat",
            },
            {
                "id_order": "ORD-WRG-9932",
                "pelanggan": "Rina Kusuma",
                "layanan": "Wareg Send",
                "jemput": "Toko Kue Spikoe Resep Kuno",
                "tujuan": "Perumahan Galaxy Bumi Permai",
                "status": "Selesai",
                "pendapatan": 22000,
                "jarak_km": 5.4,
                "waktu": "1 jam lalu",
                "catatan": "Kue mudah terguncang, mohon hati-hati",
            },
            {
                "id_order": "ORD-WRG-9927",
                "pelanggan": "Fajar Nugroho",
                "layanan": "Wareg Car",
                "jemput": "Bandara Juanda Terminal 1",
                "tujuan": "Hotel JW Marriott Surabaya",
                "status": "Selesai",
                "pendapatan": 65000,
                "jarak_km": 17.2,
                "waktu": "3 jam lalu",
                "catatan": "Bawa 2 koper kabin",
            },
        ],
        "kandidat_simulasi_order": [
            {
                "id_order": "ORD-WRG-9946",
                "pelanggan": "Dimas Pratama",
                "layanan": "Wareg Food",
                "jemput": "Bebek Sinjay Ahmad Yani",
                "tujuan": "Jl. Ketintang Baru IV No. 12",
                "pendapatan": 21000,
                "jarak_km": 4.6,
                "catatan": "Sambal pencit dipisah",
            },
            {
                "id_order": "ORD-WRG-9947",
                "pelanggan": "Nadia Putri",
                "layanan": "Wareg Ride",
                "jemput": "Universitas Airlangga Kampus B",
                "tujuan": "Grand City Mall Surabaya",
                "pendapatan": 15500,
                "jarak_km": 3.1,
                "catatan": "Pakai jaket biru di gerbang utama",
            },
            {
                "id_order": "ORD-WRG-9948",
                "pelanggan": "Hendra Gunawan",
                "layanan": "Wareg Send",
                "jemput": "Gudang Elektronik Merr",
                "tujuan": "Ruko Klampis Jaya No. 19",
                "pendapatan": 24000,
                "jarak_km": 5.8,
                "catatan": "Dokumen penting dalam map plastik",
            },
        ],
        "notifikasi": [
            {
                "judul": "Bonus Harian Wareg Express!",
                "pesan": "Selesaikan 2 order lagi untuk klaim bonus tambahan Rp 25.000.",
                "waktu": "10 mnt lalu",
                "dibaca": False,
            },
            {
                "judul": "Zona Permintaan Tinggi",
                "pesan": "Area Tunjungan & Embong Malang sedang ramai pesanan Wareg Food.",
                "waktu": "35 mnt lalu",
                "dibaca": False,
            },
            {
                "judul": "Pembayaran Masuk",
                "pesan": "Pendapatan Rp 18.500 dari order ORD-WRG-9941 telah masuk ke dompet.",
                "waktu": "1 jam lalu",
                "dibaca": True,
            },
        ],
        "pengaturan": {
            "auto_accept": False,
            "suara_order": True,
            "hemat_baterai": False,
            "radius_km": 5,
        },
        "filter_riwayat": "Semua",
        "active_tab": 0,  # 0: Beranda, 1: Pesanan, 2: Riwayat, 3: Pendapatan, 4: Profil
    }


# ==============================================================================
# 4. KOMPONEN UI MODULAR (BERANDA)
# ==============================================================================
def build_header_driver(
    state: Dict,
    on_open_notif: Callable,
    on_open_settings: Callable,
) -> ft.Container:
    """Bagian B: Header profil driver dengan avatar, ID, rating, notifikasi, & pengaturan."""
    driver = state["driver"]
    is_online = state["is_online"]
    unread_count = sum(1 for n in state["notifikasi"] if not n["dibaca"])

    avatar_stack = ft.Stack(
        width=52,
        height=52,
        controls=[
            ft.Container(
                width=50,
                height=50,
                border_radius=25,
                bgcolor=WaregTheme.CARD_SECONDARY,
                border=BorderCls.all(2, WaregTheme.ACCENT),
                alignment=ALIGN_CENTER,
                content=ft.Text(
                    driver["inisial"],
                    size=17,
                    weight=ft.FontWeight.BOLD,
                    color=WaregTheme.ACCENT,
                ),
            ),
            ft.Container(
                width=14,
                height=14,
                right=1,
                bottom=1,
                border_radius=7,
                bgcolor=WaregTheme.STATUS_ONLINE if is_online else WaregTheme.STATUS_OFFLINE,
                border=BorderCls.all(2, WaregTheme.BG_PRIMARY),
            ),
        ],
    )

    notif_button = ft.Stack(
        width=42,
        height=42,
        controls=[
            ft.Container(
                width=42,
                height=42,
                border_radius=12,
                bgcolor=WaregTheme.CARD_PRIMARY,
                border=BorderCls.all(1, WaregTheme.BORDER_SUBTLE),
                ink=True,
                on_click=on_open_notif,
                tooltip="Notifikasi",
                alignment=ALIGN_CENTER,
                content=ft.Icon(
                    get_icon("NOTIFICATIONS_OUTLINED", "NOTIFICATIONS"),
                    color=WaregTheme.TEXT_PRIMARY,
                    size=20,
                ),
            ),
            ft.Container(
                visible=unread_count > 0,
                right=7,
                top=7,
                width=9,
                height=9,
                border_radius=5,
                bgcolor=WaregTheme.ACCENT,
            ),
        ],
    )

    settings_button = ft.Container(
        width=42,
        height=42,
        border_radius=12,
        bgcolor=WaregTheme.CARD_PRIMARY,
        border=BorderCls.all(1, WaregTheme.BORDER_SUBTLE),
        ink=True,
        on_click=on_open_settings,
        tooltip="Pengaturan Driver",
        alignment=ALIGN_CENTER,
        content=ft.Icon(
            get_icon("SETTINGS_OUTLINED", "SETTINGS"),
            color=WaregTheme.TEXT_PRIMARY,
            size=20,
        ),
    )

    return ft.Container(
        bgcolor=WaregTheme.CARD_PRIMARY,
        border_radius=16,
        padding=PaddingCls.symmetric(horizontal=16, vertical=12),
        border=BorderCls.all(1, WaregTheme.BORDER_SUBTLE),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Row(
                    spacing=12,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    expand=True,
                    controls=[
                        avatar_stack,
                        ft.Column(
                            spacing=3,
                            expand=True,
                            controls=[
                                ft.Row(
                                    spacing=8,
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    controls=[
                                        ft.Text(
                                            driver["nama"],
                                            size=17,
                                            weight=ft.FontWeight.BOLD,
                                            color=WaregTheme.TEXT_PRIMARY,
                                            max_lines=1,
                                            overflow=ft.TextOverflow.ELLIPSIS,
                                        ),
                                        ft.Container(
                                            padding=PaddingCls.symmetric(horizontal=8, vertical=2),
                                            border_radius=6,
                                            bgcolor=WaregTheme.ACCENT_DARK,
                                            content=ft.Text(
                                                "WAREG EXPRESS",
                                                size=10,
                                                weight=ft.FontWeight.BOLD,
                                                color=WaregTheme.ACCENT,
                                            ),
                                        ),
                                    ],
                                ),
                                ft.Row(
                                    spacing=10,
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    controls=[
                                        ft.Text(
                                            driver["id_driver"],
                                            size=12,
                                            color=WaregTheme.TEXT_SECONDARY,
                                        ),
                                        ft.Container(
                                            padding=PaddingCls.symmetric(horizontal=7, vertical=2),
                                            border_radius=6,
                                            bgcolor=WaregTheme.CARD_SECONDARY,
                                            content=ft.Row(
                                                spacing=3,
                                                tight=True,
                                                controls=[
                                                    ft.Icon(
                                                        get_icon("STAR_ROUNDED", "STAR"),
                                                        size=14,
                                                        color=WaregTheme.WARNING,
                                                    ),
                                                    ft.Text(
                                                        f"{driver['rating']:.2f}",
                                                        size=12,
                                                        weight=ft.FontWeight.BOLD,
                                                        color=WaregTheme.TEXT_PRIMARY,
                                                    ),
                                                ],
                                            ),
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
                ft.Row(
                    spacing=8,
                    controls=[notif_button, settings_button],
                ),
            ],
        ),
    )


def build_status_online_card(
    state: Dict,
    on_toggle_status: Callable,
    on_simulate_order: Callable,
    on_open_active_order: Callable,
) -> ft.Container:
    """Bagian C: Kartu toggle status Online / Offline interaktif."""
    is_online = state["is_online"]
    pesanan_aktif = state["pesanan_aktif"]
    status_color = WaregTheme.STATUS_ONLINE if is_online else WaregTheme.STATUS_OFFLINE
    badge_bg = WaregTheme.STATUS_ONLINE_BG if is_online else WaregTheme.STATUS_OFFLINE_BG
    status_title = "Kamu sedang online" if is_online else "Kamu sedang offline"
    status_desc = (
        "Siap menerima pesanan Wareg Express di sekitarmu"
        if is_online
        else "Aktifkan status untuk mulai menerima pesanan"
    )

    bottom_bar_controls: List[ft.Control] = []
    if pesanan_aktif is not None:
        bottom_bar_controls.append(
            ft.Container(
                bgcolor=WaregTheme.ACCENT_DARK,
                border_radius=10,
                padding=PaddingCls.symmetric(horizontal=12, vertical=8),
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Row(
                            spacing=8,
                            expand=True,
                            controls=[
                                ft.Icon(
                                    get_icon("DELIVERY_DINING_ROUNDED", "LOCAL_SHIPPING"),
                                    size=18,
                                    color=WaregTheme.ACCENT,
                                ),
                                ft.Text(
                                    f"Order Aktif: {pesanan_aktif['pelanggan']} ({pesanan_aktif['tahap_label']})",
                                    size=12,
                                    weight=ft.FontWeight.BOLD,
                                    color=WaregTheme.TEXT_PRIMARY,
                                    max_lines=1,
                                    overflow=ft.TextOverflow.ELLIPSIS,
                                    expand=True,
                                ),
                            ],
                        ),
                        ft.TextButton(
                            content=ft.Text("Kelola Order", size=12, weight=ft.FontWeight.BOLD),
                            style=ft.ButtonStyle(color=WaregTheme.ACCENT),
                            on_click=on_open_active_order,
                        ),
                    ],
                ),
            )
        )
    elif is_online:
        bottom_bar_controls.append(
            ft.Container(
                bgcolor=WaregTheme.CARD_SECONDARY,
                border_radius=10,
                padding=PaddingCls.symmetric(horizontal=12, vertical=8),
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Row(
                            spacing=8,
                            expand=True,
                            controls=[
                                ft.Icon(
                                    get_icon("RADAR_ROUNDED", "WIFI_TETHERING"),
                                    size=16,
                                    color=WaregTheme.ACCENT,
                                ),
                                ft.Text(
                                    f"Mencari order (radius {state['pengaturan']['radius_km']} km)...",
                                    size=12,
                                    color=WaregTheme.TEXT_SECONDARY,
                                    max_lines=1,
                                    overflow=ft.TextOverflow.ELLIPSIS,
                                    expand=True,
                                ),
                            ],
                        ),
                        ft.TextButton(
                            content=ft.Text("Simulasi Order", size=12, weight=ft.FontWeight.BOLD),
                            style=ft.ButtonStyle(
                                color=WaregTheme.ACCENT,
                                padding=PaddingCls.symmetric(horizontal=8, vertical=2),
                            ),
                            on_click=on_simulate_order,
                        ),
                    ],
                ),
            )
        )

    return ft.Container(
        bgcolor=WaregTheme.CARD_PRIMARY,
        border_radius=16,
        padding=16,
        border=BorderCls.all(
            1.2,
            WaregTheme.STATUS_ONLINE if is_online else WaregTheme.BORDER_SUBTLE,
        ),
        content=ft.Column(
            spacing=12,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Row(
                            spacing=12,
                            expand=True,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Container(
                                    width=44,
                                    height=44,
                                    border_radius=12,
                                    bgcolor=badge_bg,
                                    alignment=ALIGN_CENTER,
                                    content=ft.Icon(
                                        get_icon("POWER_SETTINGS_NEW_ROUNDED", "POWER_SETTINGS_NEW"),
                                        color=status_color,
                                        size=22,
                                    ),
                                ),
                                ft.Column(
                                    spacing=2,
                                    expand=True,
                                    controls=[
                                        ft.Row(
                                            spacing=6,
                                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                            controls=[
                                                ft.Container(
                                                    width=8,
                                                    height=8,
                                                    border_radius=4,
                                                    bgcolor=status_color,
                                                ),
                                                ft.Text(
                                                    status_title,
                                                    size=15,
                                                    weight=ft.FontWeight.BOLD,
                                                    color=WaregTheme.TEXT_PRIMARY,
                                                ),
                                            ],
                                        ),
                                        ft.Text(
                                            status_desc,
                                            size=12,
                                            color=WaregTheme.TEXT_SECONDARY,
                                        ),
                                    ],
                                ),
                            ],
                        ),
                        make_switch(
                            value=is_online,
                            on_change=on_toggle_status,
                            active_color=WaregTheme.STATUS_ONLINE,
                            inactive_color=WaregTheme.STATUS_OFFLINE,
                        ),
                    ],
                ),
                *bottom_bar_controls,
            ],
        ),
    )


def build_pendapatan_card(
    state: Dict,
    on_detail_pendapatan: Callable,
    on_claim_bonus: Callable,
) -> ft.Container:
    """Bagian D: Kartu ringkasan pendapatan driver dalam mata uang Rupiah."""
    pendapatan = state["pendapatan"]
    selesai = pendapatan["pesanan_selesai"]
    target = pendapatan["target_harian_order"]
    progress = min(selesai / max(target, 1), 1.0)
    can_claim = selesai >= target and not pendapatan["bonus_diklaim"]

    def mini_metric(label: str, value: str, icon_name) -> ft.Container:
        return ft.Container(
            expand=True,
            bgcolor=WaregTheme.CARD_SECONDARY,
            border_radius=12,
            padding=10,
            content=ft.Column(
                spacing=4,
                controls=[
                    ft.Row(
                        spacing=4,
                        controls=[
                            ft.Icon(icon_name, size=14, color=WaregTheme.ACCENT),
                            ft.Text(
                                label,
                                size=11,
                                color=WaregTheme.TEXT_SECONDARY,
                                max_lines=1,
                                overflow=ft.TextOverflow.ELLIPSIS,
                            ),
                        ],
                    ),
                    ft.Text(
                        value,
                        size=13,
                        weight=ft.FontWeight.BOLD,
                        color=WaregTheme.TEXT_PRIMARY,
                    ),
                ],
            ),
        )

    bonus_row_controls: List[ft.Control] = [
        ft.Text(
            (
                "Bonus harian Rp 25.000 sudah diklaim!"
                if pendapatan["bonus_diklaim"]
                else f"Target Bonus Harian ({selesai}/{target} order)"
            ),
            size=11,
            color=WaregTheme.STATUS_ONLINE if pendapatan["bonus_diklaim"] else WaregTheme.TEXT_SECONDARY,
        ),
    ]
    if can_claim:
        bonus_row_controls.append(
            ft.TextButton(
                content=ft.Text("Klaim Rp 25.000", size=11, weight=ft.FontWeight.BOLD),
                style=ft.ButtonStyle(color=WaregTheme.STATUS_ONLINE),
                on_click=on_claim_bonus,
            )
        )
    else:
        bonus_row_controls.append(
            ft.Text(
                f"{int(progress * 100)}%",
                size=11,
                weight=ft.FontWeight.BOLD,
                color=WaregTheme.ACCENT,
            )
        )

    return ft.Container(
        bgcolor=WaregTheme.CARD_PRIMARY,
        border_radius=16,
        padding=16,
        border=BorderCls.all(1, WaregTheme.BORDER_SUBTLE),
        content=ft.Column(
            spacing=14,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                    controls=[
                        ft.Column(
                            spacing=3,
                            controls=[
                                ft.Text(
                                    "Pendapatan Hari Ini",
                                    size=12,
                                    color=WaregTheme.TEXT_SECONDARY,
                                ),
                                ft.Text(
                                    format_rupiah(pendapatan["hari_ini"]),
                                    size=26,
                                    weight=ft.FontWeight.BOLD,
                                    color=WaregTheme.TEXT_PRIMARY,
                                ),
                            ],
                        ),
                        ft.Container(
                            padding=PaddingCls.symmetric(horizontal=10, vertical=5),
                            border_radius=20,
                            bgcolor=WaregTheme.ACCENT_DARK,
                            content=ft.Row(
                                spacing=4,
                                controls=[
                                    ft.Icon(
                                        get_icon("TRENDING_UP_ROUNDED", "TRENDING_UP"),
                                        size=14,
                                        color=WaregTheme.ACCENT,
                                    ),
                                    ft.Text(
                                        "+14%",
                                        size=11,
                                        weight=ft.FontWeight.BOLD,
                                        color=WaregTheme.ACCENT,
                                    ),
                                ],
                            ),
                        ),
                    ],
                ),
                ft.Row(
                    spacing=8,
                    controls=[
                        mini_metric(
                            "Minggu Ini",
                            format_rupiah(pendapatan["minggu_ini"]),
                            get_icon("CALENDAR_TODAY_ROUNDED", "CALENDAR_TODAY"),
                        ),
                        mini_metric(
                            "Selesai",
                            f"{selesai} Order",
                            get_icon("CHECK_CIRCLE_OUTLINE_ROUNDED", "CHECK_CIRCLE_OUTLINE"),
                        ),
                        mini_metric(
                            "Bonus",
                            format_rupiah(pendapatan["bonus_insentif"]),
                            get_icon("CARD_GIFTCARD_ROUNDED", "CARD_GIFTCARD"),
                        ),
                    ],
                ),
                ft.Column(
                    spacing=6,
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=bonus_row_controls,
                        ),
                        ft.ProgressBar(
                            value=progress,
                            color=WaregTheme.STATUS_ONLINE if can_claim else WaregTheme.ACCENT,
                            bgcolor=WaregTheme.CARD_SECONDARY,
                            height=6,
                            border_radius=3,
                        ),
                    ],
                ),
                ft.Container(
                    width=float("inf"),
                    content=ButtonCls(
                        on_click=on_detail_pendapatan,
                        style=ft.ButtonStyle(
                            bgcolor=WaregTheme.ACCENT,
                            color="#000000",
                            shape=ft.RoundedRectangleBorder(radius=12),
                            padding=PaddingCls.symmetric(vertical=12),
                        ),
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=6,
                            controls=[
                                ft.Icon(
                                    get_icon("ACCOUNT_BALANCE_WALLET_ROUNDED", "ACCOUNT_BALANCE_WALLET"),
                                    size=18,
                                ),
                                ft.Text(
                                    "Lihat Detail Pendapatan",
                                    size=13,
                                    weight=ft.FontWeight.BOLD,
                                ),
                            ],
                        ),
                    ),
                ),
            ],
        ),
    )


def build_peta_lokasi_card(
    state: Dict,
    on_my_location: Callable,
    on_open_navigation: Callable,
    on_select_spot_direct: Callable[[Dict], None],
) -> ft.Container:
    """Bagian E: Area peta gelap interaktif (placeholder tanpa mengklaim GPS aktif)."""
    lokasi = state["lokasi"]
    is_online = state["is_online"]
    pin_color = WaregTheme.ACCENT if is_online else WaregTheme.STATUS_OFFLINE
    clip_hard = getattr(getattr(ft, "ClipBehavior", None), "HARD_EDGE", None)

    spot_tp = lokasi["sekitar"][0]
    spot_mg = lokasi["sekitar"][1]

    map_canvas = ft.Container(
        height=210,
        border_radius=14,
        bgcolor="#0C1118",
        border=BorderCls.all(1, WaregTheme.BORDER_SUBTLE),
        clip_behavior=clip_hard,
        content=ft.Stack(
            controls=[
                # Blok jalan & tata kota gelap
                ft.Container(left=24, top=28, width=130, height=56, border_radius=8, bgcolor="#131B26"),
                ft.Container(right=24, top=30, width=145, height=52, border_radius=8, bgcolor="#131B26"),
                ft.Container(left=30, bottom=24, width=150, height=52, border_radius=8, bgcolor="#131B26"),
                ft.Container(right=28, bottom=24, width=135, height=56, border_radius=8, bgcolor="#131B26"),
                # Garis jalan utama
                ft.Container(left=0, right=0, top=102, height=6, bgcolor="#1E293B"),
                ft.Container(top=0, bottom=0, left=200, width=6, bgcolor="#1E293B"),
                ft.Container(left=0, right=0, top=104, height=2, bgcolor=WaregTheme.ACCENT_DARK),
                # Hotspot 1 (bisa diklik langsung di peta)
                ft.Container(
                    left=34,
                    top=44,
                    padding=PaddingCls.symmetric(horizontal=9, vertical=5),
                    border_radius=8,
                    bgcolor="#171717E6",
                    border=BorderCls.all(1, WaregTheme.WARNING),
                    ink=True,
                    on_click=lambda e: on_select_spot_direct(spot_tp),
                    tooltip="Klik untuk arahkan ke Tunjungan Plaza",
                    content=ft.Row(
                        spacing=4,
                        tight=True,
                        controls=[
                            ft.Icon(
                                get_icon("LOCAL_FIRE_DEPARTMENT_ROUNDED", "LOCAL_FIRE_DEPARTMENT"),
                                size=13,
                                color=WaregTheme.WARNING,
                            ),
                            ft.Text("Tunjungan Plaza (450m)", size=10, color=WaregTheme.TEXT_PRIMARY),
                        ],
                    ),
                ),
                # Hotspot 2 (bisa diklik langsung di peta)
                ft.Container(
                    right=32,
                    bottom=34,
                    padding=PaddingCls.symmetric(horizontal=9, vertical=5),
                    border_radius=8,
                    bgcolor="#171717E6",
                    border=BorderCls.all(1, WaregTheme.ACCENT),
                    ink=True,
                    on_click=lambda e: on_select_spot_direct(spot_mg),
                    tooltip="Klik untuk arahkan ke Mie Gacoan Ambengan",
                    content=ft.Row(
                        spacing=4,
                        tight=True,
                        controls=[
                            ft.Icon(
                                get_icon("RESTAURANT_ROUNDED", "RESTAURANT"),
                                size=13,
                                color=WaregTheme.ACCENT,
                            ),
                            ft.Text("Mie Gacoan (1,1km)", size=10, color=WaregTheme.TEXT_PRIMARY),
                        ],
                    ),
                ),
                # Penanda Posisi Driver
                ft.Container(
                    left=lokasi["pin_left"],
                    top=lokasi["pin_top"],
                    width=66,
                    height=66,
                    border_radius=33,
                    bgcolor="#00b6fd22",
                    border=BorderCls.all(1, "#00b6fd55"),
                    alignment=ALIGN_CENTER,
                    content=ft.Container(
                        width=34,
                        height=34,
                        border_radius=17,
                        bgcolor=pin_color,
                        border=BorderCls.all(2.5, "#FFFFFF"),
                        alignment=ALIGN_CENTER,
                        content=ft.Icon(
                            get_icon("NAVIGATION_ROUNDED", "NAVIGATION"),
                            size=18,
                            color="#000000" if is_online else "#FFFFFF",
                        ),
                    ),
                ),
                # Label disclaimer jujur mode pratinjau simulasi
                ft.Container(
                    left=10,
                    top=10,
                    padding=PaddingCls.symmetric(horizontal=8, vertical=4),
                    border_radius=8,
                    bgcolor="#000000CC",
                    border=BorderCls.all(1, WaregTheme.BORDER_SUBTLE),
                    content=ft.Row(
                        spacing=5,
                        tight=True,
                        controls=[
                            ft.Icon(
                                get_icon("MAP_OUTLINED", "MAP"),
                                size=12,
                                color=WaregTheme.ACCENT,
                            ),
                            ft.Text(
                                "Pratinjau Peta Gelap (Simulasi Lokasi)",
                                size=10,
                                color=WaregTheme.TEXT_SECONDARY,
                            ),
                        ],
                    ),
                ),
                # Badge Zona Sekitar
                ft.Container(
                    right=10,
                    top=10,
                    padding=PaddingCls.symmetric(horizontal=8, vertical=4),
                    border_radius=8,
                    bgcolor=WaregTheme.ACCENT_DARK,
                    content=ft.Text(
                        lokasi["zona"],
                        size=10,
                        weight=ft.FontWeight.BOLD,
                        color=WaregTheme.ACCENT,
                    ),
                ),
            ],
        ),
    )

    return ft.Container(
        bgcolor=WaregTheme.CARD_PRIMARY,
        border_radius=16,
        padding=16,
        border=BorderCls.all(1, WaregTheme.BORDER_SUBTLE),
        content=ft.Column(
            spacing=12,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text(
                            "Peta & Lokasi Sekitar",
                            size=15,
                            weight=ft.FontWeight.BOLD,
                            color=WaregTheme.TEXT_PRIMARY,
                        ),
                        ft.Text(
                            lokasi["koordinat"],
                            size=11,
                            color=WaregTheme.TEXT_SECONDARY,
                        ),
                    ],
                ),
                map_canvas,
                ft.Row(
                    spacing=8,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Icon(
                            get_icon("LOCATION_ON_ROUNDED", "LOCATION_ON"),
                            size=18,
                            color=WaregTheme.ACCENT,
                        ),
                        ft.Text(
                            lokasi["alamat"],
                            size=12,
                            color=WaregTheme.TEXT_PRIMARY,
                            expand=True,
                            max_lines=1,
                            overflow=ft.TextOverflow.ELLIPSIS,
                        ),
                    ],
                ),
                ft.Row(
                    spacing=10,
                    controls=[
                        ft.Container(
                            expand=True,
                            content=ft.OutlinedButton(
                                on_click=on_my_location,
                                style=ft.ButtonStyle(
                                    side=ft.BorderSide(1, WaregTheme.ACCENT),
                                    color=WaregTheme.ACCENT,
                                    shape=ft.RoundedRectangleBorder(radius=10),
                                    padding=PaddingCls.symmetric(vertical=10),
                                ),
                                content=ft.Row(
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    spacing=6,
                                    controls=[
                                        ft.Icon(
                                            get_icon("MY_LOCATION_ROUNDED", "MY_LOCATION"),
                                            size=16,
                                        ),
                                        ft.Text("Lokasi Saya", size=12, weight=ft.FontWeight.W_600),
                                    ],
                                ),
                            ),
                        ),
                        ft.Container(
                            expand=True,
                            content=ButtonCls(
                                on_click=on_open_navigation,
                                style=ft.ButtonStyle(
                                    bgcolor=WaregTheme.CARD_SECONDARY,
                                    color=WaregTheme.TEXT_PRIMARY,
                                    shape=ft.RoundedRectangleBorder(radius=10),
                                    padding=PaddingCls.symmetric(vertical=10),
                                ),
                                content=ft.Row(
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    spacing=6,
                                    controls=[
                                        ft.Icon(
                                            get_icon("NEAR_ME_ROUNDED", "NEAR_ME"),
                                            size=16,
                                            color=WaregTheme.ACCENT,
                                        ),
                                        ft.Text("Navigasi Peta", size=12, weight=ft.FontWeight.W_600),
                                    ],
                                ),
                            ),
                        ),
                    ],
                ),
            ],
        ),
    )


def build_statistik_aktivitas_section(state: Dict) -> ft.Container:
    """Bagian F: Statistik aktivitas driver hari ini."""
    stats = state["statistik"]

    def stat_card(title: str, value: str, subtitle: str, icon_name, icon_color: str) -> ft.Container:
        return ft.Container(
            expand=True,
            bgcolor=WaregTheme.CARD_SECONDARY,
            border_radius=12,
            padding=12,
            content=ft.Column(
                spacing=5,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Icon(icon_name, size=18, color=icon_color),
                            ft.Text(
                                subtitle,
                                size=10,
                                color=WaregTheme.TEXT_SECONDARY,
                            ),
                        ],
                    ),
                    ft.Text(
                        value,
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        color=WaregTheme.TEXT_PRIMARY,
                    ),
                    ft.Text(
                        title,
                        size=11,
                        color=WaregTheme.TEXT_SECONDARY,
                    ),
                ],
            ),
        )

    return ft.Container(
        bgcolor=WaregTheme.CARD_PRIMARY,
        border_radius=16,
        padding=16,
        border=BorderCls.all(1, WaregTheme.BORDER_SUBTLE),
        content=ft.Column(
            spacing=12,
            controls=[
                ft.Text(
                    "Statistik Aktivitas",
                    size=15,
                    weight=ft.FontWeight.BOLD,
                    color=WaregTheme.TEXT_PRIMARY,
                ),
                ft.Row(
                    spacing=10,
                    controls=[
                        stat_card(
                            "Total Order Hari Ini",
                            f"{stats['total_order']} Order",
                            "Hari ini",
                            get_icon("SHOPPING_BAG_OUTLINED", "SHOPPING_BAG"),
                            WaregTheme.ACCENT,
                        ),
                        stat_card(
                            "Total Jarak Perjalanan",
                            f"{stats['total_jarak_km']:.1f} km".replace(".", ","),
                            "Tempuh",
                            get_icon("ROUTE_ROUNDED", "ALT_ROUTE"),
                            WaregTheme.STATUS_ONLINE,
                        ),
                    ],
                ),
                ft.Row(
                    spacing=10,
                    controls=[
                        stat_card(
                            "Durasi Online",
                            stats["durasi_online"],
                            "Aktif",
                            get_icon("ACCESS_TIME_ROUNDED", "ACCESS_TIME"),
                            WaregTheme.ACCENT,
                        ),
                        stat_card(
                            "Rating Pelanggan",
                            f"{stats['rating_pelanggan']:.2f} / 5.0",
                            "Sangat Baik",
                            get_icon("STAR_ROUNDED", "STAR"),
                            WaregTheme.WARNING,
                        ),
                    ],
                ),
            ],
        ),
    )


def build_menu_layanan_grid(
    state: Dict,
    on_toggle_layanan: Callable[[str], None],
) -> ft.Container:
    """Bagian G: Grid menu layanan (Wareg Ride, Wareg Car, Wareg Food, Wareg Send)."""
    layanan_list = state["layanan"]

    def service_tile(item: Dict) -> ft.Container:
        aktif = item["aktif"]
        return ft.Container(
            expand=True,
            bgcolor=WaregTheme.CARD_SECONDARY,
            border_radius=14,
            padding=12,
            border=BorderCls.all(
                1.2,
                WaregTheme.ACCENT if aktif else WaregTheme.BORDER_SUBTLE,
            ),
            ink=True,
            on_click=lambda e, sid=item["id"]: on_toggle_layanan(sid),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=6,
                controls=[
                    ft.Container(
                        width=44,
                        height=44,
                        border_radius=12,
                        bgcolor=WaregTheme.ACCENT_DARK if aktif else WaregTheme.CARD_PRIMARY,
                        alignment=ALIGN_CENTER,
                        content=ft.Icon(
                            item["ikon"],
                            size=22,
                            color=WaregTheme.ACCENT if aktif else WaregTheme.TEXT_SECONDARY,
                        ),
                    ),
                    ft.Text(
                        item["nama"],
                        size=13,
                        weight=ft.FontWeight.BOLD,
                        color=WaregTheme.TEXT_PRIMARY if aktif else WaregTheme.TEXT_SECONDARY,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Container(
                        padding=PaddingCls.symmetric(horizontal=8, vertical=2),
                        border_radius=6,
                        bgcolor=WaregTheme.STATUS_ONLINE_BG if aktif else WaregTheme.CARD_PRIMARY,
                        content=ft.Text(
                            "Aktif" if aktif else "Nonaktif",
                            size=10,
                            weight=ft.FontWeight.W_600,
                            color=WaregTheme.STATUS_ONLINE if aktif else WaregTheme.TEXT_SECONDARY,
                        ),
                    ),
                ],
            ),
        )

    return ft.Container(
        bgcolor=WaregTheme.CARD_PRIMARY,
        border_radius=16,
        padding=16,
        border=BorderCls.all(1, WaregTheme.BORDER_SUBTLE),
        content=ft.Column(
            spacing=12,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text(
                            "Menu Layanan Wareg Express",
                            size=15,
                            weight=ft.FontWeight.BOLD,
                            color=WaregTheme.TEXT_PRIMARY,
                        ),
                        ft.Text(
                            "Ketuk untuk aktif/nonaktif",
                            size=11,
                            color=WaregTheme.TEXT_SECONDARY,
                        ),
                    ],
                ),
                ft.Row(
                    spacing=10,
                    controls=[service_tile(layanan_list[0]), service_tile(layanan_list[1])],
                ),
                ft.Row(
                    spacing=10,
                    controls=[service_tile(layanan_list[2]), service_tile(layanan_list[3])],
                ),
            ],
        ),
    )


def build_pesanan_terbaru_card(
    state: Dict,
    on_lihat_semua_pesanan: Callable,
    on_inspect_order: Callable[[Dict], None],
) -> ft.Container:
    """Bagian H: Ringkasan pesanan terbaru & tombol lihat seluruh pesanan."""
    pesanan_terbaru = state["pesanan_terbaru"][0]

    return ft.Container(
        bgcolor=WaregTheme.CARD_PRIMARY,
        border_radius=16,
        padding=16,
        border=BorderCls.all(1, WaregTheme.BORDER_SUBTLE),
        content=ft.Column(
            spacing=12,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Text(
                            "Pesanan Terbaru",
                            size=15,
                            weight=ft.FontWeight.BOLD,
                            color=WaregTheme.TEXT_PRIMARY,
                        ),
                        ft.Container(
                            padding=PaddingCls.symmetric(horizontal=8, vertical=3),
                            border_radius=8,
                            bgcolor=WaregTheme.STATUS_ONLINE_BG,
                            content=ft.Text(
                                pesanan_terbaru["status"],
                                size=11,
                                weight=ft.FontWeight.BOLD,
                                color=WaregTheme.STATUS_ONLINE,
                            ),
                        ),
                    ],
                ),
                ft.Container(
                    bgcolor=WaregTheme.CARD_SECONDARY,
                    border_radius=12,
                    padding=12,
                    ink=True,
                    on_click=lambda e: on_inspect_order(pesanan_terbaru),
                    content=ft.Column(
                        spacing=10,
                        controls=[
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    ft.Row(
                                        spacing=8,
                                        controls=[
                                            ft.CircleAvatar(
                                                radius=16,
                                                bgcolor=WaregTheme.ACCENT_DARK,
                                                content=ft.Text(
                                                    pesanan_terbaru["pelanggan"][0],
                                                    size=13,
                                                    weight=ft.FontWeight.BOLD,
                                                    color=WaregTheme.ACCENT,
                                                ),
                                            ),
                                            ft.Column(
                                                spacing=1,
                                                controls=[
                                                    ft.Text(
                                                        pesanan_terbaru["pelanggan"],
                                                        size=13,
                                                        weight=ft.FontWeight.BOLD,
                                                        color=WaregTheme.TEXT_PRIMARY,
                                                    ),
                                                    ft.Text(
                                                        f"{pesanan_terbaru['layanan']} • {pesanan_terbaru['waktu']}",
                                                        size=11,
                                                        color=WaregTheme.TEXT_SECONDARY,
                                                    ),
                                                ],
                                            ),
                                        ],
                                    ),
                                    ft.Column(
                                        horizontal_alignment=ft.CrossAxisAlignment.END,
                                        spacing=1,
                                        controls=[
                                            ft.Text(
                                                "Estimasi",
                                                size=10,
                                                color=WaregTheme.TEXT_SECONDARY,
                                            ),
                                            ft.Text(
                                                format_rupiah(pesanan_terbaru["pendapatan"]),
                                                size=14,
                                                weight=ft.FontWeight.BOLD,
                                                color=WaregTheme.ACCENT,
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                            ft.Divider(height=1, color=WaregTheme.BORDER_SUBTLE),
                            ft.Column(
                                spacing=8,
                                controls=[
                                    ft.Row(
                                        spacing=8,
                                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                        controls=[
                                            ft.Icon(
                                                get_icon("RADIO_BUTTON_CHECKED_ROUNDED", "RADIO_BUTTON_CHECKED"),
                                                size=15,
                                                color=WaregTheme.STATUS_ONLINE,
                                            ),
                                            ft.Column(
                                                spacing=0,
                                                expand=True,
                                                controls=[
                                                    ft.Text(
                                                        "Penjemputan",
                                                        size=10,
                                                        color=WaregTheme.TEXT_SECONDARY,
                                                    ),
                                                    ft.Text(
                                                        pesanan_terbaru["jemput"],
                                                        size=12,
                                                        color=WaregTheme.TEXT_PRIMARY,
                                                        max_lines=1,
                                                        overflow=ft.TextOverflow.ELLIPSIS,
                                                    ),
                                                ],
                                            ),
                                        ],
                                    ),
                                    ft.Row(
                                        spacing=8,
                                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                        controls=[
                                            ft.Icon(
                                                get_icon("LOCATION_ON_ROUNDED", "LOCATION_ON"),
                                                size=15,
                                                color=WaregTheme.ACCENT,
                                            ),
                                            ft.Column(
                                                spacing=0,
                                                expand=True,
                                                controls=[
                                                    ft.Text(
                                                        "Tujuan",
                                                        size=10,
                                                        color=WaregTheme.TEXT_SECONDARY,
                                                    ),
                                                    ft.Text(
                                                        pesanan_terbaru["tujuan"],
                                                        size=12,
                                                        color=WaregTheme.TEXT_PRIMARY,
                                                        max_lines=1,
                                                        overflow=ft.TextOverflow.ELLIPSIS,
                                                    ),
                                                ],
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                ),
                ft.Container(
                    width=float("inf"),
                    content=ft.OutlinedButton(
                        on_click=on_lihat_semua_pesanan,
                        style=ft.ButtonStyle(
                            side=ft.BorderSide(1, WaregTheme.BORDER_SUBTLE),
                            color=WaregTheme.TEXT_PRIMARY,
                            shape=ft.RoundedRectangleBorder(radius=12),
                            padding=PaddingCls.symmetric(vertical=11),
                        ),
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=6,
                            controls=[
                                ft.Text(
                                    "Lihat Seluruh Pesanan",
                                    size=13,
                                    weight=ft.FontWeight.W_600,
                                ),
                                ft.Icon(
                                    get_icon("ARROW_FORWARD_ROUNDED", "ARROW_FORWARD"),
                                    size=16,
                                    color=WaregTheme.ACCENT,
                                ),
                            ],
                        ),
                    ),
                ),
            ],
        ),
    )


# ==============================================================================
# 5. HALAMAN TAB LENGKAP (PESANAN, RIWAYAT, PENDAPATAN, PROFIL)
# ==============================================================================
def build_tab_pesanan_content(
    state: Dict,
    on_simulate_order: Callable,
    on_advance_order: Callable,
    on_cancel_order: Callable,
    on_inspect_order: Callable[[Dict], None],
) -> ft.Column:
    """Tab 1: Manajemen Order Aktif & Daftar Pesanan Masuk."""
    aktif = state["pesanan_aktif"]
    controls: List[ft.Control] = [
        ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Text("Manajemen Pesanan", size=18, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                ButtonCls(
                    on_click=on_simulate_order,
                    style=ft.ButtonStyle(bgcolor=WaregTheme.ACCENT, color="#000000"),
                    content=ft.Row(
                        tight=True,
                        spacing=6,
                        controls=[
                            ft.Icon(get_icon("ADD_CIRCLE_OUTLINE_ROUNDED", "ADD"), size=16),
                            ft.Text("Simulasi Order Baru", size=12, weight=ft.FontWeight.BOLD),
                        ],
                    ),
                ),
            ],
        )
    ]

    if aktif is not None:
        controls.append(
            ft.Container(
                bgcolor=WaregTheme.CARD_PRIMARY,
                border_radius=16,
                padding=16,
                border=BorderCls.all(1.5, WaregTheme.ACCENT),
                content=ft.Column(
                    spacing=12,
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Row(
                                    spacing=8,
                                    controls=[
                                        ft.Icon(
                                            get_icon("DELIVERY_DINING_ROUNDED", "LOCAL_SHIPPING"),
                                            color=WaregTheme.ACCENT,
                                        ),
                                        ft.Text(
                                            f"{aktif['id_order']} • {aktif['layanan']}",
                                            size=14,
                                            weight=ft.FontWeight.BOLD,
                                            color="#FFFFFF",
                                        ),
                                    ],
                                ),
                                ft.Container(
                                    padding=PaddingCls.symmetric(horizontal=10, vertical=4),
                                    border_radius=8,
                                    bgcolor=WaregTheme.ACCENT_DARK,
                                    content=ft.Text(
                                        aktif["tahap_label"],
                                        size=11,
                                        weight=ft.FontWeight.BOLD,
                                        color=WaregTheme.ACCENT,
                                    ),
                                ),
                            ],
                        ),
                        ft.Text(
                            f"Pelanggan: {aktif['pelanggan']} • Jarak {aktif['jarak_km']} km",
                            size=13,
                            weight=ft.FontWeight.W_600,
                            color="#FFFFFF",
                        ),
                        ft.Container(
                            bgcolor=WaregTheme.CARD_SECONDARY,
                            border_radius=12,
                            padding=12,
                            content=ft.Column(
                                spacing=6,
                                controls=[
                                    ft.Text(f"Jemput: {aktif['jemput']}", size=12, color="#FFFFFF"),
                                    ft.Text(f"Tujuan: {aktif['tujuan']}", size=12, color="#FFFFFF"),
                                    ft.Text(
                                        f"Catatan: {aktif.get('catatan', '-')}",
                                        size=11,
                                        color=WaregTheme.TEXT_SECONDARY,
                                    ),
                                ],
                            ),
                        ),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text(
                                    f"Estimasi Tarif: {format_rupiah(aktif['pendapatan'])}",
                                    size=14,
                                    weight=ft.FontWeight.BOLD,
                                    color=WaregTheme.STATUS_ONLINE,
                                ),
                                ft.Row(
                                    spacing=8,
                                    controls=[
                                        ft.OutlinedButton(
                                            on_click=on_cancel_order,
                                            style=ft.ButtonStyle(
                                                side=ft.BorderSide(1, WaregTheme.DANGER),
                                                color=WaregTheme.DANGER,
                                            ),
                                            content=ft.Text("Batalkan", size=12),
                                        ),
                                        ButtonCls(
                                            on_click=on_advance_order,
                                            style=ft.ButtonStyle(
                                                bgcolor=WaregTheme.STATUS_ONLINE,
                                                color="#000000",
                                            ),
                                            content=ft.Text(
                                                aktif["next_action_label"],
                                                size=12,
                                                weight=ft.FontWeight.BOLD,
                                            ),
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
            )
        )
    else:
        controls.append(
            ft.Container(
                bgcolor=WaregTheme.CARD_PRIMARY,
                border_radius=16,
                padding=20,
                border=BorderCls.all(1, WaregTheme.BORDER_SUBTLE),
                content=ft.Row(
                    spacing=12,
                    controls=[
                        ft.Icon(get_icon("INBOX_ROUNDED", "INBOX"), size=30, color=WaregTheme.TEXT_SECONDARY),
                        ft.Column(
                            spacing=2,
                            expand=True,
                            controls=[
                                ft.Text(
                                    "Belum ada pesanan yang sedang diantar",
                                    size=14,
                                    weight=ft.FontWeight.BOLD,
                                    color="#FFFFFF",
                                ),
                                ft.Text(
                                    "Klik 'Simulasi Order Baru' di atas untuk menguji penerimaan & penyelesaian order.",
                                    size=12,
                                    color=WaregTheme.TEXT_SECONDARY,
                                ),
                            ],
                        ),
                    ],
                ),
            )
        )

    controls.append(
        ft.Text("Daftar Pesanan Terakhir", size=15, weight=ft.FontWeight.BOLD, color="#FFFFFF")
    )
    for item in state["pesanan_terbaru"]:
        controls.append(
            ft.Container(
                bgcolor=WaregTheme.CARD_PRIMARY,
                border_radius=14,
                padding=14,
                border=BorderCls.all(1, WaregTheme.BORDER_SUBTLE),
                ink=True,
                on_click=lambda e, order=item: on_inspect_order(order),
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Column(
                            spacing=4,
                            expand=True,
                            controls=[
                                ft.Text(
                                    f"{item['pelanggan']} • {item['layanan']}",
                                    size=13,
                                    weight=ft.FontWeight.BOLD,
                                    color="#FFFFFF",
                                ),
                                ft.Text(
                                    f"{item['jemput']} → {item['tujuan']}",
                                    size=12,
                                    color=WaregTheme.TEXT_SECONDARY,
                                    max_lines=1,
                                    overflow=ft.TextOverflow.ELLIPSIS,
                                ),
                            ],
                        ),
                        ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.END,
                            spacing=3,
                            controls=[
                                ft.Text(
                                    format_rupiah(item["pendapatan"]),
                                    size=13,
                                    weight=ft.FontWeight.BOLD,
                                    color=WaregTheme.ACCENT,
                                ),
                                ft.Text(item["waktu"], size=11, color=WaregTheme.TEXT_SECONDARY),
                            ],
                        ),
                    ],
                ),
            )
        )

    return ft.Column(spacing=12, controls=controls)


def build_tab_riwayat_content(
    state: Dict,
    on_change_filter: Callable[[str], None],
    on_inspect_order: Callable[[Dict], None],
) -> ft.Column:
    """Tab 2: Riwayat Perjalanan dengan filter layanan Wareg Express."""
    selected = state["filter_riwayat"]
    categories = ["Semua", "Wareg Ride", "Wareg Car", "Wareg Food", "Wareg Send"]

    chips = [
        ft.Container(
            padding=PaddingCls.symmetric(horizontal=12, vertical=7),
            border_radius=20,
            bgcolor=WaregTheme.ACCENT if cat == selected else WaregTheme.CARD_PRIMARY,
            border=BorderCls.all(1, WaregTheme.ACCENT if cat == selected else WaregTheme.BORDER_SUBTLE),
            ink=True,
            on_click=lambda e, c=cat: on_change_filter(c),
            content=ft.Text(
                cat,
                size=12,
                weight=ft.FontWeight.BOLD if cat == selected else ft.FontWeight.NORMAL,
                color="#000000" if cat == selected else "#FFFFFF",
            ),
        )
        for cat in categories
    ]

    filtered = [
        p
        for p in state["pesanan_terbaru"]
        if selected == "Semua" or p["layanan"] == selected
    ]

    cards = [
        ft.Container(
            bgcolor=WaregTheme.CARD_PRIMARY,
            border_radius=14,
            padding=14,
            border=BorderCls.all(1, WaregTheme.BORDER_SUBTLE),
            ink=True,
            on_click=lambda e, order=p: on_inspect_order(order),
            content=ft.Column(
                spacing=8,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text(
                                f"{p['id_order']} • {p['layanan']}",
                                size=12,
                                weight=ft.FontWeight.BOLD,
                                color=WaregTheme.ACCENT,
                            ),
                            ft.Text(p["waktu"], size=11, color=WaregTheme.TEXT_SECONDARY),
                        ],
                    ),
                    ft.Text(
                        f"Pelanggan: {p['pelanggan']}",
                        size=13,
                        weight=ft.FontWeight.BOLD,
                        color="#FFFFFF",
                    ),
                    ft.Text(f"Dari: {p['jemput']}", size=12, color=WaregTheme.TEXT_SECONDARY),
                    ft.Text(f"Ke: {p['tujuan']}", size=12, color=WaregTheme.TEXT_SECONDARY),
                    ft.Divider(height=1, color=WaregTheme.BORDER_SUBTLE),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text(f"Jarak: {p.get('jarak_km', 3.5)} km", size=12, color=WaregTheme.TEXT_SECONDARY),
                            ft.Text(
                                format_rupiah(p["pendapatan"]),
                                size=14,
                                weight=ft.FontWeight.BOLD,
                                color=WaregTheme.STATUS_ONLINE,
                            ),
                        ],
                    ),
                ],
            ),
        )
        for p in filtered
    ]

    if not cards:
        cards.append(
            ft.Container(
                bgcolor=WaregTheme.CARD_PRIMARY,
                border_radius=14,
                padding=20,
                content=ft.Text(
                    f"Belum ada riwayat untuk kategori {selected}.",
                    size=13,
                    color=WaregTheme.TEXT_SECONDARY,
                ),
            )
        )

    return ft.Column(
        spacing=12,
        controls=[
            ft.Text("Riwayat Pengantaran", size=18, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
            ft.Row(spacing=8, wrap=True, controls=chips),
            *cards,
        ],
    )


def build_tab_pendapatan_content(
    state: Dict,
    on_open_withdraw: Callable,
) -> ft.Column:
    """Tab 3: Dompet Wareg Express, Rincian Pendapatan, & Penarikan Saldo."""
    pendapatan = state["pendapatan"]

    rincian_cards = [
        ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Text(r["judul"], size=13, color=WaregTheme.TEXT_SECONDARY),
                ft.Text(format_rupiah(r["nominal"]), size=13, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
            ],
        )
        for r in pendapatan["rincian_hari_ini"]
    ]

    wd_cards = [
        ft.Container(
            bgcolor=WaregTheme.CARD_SECONDARY,
            border_radius=10,
            padding=10,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Column(
                        spacing=2,
                        controls=[
                            ft.Text(w["tujuan"], size=13, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                            ft.Text(w["tanggal"], size=11, color=WaregTheme.TEXT_SECONDARY),
                        ],
                    ),
                    ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.END,
                        spacing=2,
                        controls=[
                            ft.Text(
                                f"- {format_rupiah(w['nominal'])}",
                                size=13,
                                weight=ft.FontWeight.BOLD,
                                color=WaregTheme.ACCENT,
                            ),
                            ft.Text(w["status"], size=11, color=WaregTheme.STATUS_ONLINE),
                        ],
                    ),
                ],
            ),
        )
        for w in pendapatan["riwayat_penarikan"]
    ]

    return ft.Column(
        spacing=14,
        controls=[
            ft.Text("Dompet & Pendapatan", size=18, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
            ft.Container(
                bgcolor=WaregTheme.CARD_PRIMARY,
                border_radius=16,
                padding=18,
                border=BorderCls.all(1, WaregTheme.ACCENT),
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Column(
                            spacing=4,
                            controls=[
                                ft.Text("Saldo Dompet Tersedia", size=12, color=WaregTheme.TEXT_SECONDARY),
                                ft.Text(
                                    format_rupiah(pendapatan["saldo_dompet"]),
                                    size=26,
                                    weight=ft.FontWeight.BOLD,
                                    color=WaregTheme.ACCENT,
                                ),
                                ft.Text(
                                    f"Total Minggu Ini: {format_rupiah(pendapatan['minggu_ini'])}",
                                    size=12,
                                    color=WaregTheme.TEXT_SECONDARY,
                                ),
                            ],
                        ),
                        ButtonCls(
                            on_click=on_open_withdraw,
                            style=ft.ButtonStyle(
                                bgcolor=WaregTheme.ACCENT,
                                color="#000000",
                                shape=ft.RoundedRectangleBorder(radius=12),
                                padding=PaddingCls.symmetric(horizontal=16, vertical=12),
                            ),
                            content=ft.Row(
                                tight=True,
                                spacing=6,
                                controls=[
                                    ft.Icon(get_icon("PAYMENTS_ROUNDED", "ACCOUNT_BALANCE"), size=18),
                                    ft.Text("Tarik Saldo", size=13, weight=ft.FontWeight.BOLD),
                                ],
                            ),
                        ),
                    ],
                ),
            ),
            ft.Container(
                bgcolor=WaregTheme.CARD_PRIMARY,
                border_radius=16,
                padding=16,
                border=BorderCls.all(1, WaregTheme.BORDER_SUBTLE),
                content=ft.Column(
                    spacing=10,
                    controls=[
                        ft.Text("Rincian Pendapatan Hari Ini", size=15, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                        *rincian_cards,
                        ft.Divider(height=1, color=WaregTheme.BORDER_SUBTLE),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text("Total Hari Ini", size=14, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                                ft.Text(
                                    format_rupiah(pendapatan["hari_ini"]),
                                    size=15,
                                    weight=ft.FontWeight.BOLD,
                                    color=WaregTheme.STATUS_ONLINE,
                                ),
                            ],
                        ),
                    ],
                ),
            ),
            ft.Container(
                bgcolor=WaregTheme.CARD_PRIMARY,
                border_radius=16,
                padding=16,
                border=BorderCls.all(1, WaregTheme.BORDER_SUBTLE),
                content=ft.Column(
                    spacing=10,
                    controls=[
                        ft.Text("Riwayat Penarikan Saldo", size=15, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                        *wd_cards,
                    ],
                ),
            ),
        ],
    )


def build_tab_profil_content(
    state: Dict,
    on_edit_profile: Callable,
    on_logout: Optional[Callable] = None,
) -> ft.Column:
    """Tab 4: Profil Lengkap Mitra Driver Wareg Express."""
    driver = state["driver"]

    def info_row(label: str, val: str) -> ft.Row:
        return ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Text(label, size=13, color=WaregTheme.TEXT_SECONDARY),
                ft.Text(val, size=13, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
            ],
        )

    controls: List[ft.Control] = [
        ft.Text("Profil Mitra Driver", size=18, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
        ft.Container(
            bgcolor=WaregTheme.CARD_PRIMARY,
            border_radius=16,
            padding=18,
            border=BorderCls.all(1, WaregTheme.BORDER_SUBTLE),
            content=ft.Column(
                spacing=12,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Row(
                                spacing=12,
                                controls=[
                                    ft.CircleAvatar(
                                        radius=26,
                                        bgcolor=WaregTheme.ACCENT_DARK,
                                        content=ft.Text(
                                            driver["inisial"],
                                            size=18,
                                            weight=ft.FontWeight.BOLD,
                                            color=WaregTheme.ACCENT,
                                        ),
                                    ),
                                    ft.Column(
                                        spacing=2,
                                        controls=[
                                            ft.Text(
                                                driver["nama"],
                                                size=16,
                                                weight=ft.FontWeight.BOLD,
                                                color="#FFFFFF",
                                            ),
                                            ft.Text(
                                                f"Mitra Resmi Wareg Express • Rating {driver['rating']:.2f}",
                                                size=12,
                                                color=WaregTheme.ACCENT,
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                            ft.OutlinedButton(
                                on_click=on_edit_profile,
                                style=ft.ButtonStyle(
                                    side=ft.BorderSide(1, WaregTheme.ACCENT),
                                    color=WaregTheme.ACCENT,
                                ),
                                content=ft.Text("Edit Profil", size=12),
                            ),
                        ],
                    ),
                    ft.Divider(height=1, color=WaregTheme.BORDER_SUBTLE),
                    info_row("ID Mitra Driver", driver["id_driver"]),
                    info_row("Nomor Telepon", driver["no_hp"]),
                    info_row("Kendaraan", driver["kendaraan"]),
                    info_row("Nomor Polisi", driver["plat_nomor"]),
                    info_row("Tingkat Penyelesaian", "98,5%"),
                ],
            ),
        ),
    ]

    if on_logout is not None:
        controls.append(
            ft.Container(
                width=float("inf"),
                content=ft.OutlinedButton(
                    on_click=lambda e: on_logout(),
                    style=ft.ButtonStyle(
                        side=ft.BorderSide(1, WaregTheme.DANGER),
                        color=WaregTheme.DANGER,
                        shape=ft.RoundedRectangleBorder(radius=12),
                        padding=PaddingCls.symmetric(vertical=12),
                    ),
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=6,
                        controls=[
                            ft.Icon(get_icon("LOGOUT_ROUNDED", "LOGOUT"), size=18),
                            ft.Text("Keluar Akun (Logout)", size=13, weight=ft.FontWeight.BOLD),
                        ],
                    ),
                ),
            )
        )

    return ft.Column(spacing=14, controls=controls)


# ==============================================================================
# 6. BOTTOM NAVIGATION BAR (FULL-WIDTH RESPONSIVE)
# ==============================================================================
def build_bottom_navigation(
    active_index: int,
    on_select_tab: Callable[[int], None],
) -> ft.Container:
    """Bagian I: Navigasi bawah 5 menu dengan warna aktif #00b6fd."""
    nav_items = [
        {
            "label": "Beranda",
            "icon": get_icon("HOME_OUTLINED", "HOME"),
            "active_icon": get_icon("HOME_ROUNDED", "HOME"),
        },
        {
            "label": "Pesanan",
            "icon": get_icon("RECEIPT_LONG_OUTLINED", "RECEIPT_LONG"),
            "active_icon": get_icon("RECEIPT_LONG_ROUNDED", "RECEIPT_LONG"),
        },
        {
            "label": "Riwayat",
            "icon": get_icon("HISTORY_OUTLINED", "HISTORY"),
            "active_icon": get_icon("HISTORY_ROUNDED", "HISTORY"),
        },
        {
            "label": "Pendapatan",
            "icon": get_icon("ACCOUNT_BALANCE_WALLET_OUTLINED", "ACCOUNT_BALANCE_WALLET"),
            "active_icon": get_icon("ACCOUNT_BALANCE_WALLET_ROUNDED", "ACCOUNT_BALANCE_WALLET"),
        },
        {
            "label": "Profil",
            "icon": get_icon("PERSON_OUTLINE_ROUNDED", "PERSON_OUTLINE"),
            "active_icon": get_icon("PERSON_ROUNDED", "PERSON"),
        },
    ]

    controls = []
    for idx, item in enumerate(nav_items):
        is_active = idx == active_index
        color = WaregTheme.ACCENT if is_active else WaregTheme.TEXT_SECONDARY
        controls.append(
            ft.Container(
                expand=True,
                padding=PaddingCls.symmetric(vertical=8),
                ink=True,
                on_click=lambda e, target_idx=idx: on_select_tab(target_idx),
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=4,
                    tight=True,
                    controls=[
                        ft.Container(
                            width=28,
                            height=3,
                            border_radius=2,
                            bgcolor=WaregTheme.ACCENT if is_active else "transparent",
                        ),
                        ft.Icon(
                            item["active_icon"] if is_active else item["icon"],
                            size=22,
                            color=color,
                        ),
                        ft.Text(
                            item["label"],
                            size=11,
                            weight=ft.FontWeight.BOLD if is_active else ft.FontWeight.NORMAL,
                            color=color,
                        ),
                    ],
                ),
            )
        )

    return ft.Container(
        bgcolor=WaregTheme.CARD_PRIMARY,
        border=BorderCls.only(top=ft.BorderSide(1, WaregTheme.BORDER_SUBTLE)),
        padding=PaddingCls.symmetric(horizontal=12, vertical=2),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            controls=controls,
        ),
    )


# ==============================================================================
# 7. CONTROLLER & BUILDER UTAMA HALAMAN BERANDA DRIVER
# ==============================================================================
class BerandaDriverController:
    """Mengelola state dan interaksi UI halaman Beranda Driver Wareg Express."""

    def __init__(
        self,
        page: ft.Page,
        driver_data: Optional[Dict] = None,
        on_navigate: Optional[Callable[[str], None]] = None,
        on_logout: Optional[Callable[[], None]] = None,
    ) -> None:
        self.page = page
        self.state = get_default_driver_state()
        if driver_data:
            self.state["driver"].update(driver_data)

        self.on_navigate = on_navigate
        self.on_logout = on_logout

        self.scroll_body = ft.Column(
            spacing=16,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )
        self.bottom_nav_host = ft.Container()

        # Root container melebar penuh mengikuti layar laptop maupun HP
        self.root_container = ft.Container(
            expand=True,
            bgcolor=WaregTheme.BG_PRIMARY,
            content=ft.Column(
                spacing=0,
                expand=True,
                controls=[
                    ft.Container(
                        expand=True,
                        padding=PaddingCls.symmetric(horizontal=20, vertical=12),
                        content=self.scroll_body,
                    ),
                    self.bottom_nav_host,
                ],
            ),
        )
        self.refresh_ui(initial=True)

    # --- Event Handlers ---
    def handle_toggle_status(self, e: ft.ControlEvent) -> None:
        self.state["is_online"] = bool(e.control.value)
        if self.state["is_online"]:
            show_snackbar(self.page, "Status ONLINE: Siap menerima pesanan Wareg Express!")
        else:
            show_snackbar(self.page, "Status OFFLINE: Kamu tidak menerima pesanan.")
        self.refresh_ui()

    def handle_toggle_layanan(self, service_id: str) -> None:
        layanan_list = self.state["layanan"]
        aktif_count = sum(1 for item in layanan_list if item["aktif"])

        for item in layanan_list:
            if item["id"] == service_id:
                if item["aktif"] and aktif_count <= 1:
                    show_snackbar(self.page, "Minimal 1 layanan Wareg Express harus tetap aktif.")
                    return
                item["aktif"] = not item["aktif"]
                status_txt = "diaktifkan" if item["aktif"] else "dinonaktifkan"
                show_snackbar(self.page, f"Layanan {item['nama']} {status_txt}.")
                break
        self.refresh_ui()

    def handle_my_location(self, e: ft.ControlEvent) -> None:
        self.state["lokasi"]["alamat"] = "Jl. Basuki Rahmat No. 88, Surabaya"
        self.state["lokasi"]["koordinat"] = "-7.2657, 112.7418"
        self.state["lokasi"]["zona"] = "Zona Ramai • Pusat Kota"
        self.state["lokasi"]["pin_left"] = 180
        self.state["lokasi"]["pin_top"] = 70
        show_snackbar(self.page, "Posisi dipusatkan ke lokasi awal driver.")
        self.refresh_ui()

    def handle_select_spot_direct(self, spot: Dict) -> None:
        self.state["lokasi"]["alamat"] = f"{spot['nama']} ({spot['alamat']})"
        self.state["lokasi"]["koordinat"] = spot["koordinat"]
        self.state["lokasi"]["zona"] = f"Hotspot • Permintaan {spot['permintaan']}"
        self.state["lokasi"]["pin_left"] = spot["pin_left"]
        self.state["lokasi"]["pin_top"] = spot["pin_top"]
        show_snackbar(self.page, f"Simulasi posisi diarahkan ke {spot['nama']} ({spot['jarak']}).")
        self.refresh_ui()

    def handle_open_navigation(self, e: ft.ControlEvent) -> None:
        dialog = ft.AlertDialog(
            bgcolor=WaregTheme.CARD_PRIMARY,
            title=ft.Text("Navigasi ke Zona Ramai", size=16, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
        )

        sekitar_items = [
            ft.Container(
                bgcolor=WaregTheme.CARD_SECONDARY,
                border_radius=10,
                padding=10,
                ink=True,
                on_click=lambda ev, spot=spot: (
                    close_modal(self.page, dialog),
                    self.handle_select_spot_direct(spot),
                ),
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Column(
                            spacing=2,
                            controls=[
                                ft.Text(spot["nama"], size=13, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                                ft.Text(f"Permintaan: {spot['permintaan']}", size=11, color=WaregTheme.ACCENT),
                            ],
                        ),
                        ft.Text(spot["jarak"], size=12, color=WaregTheme.TEXT_SECONDARY),
                    ],
                ),
            )
            for spot in self.state["lokasi"]["sekitar"]
        ]

        dialog.content = ft.Column(
            tight=True,
            spacing=8,
            controls=[
                ft.Text(
                    "Pilih titik hotspot untuk menggerakkan penanda pada peta simulasi:",
                    size=12,
                    color=WaregTheme.TEXT_SECONDARY,
                ),
                *sekitar_items,
            ],
        )
        dialog.actions = [
            ft.TextButton(
                content=ft.Text("Tutup", color=WaregTheme.ACCENT),
                on_click=lambda ev: close_modal(self.page, dialog),
            ),
        ]
        open_modal(self.page, dialog)

    def handle_open_notif(self, e: ft.ControlEvent) -> None:
        for n in self.state["notifikasi"]:
            n["dibaca"] = True

        dialog = ft.AlertDialog(
            bgcolor=WaregTheme.CARD_PRIMARY,
            title=ft.Text("Notifikasi Wareg Express", size=16, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
        )

        if self.state["notifikasi"]:
            notif_controls = [
                ft.Container(
                    bgcolor=WaregTheme.CARD_SECONDARY,
                    border_radius=10,
                    padding=10,
                    content=ft.Column(
                        spacing=3,
                        controls=[
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Text(n["judul"], size=12, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                                    ft.Text(n["waktu"], size=10, color=WaregTheme.TEXT_SECONDARY),
                                ],
                            ),
                            ft.Text(n["pesan"], size=11, color=WaregTheme.TEXT_SECONDARY),
                        ],
                    ),
                )
                for n in self.state["notifikasi"]
            ]
        else:
            notif_controls = [
                ft.Text("Tidak ada notifikasi baru.", size=12, color=WaregTheme.TEXT_SECONDARY)
            ]

        def clear_all_notif(ev) -> None:
            self.state["notifikasi"].clear()
            close_modal(self.page, dialog)
            show_snackbar(self.page, "Semua notifikasi telah dibersihkan.")
            self.refresh_ui()

        dialog.content = ft.Column(tight=True, spacing=8, controls=notif_controls)
        dialog.actions = [
            ft.TextButton(
                content=ft.Text("Hapus Semua", color=WaregTheme.DANGER),
                on_click=clear_all_notif,
            ),
            ft.TextButton(
                content=ft.Text("Tutup", color=WaregTheme.ACCENT),
                on_click=lambda ev: close_modal(self.page, dialog),
            ),
        ]
        open_modal(self.page, dialog)
        self.refresh_ui()

    def handle_open_settings(self, e: ft.ControlEvent) -> None:
        cfg = self.state["pengaturan"]

        def toggle_cfg(key: str, val: bool) -> None:
            cfg[key] = val

        radius_text = ft.Text(f"Radius Pencarian Order: {cfg['radius_km']} km", size=12, color="#FFFFFF")

        def change_radius(ev: ft.ControlEvent) -> None:
            cfg["radius_km"] = int(ev.control.value)
            radius_text.value = f"Radius Pencarian Order: {cfg['radius_km']} km"
            self.page.update()

        dialog = ft.AlertDialog(
            bgcolor=WaregTheme.CARD_PRIMARY,
            title=ft.Text("Pengaturan Cepat Driver", size=16, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
            content=ft.Column(
                tight=True,
                spacing=10,
                controls=[
                    make_switch(
                        label="Terima Pesanan Otomatis",
                        value=cfg["auto_accept"],
                        active_color=WaregTheme.ACCENT,
                        on_change=lambda ev: toggle_cfg("auto_accept", bool(ev.control.value)),
                    ),
                    make_switch(
                        label="Suara Notifikasi Order",
                        value=cfg["suara_order"],
                        active_color=WaregTheme.ACCENT,
                        on_change=lambda ev: toggle_cfg("suara_order", bool(ev.control.value)),
                    ),
                    make_switch(
                        label="Mode Hemat Daya Peta",
                        value=cfg["hemat_baterai"],
                        active_color=WaregTheme.ACCENT,
                        on_change=lambda ev: toggle_cfg("hemat_baterai", bool(ev.control.value)),
                    ),
                    radius_text,
                    ft.Slider(
                        min=1,
                        max=15,
                        divisions=14,
                        value=cfg["radius_km"],
                        active_color=WaregTheme.ACCENT,
                        on_change=change_radius,
                    ),
                ],
            ),
        )
        dialog.actions = [
            ft.TextButton(
                content=ft.Text("Simpan", color=WaregTheme.ACCENT),
                on_click=lambda ev: (
                    close_modal(self.page, dialog),
                    show_snackbar(self.page, "Pengaturan driver disimpan."),
                    self.refresh_ui(),
                ),
            ),
        ]
        open_modal(self.page, dialog)

    def handle_claim_bonus(self, e: ft.ControlEvent) -> None:
        pendapatan = self.state["pendapatan"]
        if pendapatan["pesanan_selesai"] >= pendapatan["target_harian_order"] and not pendapatan["bonus_diklaim"]:
            bonus = pendapatan["bonus_target_nominal"]
            pendapatan["bonus_diklaim"] = True
            pendapatan["bonus_insentif"] += bonus
            pendapatan["hari_ini"] += bonus
            pendapatan["minggu_ini"] += bonus
            pendapatan["saldo_dompet"] += bonus
            pendapatan["rincian_hari_ini"].append(
                {"judul": "Klaim Bonus Target Harian", "nominal": bonus}
            )
            show_snackbar(self.page, f"Selamat! Bonus {format_rupiah(bonus)} berhasil diklaim.")
            self.refresh_ui()

    def handle_detail_pendapatan(self, e: ft.ControlEvent) -> None:
        pendapatan = self.state["pendapatan"]
        rows = [
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Text(item["judul"], size=12, color=WaregTheme.TEXT_SECONDARY, expand=True),
                    ft.Text(
                        format_rupiah(item["nominal"]),
                        size=12,
                        weight=ft.FontWeight.BOLD,
                        color="#FFFFFF",
                    ),
                ],
            )
            for item in pendapatan["rincian_hari_ini"]
        ]

        dialog = ft.AlertDialog(
            bgcolor=WaregTheme.CARD_PRIMARY,
            title=ft.Text("Detail Pendapatan Hari Ini", size=16, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
            content=ft.Column(
                tight=True,
                spacing=10,
                controls=[
                    *rows,
                    ft.Divider(height=1, color=WaregTheme.BORDER_SUBTLE),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text("Total Pendapatan", size=13, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                            ft.Text(
                                format_rupiah(pendapatan["hari_ini"]),
                                size=15,
                                weight=ft.FontWeight.BOLD,
                                color=WaregTheme.ACCENT,
                            ),
                        ],
                    ),
                ],
            ),
        )
        dialog.actions = [
            ft.TextButton(
                content=ft.Text("Buka Dompet", color=WaregTheme.ACCENT),
                on_click=lambda ev: (
                    close_modal(self.page, dialog),
                    self.handle_select_tab(3),
                ),
            ),
            ft.TextButton(
                content=ft.Text("Tutup", color=WaregTheme.TEXT_SECONDARY),
                on_click=lambda ev: close_modal(self.page, dialog),
            ),
        ]
        open_modal(self.page, dialog)

    def handle_simulate_order(self, e: ft.ControlEvent) -> None:
        """Memunculkan simulasi order masuk sesuai layanan aktif."""
        if not self.state["is_online"]:
            show_snackbar(self.page, "Aktifkan status ONLINE terlebih dahulu untuk menerima order.")
            return

        if self.state["pesanan_aktif"] is not None:
            show_snackbar(self.page, "Selesaikan order aktif saat ini terlebih dahulu.")
            self.handle_select_tab(1)
            return

        aktif_names = {item["nama"] for item in self.state["layanan"] if item["aktif"]}
        kandidat = [
            o for o in self.state["kandidat_simulasi_order"] if o["layanan"] in aktif_names
        ] or self.state["kandidat_simulasi_order"]
        order = dict(random.choice(kandidat))

        dialog = ft.AlertDialog(
            bgcolor=WaregTheme.CARD_PRIMARY,
            title=ft.Row(
                spacing=8,
                controls=[
                    ft.Icon(get_icon("FASTFOOD_ROUNDED", "RESTAURANT"), color=WaregTheme.ACCENT),
                    ft.Text(
                        f"Order Masuk • {order['layanan']}",
                        size=15,
                        weight=ft.FontWeight.BOLD,
                        color="#FFFFFF",
                    ),
                ],
            ),
            content=ft.Column(
                tight=True,
                spacing=8,
                controls=[
                    ft.Text(
                        f"Pelanggan: {order['pelanggan']} ({order['jarak_km']} km)",
                        size=13,
                        color="#FFFFFF",
                        weight=ft.FontWeight.W_600,
                    ),
                    ft.Text(f"Jemput: {order['jemput']}", size=12, color=WaregTheme.TEXT_SECONDARY),
                    ft.Text(f"Tujuan: {order['tujuan']}", size=12, color=WaregTheme.TEXT_SECONDARY),
                    ft.Text(f"Catatan: {order['catatan']}", size=11, color=WaregTheme.TEXT_SECONDARY),
                    ft.Container(
                        bgcolor=WaregTheme.ACCENT_DARK,
                        padding=10,
                        border_radius=10,
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text("Estimasi Pendapatan", size=12, color=WaregTheme.TEXT_PRIMARY),
                                ft.Text(
                                    format_rupiah(order["pendapatan"]),
                                    size=14,
                                    weight=ft.FontWeight.BOLD,
                                    color=WaregTheme.ACCENT,
                                ),
                            ],
                        ),
                    ),
                ],
            ),
        )
        dialog.actions = [
            ft.TextButton(
                content=ft.Text("Tolak", color=WaregTheme.TEXT_SECONDARY),
                on_click=lambda ev: (
                    close_modal(self.page, dialog),
                    show_snackbar(self.page, "Pesanan dilewati."),
                ),
            ),
            ButtonCls(
                content=ft.Text("Terima Order", weight=ft.FontWeight.BOLD),
                style=ft.ButtonStyle(bgcolor=WaregTheme.STATUS_ONLINE, color="#000000"),
                on_click=lambda ev: self._accept_order(dialog, order),
            ),
        ]
        open_modal(self.page, dialog)

    def _accept_order(self, dialog: ft.AlertDialog, order: Dict) -> None:
        close_modal(self.page, dialog)
        order["tahap"] = 1
        order["tahap_label"] = "Menuju Titik Jemput"
        order["next_action_label"] = "Sudah di Titik Jemput"
        self.state["pesanan_aktif"] = order
        self.state["active_tab"] = 1
        show_snackbar(self.page, f"Order {order['id_order']} diterima! Silakan menuju titik jemput.")
        self.refresh_ui()

    def handle_advance_order(self, e: ft.ControlEvent) -> None:
        aktif = self.state["pesanan_aktif"]
        if aktif is None:
            return

        if aktif["tahap"] == 1:
            aktif["tahap"] = 2
            aktif["tahap_label"] = "Mengantar ke Tujuan"
            aktif["next_action_label"] = "Selesaikan Pesanan"
            show_snackbar(self.page, "Pesanan diambil! Lanjut antar ke lokasi tujuan.")
        else:
            # Selesaikan order dan perbarui seluruh metrik
            tarif = aktif["pendapatan"]
            jarak = aktif.get("jarak_km", 4.0)
            self.state["pendapatan"]["hari_ini"] += tarif
            self.state["pendapatan"]["minggu_ini"] += tarif
            self.state["pendapatan"]["saldo_dompet"] += tarif
            self.state["pendapatan"]["pesanan_selesai"] += 1
            self.state["statistik"]["total_order"] += 1
            self.state["statistik"]["total_jarak_km"] += jarak

            completed_record = {
                "id_order": aktif["id_order"],
                "pelanggan": aktif["pelanggan"],
                "layanan": aktif["layanan"],
                "jemput": aktif["jemput"],
                "tujuan": aktif["tujuan"],
                "status": "Selesai",
                "pendapatan": tarif,
                "jarak_km": jarak,
                "waktu": "Baru saja",
                "catatan": aktif.get("catatan", "-"),
            }
            self.state["pesanan_terbaru"].insert(0, completed_record)
            self.state["pesanan_aktif"] = None
            show_snackbar(self.page, f"Pesanan selesai! +{format_rupiah(tarif)} ditambahkan ke saldo.")

        self.refresh_ui()

    def handle_cancel_order(self, e: ft.ControlEvent) -> None:
        self.state["pesanan_aktif"] = None
        show_snackbar(self.page, "Pesanan aktif dibatalkan.")
        self.refresh_ui()

    def handle_inspect_order(self, order: Dict) -> None:
        dialog = ft.AlertDialog(
            bgcolor=WaregTheme.CARD_PRIMARY,
            title=ft.Text(
                f"Detail Order • {order['id_order']}",
                size=16,
                weight=ft.FontWeight.BOLD,
                color="#FFFFFF",
            ),
            content=ft.Column(
                tight=True,
                spacing=8,
                controls=[
                    ft.Text(f"Layanan: {order['layanan']}", size=13, color=WaregTheme.ACCENT, weight=ft.FontWeight.BOLD),
                    ft.Text(f"Pelanggan: {order['pelanggan']}", size=13, color="#FFFFFF"),
                    ft.Text(f"Penjemputan: {order['jemput']}", size=12, color=WaregTheme.TEXT_SECONDARY),
                    ft.Text(f"Tujuan: {order['tujuan']}", size=12, color=WaregTheme.TEXT_SECONDARY),
                    ft.Text(f"Catatan: {order.get('catatan', '-')}", size=12, color=WaregTheme.TEXT_SECONDARY),
                    ft.Divider(height=1, color=WaregTheme.BORDER_SUBTLE),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text("Pendapatan Bersih", size=13, color="#FFFFFF"),
                            ft.Text(
                                format_rupiah(order["pendapatan"]),
                                size=15,
                                weight=ft.FontWeight.BOLD,
                                color=WaregTheme.STATUS_ONLINE,
                            ),
                        ],
                    ),
                ],
            ),
        )
        dialog.actions = [
            ft.TextButton(
                content=ft.Text("Tutup", color=WaregTheme.ACCENT),
                on_click=lambda ev: close_modal(self.page, dialog),
            ),
        ]
        open_modal(self.page, dialog)

    def handle_open_withdraw(self, e: ft.ControlEvent) -> None:
        saldo = self.state["pendapatan"]["saldo_dompet"]
        amount_field = ft.TextField(
            label="Nominal Penarikan (Rp)",
            value=str(min(100000, saldo)),
            keyboard_type=ft.KeyboardType.NUMBER,
            bgcolor=WaregTheme.CARD_SECONDARY,
            color="#FFFFFF",
            border_color=WaregTheme.BORDER_SUBTLE,
        )

        dialog = ft.AlertDialog(
            bgcolor=WaregTheme.CARD_PRIMARY,
            title=ft.Text("Tarik Saldo Wareg Express", size=16, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
            content=ft.Column(
                tight=True,
                spacing=10,
                controls=[
                    ft.Text(
                        f"Saldo tersedia: {format_rupiah(saldo)}",
                        size=13,
                        color=WaregTheme.ACCENT,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Text("Rekening Tujuan: BCA •••• 8821 (a.n. Budi Santoso)", size=12, color=WaregTheme.TEXT_SECONDARY),
                    amount_field,
                ],
            ),
        )

        def submit_withdraw(ev) -> None:
            raw = "".join(ch for ch in (amount_field.value or "") if ch.isdigit())
            nominal = int(raw) if raw else 0
            if nominal < 20000:
                show_snackbar(self.page, "Minimal penarikan saldo adalah Rp 20.000.")
                return
            if nominal > self.state["pendapatan"]["saldo_dompet"]:
                show_snackbar(self.page, "Saldo dompet tidak mencukupi.")
                return

            self.state["pendapatan"]["saldo_dompet"] -= nominal
            self.state["pendapatan"]["riwayat_penarikan"].insert(
                0,
                {
                    "tanggal": "Hari ini",
                    "tujuan": "BCA •••• 8821",
                    "nominal": nominal,
                    "status": "Berhasil",
                },
            )
            close_modal(self.page, dialog)
            show_snackbar(self.page, f"Penarikan {format_rupiah(nominal)} berhasil diproses!")
            self.refresh_ui()

        dialog.actions = [
            ft.TextButton(
                content=ft.Text("Batal", color=WaregTheme.TEXT_SECONDARY),
                on_click=lambda ev: close_modal(self.page, dialog),
            ),
            ButtonCls(
                content=ft.Text("Konfirmasi Tarik", weight=ft.FontWeight.BOLD),
                style=ft.ButtonStyle(bgcolor=WaregTheme.ACCENT, color="#000000"),
                on_click=submit_withdraw,
            ),
        ]
        open_modal(self.page, dialog)

    def handle_edit_profile(self, e: ft.ControlEvent) -> None:
        driver = self.state["driver"]
        hp_field = ft.TextField(
            label="Nomor Telepon",
            value=driver["no_hp"],
            bgcolor=WaregTheme.CARD_SECONDARY,
            color="#FFFFFF",
        )
        kendaraan_field = ft.TextField(
            label="Kendaraan",
            value=driver["kendaraan"],
            bgcolor=WaregTheme.CARD_SECONDARY,
            color="#FFFFFF",
        )
        plat_field = ft.TextField(
            label="Nomor Polisi",
            value=driver["plat_nomor"],
            bgcolor=WaregTheme.CARD_SECONDARY,
            color="#FFFFFF",
        )

        dialog = ft.AlertDialog(
            bgcolor=WaregTheme.CARD_PRIMARY,
            title=ft.Text("Edit Profil & Kendaraan", size=16, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
            content=ft.Column(
                tight=True,
                spacing=10,
                controls=[hp_field, kendaraan_field, plat_field],
            ),
        )

        def save_profile(ev) -> None:
            if hp_field.value:
                driver["no_hp"] = hp_field.value.strip()
            if kendaraan_field.value:
                driver["kendaraan"] = kendaraan_field.value.strip()
            if plat_field.value:
                driver["plat_nomor"] = plat_field.value.strip().upper()
            close_modal(self.page, dialog)
            show_snackbar(self.page, "Profil mitra berhasil diperbarui.")
            self.refresh_ui()

        dialog.actions = [
            ft.TextButton(
                content=ft.Text("Batal", color=WaregTheme.TEXT_SECONDARY),
                on_click=lambda ev: close_modal(self.page, dialog),
            ),
            ButtonCls(
                content=ft.Text("Simpan", weight=ft.FontWeight.BOLD),
                style=ft.ButtonStyle(bgcolor=WaregTheme.ACCENT, color="#000000"),
                on_click=save_profile,
            ),
        ]
        open_modal(self.page, dialog)

    def handle_select_tab(self, tab_index: int) -> None:
        route_map = {
            0: "/driver/beranda",
            1: "/driver/pesanan",
            2: "/driver/riwayat",
            3: "/driver/pendapatan",
            4: "/driver/profil",
        }
        self.state["active_tab"] = tab_index

        if tab_index != 0 and self.on_navigate is not None:
            self.on_navigate(route_map[tab_index])
            return

        self.refresh_ui()

    # --- Render UI ---
    def refresh_ui(self, initial: bool = False) -> None:
        active_tab = self.state["active_tab"]
        header = build_header_driver(
            state=self.state,
            on_open_notif=self.handle_open_notif,
            on_open_settings=self.handle_open_settings,
        )

        if active_tab == 0:
            # Layout responsif: melebar 2 kolom di laptop/desktop, 1 kolom di HP
            responsive_grid = ft.ResponsiveRow(
                spacing=16,
                run_spacing=16,
                controls=[
                    ft.Column(
                        col={"xs": 12, "lg": 6},
                        spacing=16,
                        controls=[
                            build_status_online_card(
                                state=self.state,
                                on_toggle_status=self.handle_toggle_status,
                                on_simulate_order=self.handle_simulate_order,
                                on_open_active_order=lambda e: self.handle_select_tab(1),
                            ),
                            build_pendapatan_card(
                                state=self.state,
                                on_detail_pendapatan=self.handle_detail_pendapatan,
                                on_claim_bonus=self.handle_claim_bonus,
                            ),
                            build_menu_layanan_grid(
                                state=self.state,
                                on_toggle_layanan=self.handle_toggle_layanan,
                            ),
                        ],
                    ),
                    ft.Column(
                        col={"xs": 12, "lg": 6},
                        spacing=16,
                        controls=[
                            build_peta_lokasi_card(
                                state=self.state,
                                on_my_location=self.handle_my_location,
                                on_open_navigation=self.handle_open_navigation,
                                on_select_spot_direct=self.handle_select_spot_direct,
                            ),
                            build_statistik_aktivitas_section(state=self.state),
                            build_pesanan_terbaru_card(
                                state=self.state,
                                on_lihat_semua_pesanan=lambda e: self.handle_select_tab(1),
                                on_inspect_order=self.handle_inspect_order,
                            ),
                        ],
                    ),
                ],
            )
            self.scroll_body.controls = [
                header,
                responsive_grid,
                ft.Container(height=12),
            ]
        elif active_tab == 1:
            self.scroll_body.controls = [
                header,
                build_tab_pesanan_content(
                    state=self.state,
                    on_simulate_order=self.handle_simulate_order,
                    on_advance_order=self.handle_advance_order,
                    on_cancel_order=self.handle_cancel_order,
                    on_inspect_order=self.handle_inspect_order,
                ),
            ]
        elif active_tab == 2:
            self.scroll_body.controls = [
                header,
                build_tab_riwayat_content(
                    state=self.state,
                    on_change_filter=lambda cat: (
                        self.state.update({"filter_riwayat": cat}),
                        self.refresh_ui(),
                    ),
                    on_inspect_order=self.handle_inspect_order,
                ),
            ]
        elif active_tab == 3:
            self.scroll_body.controls = [
                header,
                build_tab_pendapatan_content(
                    state=self.state,
                    on_open_withdraw=self.handle_open_withdraw,
                ),
            ]
        else:
            self.scroll_body.controls = [
                header,
                build_tab_profil_content(
                    state=self.state,
                    on_edit_profile=self.handle_edit_profile,
                    on_logout=self.on_logout,
                ),
            ]

        self.bottom_nav_host.content = build_bottom_navigation(
            active_index=active_tab,
            on_select_tab=self.handle_select_tab,
        )

        if not initial:
            self.page.update()


# ==============================================================================
# 8. ENTRY-POINT FLEKSIBEL UNTUK INTEGRASI KE main.py
# ==============================================================================
def build_beranda_driver_content(
    page: ft.Page,
    driver_data: Optional[Dict] = None,
    on_navigate: Optional[Callable[[str], None]] = None,
    on_logout: Optional[Callable[[], None]] = None,
) -> ft.Container:
    """Mengembalikan komponen ft.Container utama halaman Beranda Driver."""
    controller = BerandaDriverController(
        page=page,
        driver_data=driver_data,
        on_navigate=on_navigate,
        on_logout=on_logout,
    )
    return controller.root_container


def build_beranda_driver_view(
    page: ft.Page,
    route: str = "/driver/beranda",
    driver_data: Optional[Dict] = None,
    on_navigate: Optional[Callable[[str], None]] = None,
    on_logout: Optional[Callable[[], None]] = None,
) -> ft.View:
    """Mengembalikan ft.View untuk routing page.views di main.py."""
    content = build_beranda_driver_content(
        page=page,
        driver_data=driver_data,
        on_navigate=on_navigate,
        on_logout=on_logout,
    )
    return ft.View(
        route=route,
        bgcolor=WaregTheme.BG_PRIMARY,
        padding=0,
        controls=[content],
    )


def beranda_driver_page(
    page: ft.Page,
    driver_data: Optional[Dict] = None,
    on_navigate: Optional[Callable[[str], None]] = None,
    on_logout: Optional[Callable[[], None]] = None,
) -> ft.Container:
    """Fungsi pemanggil langsung apabila main.py memanggil halaman dengan (page)."""
    page.title = "Wareg Express • Beranda Driver"
    page.bgcolor = WaregTheme.BG_PRIMARY
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0

    content = build_beranda_driver_content(
        page=page,
        driver_data=driver_data,
        on_navigate=on_navigate,
        on_logout=on_logout,
    )
    page.controls.clear()
    page.add(content)
    page.update()
    return content


# ==============================================================================
# 9. MODE PREVIEW MANDIRI (MENDUKUNG ft.run() MAUPUN ft.app())
# ==============================================================================
if __name__ == "__main__":
    def _preview_main(page: ft.Page) -> None:
        if hasattr(page, "window") and page.window is not None:
            page.window.width = 1180
            page.window.height = 820
        beranda_driver_page(page)

    if hasattr(ft, "run"):
        ft.run(_preview_main)
    else:
        ft.app(target=_preview_main)