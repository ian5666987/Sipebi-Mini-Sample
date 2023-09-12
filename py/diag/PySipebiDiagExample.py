# baris-baris di bawah ini harus ada untuk mengimpor kelas-kelas inti Python
from core.PySipebiDiagnosticsError import PySipebiDiagnosticsError
from core.PySipebiDiagnosticsBase import PySipebiDiagnosticsBase

# setiap kelas inti Python harus diturunkan dari PySipebiDiagnosticsBase
class PySipebiDiagExample(PySipebiDiagnosticsBase):
	varNo = 0  # contoh angka
	varStr = 'sample text'  # contoh teks
	diagList = []  # daftar kesalahan. List ini harus ada (hanya contoh, dapat dihapus, sudah terdefinisikan pada PySipebiAnalyzerBase)
	isReady = False  # bendera yang menandakan pengaturan awal sudah selesai dikerjakan. Bendera ini harus ada (hanya contoh, dapat dihapus, sudah terdefinisikan pada PySipebiAnalyzerBase)
	hasSharedResources = True  # diagnosis ini memiliki shared resources
	sharedResourcesInputKeys = []  # tidak memerlukan input selain text untuk membuat shared resources
	sharedResourcesOutputKeys = ['DummySharedResource']  # contoh shared_resource yang akan dihasilkan eksekusi yang berantai

	# setup: fungsi untuk melakukan pengaturan awal sebelum 'execute' dijalankan. Fungsi ini harus ada (sudah terdefinisikan pada PySipebiAnalyzerBase)
	def setup(self):  # signature dari fungsi harus selalu seperti ini: setup(self):
		# ---lakukan pengaturan awal di sini---
		# ---mis: membaca data (dari folder \data), melakukan sorting internal, mempersiapkan variabel, dsb.---
		self.isReady = True  # Fungi setup(), jika dianggap sudah dijalankan dengan benar, harus diakhiri dengan baris ini

	# execute: fungsi untuk menjalankan penyuntingan. Fungsi ini harus ada (sudah terdefinisikan pada PySipebiAnalyzerBase)
	def execute(self, text):  # harus ada, signature dari fungsi harus selalu seperti ini: def execute(self, text):
		self.varNo = self.varNo + 1  # contoh penggunaan variabel
		self.varStr = text  # contoh penggunaan input/variabel
		# ---text dapat diproses di sini untuk mendapatkan hasil diagnosis---
		# contoh penambahan hasil diagnosis dapat dilihat di bawah
		# elemen PySipebiDiagnosticsError dalam contoh di bawah tidak lengkap, hanya diperuntukkan sebagai contoh, silakan dilengkapi
		self.run_common_diagnostics()
		self.isCompleted = True  # Bendera ini harus diset jika eksekusi berjalan dengan sempurna

	# create_shared_resources: fungsi untuk mempersiapkan shared resources, jika ada
	# fungsi ini harus di-override jika hasSharedResources = True
	# input_resources adalah sebuah dictionary(string:object) yang boleh kosong
	#   string (keys) dari input_resources adalah sama dengan yang terdaftar pada sharedResourcesInputKeys
	def create_shared_resources(self, text, input_resources):
		output_resources = {}
		dummy_object = None
		output_resources['DummySharedResource'] = dummy_object
		return output_resources

	# execute_with_shared_resources: fungsi untuk menjalankan penyuntingan menggunakan
	#   resources yang terdaftar di sharedResourcesOutputKeys
	# fungsi ini harus di-override jika hasSharedResources = True
	# shared_resources adalah sebuah dictionary(string:object)
	#   string (keys) dari shared_resources adalah sama dengan yang terdaftar pada sharedResourcesOutputKeys
	def execute_with_shared_resources(self, text, shared_resources):
		self.isCompleted = False  # bendera ini harus selalu direset sebelum eksekusi
		self.diagList = []  # kosongkan daftar kesalahan sebelum script dijalankan ulang
		self.varNo = self.varNo + 1  # contoh penggunaan variabel
		self.varStr = text  # contoh penggunaan input/variabel
		self.run_common_diagnostics()
		if type(shared_resources is dict) and ('DummySharedResource' in shared_resources.keys()):
			hasil_diagnosis = PySipebiDiagnosticsError()
			hasil_diagnosis.ErrorCode = '[Kode Contoh A]'
			hasil_diagnosis.OriginalElement = 'sr-contoh-' + str(self.varNo)
			hasil_diagnosis.CorrectedElement = 'sr-contoh-' + str(self.varNo) + 'A'
			hasil_diagnosis.IsAmbiguous = True
			self.diagList.append(hasil_diagnosis)
			if len(self.diagList) > 10:
				self.diagList.pop(0)
		self.isCompleted = True  # Bendera ini harus diset jika eksekusi berjalan dengan sempurna

	# run_diagnostics: tambahan fungsi khusus skrip diagnosis ini
	#   kode fungsi ini dapat pula langsung diletakkan di dalam execute dan/atau execute_with_shared_resources
	def run_common_diagnostics(self):
		hasil_diagnosis = PySipebiDiagnosticsError()
		hasil_diagnosis.ErrorCode = '[Kode Contoh A]'
		hasil_diagnosis.OriginalElement = 'contoh-' + str(self.varNo)
		hasil_diagnosis.CorrectedElement = 'contoh-' + str(self.varNo) + 'A'
		hasil_diagnosis.IsAmbiguous = True
		self.diagList.append(hasil_diagnosis)
		hasil_diagnosis = PySipebiDiagnosticsError()
		hasil_diagnosis.ErrorCode = '[Kode Contoh B]'
		hasil_diagnosis.OriginalElement = 'contoh-' + str(self.varNo)
		hasil_diagnosis.CorrectedElement = 'contoh-' + str(self.varNo) + 'B'
		hasil_diagnosis.IsAmbiguous = True
		self.diagList.append(hasil_diagnosis)
		if len(self.diagList) > 10:
			self.diagList.pop(1)
			self.diagList.pop(0)
