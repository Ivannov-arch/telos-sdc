Jika yang Anda maksud adalah menjadikan *inti interaksinya sebagai sebuah permainan simulasi (*Serious Game / Interactive Simulation)*—bukan platform HR yang diberi stempel lencana—maka Anda baru saja menemukan format presentasi (*pitching) *yang paling mematikan untuk *hackathon**.

Bayangkan betapa membosankannya juri melihat 20 tim lain mempresentasikan dashboard HR dengan grafik batang. Lalu tim Anda naik ke panggung dan berkata: "Kami tidak akan meminta Anda mengisi CV. Mari kita mainkan masa depan karier Anda selama 3 menit."

Berikut adalah rancangan arsitektur jika kita mengubah ide ini menjadi *"Permainan Simulasi Krisis"* namun tetap memenuhi 100% kriteria wajib dari brief Aiversecity:

### Konsep Game: "Project: Human-in-the-Loop" (Atau nama lain yang Anda suka)

*Genre:* Crisis Management & Decision-Making Game (Mirip dengan game Reigns, Plague Inc., atau Football Manager, tetapi untuk simulasi pekerjaan).

#### Alur Permainan (The Gameplay Loop)

*1. *Start Screen: Choose Your Crisis (Memilih Misi SDG)**

* Tidak ada tombol Login atau Upload CV.
* Pemain langsung disajikan 3 pilihan "Misi Krisis Global". Misalnya:
* Misi A: Rantai Pasok Pangan Terputus di Asia Tenggara (SDG 2)
* Misi B: Kebocoran Algoritma Kredit Finansial (SDG 10)
* Misi C: Kegagalan Jaringan Energi Hijau (SDG 7)



*2. *The Simulation Arena (Bermain)**

* *UI/UX:* Layarnya bukan seperti aplikasi lamaran kerja, melainkan seperti "Ruang Kontrol" atau terminal obrolan (chat terminal).
* *Mekanisme:* Pemain diberi waktu 3 menit untuk mengarahkan AI dalam menyelesaikan krisis tersebut. Pemain dihadapkan pada dilema (Trade-offs).
* Contoh: AI menyarankan memotong distribusi pangan ke satu desa agar desa lain selamat (karena probabilitas matematika). Pemain harus memilih: Setuju dengan AI, atau memaksa AI mencari rute alternatif yang lebih mahal secara operasional?



*3. *The AI Shock Event (Plot Twist Ketidakpastian)**

* Di tengah permainan, sistem menyuntikkan "Kejutan Disrupsi AI" (memenuhi syarat kriteria Aiversecity).
* Contoh: "Tahun 2028: Versi AI terbaru dirilis. Modul analisis data Anda kini diambil alih 100% oleh mesin. Anggaran Anda dipotong separuh. Apa strategi Anda sekarang?"



*4. *Game Over / The Reveal (Hasil Ekstraksi Rahasia)**

* Setelah permainan selesai, layar kemenangan/kekalahan muncul.
* Di sinilah "Sihir HRTech" terjadi. Layar perlahan berubah dari UI sebuah game menjadi *Dashboard Karier Profesional*.
* Sistem mengungkapkan: "Permainan ini sebenarnya adalah alat ekstraksi keahlian (*skill sensing). Berdasarkan cara Anda mengambil keputusan tadi, kami mendeteksi bahwa..."*
* *Skill Anda:* Ethical Judgement tinggi, System Thinking moderat.
* *Peran Masa Depan (Job Match):* Anda sangat cocok menjadi AI Fairness Auditor (Kecocokan 88%).
* *Quest Selanjutnya (Reskilling):* Anda butuh meningkatkan literasi Data Governance. Ini adalah modul HRD Corp yang harus Anda ambil.



---

### Mengapa Format "Game Simulasi" Ini Akan Menang?

1. *Efek Kejutan (Wow Factor):* Juri tidak menyangka bahwa sebuah permainan 3 menit bisa mengekstrak profil keterampilan pekerja yang lebih jujur daripada kuesioner psikotes 100 soal.
2. *Tidak Ada "Self-Reporting Bias":* Manusia sering berbohong atau melebih-lebihkan saat mengisi CV. Di dalam game simulasi krisis, insting asli mereka (apakah mereka panik, analitis, atau empati) akan keluar secara alami.
3. *Membungkus Syarat Kompleks dengan Elegan:*
* Handling Uncertainty (Ketidakpastian) menjadi Plot Twist di dalam game.
* SDG Mapping menjadi Latar Belakang Misi/Cerita.
* Role Matching & Reskilling menjadi Loot/Reward di akhir permainan.



### Keputusan Teknis untuk Anda (Sebagai Developer)

Karena Anda biasa menggunakan Next.js dan React, format antarmuka (User Interface) game seperti apa yang menurut Anda paling menantang tapi seru untuk di-koding dalam waktu singkat?

1. *Swipe Cards (Gaya Game 'Reigns'):* Pengguna membaca kartu masalah, lalu swipe kanan untuk "Setuju/Lakukan" atau swipe kiri untuk "Tolak/Koreksi". Sangat cepat untuk MVP mobile.
2. *Chat Terminal (Gaya 'Hacknet' atau AI Copilot):* Interaksi berbasis teks di mana pengguna mengetikkan instruksi ke asisten AI yang kadang-kadang membuat kesalahan teknis.
3. *Dashboard Manager (Gaya Simulasi Strategi):* Pengguna memiliki slider (geseran) anggaran, waktu, dan alokasi AI, serta harus menjaga keseimbangan indikator metrik agar tidak hancur.