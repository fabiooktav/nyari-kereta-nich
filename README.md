# nyari kereta nich (updated database)
Database ini mengutamakan rekap kategori formasi yang diberikan pengguna.

## Isi
- `data.json`: kategori formasi/rentang nomor, daftar lokomotif pendukung, daftar batas 110 km/jam/Sub B, aturan arah/tanda bintang, dan KA tambahan.
- `main.py`: bot Discord yang merespons nama/nomor KA dengan embed.
- `requirements.txt`: dependensi Python.

## Environment Variables
- `DISCORD_TOKEN` (wajib, rahasia)
- `SEARCH_CHANNEL_ID` (opsional; batasi respons ke satu channel)
- `DATA_FILE` (opsional, default `data.json`)

## Penting
Jadwal lengkap Gapeka belum digabung sebagai tabel terpisah pada versi ini; jangan menganggap embed berisi jam jadwal yang sudah terverifikasi. Data formasi/nomor kategori mengikuti rekap pengguna, termasuk ejaan sebagaimana dikirim. Daftar CC adalah daftar pendukung, bukan jaminan penugasan aktual.
