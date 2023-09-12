using SipebiMini.Core;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Xml.Serialization;

namespace SipebiMini {
	public class SipebiMiniState {
		public const string JudulContohTeksBawaan = "contoh-teks.txt";
		public const string JudulTeksAwalBawaan = "teks-awal.txt";
		public const string JudulLaporanAnalisisBuatan = "laporan-diagnosis-buatan.xml";
		public const string JudulLaporanAnalisisPython = "laporan-diagnosis-python.xml";
		public const string JudulTambahanDataBuatan = "tambahan-data-buatan.txt"; //tambahan data untuk proses penyuntingan buatan
		public const string JudulLaporanAnalisisBawaan = "laporan-diagnosis.xml"; //Jangan diganti
		public const string JudulDaftarDiagnosisBawaan = "daftar-diagnosis.xml"; //Jangan diganti
		public const string JudulDaftarDiagnosisTambahan = "daftar-diagnosis-tambahan.xml"; //Jangan diganti
		public const string NamaProsesAnalisis = "SipebiMini.Analyser.exe"; //Jangan diganti
		public const string NamaProsesPenyuntingan = "SipebiMini.Editor.exe"; //Jangan diganti

		public Dictionary<string, SipebiDiagnosticsErrorInformation> InformasiKesalahan = 
			new Dictionary<string, SipebiDiagnosticsErrorInformation>();

		SipebiDiagnosticsErrorInformation kesalahanPenulisanSingkatDefinit;
		SipebiDiagnosticsErrorInformation kesalahanPenulisanSingkatAmbigu;
		Dictionary<string, List<string>> daftarKesalahanPenulisanSingkat = new Dictionary<string, List<string>>();

		public void Inisiasi() {
			XmlSerializer serializer = new XmlSerializer(typeof(List<SipebiDiagnosticsErrorInformation>));
			List<SipebiDiagnosticsErrorInformation> daftarDiagnosis = new List<SipebiDiagnosticsErrorInformation>();

			//Penambahan daftar diagnosis bawaan
			InformasiKesalahan.Clear();
			using (FileStream fileStream = new FileStream(JudulDaftarDiagnosisBawaan, FileMode.Open))
				daftarDiagnosis = (List<SipebiDiagnosticsErrorInformation>)serializer.Deserialize(fileStream);
			foreach (var info in daftarDiagnosis)
				InformasiKesalahan.Add(info.ErrorCode, info);

			//Penambahan daftar diagnosis tambahan
			if (File.Exists(JudulDaftarDiagnosisTambahan)) {
				using (FileStream fileStream = new FileStream(JudulDaftarDiagnosisTambahan, FileMode.Open))
					daftarDiagnosis = (List<SipebiDiagnosticsErrorInformation>)serializer.Deserialize(fileStream);
				foreach (var info in daftarDiagnosis)
					InformasiKesalahan.Add(info.ErrorCode, info);
			}

			//Dapatkan informasi kesalahan suntingan buatan
			// kesalahanPenulisanSingkatDefinit = InformasiKesalahan["[Buatan-KPS-D]"];
			// kesalahanPenulisanSingkatAmbigu = InformasiKesalahan["[Buatan-KPS-A]"];

			//Tambahkan proses inisiasi lain untuk proses penyuntingan buatan			
			try { //Muat fail tambahan untuk proses penyuntingan buatan
				string[] barisTeksBuatan = File.ReadAllLines(JudulTambahanDataBuatan);
				daftarKesalahanPenulisanSingkat = barisTeksBuatan.Select(x => x.Split('|')
					.Where(y => !string.IsNullOrWhiteSpace(y)).Select(y => y.Trim()).ToList())
					.Where(x => x.Count == 2).ToDictionary(x => x[0],
						x => x[1].Split(',').Where(y => !string.IsNullOrWhiteSpace(y))
						.Select(y => y.Trim()).ToList());
			} catch (Exception exc){
				throw new Exception($"Terjadi kesalahan pada proses inisiasi data buatan: {exc}");
			}
		}

		public string MuatContoh(string judulContohTeks = null) => 
			File.ReadAllText(string.IsNullOrWhiteSpace(judulContohTeks) || !File.Exists(judulContohTeks) ? 
				JudulContohTeksBawaan : judulContohTeks);		
		
		public Tuple<SipebiMiniDiagnosticsReport, string> SuntingAsal(string teksAwal) {
			SipebiMiniDiagnosticsReport laporan = analisis(teksAwal);
			string teksPenyuntingan = sunting(teksAwal);
			return new Tuple<SipebiMiniDiagnosticsReport, string>(laporan, teksPenyuntingan);
		}
				
		public Tuple<SipebiMiniDiagnosticsReport, string> SuntingBuatan(string teksAwal) {
			SipebiMiniDiagnosticsReport laporan = analisis(teksAwal);
			string teksPenyuntingan = suntingBuatan(teksAwal, laporan);
			return new Tuple<SipebiMiniDiagnosticsReport, string>(laporan, teksPenyuntingan);
		}

		public Tuple<SipebiMiniDiagnosticsReport, string> SuntingPython(string teksAwal) {
			SipebiMiniDiagnosticsReport laporan = analisis(teksAwal);
			string teksPenyuntingan = suntingPython(teksAwal, laporan);
			return new Tuple<SipebiMiniDiagnosticsReport, string>(laporan, teksPenyuntingan);
		}

		private SipebiMiniDiagnosticsReport analisis(string teksAwal) {
			//Jalankan prosedur umum menggunakan nama dan argumen proses analisis
			prosedurUmum(teksAwal, JudulLaporanAnalisisBawaan, NamaProsesAnalisis,
				$"\"{JudulTeksAwalBawaan}\"", "Proses analisis gagal diselesaikan!"); 

			//Lakukan deserialisasi fail hasil proses analisis Sipebi
			SipebiMiniDiagnosticsReport laporan = null;
			XmlSerializer serializer = new XmlSerializer(typeof(SipebiMiniDiagnosticsReport));
			using (FileStream stream = new FileStream(JudulLaporanAnalisisBawaan, FileMode.Open))
				laporan = (SipebiMiniDiagnosticsReport)serializer.Deserialize(stream);

			//Kembalikan hasil proses analisis Sipebi
			return laporan;
		}

		private string sunting(string teksAwal) {
			//Fail hasil perbaikan
			string failHasil = JudulTeksAwalBawaan.Substring(0, JudulTeksAwalBawaan.Length - 4) + "-perbaikan.txt";

			//Jalankan prosedur umum menggunakan nama dan argumen proses penyuntingan
			prosedurUmum(teksAwal, failHasil, NamaProsesPenyuntingan,
				$"\"{JudulTeksAwalBawaan}\" \"{JudulLaporanAnalisisBawaan}\"", 
				"Proses penyuntingan gagal diselesaikan!");

			//Kembalikan isi teks fail hasil
			return File.ReadAllText(failHasil);
		}

		private List<SipebiDiagnosticsError> dapatkanKesalahanPenulisanSingkat(SipebiMiniDiagnosticsReport laporan) {
			List<SipebiDiagnosticsError> daftarKesalahanTambahan = new List<SipebiDiagnosticsError>();
			//cek setiap paragraf
			foreach (var paragraf in laporan.Paragraphs) {
				//cek setiap kata pada paragraf																										 
				foreach (var kata in paragraf.WordDivs) {
					//jika tidak terdapat kata pada divisi ini (misalnya, hanya tanda baca saja), lewati saja
					if (string.IsNullOrWhiteSpace(kata.CleanWordString)) continue;

					//untuk mengecek kesalahan, gunakan variasi huruf kecil kata tersebut saja 
					string hkKata = kata.CleanWordString.ToLower();

					//jika kata ini tidak ditemukan dalam daftar kesalahan, jangan apa-apakan
					if (!daftarKesalahanPenulisanSingkat.ContainsKey(hkKata)) continue; 

					//Jika kesalahan penulisan terdeteksi, siapkan perbaikan
					var daftarPerbaikan = daftarKesalahanPenulisanSingkat[hkKata]; //dapatkan daftar perbaikan
					bool apakahKesalahanDefinit = daftarPerbaikan.Count == 1; //jika perbaikan hanya 1: definit, jika lebih: ambigu

					//Dapatkan jenis kesalahan
					SipebiDiagnosticsErrorInformation jenisKesalahan = apakahKesalahanDefinit ?
						kesalahanPenulisanSingkatDefinit : kesalahanPenulisanSingkatAmbigu;

					//Buat kesalahan dan perbaikannya 
					SipebiDiagnosticsError kesalahan = new SipebiDiagnosticsError(jenisKesalahan.ErrorCode,
						paragraf.Index, paragraf.Offset, kata.ElementNo, kata.PositionOffset,
						originalElement: kata.OriginalString,
						isAmbiguous: !apakahKesalahanDefinit);

					//Jika kesalahan ini definit
					if (apakahKesalahanDefinit) {
						string perbaikanMentah = daftarPerbaikan[0];  //Dapatkan teks perbaikan mentah
						bool perbaikanMentahMemilikiHurufKapital = perbaikanMentah.Any(x => char.IsUpper(x));

						//Jika perbaikan mentah memiliki huruf kapital, gunakan langsung, karena mungkin huruf kapital pada perbaikan dimaksudkan
						string perbaikan = perbaikanMentahMemilikiHurufKapital ? perbaikanMentah : //jika tidak, cek apakah awalnya terdapat huruf kapital
							kata.FirstCharIsCapitalized && perbaikanMentah.Length > 1 ? //jika kata asal diawali dengan huruf kapital
							(char.ToUpper(perbaikanMentah[0]).ToString() + perbaikanMentah.Substring(1)) : //perbaiki dengan mempertahankan huruf kapital di awal kata
							perbaikanMentah; //jika kata asal tidak diawali dengan huruf kapital, perbaikan mentah juga dapat digunakan langsung
						kesalahan.CorrectedElement = perbaikan;
					} else //jika kesalahan ini ambigu
						kesalahan.CorrectedElement = string.Join(", ", daftarPerbaikan); //dapatkan saran perbaikan, bukan hanya satu perbaikan						

					//daftarkan kesalahan ini
					daftarKesalahanTambahan.Add(kesalahan);
				}
			}

			//Kembalikan daftar kesalahan yang didapat
			return daftarKesalahanTambahan; 
		}

		private string suntingBuatan(string teksAwal, SipebiMiniDiagnosticsReport laporan) {
			//Kerjakan penyuntingan tambahan di sini
			List<SipebiDiagnosticsError> daftarKesalahanTambahan = dapatkanKesalahanPenulisanSingkat(laporan);

			//Masukkan daftar kesalahan tambahan pada laporan, dan urutkan ulang posisi kesalahan pada daftar kesalahan
			laporan.Errors.AddRange(daftarKesalahanTambahan);
			laporan.Errors = laporan.Errors.OrderBy(x => x.ParagraphNo).ThenBy(x => x.PositionOffset).ToList();

			//Pastikan fail hasil analisis buatan terhapus (jika ada)
			bool hasil = FileHelper.PastikanTerhapus(JudulLaporanAnalisisBuatan);

			//Simpan hasil penyuntingan buatan
			XmlSerializer serializer = new XmlSerializer(typeof(SipebiMiniDiagnosticsReport));
			using (FileStream stream = new FileStream(JudulLaporanAnalisisBuatan, FileMode.Create))
				serializer.Serialize(stream, laporan);

			//Pastikan fail hasil analisis buatan telah dibuat dengan sempurna
			hasil = FileHelper.PastikanTerbuat(JudulLaporanAnalisisBuatan);

			//Fail hasil perbaikan
			string failHasil = JudulTeksAwalBawaan.Substring(0, JudulTeksAwalBawaan.Length - 4) + "-perbaikan.txt";

			//Jalankan prosedur umum menggunakan nama dan argumen proses penyuntingan buatan
			prosedurUmum(teksAwal, failHasil, NamaProsesPenyuntingan,
				$"\"{JudulTeksAwalBawaan}\" \"{JudulLaporanAnalisisBuatan}\"",
				"Proses penyuntingan buatan gagal diselesaikan!");

			//Kembalikan isi teks fail hasil penyuntingan buatan
			return File.ReadAllText(failHasil);
		}

		private string suntingPython(string teksAwal, SipebiMiniDiagnosticsReport laporan) {
			//Jalankan diagnosis Python di sini
			List<SipebiDiagnosticsError> daftarKesalahanTambahan = SipebiPythonManager.RunDiagnostics(teksAwal, laporan);

			//Masukkan daftar kesalahan tambahan pada laporan, dan urutkan ulang posisi kesalahan pada daftar kesalahan
			laporan.Errors.AddRange(daftarKesalahanTambahan);
			laporan.Errors = laporan.Errors.OrderBy(x => x.ParagraphNo).ThenBy(x => x.PositionOffset).ToList();

			//Pastikan fail hasil analisis Python terhapus (jika ada)
			bool hasil = FileHelper.PastikanTerhapus(JudulLaporanAnalisisPython);

			//Simpan hasil penyuntingan Python
			XmlSerializer serializer = new XmlSerializer(typeof(SipebiMiniDiagnosticsReport));
			using (FileStream stream = new FileStream(JudulLaporanAnalisisPython, FileMode.Create))
				serializer.Serialize(stream, laporan);

			//Pastikan fail hasil analisis Python telah dibuat dengan sempurna
			hasil = FileHelper.PastikanTerbuat(JudulLaporanAnalisisPython);

			//Fail hasil perbaikan
			string failHasil = JudulTeksAwalBawaan.Substring(0, JudulTeksAwalBawaan.Length - 4) + "-perbaikan.txt";

			//Jalankan prosedur umum menggunakan nama dan argumen proses penyuntingan Python
			prosedurUmum(teksAwal, failHasil, NamaProsesPenyuntingan,
				$"\"{JudulTeksAwalBawaan}\" \"{JudulLaporanAnalisisPython}\"",
				"Proses penyuntingan Python gagal diselesaikan!");

			//Kembalikan isi teks fail hasil penyuntingan Python
			return File.ReadAllText(failHasil);
		}

		private void prosedurUmum(string teksAwal, string failHasilProses, 
			string namaProses, string argumenProses, string pesanKesalahanProses) {
			string teks = teksAwal;
			//perbaikan teks yang tidak mengandung petanda paragaf akibat penggunaan "RichTexBox.Text" milik Windows Form
			if (!teks.Contains("\r\n"))
				teks = teks.Replace("\n", "\r\n");

			//Hapus fail teks awal terlebih dahulu jika ada
			bool hasil = FileHelper.PastikanTerhapus(JudulTeksAwalBawaan);

			//Pastikan fail hasil proses terhapus
			hasil = FileHelper.PastikanTerhapus(failHasilProses);

			//Buat fail teks awal untuk dianalisis
			using (var writer = File.CreateText(JudulTeksAwalBawaan)) {
				writer.Write(teks);
				writer.Close();
			}

			//Pastikan fail teks awal telah dibuat dengan sempurna
			hasil = FileHelper.PastikanTerbuat(JudulTeksAwalBawaan);

			//Jalankan proses
			ProcessStartInfo processStartInfo = new ProcessStartInfo {
				FileName = namaProses,
				Arguments = argumenProses,
				CreateNoWindow = true,
			};
			bool terjadiKesalahan = false;
			int kodeError = -1;
			bool selesai = Task.Run(() => {
				Process process = Process.Start(processStartInfo);
				process.WaitForExit();
				kodeError = process.ExitCode;
				terjadiKesalahan = process.ExitCode != 0;
			}).Wait(10000); //Tunggu sebentar hingga proses selesai
			if (!selesai || terjadiKesalahan) //Lemparkan kesalahan jika proses tidak berhasil dijalankan dengan sempurna
				throw new Exception($"{pesanKesalahanProses}\r\n\r\nKode error: 0x{kodeError.ToString("X8")}\r\n");

			//Pastikan fail hasil proses telah dibuat dengan sempurna
			hasil = FileHelper.PastikanTerbuat(failHasilProses);
		}
	}
}
