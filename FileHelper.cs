using System.IO;
using System.Threading;

namespace SipebiMini.Sample {
	public class FileHelper {
		public static bool PastikanTerhapus(string namaFail)  {
			int counter = 0;
			int counterMaksimum = 50;

			//Hapus fail jika ada
			if (File.Exists(namaFail)) {
				File.Delete(namaFail);
				while (File.Exists(namaFail) && counter <= counterMaksimum) {
					Thread.Sleep(100); //tunggu hingga fail selesai dihapus dengan sempurna
					counter++;
				}
			}
			return counter <= counterMaksimum;
		}

		public static bool PastikanTerbuat(string namaFail) {
			//Pastikan fail telah dibuat dengan sempurna
			FileInfo informasiFail = new FileInfo(namaFail);
			int counter = 0;
			int counterMaksimum = 50;
			while (isFileLocked(informasiFail) && counter <= counterMaksimum) {
				Thread.Sleep(100);
				counter++;
			}
			return counter <= counterMaksimum;
		}

		//Didapat dari: https://stackoverflow.com/questions/10982104/wait-until-file-is-completely-written
		private static bool isFileLocked(FileInfo file) {
			FileStream stream = null;

			try {
				stream = file.Open(FileMode.Open, FileAccess.ReadWrite, FileShare.None);
			} catch (IOException) {
				//the file is unavailable because it is:
				//still being written to
				//or being processed by another thread
				//or does not exist (has already been processed)
				return true;
			} finally {
				if (stream != null)
					stream.Close();
			}

			//file is not locked
			return false;
		}
	}
}
