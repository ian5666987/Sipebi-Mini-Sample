#kelas dasar Python bagi kelas-kelas penyuntingan lainnya
class PySipebiDiagnosticsBase:
	diagList = [] #daftar kesalahan. List ini harus ada
	isReady = False #bendera yang menandakan pengaturan awal sudah selesai dikerjakan. Bendera ini harus ada
	#setup: fungsi untuk melakukan pengaturan awal sebelum 'execute' dijalankan. Fungsi ini harus ada
	def setup(self):
		self.isReady = True
	#execute: fungsi untuk menjalankan penyuntingan. Fungsi ini harus ada
	def execute(self, text):
		pass
