"""Antarmuka console untuk Sistem Informasi Mahasiswa."""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from src.models import DaftarMahasiswa, Mahasiswa

console = Console()
daftar = DaftarMahasiswa()


def tampilkan_menu() -> None:
    """Tampilkan pilihan operasi aplikasi."""
    menu = (
        "1. Tambah mahasiswa\n"
        "2. Tampilkan semua mahasiswa\n"
        "3. Cari mahasiswa berdasarkan NIM\n"
        "4. Hapus mahasiswa\n"
        "5. Edit IPK\n"
        "0. Keluar"
    )
    console.print(Panel(menu, title="Sistem Informasi Mahasiswa", border_style="cyan"))


def tambah_mahasiswa() -> None:
    """Minta data dan tambahkan mahasiswa baru."""
    console.print("\n[bold]Tambah Mahasiswa[/]")
    try:
        nim = console.input("NIM: ")
        nama = console.input("Nama: ")
        program_studi = console.input("Program studi: ")
        angkatan = int(console.input("Angkatan: "))
        ipk = float(console.input("IPK (kosong untuk 0.0): ") or "0.0")
        mahasiswa = Mahasiswa(nim, nama, program_studi, angkatan, ipk)
        daftar.tambah(mahasiswa)
    except ValueError as error:
        console.print(f"[red]Gagal menambahkan mahasiswa: {error}[/]")
        return
    console.print(f"[green]Mahasiswa {mahasiswa.nama} berhasil ditambahkan.[/]")


def tampilkan_semua() -> None:
    """Tampilkan semua mahasiswa dalam tabel."""
    if not daftar.data:
        console.print("[yellow]Belum ada data mahasiswa.[/]")
        return

    tabel = Table(title="Daftar Mahasiswa")
    tabel.add_column("NIM", style="cyan")
    tabel.add_column("Nama")
    tabel.add_column("Program Studi")
    tabel.add_column("Angkatan", justify="right")
    tabel.add_column("IPK", justify="right")
    for mahasiswa in daftar.data:
        tabel.add_row(
            mahasiswa.nim,
            mahasiswa.nama,
            mahasiswa.program_studi,
            str(mahasiswa.angkatan),
            f"{mahasiswa.ipk:.2f}",
        )
    console.print(tabel)


def cari_mahasiswa() -> None:
    """Cari dan tampilkan satu mahasiswa berdasarkan NIM."""
    nim = console.input("Masukkan NIM yang dicari: ")
    mahasiswa = daftar.cari(nim)
    if mahasiswa is None:
        console.print(f"[yellow]Mahasiswa dengan NIM {nim} tidak ditemukan.[/]")
        return
    console.print(mahasiswa)


def hapus_mahasiswa() -> None:
    """Hapus satu mahasiswa berdasarkan NIM."""
    nim = console.input("Masukkan NIM yang akan dihapus: ")
    if daftar.hapus(nim):
        console.print(f"[green]Mahasiswa dengan NIM {nim} berhasil dihapus.[/]")
    else:
        console.print(f"[yellow]Mahasiswa dengan NIM {nim} tidak ditemukan.[/]")


def edit_ipk() -> None:
    """Perbarui IPK mahasiswa berdasarkan NIM."""
    nim = console.input("Masukkan NIM: ")
    try:
        ipk = float(console.input("IPK baru (0.0-4.0): "))
        berhasil = daftar.perbarui_ipk(nim, ipk)
    except ValueError as error:
        console.print(f"[red]Gagal memperbarui IPK: {error}[/]")
        return

    if berhasil:
        console.print("[green]IPK berhasil diperbarui.[/]")
    else:
        console.print(f"[yellow]Mahasiswa dengan NIM {nim} tidak ditemukan.[/]")


def main() -> None:
    """Jalankan menu sampai pengguna memilih keluar."""
    while True:
        tampilkan_menu()
        pilihan = console.input("Pilih menu [0-5]: ").strip()

        if pilihan == "1":
            tambah_mahasiswa()
        elif pilihan == "2":
            tampilkan_semua()
        elif pilihan == "3":
            cari_mahasiswa()
        elif pilihan == "4":
            hapus_mahasiswa()
        elif pilihan == "5":
            edit_ipk()
        elif pilihan == "0":
            console.print("[bold]Sampai jumpa![/]")
            break
        else:
            console.print("[red]Pilihan tidak valid. Masukkan angka 0 sampai 5.[/]")


if __name__ == "__main__":
    main()
