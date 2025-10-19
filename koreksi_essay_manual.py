import re

def bersihkan_teks(teks):
    """
    Membersihkan teks: lowercase, hapus tanda baca, hapus angka.
    Mengembalikan teks yang bersih.
    """
    teks = teks.lower()
    teks = re.sub(r'[^\w\s]', '', teks) # Hapus tanda baca
    teks = re.sub(r'\d+', '', teks)      # Hapus angka
    return teks

def hitung_jaccard_similarity(set1, set2):
    """
    Menghitung Jaccard Similarity antara dua set kata.
    Mengembalikan nilai float antara 0.0 dan 1.0.
    """
    interseksi = len(set1.intersection(set2))
    union = len(set1.union(set2))
    if union == 0:
        return 0.0 # Hindari ZeroDivisionError jika kedua set kosong
    return interseksi / union

def koreksi_esai_dan_nilai(jawaban_siswa, kunci_jawaban_paragraf):
    """
    Mengoreksi jawaban esai dengan membandingkan kemiripan paragraf
    dan memberikan nilai dari 0 sampai 100.

    Args:
        jawaban_siswa (str): Jawaban yang diberikan oleh siswa.
        kunci_jawaban_paragraf (str): Kunci jawaban dalam bentuk paragraf.

    Returns:
        tuple: (nilai_siswa, feedback)
    """
    feedback = []

    # 1. Bersihkan teks dari jawaban siswa dan kunci jawaban
    jawaban_siswa_bersih = bersihkan_teks(jawaban_siswa)
    kunci_jawaban_bersih = bersihkan_teks(kunci_jawaban_paragraf)

    # 2. Tokenisasi (pecah menjadi kata-kata) dan buat set kata unik
    # Menggunakan set agar hanya kata unik yang dihitung dan urutan tidak relevan
    kata_jawaban_siswa = set(jawaban_siswa_bersih.split())
    kata_kunci_jawaban = set(kunci_jawaban_bersih.split())

    # 3. Hitung Jaccard Similarity
    kemiripan = hitung_jaccard_similarity(kata_jawaban_siswa, kata_kunci_jawaban)

    # 4. Konversi kemiripan (0-1) menjadi nilai (0-100)
    nilai_siswa = kemiripan * 100

    # 5. Tambahkan feedback berdasarkan tingkat kemiripan
    feedback.append(f"Tingkat kemiripan (Jaccard Similarity): {kemiripan:.2f}")
    if kemiripan >= 0.8:
        feedback.append("Jawaban sangat baik dan sangat relevan dengan kunci jawaban.")
    elif kemiripan >= 0.5:
        feedback.append("Jawaban cukup baik dan relevan, namun ada ruang untuk detail lebih lanjut.")
    elif kemiripan > 0:
        feedback.append("Jawaban kurang relevan atau tidak lengkap dibandingkan kunci jawaban.")
    else:
        feedback.append("Jawaban tidak memiliki kemiripan dengan kunci jawaban.")


    return round(nilai_siswa), feedback # Mengembalikan nilai bulat dan feedback

# --- Contoh Penggunaan ---

# Kunci Jawaban dalam bentuk paragraf
kunci_jawaban_revolusi_industri = """
Revolusi Industri adalah periode transformasi besar dalam sejarah manusia, dimulai pada akhir abad ke-18 dan awal abad ke-19, terutama di Britania Raya.
Perubahan utama meliputi peralihan dari metode produksi tangan ke mesin, penggunaan energi uap dan air, serta pengembangan sistem pabrik.
Ini menyebabkan urbanisasi besar-besaran, munculnya kelas pekerja baru, peningkatan produksi barang, dan perubahan drastis dalam struktur sosial dan ekonomi.
Penemuan-penemuan penting termasuk mesin uap oleh James Watt dan Spinning Jenny.
"""

kunci_jawaban_fotosintesis = """
Fotosintesis adalah proses biokimia di mana organisme autotrof, terutama tumbuhan, alga, dan beberapa bakteri, mengubah energi cahaya menjadi energi kimia.
Proses ini menggunakan sinar matahari, karbon dioksida dari udara, dan air dari tanah untuk menghasilkan glukosa (sebagai sumber energi) dan oksigen (sebagai produk sampingan).
Fotosintesis sangat penting bagi kehidupan di Bumi karena menghasilkan oksigen yang dihirup sebagian besar makhluk hidup dan merupakan dasar dari sebagian besar rantai makanan.
"""

# Jawaban Siswa untuk Soal Revolusi Industri
jawaban_ri_siswa_1 = """
Revolusi Industri adalah masa perubahan signifikan di abad ke-18 dan ke-19, dimulai di Inggris.
Produksi beralih dari manual ke mesin, dengan penemuan mesin uap dan pabrik.
Terjadi urbanisasi dan munculnya kelas pekerja, serta perubahan ekonomi dan sosial yang mendalam.
"""

jawaban_ri_siswa_2 = """
Revolusi terjadi di industri. Ada mesin baru dan orang-orang pindah ke kota. Produksi jadi lebih cepat.
"""

jawaban_ri_siswa_3 = """
Ini tentang sejarah lama yang ada mesinnya. Itu aja.
"""

# Jawaban Siswa untuk Soal Fotosintesis
jawaban_fotosintesis_siswa_1 = """
Tumbuhan melakukan fotosintesis, menggunakan cahaya matahari, karbondioksida, dan air untuk membuat glukosa dan melepaskan oksigen.
Ini penting untuk kehidupan karena menghasilkan oksigen yang kita butuhkan.
"""

jawaban_fotosintesis_siswa_2 = """
Tumbuhan buat makanan pakai matahari.
"""

jawaban_fotosintesis_siswa_3 = """
Saya tidak tahu jawabannya.
"""


# --- Hasil Koreksi ---

print("--- Koreksi Soal Revolusi Industri ---")
nilai_1, feedback_1 = koreksi_esai_dan_nilai(jawaban_ri_siswa_1, kunci_jawaban_revolusi_industri)
print(f"Jawaban Siswa (Baik):\n{jawaban_ri_siswa_1}\n")
print(f"Nilai: {nilai_1}")
print(f"Feedback: {'; '.join(feedback_1)}\n")

nilai_2, feedback_2 = koreksi_esai_dan_nilai(jawaban_ri_siswa_2, kunci_jawaban_revolusi_industri)
print(f"Jawaban Siswa (Sedang):\n{jawaban_ri_siswa_2}\n")
print(f"Nilai: {nilai_2}")
print(f"Feedback: {'; '.join(feedback_2)}\n")

nilai_3, feedback_3 = koreksi_esai_dan_nilai(jawaban_ri_siswa_3, kunci_jawaban_revolusi_industri)
print(f"Jawaban Siswa (Kurang):\n{jawaban_ri_siswa_3}\n")
print(f"Nilai: {nilai_3}")
print(f"Feedback: {'; '.join(feedback_3)}\n")

print("\n--- Koreksi Soal Fotosintesis ---")
nilai_4, feedback_4 = koreksi_esai_dan_nilai(jawaban_fotosintesis_siswa_1, kunci_jawaban_fotosintesis)
print(f"Jawaban Siswa (Baik):\n{jawaban_fotosintesis_siswa_1}\n")
print(f"Nilai: {nilai_4}")
print(f"Feedback: {'; '.join(feedback_4)}\n")

nilai_5, feedback_5 = koreksi_esai_dan_nilai(jawaban_fotosintesis_siswa_2, kunci_jawaban_fotosintesis)
print(f"Jawaban Siswa (Pendek):\n{jawaban_fotosintesis_siswa_2}\n")
print(f"Nilai: {nilai_5}")
print(f"Feedback: {'; '.join(feedback_5)}\n")

nilai_6, feedback_6 = koreksi_esai_dan_nilai(jawaban_fotosintesis_siswa_3, kunci_jawaban_fotosintesis)
print(f"Jawaban Siswa (Tidak Tahu):\n{jawaban_fotosintesis_siswa_3}\n")
print(f"Nilai: {nilai_6}")
print(f"Feedback: {'; '.join(feedback_6)}\n")