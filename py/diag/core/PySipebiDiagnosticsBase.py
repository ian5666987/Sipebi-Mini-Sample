# kelas dasar Python bagi kelas-kelas penyuntingan lainnya
class PySipebiDiagnosticsBase:
	# diagList: daftar kesalahan. List ini harus ada
	diagList = []
	# isReady: bendera yang menandakan pengaturan awal sudah selesai dikerjakan. Bendera ini harus ada
	isReady = False
	# isCompleted: bendera yang menandakan diagnosis telah selesai dikerjakan dengan sempurna
	isCompleted = False
	# hasSharedResources: menandakan diagnosis ini memiliki shared resources
	hasSharedResources = False
	# sharedResourcesInputKeys: daftar key dari input_resources
	#   yang diperlukan untuk menjalankan create_shared_resources
	sharedResourcesInputKeys = []
	# sharedResourcesOutputKeys: daftar key yang, jika create_shared_resources berjalan dengan benar,
	#   akan dihasilkan (yaitu, output_resources) dari menjalankan create_shared_resources,
	#   yang juga merupakan keys yang dimiliki oleh shared_resources pada execute_with_shared_resources
	sharedResourcesOutputKeys = []
	# Catatan:
	# - Idealnya, sharedResourcesInputKeys dan sharedResourcesOutputKeys tidak dibuat beririsan

	# setup: fungsi untuk melakukan pengaturan awal sebelum 'execute' dijalankan
	# fungsi ini harus di-override jika terdapat persiapan awal satu kali (one-time setup) untuk diagnosis ini
	def setup(self):
		self.isReady = True

	# execute: fungsi untuk menjalankan penyuntingan tanpa input lain selain teks awal
	# fungsi ini harus di-override
	def execute(self, text):
		self.isCompleted = True

	# create_shared_resources: fungsi untuk mempersiapkan shared resources, jika ada
	# fungsi ini harus di-override jika hasSharedResources = True
	# input_resources adalah sebuah dictionary(string:object) yang boleh kosong
	#   string (keys) dari input_resources adalah sama dengan yang terdaftar pada sharedResourcesInputKeys
	def create_shared_resources(self, text, input_resources):
		# output_resources harus merupakan sebuah dictionary(string:object)
		# di dalam semua kelas yang diturunkan dari PySipebiDiagnosticsBase,
		#   output_resources TIDAK boleh kosong, tetapi harus menghasilkan
		#   dictionary dengan keys yang sama persis dengan
		#   yang didaftarkan pada sharedResourcesOutputKeys
		output_resources = {}
		return output_resources

	# execute_with_shared_resources: fungsi untuk menjalankan penyuntingan menggunakan
	#   resources yang terdaftar di sharedResourcesOutputKeys
	# fungsi ini harus di-override jika hasSharedResources = True
	# shared_resources adalah sebuah dictionary(string:object)
	#   string (keys) dari shared_resources adalah sama dengan yang terdaftar pada sharedResourcesOutputKeys
	def execute_with_shared_resources(self, text, shared_resources):
		self.isCompleted = True
