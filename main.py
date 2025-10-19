import re
from flask import Flask, request, jsonify

app = Flask(__name__)

# --- Fungsi Koreksi Esai (dari kode sebelumnya) ---

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

    return round(nilai_siswa), feedback

# --- Endpoint API ---

@app.route('/koreksi_esai', methods=['POST'])
def koreksi_esai_api():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    jawaban_siswa = data.get('jawaban_siswa')
    kunci_jawaban_paragraf = data.get('kunci_jawaban') # Nama key di request menjadi 'kunci_jawaban'
    id_soal = data.get('id_soal', 'Tidak Spesifik') # ID soal opsional, untuk identifikasi

    if not jawaban_siswa or not kunci_jawaban_paragraf:
        return jsonify({"error": "Missing 'jawaban_siswa' or 'kunci_jawaban' in request"}), 400

    nilai, feedback = koreksi_esai_dan_nilai(jawaban_siswa, kunci_jawaban_paragraf)

    response = {
        "id_soal": id_soal, # Sertakan ID soal jika disediakan
        "jawaban_siswa": jawaban_siswa,
        "kunci_jawaban": kunci_jawaban_paragraf, # Sertakan kunci jawaban di response
        "nilai": nilai,
        "feedback": feedback
    }
    return jsonify(response), 200

# --- Menjalankan Aplikasi Flask ---
if __name__ == '__main__':
    app.run(debug=True, port=5000)