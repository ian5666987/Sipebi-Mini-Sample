# kelas dasar Python bagi kelas-kelas penyuntingan lainnya
class PySipebiDiagnosticsBase:
	# diagList: daftar kesalahan. List ini harus ada
	diagList = []
	# isReady: bendera yang menandakan pengaturan awal sudah selesai dikerjakan. Bendera ini harus ada
	isReady = False
	# isCompleted: bendera yang menandakan diagnosis telah selesai dikerjakan dengan sempurna
	isCompleted = False
	# hasSharedResources: menandakan diagnosis ini membutuhkan shared resources atau file resources
	hasSharedResources = False
	# sharedResourcesInputKeys: daftar key dari input_resources
	#   yang diperlukan untuk menjalankan create_shared_resources
	sharedResourcesInputKeys = []
	# sharedResourcesOutputKeys: daftar key yang, jika create_shared_resources berjalan dengan benar,
	#   akan dihasilkan (yaitu, output_resources) dari menjalankan create_shared_resources,
	#   yang juga merupakan keys yang dimiliki oleh shared_resources pada execute_with_shared_resources
	# Catatan:
	# - Idealnya, sharedResourcesInputKeys dan sharedResourcesOutputKeys tidak dibuat beririsan
	sharedResourcesOutputKeys = []
	# fileResourceNames: daftar nama file resource yang terdapat pada folder py\diag\resources
	#   yang diperlukan untuk menjalankan skrip diagnosis dengan benar
	fileResourceNames = []

	# setup: fungsi untuk melakukan pengaturan awal satu kali saja sebelum 'execute' dijalankan berulang kali
	# fungsi ini harus di-override jika terdapat persiapan awal satu kali (one-time setup) untuk diagnosis ini
	def setup(self):
		self.isReady = True

	# pre_execute: fungsi yang akan secara otomatis dijalankan sebelum fungsi execute dijalankan
	# override fungsi ini jika diperlukan
	def pre_execute(self):
		self.isCompleted = False  # bendera ini harus selalu direset sebelum eksekusi
		self.diagList = []  # kosongkan daftar kesalahan sebelum script dijalankan ulang

	# execute: fungsi untuk menjalankan penyuntingan tanpa input lain selain teks awal
	# fungsi ini harus di-override
	def execute(self, text):
		self.isCompleted = True

	# post_execute: fungsi yang akan secara otomatis dijalankan setelah fungsi execute selesai dijalankan
	# override fungsi ini jika diperlukan
	def post_execute(self):
		pass

	# require_shared_resources: fungsi untuk mengindikasikan apakah fungsi ini harus dijalankan menggunakan
	#   execute_with_shared_resources atau dapat dijalankan menggunakan execute saja jika shared_resources
	#   tidak secara lengkap berhasil ditemukan
	# override fungsi ini jika diperlukan
	def require_shared_resources(self):
		return False

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

	# get_file_resource_key: fungsi untuk mendapatkan nama file resource key yang digunakan pada shared_resources
	#   pada waktu menjalankan execute_with_shared_resources
	def get_file_resource_key(self, file_resource_name):
		return "diag\\data\\" + file_resource_name

	# open_file: fungsi untuk mendapatkan file yang sudah terlebih dahulu didaftarkan pada fileResourceNames
	#   fungsi ini memerlukan input berupa shared_resources
	#   dengan demikian, fungsi ini hanya dapat berjalan dengan jika dipanggil di dalam fungsi execute_with_shared_resources
	# catatan: saat ini encoding yang digunakan untuk semua file resources adalah 'UTF-8'
	def open_file(self, file_name, shared_resources):
		# contoh cara mendapatkan file resource key bagi skrip diagnosis
		file_resource_key = self.get_file_resource_key(file_name)
		# contoh cara mengecek apakah file resource key ditemukan pada shared_resources
		if (file_resource_key in shared_resources.keys()):
			# contoh cara mendapatkan teks pada file resource menggunakan file resource key
			return shared_resources[file_resource_key]
		return ''  # jika file yang diminta tidak berhasil ditemukan pada shared_resources, maka yang dikembalikan berupa string kosong