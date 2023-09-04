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

namespace SipebiMini {
	//Contoh penggunaan IronPython didapat dari:
	//https://www.dotnetlovers.com/article/216/executing-python-script-from-c-sharp
	public class SipebiMiniPythonRunner {
		//Berbagai konstan
		private const string NAMA_DIR_PY = "py";
		private const string NAMA_DIR_INTI = "core";
		private const string NAMA_DIR_PAKET = "libs";
		private const string NAMA_DIR_DATA = "data";
		private const string NAMA_FAIL_CONTOH = "contoh.py";
		private const string NAMA_CONTOH_KELAS_PY = "PySampleClass";
		private const string NAMA_FAIL_HASIL_DIAGNOSIS_PY = "PySipebiDiagnosticsError.py";
		private const string NAMA_KELAS_HASIL_DIAGNOSIS_PY = "PySipebiDiagnosticsError";
		private const string NAMA_KUNCI_DAFTAR_FAIL_DIAGNOSIS_PY = "PyDiagnosticsScripts";
		private const bool BUAT_FAIL_SAMPEL = true;
		private const bool GUNAKAN_FAIL_SAMPEL = true;

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
		private static string packageDir;
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
				packageDir = Path.Combine(baseDir, NAMA_DIR_PAKET);
				dataDir = Path.Combine(baseDir, NAMA_DIR_DATA);
				Directory.CreateDirectory(baseDir);
				Directory.CreateDirectory(coreDir);
				Directory.CreateDirectory(packageDir);
				Directory.CreateDirectory(dataDir);

				//Pembuatan fail kelas hasil diagnosis, jika tidak ada
				diagnosticErrorClassFilePath = Path.Combine(coreDir, NAMA_FAIL_HASIL_DIAGNOSIS_PY);
				if (!File.Exists(diagnosticErrorClassFilePath))
					buatFailKelasHasilDiagnosis();

				//Penambahan search paths
				List<string> searchPaths = new List<string>();
				searchPaths.Add(baseDir);
				searchPaths.Add(coreDir);
				searchPaths.Add(packageDir);
				pythonEngine.SetSearchPaths(searchPaths);

				//Dapatkan semua fail Python yang akan digunakan dalam diagnosis
				if (ConfigurationManager.AppSettings.AllKeys.Contains(NAMA_KUNCI_DAFTAR_FAIL_DIAGNOSIS_PY))
					pyDiagnosticsScripts = ConfigurationManager
						.AppSettings[NAMA_KUNCI_DAFTAR_FAIL_DIAGNOSIS_PY]
						.Split(new string[] { "," }, StringSplitOptions.RemoveEmptyEntries)
						.Select(x => x.Trim()).ToList();

				//Pembuatan sampel
				if (BUAT_FAIL_SAMPEL) {
					sampleFilePath = Path.Combine(baseDir, NAMA_FAIL_CONTOH);
					if (!File.Exists(sampleFilePath)) {
						buatFailDenganSkripSampel();
						return;
					}
				}  
				sampleScript = dapatkanSkripSampel();
			} catch (Exception ex){
				throw new Exception($"Gagal menginisiasi [{nameof(SipebiMiniPythonRunner)}]: {ex}");
			}
		}

		private static void jalankanSkripDiagnosis(string script) {

		}

		public static void JalankanDiagnosis() {
			if (pythonEngine == null) return;
			string currentDiagnosticsScript = string.Empty;
			try {
				foreach (var script in pyDiagnosticsScripts) {
					//Dapatkan skrip diagnosis yang akan digunakan satu per satu
					currentDiagnosticsScript = script;

					//Jalankan skrip diagnosis
					jalankanSkripDiagnosis(script);
				}
			} catch (Exception ex) {
				throw new Exception($"Diagnosis [{currentDiagnosticsScript}] gagal: {ex}");
			}
		}

		#region Sampel
		public static string JalankanSampel() {
			if (pythonEngine == null) return "Tes gagal!";
			if (string.IsNullOrWhiteSpace(sampleScript) ||
				(GUNAKAN_FAIL_SAMPEL && (string.IsNullOrWhiteSpace(sampleFilePath) || !File.Exists(sampleFilePath))))
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
			sampleInstance.execute("teks awal");
			StringBuilder sb = new StringBuilder();
			sb.AppendLine($"varNo: {sampleInstance.varNo.ToString()}");
			sb.AppendLine($"varStr: {sampleInstance.varStr.ToString()}");
			PythonList diagList = sampleInstance.diagList;
			sb.AppendLine($"diagList: \n-{string.Join("\n-", diagList.ToList().Select(x => ((dynamic)x).SimpleDisplay()))}");
			return sb.ToString();
		}

		private static string dapatkanSkripSampel() => GUNAKAN_FAIL_SAMPEL ? 
			File.ReadAllText(sampleFilePath) : buatSkripSampel();

		private static void buatFailKelasHasilDiagnosis() {
			File.WriteAllText(diagnosticErrorClassFilePath, buatSkripKelasHasilDiagnosis());
			int maxCount = 1000;
			int currentCount = 0;
			while (!File.Exists(diagnosticErrorClassFilePath) && currentCount < maxCount) {
				Thread.Sleep(1);
				currentCount++;
			}
			if (!File.Exists(diagnosticErrorClassFilePath))
				throw new Exception($"Gagal membuat [{NAMA_FAIL_HASIL_DIAGNOSIS_PY}]");
		}

		private static string buatSkripKelasHasilDiagnosis() {
			StringBuilder sb = new StringBuilder();
			sb.AppendLine($"class {NAMA_KELAS_HASIL_DIAGNOSIS_PY}:");
			sb.AppendLine("\tErrorCode = '[Kode]'");
			sb.AppendLine("\tParagraphNo = 0");
			sb.AppendLine("\tElementNo = 0");
			sb.AppendLine("\tOriginalElement = ''");
			sb.AppendLine("\tCorrectedElement = ''");
			sb.AppendLine("\tOriginalParagraphOffset = 0");
			sb.AppendLine("\tPositionOffset = 0");
			sb.AppendLine("\tCorrectedCharPosition = 0");
			sb.AppendLine("\tIsAmbiguous = False");
			sb.AppendLine("\tdef SimpleDisplay(self):");
			sb.AppendLine("\t\treturn self.ErrorCode + ' ' + self.OriginalElement + ' -> ' + self.CorrectedElement");
			return sb.ToString();
		}

		private static void buatFailDenganSkripSampel() {
			File.WriteAllText(sampleFilePath, buatSkripSampel());
			int maxCount = 1000;
			int currentCount = 0;
			while (!File.Exists(sampleFilePath) && currentCount < maxCount) {
				Thread.Sleep(1);
				currentCount++;
			}
			if (!File.Exists(sampleFilePath))
				throw new Exception("Gagal membuat [contoh.py]");
		}

		private static string buatSkripSampel() {
			StringBuilder sb = new StringBuilder();
			sb.AppendLine($"#baris di bawah ini harus ada untuk mengimpor {NAMA_KELAS_HASIL_DIAGNOSIS_PY}");
			sb.AppendLine($"from {NAMA_KELAS_HASIL_DIAGNOSIS_PY} import {NAMA_KELAS_HASIL_DIAGNOSIS_PY}");
			sb.AppendLine($"class {NAMA_CONTOH_KELAS_PY}:");
			sb.AppendLine("\tvarNo = 0 #contoh angka");
			sb.AppendLine("\tvarStr = 'sample text' #contoh teks");
			sb.AppendLine("\tdiagList = [] #daftar kesalahan, list ini harus ada");
			sb.AppendLine("\tdef execute(self, text): #signature dari fungsi harus selalu seperti ini: def execute(self, text):");
			sb.AppendLine("\t\tself.varNo = self.varNo + 1 #contoh penggunaan variabel");
			sb.AppendLine("\t\tself.varStr = text #contoh penggunaan input/variabel");
			sb.AppendLine("\t\t#---text dapat diproses di sini untuk mendapatkan hasil diagnosis---");
			sb.AppendLine("\t\t#contoh penambahan hasil diagnosis dapat dilihat di bawah");
			sb.AppendLine("\t\t#elemen PySipebiDiagnosticsError dalam contoh di bawah tidak lengkap, hanya diperuntukkan sebagai contoh, silakan dilengkapi");
			sb.AppendLine("\t\thasilDiagnosis = PySipebiDiagnosticsError()");
			sb.AppendLine("\t\thasilDiagnosis.ErrorCode = '[Kode Contoh A]'");
			sb.AppendLine("\t\thasilDiagnosis.OriginalElement = 'contoh-' + str(self.varNo)");
			sb.AppendLine("\t\thasilDiagnosis.CorrectedElement = 'contoh-' + str(self.varNo) + 'A'");
			sb.AppendLine("\t\tself.diagList.append(hasilDiagnosis)");
			sb.AppendLine("\t\thasilDiagnosis = PySipebiDiagnosticsError()");
			sb.AppendLine("\t\thasilDiagnosis.ErrorCode = '[Kode Contoh B]'");
			sb.AppendLine("\t\thasilDiagnosis.OriginalElement = 'contoh-'+ str(self.varNo)");
			sb.AppendLine("\t\thasilDiagnosis.CorrectedElement = 'contoh-' + str(self.varNo) + 'B'");
			sb.AppendLine("\t\tself.diagList.append(hasilDiagnosis)");
			sb.AppendLine("\t\tif len(self.diagList) > 10:");
			sb.AppendLine("\t\t\tself.diagList.pop(1)");
			sb.AppendLine("\t\t\tself.diagList.pop(0)");
			return sb.ToString();
		}
		#endregion Sampel
	}
}
