using SipebiMini.Core;
using System;
using System.Linq;
using System.Reflection;
using System.Windows.Forms;
using py = SipebiMini.SipebiMiniPythonRunner;

namespace SipebiMini {
	public partial class SampleForm : Form {
		public SampleForm() {
			InitializeComponent();
			Text += $" v{Assembly.GetExecutingAssembly().GetName().Version}";
			state.Inisiasi();
			py.Inisiasi();
		}

		SipebiMiniState state = new SipebiMiniState();
		const string formatPesanMuatContoh = "Contoh {0} dimuat!";
		const string formatPesanPenyuntinganAsal = "Penyuntingan dengan cara asal Sipebi {0}!";
		const string formatPesanPenyuntinganBuatan = "Penyuntingan dengan cara buatan Sipebi {0}!";

		private void buttonMuatContoh_Click(object sender, EventArgs e) {
			prosedurUmum(formatPesanMuatContoh, () => {
				richTextBoxTeksMasukan.Text = state.MuatContoh();
			});
		}

		private void buttonSuntingAsal_Click(object sender, EventArgs e) {
			prosedurUmumPenyuntingan(formatPesanPenyuntinganAsal, state.SuntingAsal);
		}

		private void buttonSuntingBuatan_Click(object sender, EventArgs e) {
			prosedurUmumPenyuntingan(formatPesanPenyuntinganBuatan, state.SuntingBuatan);
		}

		private void tampilkanHasilAnalisis(SipebiMiniDiagnosticsReport report) {
			DataGridView dgv = dataGridViewHasilAnalisis;
			int indeks = 0;
			dgv.Rows.Clear();
			foreach (var hasil in report.Errors) {				
				indeks = dgv.RowCount - 1;
				DataGridViewRow baris = (DataGridViewRow)dgv.RowTemplate.Clone();
				baris.CreateCells(dgv, indeks + 1, hasil.ParagraphNo, hasil.ElementNo, hasil.ErrorCode,
					state.InformasiKesalahan[hasil.ErrorCode].Error, 
					hasil.OriginalElement, hasil.CorrectedElementDisplay,
					state.InformasiKesalahan[hasil.ErrorCode].ErrorExplanation);
				dgv.Rows.Add(baris);
			}
		}

		private string pesanTambahan = "";
		private DateTime waktuMulai, waktuSelesai;
		private TimeSpan durasiDiagnosis;
		private void prosedurUmumPenyuntingan(string formatPesan,
			Func<string, Tuple<SipebiMiniDiagnosticsReport, string>> fungsiPenyuntingan) {
			string teksAsal = richTextBoxTeksMasukan.Text;
			prosedurUmum(formatPesan, () => {
				waktuMulai = DateTime.Now;
				Tuple<SipebiMiniDiagnosticsReport, string> hasil = fungsiPenyuntingan(teksAsal);
				tampilkanHasilAnalisis(hasil.Item1);
				richTextBoxTeksSuntingan.Text = hasil.Item2;
				waktuSelesai = DateTime.Now;
				durasiDiagnosis = waktuSelesai - waktuMulai;
				pesanTambahan = dapatkanPesanJumlahKesalahanTerdeteksi(hasil, teksAsal.Length);
			});
		}

		private void prosedurUmum(string formatPesan, Action aksi) {
			string teksHasil = "gagal";
			string pesanKesalahan = string.Empty;
			try {
				aturKontrol(false);
				aksi();
				teksHasil = "berhasil";
			} catch (Exception exc) {
				pesanKesalahan = Environment.NewLine + Environment.NewLine + "Kesalahan: " + exc.ToString();
			}
			MessageBox.Show(string.Format(formatPesan, teksHasil) + 
				pesanTambahan + pesanKesalahan, 
				char.ToUpper(teksHasil[0]) + teksHasil.Substring(1));
			aturKontrol(true);
		}

		private void aturKontrol(bool aktifkan) {
			flowLayoutPanelActions.Enabled = aktifkan;
		}

		private void buttonUjiCobaPython_Click(object sender, EventArgs e) {
			string result = SipebiMiniPythonRunner.JalankanSampel();
			MessageBox.Show($"{result}", "Hasil Uji Coba", MessageBoxButtons.OK);
		}

		private void buttonSuntingPython_Click(object sender, EventArgs e) {

		}

		private string dapatkanPesanJumlahKesalahanTerdeteksi(Tuple<SipebiMiniDiagnosticsReport, string> hasil,
			int panjangTeksAwal) {
			if (hasil == null || hasil.Item1 == null || hasil.Item1.Errors == null) return string.Empty;
			var grupKesalahan = hasil.Item1.Errors.GroupBy(x => x.ErrorCode).OrderByDescending(x => x.Count());
			return Environment.NewLine + Environment.NewLine +
				$"Jumlah Kesalahan Terdeteksi: {hasil.Item1.Errors.Count}" + Environment.NewLine +
				$" Definit: {hasil.Item1.Errors.Count(x => !x.IsAmbiguous)}" + Environment.NewLine +
				$" Ambigu: {hasil.Item1.Errors.Count(x => x.IsAmbiguous)}" + Environment.NewLine +
				Environment.NewLine +
				string.Join(Environment.NewLine, grupKesalahan
					.Select(x => $"{x.Count()} {state.InformasiKesalahan[x.Key].ErrorCode} - " +
						$"{state.InformasiKesalahan[x.Key].Error}")) + Environment.NewLine +
				Environment.NewLine +
				$"Durasi Diagnosis: {durasiDiagnosis.TotalSeconds.ToString("F2")} detik" + Environment.NewLine +
				$"Panjang Teks: {panjangTeksAwal}" + Environment.NewLine +
				$"Jumlah Paragraf: {hasil.Item1.Paragraphs.Count}" + Environment.NewLine +
				$"Jumlah Elemen: {hasil.Item1.Paragraphs.Sum(x => x.WordDivs.Count)}" + Environment.NewLine +
				Environment.NewLine +
				$"Waktu Mulai Diagnosis: {waktuMulai.ToString("dd-MM-yyyy HH:mm:sss.fff")}" + Environment.NewLine +
				$"Waktu Selesai Diagnosis: {waktuSelesai.ToString("dd-MM-yyyy HH:mm:sss.fff")}" + Environment.NewLine +
				Environment.NewLine;
		}
	}
}
