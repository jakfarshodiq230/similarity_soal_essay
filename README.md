# Proyek Koreksi Esai Otomatis dengan Jaccard Similarity

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.x-lightgrey?logo=flask)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Proyek ini menyediakan sebuah API service sederhana menggunakan Flask untuk mengoreksi jawaban esai secara otomatis. Koreksi dilakukan dengan membandingkan kemiripan antara jawaban siswa dan kunci jawaban (keduanya dalam format paragraf/teks panjang) menggunakan algoritma **Jaccard Similarity**. Hasil koreksi akan berupa nilai dari 0 hingga 100 dan umpan balik (`feedback`) berdasarkan tingkat kemiripan yang terdeteksi.

## Daftar Isi

- [Fitur Utama](#fitur-utama)
- [Konsep di Balik Koreksi](#konsep-di-balik-koreksi)
- [Struktur Proyek](#struktur-proyek)
- [Persyaratan Sistem](#persyaratan-sistem)
- [Instalasi](#instalasi)
- [Cara Menjalankan API Service](#cara-menjalankan-api-service)
- [Penggunaan API](#penggunaan-api)
  - [Endpoint](#endpoint)
  - [Request Body](#request-body)
  - [Contoh Permintaan (Postman)](#contoh-permintaan-postman)
  - [Contoh Permintaan (Python `requests`)](#contoh-permintaan-python-requests)
  - [Contoh Respons](#contoh-respons)
- [Pengembangan Lanjutan](#pengembangan-lanjutan)
- [Lisensi](#lisensi)

## Fitur Utama

*   **Koreksi Esai Otomatis:** Menilai jawaban esai siswa secara otomatis.
*   **Perbandingan Paragraf:** Mendukung kunci jawaban dan jawaban siswa dalam bentuk teks/paragraf panjang.
*   **Metode Jaccard Similarity:** Mengukur kemiripan set kata unik antar dua dokumen.
*   **Skala Nilai 0-100:** Mengkonversi tingkat kemiripan menjadi nilai yang mudah dipahami.
*   **Umpan Balik Instan:** Memberikan feedback sederhana berdasarkan tingkat relevansi.
*   **API RESTful (Flask):** Mudah diintegrasikan dengan aplikasi lain melalui HTTP POST request.

## Konsep di Balik Koreksi

Proyek ini menggunakan **Jaccard Similarity** sebagai inti dari algoritma koreksi. Berikut adalah bagaimana cara kerjanya:

1.  **Pembersihan Teks:** Jawaban siswa dan kunci jawaban dibersihkan terlebih dahulu. Ini melibatkan:
    *   Mengubah semua teks menjadi huruf kecil (`lowercase`) untuk memastikan "Revolusi" sama dengan "revolusi".
    *   Menghapus tanda baca (koma, titik, tanda tanya, dll.).
    *   Menghapus angka.
2.  **Tokenisasi dan Pembentukan Set:** Teks yang sudah bersih kemudian dipecah menjadi kata-kata individual (token). Dari kata-kata ini, dibuatlah sebuah "set" kata unik. Penggunaan set memastikan bahwa setiap kata hanya dihitung satu kali, dan urutan kata tidak memengaruhi perhitungan.
3.  **Perhitungan Jaccard Similarity:** Dihitung dengan rumus:
    $$ J(A, B) = \frac{|A \cap B|}{|A \cup B|} $$
    Di mana:
    *   $A$ adalah set kata dari jawaban siswa.
    *   $B$ adalah set kata dari kunci jawaban.
    *   $|A \cap B|$ adalah jumlah kata yang ada di kedua set (irisan).
    *   $|A \cup B|$ adalah jumlah kata unik yang ada di salah satu atau kedua set (gabungan).
    Nilai Jaccard Similarity berkisar antara 0 (tidak ada kemiripan sama sekali) hingga 1 (sangat mirip atau identik).
4.  **Skala Nilai:** Nilai Jaccard Similarity kemudian dikalikan 100 untuk mendapatkan skor akhir dalam skala 0-100.
5.  **Umpan Balik:** Pesan feedback sederhana dihasilkan berdasarkan rentang nilai Jaccard Similarity untuk memberikan indikasi awal tentang kualitas jawaban.

**Batasan:** Penting untuk dicatat bahwa metode ini berfokus pada kemiripan kata-kata. Ini tidak memahami konteks semantik, tata bahasa, struktur kalimat, atau penalaran mendalam. Untuk koreksi esai yang lebih canggih, diperlukan teknik Natural Language Processing (NLP) yang lebih kompleks (misalnya, word embeddings, analisis sintaksis, model pembelajaran mesin).

## Struktur Proyek
├── koreksi_essay_manual.py # File utama koreksi secara local manual tanpa Flask Api
├── main.py # File utama aplikasi Flask API
├── README.md # File penjelasan proyek (ini)
└── penggunaan.txt # Daftar dependensi Python
## Persyaratan Sistem

*   Python 3.8 atau lebih tinggi

## Instalasi

1.  **Clone repositori ini:**
    ```bash
    git clone https://github.com/username_anda/nama_repo_anda.git
    cd nama_repo_anda
    ```
    (Ganti `username_anda` dan `nama_repo_anda` dengan detail repositori Anda)

2.  **Buat Virtual Environment (Direkomendasikan):**
    ```bash
    python -m venv venv
    ```

3.  **Aktifkan Virtual Environment:**
    *   **Windows:**
        ```bash
        .\venv\Scripts\activate
        ```
    *   **macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```

4.  **Instal dependensi:**
    ```bash
    pip install -r penggunaan.txt
    ```
    (Pastikan `requirements.txt` berisi `Flask` jika Anda belum membuatnya: `echo "Flask" > requirements.txt`)

## Cara Menjalankan API Service

Setelah instalasi, Anda bisa menjalankan aplikasi Flask:

```bash
python main.py

* Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: XXX-XXX-XXX
