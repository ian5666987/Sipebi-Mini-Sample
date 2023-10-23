# Core Dari Diagnosis

## PySipebiDiagnosticsError.py
Fail ini berisi hanya satu buah *class* yang bernama `PySipebiDiagnosticsError`, dimana *class* tersebut merupakan representasi dari sebuah kesalahan diagnosis. Misalnya, sebuah teks dengan isi
```
kamu adalah aku. Benar kah itu?
```
memiliki 2 buah kesalahan diagnosis yang masing-masing kesalahan diagnosis itu akan dibungkus dalam satu objek `PySipebiDiagnosticError`, yaitu:
1. Kesalahan pada kata **"kamu"** pada paragraf pertama, kata pertama. Kata **"kamu"** harusnya ditulis dengan huruf kapital, yaitu **"Kamu"** karena berada pada awal kalimat.\
Objek `PySipebiDiagnosticError`-nya akan berisi.
```
ErrorCode: [HF01]
ParagraphNo = 1
ElementNo = 1
OriginalElement = kamu
CorrectedElement = Kamu
OriginalParagraphOffset = 1
PositionOffset = 1
CorrectedCharPosition = 0
IsAmbiguous = False
```
`ErrorCode` **HF01** merupakan kode aturan ejaan kapitalisasi pada awal kalimat sesuai dengan Google Sheets EYD Analyzer. Karena kata **"kamu"** berada pada kata pertama pada paragraf pertama, maka `ParagraphNo` dan `ElementNo` bernilai 1. `IsAmbigous` berisi elemen **True/False** tergantung ambiguitas apakah `CorrectedElement` harus menggantikan `OriginalElement` atau tidak. Karena pada kasus ini, tidak ada ambiguitas, maka `IsAmbiguous` bernilai False.

2. Kesalahan pada kata **"Benar kah"** pada kata keempat paragraf pertama. Kata **"Benar kah"** harusnya ditulis dengan cara digabung, yaitu **"Benarkah"** karena partikel lah, kah, dan tah seharusnya digabung dengan kata sebelumnya.\
Objek `PySipebiDiagnosticError`-nya akan berisi.
```
ErrorCode: [KE01]
ParagraphNo = 1
ElementNo = 4
OriginalElement = Benar kah
CorrectedElement = Benarkah
OriginalParagraphOffset = 1
PositionOffset = 1
CorrectedCharPosition = 0
IsAmbiguous = False
```

## PySipebiDiagnosticsBase.py

Fail ini berisi hanya satu buah *class* yang bernama `PySipebiDiagnosticsBase`, dimana *class* tersebut merupakan sebuah *class* dasar yang harus di-*extends* oleh semua *class* diagnosis yang akan dibuat.\
*Class* ini memiliki beberapa atribut, di antaranya:
### 1. `diagList`
Daftar dari semua kesalahan diagnosis pada sebuah teks untuk satu spesifik *class* diagnosisnya. Satu kesalahan diagnosis direpresentasikan sebagai objek dari *class* `PySipebiDiagnosticsError`.\
Contoh: Pada teks 
```
aku akan pergi. kamu juga boleh pergi
```
terdapat 2 aturan ejaan yang tidak sesuai dengan aturan kapitalisasi pada awal kalimat, yaitu   `aku -> Aku` dan `kamu -> Kamu`. *Class* diagnosis yang mengatur aturan ejaan kapitalisasi pada awal kalimat yang sudah melakukan *extends* dari class `PySipebiDiagnosticsBase` pasti akan memiliki atribut - atribut *parent*-nya. Salah satunya adalah `diagList`. Jika kode diagnosis kesalahan berjalan sesuai fungsi awalnya dan efektif, maka `diagList` akan berisi 2 buah elemen objek dari `PySipebiDiagnosticsError`, dimana elemen pertamanya merepresentasikan kesalahan pada kata **"aku"** dan elemen keduanya merepresentasikan kesalahan pada kata **"kamu"**.

### 2. `isReady`
Bendera yang menandakan apakah *class* diagnosis sudah siap untuk melakukan diagnosis atau belum. Jika `isReady` bernilai `False`, maka *class* diagnosis tidak akan melakukan diagnosis. Jika `isReady` bernilai `True`, maka *class* diagnosis akan melakukan diagnosis.\

### 3. `isCompleted`
Bendera yang menandakan diagnosis telah selesai dilakukan atau belum. Jika `isCompleted` bernilai `False`, maka diagnosis belum selesai dilakukan. Jika `isCompleted` bernilai `True`, maka diagnosis telah selesai dilakukan.\

### 4. `hasSharedResources`
Bendera yang menandakan apakah *class* diagnosis akan membuat atau membutuhkan sumber daya bersama atau tidak. Jika `hasSharedResources` bernilai `False`, maka *class* diagnosis tidak akan membuat dan membutuhkan sumber daya bersama. Jika `hasSharedResources` bernilai `True`, maka *class* diagnosis akan membuat dan membutuhkan sumber daya bersama.\

### 5. `sharedResourcesInputKeys`
Daftar *key* input yang dibutuhkan oleh *class* diagnosis untuk membuat sumber daya bersama. Isi dari list ini akan diinput ke dalam key dictionary yang menjadi parameter yang bernama `input_resources` pada fungsi `create_shared_resources`. Jika menginput key pada `sharedResourcesInputKeys`, pastikan menjalankan fungsi `create_shared_resources`.\

### 6. `sharedResourcesOutputKeys`
Daftar *key* output yang akan dipakai *class* diagnosis terkait setelah. Isi dari list ini akan menjadi key pada variabel dictionary `shared_resources` yang merupakan parameter dari fungsi `executed_with_shared_resources`. Jika menginput key pada `sharedResourcesOutputKeys`, pastikan menjalankan fungsi `executed_with_shared_resources` dan memakai dictionary `shared_resources` sebagai sumber daya bersama yang sudah dibuat sebelumnya.\ 

### 7. `fileResourceNames`
Daftar nama file resource yang terdapat pada folder `py\diag\data` yang diperlukan untuk menjalankan skrip diagnosis dengan benar. Untuk membaca fail, panggil fungsi `read_file` dengan parameter `file_name` yang merupakan nama file resource yang terdapat pada folder `py\diag\data` dan parameter `shared_resources` yang merupakan sumber daya yang dibagikan bersama.\

Selain itu, class ini juga memiliki beberarapa method atau fungsi, di antaranya:
### 1. `setup()`
Fungsi untuk melakukan pengaturan awal satu kali saja sebelum `execute` atau `execute_with_shared_resources` dijalankan berulang kali. Fungsi ini harus di-override jika terdapat persiapan awal satu kali (one-time setup) untuk diagnosis terkait.

### 2. `pre_execute()`
Fungsi untuk melakukan persiapan sebelum `execute` atau `execute_with_shared_resources` dijalankan. Defaultnya adalah mereset bendera `isCompleted` menjadi `False` dan mengosongkan daftar kesalahan diagnosis `diagList`.

### 3. `execute(text)`
>`text: string` = Teks yang akan didiagnosis.

Fungsi untuk melakukan diagnosis pada teks yang diberikan. Fungsi ini dijalankan ketika tidak ada sumber daya bersama yang dibagikan. Fungsi ini harus di-override jika tidak menjalankan fungsi `execute_with_shared_resources`.

### 4. `post_execute()`
Fungsi yang dijalankan setelah `execute` atau `execute_with_shared_resources` dijalankan. Override fungsi ini jika diperlukan

### 5. `require_shared_resources()`
Fungsi untuk mengindikasikan apakah kelas diagnosis terkait harus dijalankan menggunakan fungsi `execute_with_shared_resources` atau dapat dijalankan menggunakan fungsi `execute` saja jika `shared_resources` tidak secara lengkap berhasil ditemukan.

### 6. `create_shared_resources(text, input_resources)`
> `text: string` = Teks yang akan didiagnosis.\
> `input_resources: dict(key:string, value:object)` = Daftar key dari sumber daya bersama akan dibuat. Isi keynya sama dengan isi atribut [sharedResourcesInputKeys](#5-sharedresourcesinputkeys). Dictionary ini boleh kosong.

Fungsi untuk membuat sumber daya baru jika ada. Fungsi ini akan mengembalikan dictionary yang berisi sumber daya bersama yang baru dibuat.

>`output_resources: dict(key:string, value:object)` = Daftar key dari sumber daya bersama yang baru dibuat beserta valuenya. Dictionary tidak boleh kosong.

### 7. execute_with_shared_resources(text, shared_resources)
> `text: string` = Teks yang akan didiagnosis.\
> `shared_resources: dict(key:string, value:object)` = Daftar key dari sumber daya bersama yang akan digunakan. Isi keynya sama dengan isi atribut [sharedResourcesOutputKeys](#6-sharedresourcesoutputkeys).

Fungsi untuk melakukan diagnosis pada teks yang diberikan. Fungsi ini dijalankan ketika ada sumber daya bersama yang dipakai. Fungsi ini harus di-override jika tidak menjalankan fungsi `execute`.

### 8. `get_file_resource_key(file_resource_name)`
> `file_resource_name: string` = Nama file resource yang terdapat pada folder `py\diag\data`.

Fungsi untuk mendapatkan nama file resource key yang digunakan pada `shared_resources` pada waktu menjalankan fungsi `execute_with_shared_resources`.\
Contoh, jika `file_resource_name` bernilai `file1.txt`, maka `get_file_resource_key` akan mengembalikan nilai `diag\data\file1.txt`.

### 9. `read_file(file_name, shared_resources)`
> `file_name: string` = Nama file resource yang terdapat pada folder `py\diag\data`.\
> `shared_resources: dict(key:string, value:object)` = Daftar key dari sumber daya bersama yang akan digunakan. Isi keynya sama dengan isi atribut [sharedResourcesOutputKeys](#6-sharedresourcesoutputkeys).

Fungsi untuk membaca file resource yang terdapat pada folder `py\diag\data` yang telah disimpan sebagai salah satu *key-value pair* pada dictionary `shared_resources`. Fungsi ini akan mengembalikan isi file resource yang terdapat pada folder `py\diag\data` dalam bentuk string.\
Contoh, jika `file_name` bernilai `file1.txt` berisi:
```
ini paragraf 1
ini paragraf 2
```
maka `read_file(file1.txt, shared_resources)` akan mengembalikan string 
```
ini paragraf 1\r\niniparagraf2
```
Fungsi ini seharusnya dipanggil pada fungsi `execute_with_shared_resources` jika terdapat file resource yang perlu dibaca.
