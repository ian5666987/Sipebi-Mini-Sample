#baris-baris di bawah ini harus ada untuk mengimpor kelas-kelas inti Python
from PySipebiDiagnosticsError import PySipebiDiagnosticsError
from PySipebiAnalyzerBase import PySipebiAnalyzerBase
class PySampleClass(PySipebiAnalyzerBase):
	varNo = 0 #contoh angka
	varStr = 'sample text' #contoh teks
	diagList = [] #daftar kesalahan. List ini harus ada (hanya contoh, dapat dihapus, sudah terdefinisikan pada PySipebiAnalyzerBase)
	isReady = False #bendera yang menandakan pengaturan awal sudah selesai dikerjakan. Bendera ini harus ada (hanya contoh, dapat dihapus, sudah terdefinisikan pada PySipebiAnalyzerBase)
	#setup: fungsi untuk melakukan pengaturan awal sebelum 'execute' dijalankan. Fungsi ini harus ada (sudah terdefinisikan pada PySipebiAnalyzerBase)
	def setup(self): #signature dari fungsi harus selalu seperti ini: setup(self):
		#---lakukan pengaturan awal di sini---
		#---mis: membaca data (dari folder \data), melakukan sorting internal, mempersiapkan variabel, dsb.---
		self.isReady = True #Fungi setup(), jika dianggap sudah dijalankan dengan benar, harus diakhiri dengan baris ini
	#execute: fungsi untuk menjalankan penyuntingan. Fungsi ini harus ada (sudah terdefinisikan pada PySipebiAnalyzerBase)
	def execute(self, text): #harus ada, signature dari fungsi harus selalu seperti ini: def execute(self, text):
		self.varNo = self.varNo + 1 #contoh penggunaan variabel
		self.varStr = text #contoh penggunaan input/variabel
		#---text dapat diproses di sini untuk mendapatkan hasil diagnosis---
		#contoh penambahan hasil diagnosis dapat dilihat di bawah
		#elemen PySipebiDiagnosticsError dalam contoh di bawah tidak lengkap, hanya diperuntukkan sebagai contoh, silakan dilengkapi
		hasilDiagnosis = PySipebiDiagnosticsError()
		hasilDiagnosis.ErrorCode = '[Kode Contoh A]'
		hasilDiagnosis.OriginalElement = 'contoh-' + str(self.varNo)
		hasilDiagnosis.CorrectedElement = 'contoh-' + str(self.varNo) + 'A'
		hasilDiagnosis.IsAmbiguous = True
		self.diagList.append(hasilDiagnosis)
		hasilDiagnosis = PySipebiDiagnosticsError()
		hasilDiagnosis.ErrorCode = '[Kode Contoh B]'
		hasilDiagnosis.OriginalElement = 'contoh-'+ str(self.varNo)
		hasilDiagnosis.CorrectedElement = 'contoh-' + str(self.varNo) + 'B'
		hasilDiagnosis.IsAmbiguous = True
		self.diagList.append(hasilDiagnosis)
		if len(self.diagList) > 10:
			self.diagList.pop(1)
			self.diagList.pop(0)
