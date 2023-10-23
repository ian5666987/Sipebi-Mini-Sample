# Core Dari Diagnosis

># PySipebiDiagnosticsError.py
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

># PySipebiDiagnosticsBase.py

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

# PySipebiStructs.py

Fail ini berisi beberapa *class* yang akan menjadi struktur data utama untuk membantu proses diagnosis. *Class* yang terdapat pada fail ini adalah:

## 1. PySipebiTextDivision
*Class* ini menjadi struktur data utama yang merepresentasikan sebuah teks utuh. *Class* ini memiliki beberapa atribut, di antaranya:
> - `text: string` = Teks utuh yang akan didiagnosis.
> - `length: int` = Banyak karakter pada teks.
> - `paragraph_divs: PySipebiParagraphDivision` = Daftar paragraf yang terdapat pada teks. Masing-masing elemen pada list ini direpresentasikan oleh objek dari class `PySipebiParagraphDivision`.

*Class* ini juga memiliki beberapa method atau fungsi, di antaranya:
### 1. `add_paragraph_division(paragraph_division)`
> - `paragraph_division: PySipebiParagraphDivision` = Objek       `PySipebiParagraphDivision` yang akan ditambahkan ke dalam list `paragraph_divs`.

Fungsi untuk menambahkan objek `PySipebiParagraphDivision` ke dalam list `paragraph_divs`.

### 2. `separate_paragraph_by_line_break()`
Fungsi untuk memisahkan teks menjadi beberapa paragraf jika terdapat karakter line break (`\n`) pada paragraf tersebut. Fungsi ini juga akan memanggil fungsi `add_paragraph_division` untuk menambahkan setiap paragraf baru yang terbentuk.

### 3. `process_paragraph_divisions()`
Fungsi untuk melakukan tokenisasi kata untuk setiap paragraf yang ada pada list `paragraph_divs`. Fungsi ini akan memanggil fungsi `tokenize_words` yang ada pada class `PySipebiParagraphDivision` untuk setiap paragraf yang ada pada list `paragraph_divs`.

### 4. `process_text()`
Fungsi untuk membuat struktur data teks, termasuk tokenisasi kata. Fungsi ini memanggil fungsi `separate_paragraph_by_line_break` dan `process_paragraph_divisions`. Fungsi ini dipanggil pada saat pembuatan objek `PySipebiTextDivision`.

## 2. PySipebiParagraphDivision
*Class* ini menjadi struktur data utama yang merepresentasikan sebuah paragraf. *Class* ini merupakan sebuah struktur data *doubly linked list*, dimana *node*-nya adalah setiap kata yang ada pada paragraf. *Class* ini memiliki beberapa atribut, di antaranya:
> - `text: string` = Teks paragraf yang akan didiagnosis.
> - `length: int` = Banyak karakter pada paragraf.
> - `index: int` = Indeks paragraf pada teks utuh. Paragraf pertama pada teks memiliki index 1
> -`offset: int` = Offset paragraf pada teks utuh. Offset paragraf pertama pada teks adalah 0.
> - `word_divs: PySipebiWordDivision` = Daftar kata yang terdapat pada paragraf. Masing-masing elemen pada list ini direpresentasikan oleh objek dari class `PySipebiWordDivision`.
> - `size: int` = Banyak kata yang terdapat pada paragraf.

*Class* ini juga memiliki beberapa method atau fungsi, di antaranya:

### 1. `add_word_division(word_division)`
> - `word_division: PySipebiWordDivision` = Objek `PySipebiWordDivision` yang akan ditambahkan ke dalam list `word_divs`.

Fungsi untuk menambahkan objek `PySipebiWordDivision` ke dalam list `word_divs`.

### 2. `tokenize_words()`
Fungsi untuk melakukan tokenisasi kata pada paragraf berdasarkan *whitespace*. Fungsi ini akan memanggil fungsi `add_word_division` untuk setiap kata yang terbentuk. Fungsi ini juga melakukan konfigurasi *next word* dan *previous word* pada  setiap kata yang terbentuk. Lihat implementasi fungsi untuk lebih jelasnya.

## 3. PySipebiWordDivision
*Class* yang menjadi struktur data utama yang merepresentasikan sebuah kata. Setiap objek dari *class* ini merupakan sebuah *node* dari struktur data *doubly linked list* yang direpresentasikan oleh `PySipebiParagraphDivision`. *Class* ini memiliki beberapa atribut, di antaranya:

> - `original_string: string` = Kata asli dengan tanda baca yang menyatu dengan kata dan tanpa modifikasi.
> - `element_no: int` = Nomor urut kata pada paragraf. Kata pertama pada paragraf memiliki element_no 1.
> - `position_offset: int` = Offset posisi kata pada paragraf. Offset kata pertama pada paragraf adalah 0.
> - `clean_word_string: string` = Kata asli tanpa tanda baca.
> - `pre_word: PySipebiPreWordPunctuation` = Objek `PySipebiPreWordPunctuation` yang merepresentasikan tanda baca sebelum kata.
> - `post_word: PySipebiPostWordPunctuation` = Objek `PySipebiPostWordPunctuation` yang merepresentasikan tanda baca setelah kata.
> - `is_handled: bool` = Bendera yang menandakan apakah kata sudah ditangani atau belum.
> - `next_word_div: PySipebiWordDivision` = Objek `PySipebiWordDivision` yang merepresentasikan kata selanjutnya pada paragraf berdasarkan objek `PySipebiWordDivision` yang sekarang.
> - `prev_word_div: PySipebiWordDivision` = Objek `PySipebiWordDivision` yang merepresentasikan kata sebelumnya pada paragraf berdasarkan objek `PySipebiWordDivision` yang sekarang.

Konstruktor dari *class* ini menerima 3 parameter, yaitu:
> - `element_no: int` = Nomor urut kata pada paragraf. Kata pertama pada paragraf memiliki element_no 1.
> - `original_string: string` = Kata asli
> - `offset: int` = Offset posisi kata pada paragraf. Offset kata pertama pada paragraf adalah 0.

*Class* ini juga memiliki beberapa method atau fungsi, di antaranya:

### 1. `_check_pre_word()`
Fungsi privat yang melakukan looping untuk `string` kata original, lalu menginput semua tanda baca sebelum kata ke dalam atribut `pre_word`. Setelah itu, atribut `clean_word_string` akan menjadi `string` kata, tanpa tanda baca sebelum kata tersebut.

### 2. `_check_post_word()`
Fungsi privat yang melakukan looping untuk `string` kata original, lalu menginput semua tanda baca sesudah kata ke dalam atribut `post_word`. Setelah itu, atribut `clean_word_string` akan menjadi `string` kata, tanpa tanda baca sesudah kata tersebut.

### 3. `process_word()`
Fungsi yang memanggil fungsi privat `_check_pre_word` dan fungsi privat `_check_post_word` untuk melakukan pemrosesan kata. Fungsi ini dipanggil ketika objek `PySipebiWordDivsision` dibuat.

### 4. `ended_with(character)`
> - `substring: string` = Substring yang akan dicek apakah kata berakhir dengan substring tersebut atau tidak.

Fungsi untuk mengecek apakah kata berakhir dengan substring yang diberikan atau tidak. Fungsi ini mengembalikan nilai `True` jika kata berakhir dengan substring yang diberikan dan mengembalikan nilai `False` jika kata tidak berakhir dengan substring yang diberikan.

### 5. `start_with(character)`
> - `substring: string` = Substring yang akan dicek apakah kata dimulai dengan substring tersebut atau tidak.

Fungsi untuk mengecek apakah kata dimulai dengan substring yang diberikan atau tidak. Fungsi ini mengembalikan nilai `True` jika kata dimulai dengan substring yang diberikan dan mengembalikan nilai `False` jika kata tidak dimulai dengan substring yang diberikan.

*Class* ini memiliki beberapa method spesial yang bertindak sebagai *getter*. Method-method tersebut ditandai dengan adanya *built-in decorator* `@property` di awal method. Pemanggilan method ini sama seperti pemanggilan atribut, yaitu tidak disertai tanda kurung. Misalnya, jika method bernama `has_pre_word`, maka pemanggilan method tersebut dilakukan dengan cara `obj.has_pre_word`. Method-method tersebut, di antaranya:

### 1. `has_pre_word`
Getter untuk mengecek apakah kata memiliki tanda baca sebelumnya atau tidak. Fungsi ini mengembalikan nilai `True` jika kata memiliki tanda baca sebelumnya dan mengembalikan nilai `False` jika kata tidak memiliki tanda baca sebelumnya.

### 2. `has_post_word`
Getter untuk mengecek apakah kata memiliki tanda baca setelahnya atau tidak. Fungsi ini mengembalikan nilai `True` jika kata memiliki tanda baca setelahnya dan mengembalikan nilai `False` jika kata tidak memiliki tanda baca setelahnya.

### 3. `pre_clean_word`
Getter untuk mendapatkan kata asli dengan tanda baca sebelumnya, tetapi tidak disertai dengan tanda baca setelahnya. Fungsi ini mengembalikan nilai `string` yang merupakan kata asli dengan tanda baca sebelumnya, tetapi tidak disertai dengan tanda baca setelahnya.

### 4. `clean_post_word`
Getter untuk mendapatkan kata asli dengan tanda baca setelahnya, tetapi tidak disertai dengan tanda baca sebelumnya. Fungsi ini mengembalikan nilai `string` yang merupakan kata asli dengan tanda baca setelahnya, tetapi tidak disertai dengan tanda baca sebelumnya.

### 4. `first_char_is_letter`
Getter untuk mengecek apakah karakter pertama dari kata merupakan huruf atau bukan. Fungsi ini mengembalikan nilai `True` jika karakter pertama dari kata merupakan huruf dan mengembalikan nilai `False` jika karakter pertama dari kata bukan merupakan huruf.

### 5. `first_char_is_capitalized`
Getter untuk mengecek apakah karakter pertama dari kata merupakan huruf kapital atau bukan. Fungsi ini mengembalikan nilai `True` jika karakter pertama dari kata merupakan huruf kapital dan mengembalikan nilai `False` jika karakter pertama dari kata bukan merupakan huruf kapital.

### 6. `only_has_post_word`
Getter untuk mengecek apakah kata hanya memiliki tanda baca setelahnya atau tidak. Fungsi ini mengembalikan nilai `True` jika kata hanya memiliki tanda baca setelahnya dan mengembalikan nilai `False` jika kata memiliki tanda baca sebelumnya atau tidak memiliki tanda baca sama sekali.

### 7. `is_null_or_empty`
Getter untuk mengecek apakah kata merupakan kata kosong atau tidak. Fungsi ini mengembalikan nilai `True` jika kata merupakan kata kosong dan mengembalikan nilai `False` jika kata bukan merupakan kata kosong.

Misalnya, kita ingin membuat sebuah objek `PySipebiWordDivision` dari kata `(aku,` yang berada pada indeks ke-1 pada paragraf pertama dan position offset 5. Maka, kita dapat membuat objek `PySipebiWordDivision` dengan cara:
```
word_div = PySipebiWordDivision(1, "(aku,", 5)
```
Setelah penginstansiasian objek `PySipebiWordDivision` tersebut, maka method `process_word` akan dipanggil di dalam konstruktornya. Setelah selesai, maka akan terbentuk sebuah objek `PySipebiWordDivision` dengan atribut-atributnya sebagai berikut:
```python
word_div.original_string = "(aku,"
word_div.element_no = 1
word_div.position_offset = 5
word_div.clean_word_string = "aku"
word_div.pre_word = PySipebiPreWordPunctuation("(")
word_div.post_word = PySipebiPostWordPunctuation(",")
word_div.is_handled = False
word_div.next_word_div = None
word_div.prev_word_div = None
```

## 4. PySipebiPunctuationDivision
Base *class* yang menjadi struktur data utama yang merepresentasikan sebuah tanda baca. *Class* ini memiliki beberapa atribut dan konstanta, di antaranya:

> - `PRE_CHARS_OMITTED: list(string)` = Kumpulan konstanta tanda baca yang ada sebelum sebuah kata yang sudah disepakati
> - `POST_CHARS_OMITTED: list(string)` = Kumpulan konstanta tanda baca yang ada setelah sebuah kata yang sudah disepakati
> - `punctuation_div: list(string)` = Daftar tanda baca yang ada pada sebuah kata.

*Class* ini memiliki konstruktor yang tidak menerima parameter apapun.

*Class* ini juga memiliki beberapa method atau fungsi, di antaranya:

### 1. `add_punctuation_division(char)`
> - `char: string` = Tanda baca yang akan ditambahkan ke dalam list `punctuation_div`.

Fungsi untuk menambahkan tanda baca ke dalam list `punctuation_div`.

### 2. `contains(character)`
> - `character: string` = Tanda baca yang akan dicek apakah ada pada list `punctuation_div`.

Fungsi untuk mengecek apakah tanda baca yang diberikan ada pada list `punctuation_div`. Fungsi ini mengembalikan nilai `True` jika tanda baca yang diberikan ada pada list `punctuation_div` dan mengembalikan nilai `False` jika tanda baca yang diberikan tidak ada pada list `punctuation_div`.

### 3. `ended_with(character)`
> - `character: string` = Karakter tanda baca yang akan dicek apakah keseluruhan tanda baca berakhir dengan karakter tanda baca tersebut atau tidak.

Fungsi untuk mengecek apakah keseluruhan tanda baca berakhir dengan karakter tanda baca yang diberikan atau tidak. Fungsi ini mengembalikan nilai `True` jika keseluruhan tanda baca berakhir dengan karakter tanda baca yang diberikan dan mengembalikan nilai `False` jika keseluruhan tanda baca tidak berakhir dengan karakter tanda baca yang diberikan.

### 4. `start_with(character)`
> - `character: string` = Karakter tanda baca yang akan dicek apakah keseluruhan tanda baca dimulai dengan karakter tanda baca tersebut atau tidak.

Fungsi untuk mengecek apakah keseluruhan tanda baca dimulai dengan karakter tanda baca yang diberikan atau tidak. Fungsi ini mengembalikan nilai `True` jika keseluruhan tanda baca dimulai dengan karakter tanda baca yang diberikan dan mengembalikan nilai `False` jika keseluruhan tanda baca tidak dimulai dengan karakter tanda baca yang diberikan.

### 5. `index(character)`
> - `character: string` = Karakter tanda baca yang akan dicari indeksnya pada list `punctuation_div`.

Fungsi untuk mencari indeks karakter tanda baca yang diberikan pada list `punctuation_div`. Fungsi ini mengembalikan nilai indeks karakter tanda baca yang diberikan pada list `punctuation_div` jika karakter tanda baca yang diberikan ada pada list `punctuation_div` dan mengembalikan nilai `-1` jika karakter tanda baca yang diberikan tidak ada pada list `punctuation_div`.

Selain itu, *class* ini juga memiliki beberapa method spesial yang bertindak sebagai *getter*. Method-method tersebut ditandai dengan adanya *built-in decorator* `@property` di awal method. Method-method tersebut, di antaranya:

### 1. `string_repr`
Getter untuk mendapatkan representasi string dari list `punctuation_div`. Fungsi ini mengembalikan nilai `string` yang merupakan representasi string dari list `punctuation_div`.

### 2. `length`
Getter untuk mendapatkan panjang list `punctuation_div`. Fungsi ini mengembalikan nilai `int` yang merupakan panjang list `punctuation_div` atau bisa dikatakan sebagai jumlah karakter tanda baca yang ada.

### 3. `last_punctuation`
Getter untuk mendapatkan karakter tanda baca terakhir dari list `punctuation_div`. Fungsi ini mengembalikan nilai `string` yang merupakan karakter tanda baca terakhir dari list `punctuation_div`.

### 4. `first_punctuation`
Getter untuk mendapatkan karakter tanda baca pertama dari list `punctuation_div`. Fungsi ini mengembalikan nilai `string` yang merupakan karakter tanda baca pertama dari list `punctuation_div`.

### 5. `has_punctuation_div`
Getter untuk mengecek apakah list `punctuation_div` memiliki karakter tanda baca atau tidak. Fungsi ini mengembalikan nilai `True` jika list `punctuation_div` memiliki karakter tanda baca dan mengembalikan nilai `False` jika list `punctuation_div` tidak memiliki karakter tanda baca.


## 5. PySipebiPreWordPunctuation
*Class* yang menjadi struktur data utama yang merepresentasikan tanda baca sebelum sebuah kata. *Class* ini merupakan *child class* dari `PySipebiPunctuationDivision`. *Class* ini belum memiliki atribut dan method tambahan.

## 6. PySipebiPostWordPunctuation
*Class* yang menjadi struktur data utama yang merepresentasikan tanda baca setelah sebuah kata. *Class* ini merupakan *child class* dari `PySipebiPunctuationDivision`. *Class* ini melakukan *override* method `add_punctuation_division` dari *parent class*-nya. 

## 7. PySipebiNumericDivision
*Class* yang menjadi struktur data utama yang merepresentasikan sebuah angka. *Class* ini belum diimplementasikan.


# Contoh
Berikut merupakan contoh dari penggunaan satu kesatuan struktur data yang ada pada fail `PySipebiStructs.py` untuk merepresentasikan sebuah teks utuh beserta komponen-konmponen teks tersebut.

Misalnya, kita memiliki teks berikut:
```
aku akan pergi. kamu juga boleh pergi
ibu berkata, "kamu boleh pergi!"
```
Maka, kita dapat membuat sebuah objek `PySipebiTextDivision` dengan cara:
```python
text_div = PySipebiTextDivision(text='aku akan pergi. kamu juga boleh pergi\nibu berkata, "kamu boleh pergi!"')
```
Setelah dilakukan pemrosesan teks dan tokenisasi kata, maka akan terbentuk sebuah objek `PySipebiTextDivision` dengan atribut-atributnya sebagai berikut:
```python 
text_div.text = 'aku akan pergi. kamu juga boleh pergi\nibu berkata, "kamu boleh pergi!"'
text_div.length = 74
text_div.paragraph_divs = [
    PySipebiParagraphDivision(index=1, offset=0, 'aku akan pergi. kamu juga boleh pergi', length=36),
    PySipebiParagraphDivision(index=2, offset=38, 'ibu berkata, "kamu boleh pergi!"', length=36)
]
```
Mari kita tinjau objek `PySipebiParagraphDivision` untuk paragraf kedua.

Objek tersebut memiliki atribut-atribut sebagai berikut:
```python
paragraph_div.index = 2
paragraph_div.offset = 38
paragraph_div.text = 'ibu berkata, "kamu boleh pergi!"'
paragraph_div.length = 36
paragraph_div.word_divs = [...PySipebiWordDivision...]
paragraph_div.size = 5
```

Mari kita tinjau objek `PySipebiWordDivision` untuk kata terakhir pada paragraf kedua, yaitu `pergi!"`.

Objek tersebut memiliki atribut-atribut sebagai berikut:
```python
word_div.original_string = 'pergi!"'
word_div.element_no = 5
word_div.position_offset = 32
word_div.clean_word_string = 'pergi'
word_div.pre_word = PySipebiPreWordPunctuation()
word_div.post_word = PySipebiPostWordPunctuation()
word_div.is_handled = False
word_div.next_word_div = None
word_div.prev_word_div = PySipebiWordDivision("boleh")
```

Mari kita tinjau objek `PySipebiPreWordPunctuation` untuk kata terakhir pada paragraf kedua, yaitu `pergi!"`.

Karena kata tersebut tidak memiliki tanda baca sebelumnya, maka objek tersebut tidak memiliki atribut apapun.

```python
pre_word_punctuation.punctuation_div = []
```

Mari kita tinjau objek `PySipebiPostWordPunctuation` untuk kata terakhir pada paragraf kedua, yaitu `pergi!"`.

Objek tersebut memiliki atribut-atribut sebagai berikut:
```python
post_word_punctuation.punctuation_div = ['!','"']
```

Misalkan, kita ingin mengecek apakah sebuah objek dari `PySipebiWordDivision` diakhiri dengan tanda baca petik dua (`"`). Maka, kita dapat menggunakan method `ended_with` dari objek `pre_word` dari kata tersebut dengan cara:
```python
pre_word: PySipebiPreWordPunctuation = word_div.pre_word
if pre_word.ended_with('"'):
    # do something
```

Misalkan, kita ingin mengecek apakah kata selanjutnya dari kata ini merupakan kata yang diawali dengan huruf kapital atau bukan. Maka, kita dapat menggunakan method `first_char_is_capitalized` dari objek `next_word_div` dari kata tersebut dengan cara:
```python
next_word_div: PySipebiWordDivision = word_div.next_word_div
if next_word_div.first_char_is_capitalized:
    # do something
```
