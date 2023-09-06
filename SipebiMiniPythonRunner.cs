using System;
using System.Collections.Generic;
using System.Configuration;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using IronPython;
using IronPython.Hosting;
using IronPython.Runtime;
using Microsoft.Scripting.Hosting;
using SipebiMini.Core;

namespace SipebiMini {
	//Contoh penggunaan IronPython didapat dari:
	//https://www.dotnetlovers.com/article/216/executing-python-script-from-c-sharp
	public class SipebiMiniPythonRunner {
		//Berbagai konstan
		private const string NAMA_DIR_PY = "py";
		private const string NAMA_DIR_INTI = "core";
		private const string NAMA_DIR_PAKET = "libs";
		private const string NAMA_DIR_DATA = "data";
		private const string NAMA_DIR_DOC = "docs";
		private const string NAMA_DIR_VAL = "val";
		private const string NAMA_FAIL_CONTOH = "PySampleClass.py"; 
		private const string NAMA_CONTOH_KELAS_PY = "PySampleClass";
		private const string NAMA_KUNCI_DAFTAR_FAIL_DIAGNOSIS_PY = "PyDiagnosticsScripts";

		//Python Engine, daftar skrip diagnosis
		private static ScriptEngine pythonEngine;
		private static List<string> pyDiagnosticsScripts = new List<string>();

		//Properti berhubungan dengan sampel (Python)
		private static ScriptSource sampleSource;
		private static ScriptScope sampleScope;
		private static dynamic sampleClass;
		private static dynamic sampleInstance;
		private static string sampleScript;

		//Direktori-direktori dan fail-fail
		private static string baseDir;
		private static string coreDir;
		private static string dataDir;
		private static string docsDir;
		private static string libsDir;
		private static string valDir;
		private static string valCoreDir;
		private static string valDataDir;
		private static string valLibsDir;
		private static string sampleFilePath;
		private static string diagnosticErrorClassFilePath;
		public static void Inisiasi() {
			try {
				//Inisiasi Python Engine
				if (pythonEngine != null) return;
				pythonEngine = Python.CreateEngine();

				//Pembuatan semua direktori yang diperlukan
				baseDir = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, NAMA_DIR_PY);
				coreDir = Path.Combine(baseDir, NAMA_DIR_INTI);
				dataDir = Path.Combine(baseDir, NAMA_DIR_DATA);
				docsDir = Path.Combine(baseDir, NAMA_DIR_DOC);
				libsDir = Path.Combine(baseDir, NAMA_DIR_PAKET);
				valDir = Path.Combine(baseDir, NAMA_DIR_VAL);
				valCoreDir = Path.Combine(valDir, NAMA_DIR_INTI);
				valDataDir = Path.Combine(valDir, NAMA_DIR_DATA);
				valLibsDir = Path.Combine(valDir, NAMA_DIR_PAKET);

				//Penambahan search paths
				List<string> searchPaths = new List<string>() {
					baseDir, coreDir, dataDir, docsDir, libsDir,
					valDir, valCoreDir, valDataDir, valLibsDir,
				};
				foreach (string dir in searchPaths)
					Directory.CreateDirectory(dir);
				pythonEngine.SetSearchPaths(searchPaths);

				//Dapatkan semua fail Python yang akan digunakan dalam diagnosis
				if (ConfigurationManager.AppSettings.AllKeys.Contains(NAMA_KUNCI_DAFTAR_FAIL_DIAGNOSIS_PY))
					pyDiagnosticsScripts = ConfigurationManager
						.AppSettings[NAMA_KUNCI_DAFTAR_FAIL_DIAGNOSIS_PY]
						.Split(new string[] { "," }, StringSplitOptions.RemoveEmptyEntries)
						.Select(x => x.Trim()).ToList();

				//Dapatkan skrip sampel
				sampleFilePath = Path.Combine(baseDir, NAMA_FAIL_CONTOH);
				sampleScript = dapatkanSkripSampel();
			} catch (Exception ex){
				throw new Exception($"Gagal menginisiasi [{nameof(SipebiMiniPythonRunner)}]: {ex}");
			}
		}

		private static Dictionary<string, ScriptSource> pySources = new Dictionary<string, ScriptSource>();
		private static Dictionary<string, ScriptScope> pyScopes = new Dictionary<string, ScriptScope>();
		private static Dictionary<string, dynamic> pyClasses = new Dictionary<string, dynamic>();
		private static Dictionary<string, dynamic> pyInstances = new Dictionary<string, dynamic>();
		private static List<SipebiDiagnosticsError> jalankanSkripDiagnosis(string teksAsal, string namaFailSkrip, string namaKelasPython) {
			List<SipebiDiagnosticsError> daftarKesalahanTambahan = new List<SipebiDiagnosticsError>();

			//Proses menjalankan skrip di sini
			string scriptPath = Path.Combine(baseDir, namaFailSkrip);

			//Jika skrip tidak ditemukan, diagnosis tidak perlu dijalankan
			if (!File.Exists(scriptPath)) return daftarKesalahanTambahan;

			//Ambil isi, sumber, dan cakupan skrip
			string skrip = File.ReadAllText(scriptPath);
			if (!pySources.ContainsKey(namaFailSkrip))
				pySources.Add(namaFailSkrip, pythonEngine.CreateScriptSourceFromString(skrip));
			ScriptSource pySource = pySources[namaFailSkrip];
			if (!pyScopes.ContainsKey(namaFailSkrip))
				pyScopes.Add(namaFailSkrip, pythonEngine.CreateScope());
			ScriptScope pyScope = pyScopes[namaFailSkrip];
			pySource.Execute(pyScope);
			if (!pyClasses.ContainsKey(namaFailSkrip))
				pyClasses.Add(namaFailSkrip, pyScope.GetVariable(namaKelasPython));			
			dynamic pyClass = pyClasses[namaFailSkrip];
			if (!pyInstances.ContainsKey(namaFailSkrip)) 
				pyInstances.Add(namaFailSkrip, pythonEngine.Operations.CreateInstance(pyClass));
			dynamic pyInstance = pyInstances[namaFailSkrip];

			//Siapkan skrip hanya jika belum dipersiapkan sebelumnya
			if (pyInstance.isReady == false)
				pyInstance.setup();

			//Jalankan skrip dengan input teks asal
			pyInstance.execute(teksAsal);

			//Dapatkan hasil diagnosis skrip ini
			PythonList diagList = pyInstance.diagList;
			foreach (dynamic diagItem in diagList) {
				SipebiDiagnosticsError kesalahan = new SipebiDiagnosticsError();
				kesalahan.CorrectedCharPosition = diagItem.CorrectedCharPosition;
				kesalahan.CorrectedElement = diagItem.CorrectedElement;
				kesalahan.ElementNo = diagItem.ElementNo;
				kesalahan.ErrorCode = diagItem.ErrorCode;
				kesalahan.IsAmbiguous = diagItem.IsAmbiguous;
				kesalahan.OriginalElement = diagItem.OriginalElement;
				kesalahan.OriginalParagraphOffset = diagItem.OriginalParagraphOffset;
				kesalahan.ParagraphNo = diagItem.ParagraphNo;
				kesalahan.PositionOffset = diagItem.PositionOffset;
				daftarKesalahanTambahan.Add(kesalahan);
			}

			//Kembalikan hasil daftar kesalahan tambahan
			return daftarKesalahanTambahan;
		}

		public static List<SipebiDiagnosticsError> JalankanDiagnosis(string teksAsal, SipebiMiniDiagnosticsReport laporan) {
			List<SipebiDiagnosticsError> daftarKesalahanTambahan = new List<SipebiDiagnosticsError>();
			if (pythonEngine == null) return daftarKesalahanTambahan;
			string currentDiagnosticsScript = string.Empty;
			try {
				foreach (var skripDiagnosis in pyDiagnosticsScripts) {
					//Siapkan daftar baru khusus untuk kesalahan yang ditemukan oleh skrip ini
					List<SipebiDiagnosticsError> daftarKesalahanSkripIni = new List<SipebiDiagnosticsError>();

					//Dapatkan skrip diagnosis dan nama kelas Python yang akan digunakan satu per satu
					currentDiagnosticsScript = skripDiagnosis;

					//Format skrip diagnosis: namaFailSkrip-namaKelasPython atau namaFailSkrip
					string namaFailSkrip = skripDiagnosis;
					string namaKelasPython = Path.GetFileNameWithoutExtension(skripDiagnosis);
					if (skripDiagnosis.Contains("-")) {
						List<string> bagianSkripDiagnosis = skripDiagnosis
							.Split('-').Where(x => !string.IsNullOrWhiteSpace(x))
							.Select(x => x.Trim()).ToList();
						//Bagian skrip diagnosis yang mengandung "-" harus tepat terdiri dari dua bagian
						if (bagianSkripDiagnosis.Count == 2) {
							namaFailSkrip = bagianSkripDiagnosis[0];
							namaKelasPython = bagianSkripDiagnosis[1];
						}
					}

					//Jalankan skrip diagnosis
					daftarKesalahanSkripIni = jalankanSkripDiagnosis(teksAsal, namaFailSkrip, namaKelasPython);

					//Tambahkan hasil diagnosis skrip ini ke daftar kesalahan tambahan
					daftarKesalahanTambahan.AddRange(daftarKesalahanSkripIni);
				}
			} catch (Exception ex) {
				throw new Exception($"Diagnosis [{currentDiagnosticsScript}] gagal: {ex}");
			}
			return daftarKesalahanTambahan;
		}

		#region Sampel
		public static string JalankanSampel() {
			if (pythonEngine == null) return "Tes gagal!";
			if (string.IsNullOrWhiteSpace(sampleScript) ||
				  string.IsNullOrWhiteSpace(sampleFilePath) || !File.Exists(sampleFilePath))
				sampleScript = dapatkanSkripSampel();
			if (sampleSource == null)
				sampleSource = pythonEngine.CreateScriptSourceFromString(sampleScript);
			if (sampleScope == null)
				sampleScope = pythonEngine.CreateScope();
			sampleSource.Execute(sampleScope);
			if (sampleClass == null)
				sampleClass = sampleScope.GetVariable(NAMA_CONTOH_KELAS_PY);
			if (sampleInstance == null)
				sampleInstance = pythonEngine.Operations.CreateInstance(sampleClass);
			if (sampleInstance.isReady == false)
				sampleInstance.setup();
			sampleInstance.execute("teks awal");
			StringBuilder sb = new StringBuilder();
			sb.AppendLine($"varNo: {sampleInstance.varNo.ToString()}");
			sb.AppendLine($"varStr: {sampleInstance.varStr.ToString()}");
			PythonList diagList = sampleInstance.diagList;
			sb.AppendLine($"diagList: \n-{string.Join("\n-", diagList.ToList().Select(x => ((dynamic)x).SimpleDisplay()))}");
			return sb.ToString();
		}

		private static string dapatkanSkripSampel() => File.ReadAllText(sampleFilePath);
		#endregion Sampel
	}
}
