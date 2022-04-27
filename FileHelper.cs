using System.IO;
using System.Threading;

namespace SipebiMini {
	public class FileHelper {
		// Fungsi untuk mengecek apakah file telah dihapus dari sistem
		public static bool PastikanTerhapus(string namaFail)  {
			int counter = 0;
			int counterMaksimum = 50;
			if (File.Exists(namaFail)) {
				File.Delete(namaFail);
				while (File.Exists(namaFail) && counter <= counterMaksimum) {
					Thread.Sleep(100);
					counter++;
				}
			}
			return counter <= counterMaksimum;
		}

		// Fungsi untuk mengecek apakah file telah dibuat oleh sistem
		public static bool PastikanTerbuat(string namaFail) {
			FileInfo informasiFail = new FileInfo(namaFail);
			int counter = 0;
			int counterMaksimum = 50;
			while (isFileLocked(informasiFail) && counter <= counterMaksimum) {
				Thread.Sleep(100);
				counter++;
			}
			return counter <= counterMaksimum;
		}

		/* Mengecek apakah file tidak dikunci oleh sistem atau suatu proses
		 * Didapat dari: https://stackoverflow.com/questions/10982104/wait-until-file-is-completely-written
		 */
		private static bool isFileLocked(FileInfo file) {
			FileStream stream = null;
			try {
				stream = file.Open(FileMode.Open, FileAccess.ReadWrite, FileShare.None);
			} catch (IOException) {
				return true;
			} finally {
				if (stream != null)
					stream.Close();
			}
			return false;
		}
	}
}
