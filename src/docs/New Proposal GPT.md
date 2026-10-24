# MVP: FutureProof — Human–AI Decision Lab

Konsep: game simulasi krisis yang menguji cara seseorang mengambil keputusan bersama AI, kemudian menghubungkan bukti perilakunya dengan rekomendasi karier, skill gap, dan jalur reskilling.

Target MVP bukan membuat game besar. Targetnya adalah membuktikan satu alur lengkap dari bermain → mengamati kemampuan → mengeksplorasi karier masa depan.

## 1. Fitur MVP

01\. Quick Skill Profile

Wajib

Pengguna memilih kemampuan awal, minat karier, dan waktu yang tersedia untuk belajar. Tidak perlu CV atau login untuk demo.

Output: profil awal berdasarkan pengakuan pengguna.

02\. Crisis Simulation

Fitur utama

Satu misi krisis distribusi pangan dengan empat putaran keputusan. Sebelum melihat rekomendasi AI, pemain menentukan strategi sendiri. Setelah itu, ia dapat menerima, menolak, atau mengubah rekomendasi berdasarkan bukti.

Output: riwayat keputusan, bukti yang diperiksa, dan hasil setiap putaran.

03\. Decision & Skill Report

Wajib

Sistem menganalisis kualitas keputusan, pemeriksaan bukti, kemampuan beradaptasi, dan ketepatan kepercayaan terhadap AI.

Output: laporan dengan contoh perilaku yang diamati, bukan label kepribadian atau skor kecerdasan yang tidak tervalidasi.

04\. Future Skills Radar & Role Matching

Wajib

Sistem menggunakan satu sumber data tren pekerjaan atau skill yang dapat diperbarui, menampilkan sumber dan tanggal, lalu mencocokkan pengguna dengan tiga peran yang relevan.

Output: peringkat peran, alasan kecocokan, skill yang sudah dimiliki, dan skill gap.

05\. Future Career Pathway

Wajib

Pengguna membandingkan skenario adopsi AI moderat dan cepat, melihat bagaimana prospek dan kebutuhan skill dapat berubah, lalu memperoleh jalur belajar berurutan beserta pemetaan SDG.

Output: langkah belajar, estimasi waktu, sumber belajar nyata, dan hubungan karier dengan SDGs.

Kelima modul tersebut mencakup enam fitur wajib brief Aiversecity, termasuk penanganan ketidakpastian melalui dua skenario masa depan.&#x20;

Domain 1.md



## 2. Mekanik game yang konkret

Untuk MVP, gunakan satu misi: Food Supply Crisis.

## Mission: Supply Under Pressure

4 putaran

Tujuan: mendistribusikan pangan dengan keterbatasan anggaran, waktu, dan kapasitas rute.

Putaran 1 — Pilih strategi

Pemain menentukan rute distribusi sebelum melihat saran AI.

Putaran 2 — AI memberi rekomendasi

AI menyarankan rute tercepat. Pemain dapat menerima atau memeriksa data kapasitas rute terlebih dahulu.

Putaran 3 — AI Shock

Anggaran dipotong dan muncul informasi bahwa salah satu rute memiliki batas kapasitas. Pemain harus mengevaluasi ulang strategi.

Putaran 4 — Keputusan akhir

Pemain memilih strategi distribusi akhir. Sistem menghitung konsekuensi terhadap kebutuhan pangan, biaya, waktu, dan kelompok yang terdampak.

Mekanisme penting: jawaban AI harus dikontrol oleh skenario. Sebagian rekomendasi bisa benar, sebagian bisa mengabaikan bukti penting. Jangan bergantung pada model bahasa untuk membuat kesalahan secara acak.

## 3. Apa yang dihitung oleh sistem?

Simpan event dari setiap putaran: keputusan awal, rekomendasi AI, bukti yang dibuka, keputusan akhir, dan konsekuensinya.

| Indikator             | Cara penilaian                                              |
| --------------------- | ----------------------------------------------------------- |
| Calibrated AI Trust   | Apakah pengguna menyesuaikan kepercayaan berdasarkan bukti? |
| Critical Verification | Apakah pengguna memeriksa informasi relevan?                |
| Decision Quality      | Apakah keputusan memenuhi tujuan dan batasan skenario?      |
| Adaptability          | Apakah pengguna mengubah strategi setelah kondisi berubah?  |

Contoh laporan:

> Critical Verification — Teramati
>
> Pada putaran ketiga, Anda menemukan bahwa rekomendasi AI mengabaikan kapasitas rute. Anda memperbarui strategi setelah memeriksa data tersebut.
>
> Batasan: bukti baru berasal dari satu simulasi, sehingga belum cukup untuk menyimpulkan kemampuan profesional Anda secara umum.

Penilaian inti menggunakan rubric yang ditetapkan sebelumnya. LLM boleh membantu menjelaskan hasil, tetapi tidak menjadi satu-satunya penentu skor.

## 4. Career Intelligence yang sederhana tetapi berfungsi

MVP tidak perlu mempunyai ribuan pekerjaan. Mulailah dengan tiga peran, selama data dan kebutuhan skill setiap peran dapat diverifikasi.

AI Application Engineer

Skill fokus: pengembangan aplikasi, integrasi AI, pengujian sistem.

Data Analyst

Skill fokus: analisis data, interpretasi, verifikasi kesimpulan.

AI Governance / Risk Analyst

Skill fokus: penilaian risiko, evaluasi bukti, pemeriksaan dampak sistem.

Pencocokan menggunakan tiga masukan: profil awal, bukti dari permainan, serta minat dan kebutuhan skill pekerjaan. Tampilkan alasan setiap rekomendasi. Jangan menyimpulkan bahwa seseorang cocok atau tidak cocok hanya berdasarkan cara ia menjawab empat putaran game.

Untuk tren, gunakan satu sumber yang benar-benar bisa diperbarui dan menyimpan tanggal data. Taksonomi seperti ESCO atau O\*NET dapat membantu mendefinisikan keterampilan dan pekerjaan, tetapi tidak dengan sendirinya membuktikan tren permintaan terbaru. Sinyal pasar kerja tetap harus memiliki sumber yang sesuai.

## 5. Skenario, reskilling, dan SDGs

Setelah peran dipilih, sistem memperlihatkan dua skenario:

| Skenario | Pertanyaan yang dijawab                                             |
| -------- | ------------------------------------------------------------------- |
| Moderat  | Bagaimana jalur karier jika adopsi AI berkembang bertahap?          |
| Cepat    | Bagaimana kebutuhan skill dapat berubah jika adopsi AI lebih cepat? |

MVP boleh menggunakan parameter skenario transparan, tidak perlu model peramalan kompleks. Sistem menghitung ulang relevansi skill dan rekomendasi berdasarkan asumsi yang berbeda; hasilnya harus disebut sebagai perkiraan, bukan prediksi pasti.

Jalur reskilling kemudian mengambil skill gap dan menyusunnya menjadi urutan belajar, dengan estimasi waktu serta tautan sumber yang telah diverifikasi. Setiap peran dan skill juga diberi pemetaan SDG dengan alasan yang jelas. Contohnya, pekerjaan terkait pemeriksaan bias algoritma dapat dikaitkan dengan SDG 10 jika tugasnya memang mendukung pengurangan ketimpangan.

## 6. Stack dan scope implementasi

Frontend

Next.js + React

Backend

API routes atau FastAPI

Database

Supabase / PostgreSQL

Game engine

State machine + scenario JSON

AI

Satu LLM API, terkontrol

Trend data

Satu sumber yang bisa diperbarui

Tidak perlu LangGraph, multi-agent, multiplayer, atau simulasi grafis kompleks untuk membuktikan MVP.

### Kriteria selesai

MVP dianggap bekerja ketika seorang pengguna bisa memulai dari profil kosong, menyelesaikan empat putaran krisis, melihat laporan berbasis bukti, memperoleh tiga rekomendasi peran yang bisa dijelaskan, membandingkan dua skenario, dan mendapatkan jalur reskilling beserta pemetaan SDG.

Satu hal paling penting untuk demo: perubahan data tren harus dapat mengubah rekomendasi yang terlihat. Ini membuktikan bahwa FutureProof bukan cuma game yang diikuti dashboard AI generik.