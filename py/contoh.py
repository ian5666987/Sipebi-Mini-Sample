#baris di bawah ini harus ada untuk mengimpor PySipebiDiagnosticsError
from PySipebiDiagnosticsError import PySipebiDiagnosticsError
class PySampleClass:
	varNo = 0 #contoh angka
	varStr = 'sample text' #contoh teks
	diagList = [] #daftar kesalahan, list ini harus ada
	def execute(self, text): #signature dari fungsi harus selalu seperti ini: def execute(self, text):
		self.varNo = self.varNo + 1 #contoh penggunaan variabel
		self.varStr = text #contoh penggunaan input/variabel
		#---text dapat diproses di sini untuk mendapatkan hasil diagnosis---
		#contoh penambahan hasil diagnosis dapat dilihat di bawah
		#elemen PySipebiDiagnosticsError dalam contoh di bawah tidak lengkap, hanya diperuntukkan sebagai contoh, silakan dilengkapi
		hasilDiagnosis = PySipebiDiagnosticsError()
		hasilDiagnosis.ErrorCode = '[Kode Contoh A]'
		hasilDiagnosis.OriginalElement = 'contoh-' + str(self.varNo)
		hasilDiagnosis.CorrectedElement = 'contoh-' + str(self.varNo) + 'A'
		self.diagList.append(hasilDiagnosis)
		hasilDiagnosis = PySipebiDiagnosticsError()
		hasilDiagnosis.ErrorCode = '[Kode Contoh B]'
		hasilDiagnosis.OriginalElement = 'contoh-'+ str(self.varNo)
		hasilDiagnosis.CorrectedElement = 'contoh-' + str(self.varNo) + 'B'
		self.diagList.append(hasilDiagnosis)
		if len(self.diagList) > 10:
			self.diagList.pop(1)
			self.diagList.pop(0)
