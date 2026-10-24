# Perbandingan Proposal: GPT vs Gemini

Dokumen ini membandingkan isi dari **New Proposal GPT.md** dan **New Proposal Gemini.md** tanpa menambahkan informasi baru.

---

## Tabel Perbedaan

| Dimensi | New Proposal GPT | New Proposal Gemini |
|---|---|---|
| **Nada & tujuan dokumen** | Spesifikasi teknis MVP yang siap diimplementasi. Langsung membahas fitur, mekanik, dan stack. | Persuasi dan pitching. Dokumen dimulai dengan argumen mengapa format game simulasi akan memenangkan hackathon. |
| **Jumlah misi / skenario** | Satu misi tunggal untuk MVP: *Food Supply Crisis* | Tiga pilihan misi yang bisa dipilih pemain: Rantai Pasok Pangan (SDG 2), Kebocoran Algoritma Kredit (SDG 10), Kegagalan Jaringan Energi (SDG 7) |
| **Alur permainan** | 4 putaran eksplisit dengan nama dan aturan per putaran (Pilih strategi → AI beri rekomendasi → AI Shock → Keputusan akhir) | 4 tahap naratif yang lebih longgar (Start Screen → Simulation Arena → AI Shock Event → Game Over/The Reveal) |
| **Titik masuk pengguna** | Pemain mengisi Quick Skill Profile (kemampuan awal, minat karier, waktu belajar) sebelum bermain | Tidak ada profil awal; pemain langsung memilih misi tanpa login atau upload CV |
| **Mekanisme ekstraksi skill** | Sistem menghitung 4 indikator eksplisit (Calibrated AI Trust, Critical Verification, Decision Quality, Adaptability) menggunakan rubrik yang ditetapkan sebelumnya | Skill diungkap secara dramatis di akhir game sebagai "sihir HRTech" — layar game berubah menjadi Dashboard Karier Profesional |
| **Laporan hasil** | Laporan berbasis bukti dengan contoh perilaku yang diamati dan catatan batasan interpretasi | Profil skill kuantitatif singkat (misal: "Ethical Judgement tinggi, System Thinking moderat") beserta persentase kecocokan peran |
| **Peran karier yang ditampilkan** | Tiga peran spesifik: AI Application Engineer, Data Analyst, AI Governance/Risk Analyst | Satu contoh peran disebutkan: AI Fairness Auditor (88% kecocokan); tidak ada daftar lengkap |
| **Skenario masa depan** | Dua skenario adopsi AI (Moderat vs Cepat) dibandingkan secara eksplisit, dengan hasil disebut sebagai perkiraan bukan prediksi pasti | Tidak ada skenario masa depan; ketidakpastian dimunculkan hanya sebagai plot twist di dalam permainan |
| **Jalur reskilling** | Fitur wajib dengan urutan belajar, estimasi waktu, sumber terverifikasi, dan pemetaan SDG | Disebutkan sebagai "Quest Selanjutnya" dan hanya berupa satu contoh modul; tidak ada detail urutan atau estimasi waktu |
| **Pemetaan SDG** | Setiap peran dan skill dipetakan ke SDG dengan alasan yang jelas dan eksplisit | SDG menjadi latar belakang/tema misi game, bukan pemetaan eksplisit per skill atau peran |
| **Data tren pekerjaan** | Dibahas secara teknis: satu sumber yang bisa diperbarui dengan tanggal data; ESCO / O*NET disebutkan sebagai taksonomi referensi | Tidak dibahas |
| **Stack teknologi** | Dirinci lengkap: Next.js + React, API routes / FastAPI, Supabase / PostgreSQL, state machine + scenario JSON, satu LLM API terkontrol | Hanya menyebut Next.js dan React dalam pertanyaan kepada developer; tidak ada stack backend atau database |
| **UI/UX permainan** | Tidak mendeskripsikan gaya antarmuka secara visual | Menawarkan tiga opsi antarmuka konkret: Swipe Cards (gaya Reigns), Chat Terminal (gaya Hacknet), Dashboard Manager (gaya simulasi strategi) |
| **Kriteria selesai / done** | Ada kriteria selesai yang eksplisit: pengguna bisa menyelesaikan seluruh alur dari profil kosong hingga jalur reskilling + pemetaan SDG | Tidak ada kriteria selesai yang diformulasikan |
| **Peringatan / batasan interpretasi** | Dicantumkan secara eksplisit: skor tidak boleh menyimpulkan kemampuan profesional dari satu simulasi; LLM boleh membantu menjelaskan, bukan menentukan skor | Tidak ada peringatan batasan interpretasi |
| **Referensi game lain** | Tidak menyebut game lain sebagai referensi | Menyebut Reigns, Plague Inc., Football Manager, dan Hacknet sebagai referensi genre/UI |

---

## Ringkasan

**New Proposal GPT** berfokus pada **spesifikasi implementasi** — apa yang harus dibangun, bagaimana cara kerjanya, dan apa batasan-batasannya.

**New Proposal Gemini** berfokus pada **argumen dan pitching** — mengapa format ini akan menang di hackathon, bagaimana momen dramatis didesain, dan memberikan pilihan UI kepada developer untuk didiskusikan.
