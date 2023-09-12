## Cara Membuat Skrip Diagnostics Sipebi Mini dalam Bahasa Python

### Pendahuluan
Skrip Diagnostic pada Sipebi Mini merupakan skrip yang digunakan untuk memeriksa kesalahan aturan ejaan pada Sipebi Mini. Selain bisa membuat skrip diagnostic dalam bahasa C#, Sipebi Mini juga mendukung pembuatan skrip diagnostic dalam bahasa Python. Folder `py/diag/` pada Sipebi Mini berisikan segala sesuatu yang berhubungan dengan pengerjaan skrip diagnostic dalam bahasa Python. Jika ingin membuat skrip diagnosis dalam bahasa Python, Anda diharapkan hanya fokus pada folder `py/diag/` saja dan file `App.config` pada yang terletak pada  root folder `Sipebi-Mini-Sample`. Terdapat beberapa folder dan file yang terletak pada folder `py/diag/`, yaitu:

1. Folder `core`: Folder yang berisikan file-file yang berhubungan dengan fungsi-fungsi dasar yang digunakan oleh skrip diagnostic dalam bahasa Python.
2. Folder `data`: Folder yang berisikan file-file yang berhubungan dengan data yang digunakan oleh skrip diagnostic dalam bahasa Python.
3. Folder `libs`: Folder yang berisikan file-file yang berhubungan dengan pustaka-pustaka pembantu yang digunakan oleh skrip diagnostic dalam bahasa Python.
4. File `PySipebiDiagExample.py`: File yang berisikan contoh skrip diagnostic dalam bahasa Python.

### Memahami Struktur Skrip Diagnostic dalam Bahasa Python
Sebelum masuk kepada tahap pembuatan skrip diagnostic dalam bahasa Python, Anda diharapkan memahami struktur skrip diagnostic dalam bahasa Python terlebih dahulu.

Pada folder `core` terdapat beberapa file yang berisikan fungsi-fungsi dasar yang digunakan oleh skrip diagnostic dalam bahasa Python. File-file tersebut adalah:
1.  File `PySipebiDiagnosticsBase.py`: File ini berisikan sebuah base class dari skrip - skrip diagnostics yang akan Anda buat. File ini berisikan fungsi-fungsi dasar yang digunakan oleh skrip diagnostic dalam bahasa Python. File ini juga berisikan fungsi-fungsi yang akan dipanggil oleh Sipebi Mini untuk menjalankan skrip diagnostic yang Anda buat. Luangkan waktu Anda untuk membaca file ini dan memahami fungsi-fungsi yang terdapat pada file ini.
2.  File `PySipebiDiagnosticsError.py`: File ini berisikan sebuah class yang akan merepresentasikan kesalahan aturan ejaan yang ada pada teks. Satu kesalahan aturan ejaan berarti satu objek class ini. Semua atribut yang ada pada class pada file ini harus diisi semua dengan benar agar skrip diagnostic yang Anda buat dapat berjalan dengan baik. Luangkan waktu Anda untuk membaca file ini dan memahami fungsi-fungsi yang terdapat pada file ini.

### Membuat Skrip Diagnostic dalam Bahasa Python
Setelah memahami struktur skrip diagnostic dalam bahasa Python, Anda dapat membuat skrip diagnostic dalam bahasa Python. Untuk membuat skrip diagnostic dalam bahasa Python, Anda diharapkan melakukan langkah-langkah berikut:

1. Membuat Sebuah file skrip diagnosis untuk masing - masing aturan ejaan yang ada dengan konvensi nama `PySipebiDiag<Nama Aturan Ejaan>.py`.Contohnya, `PySipebiDiagPerbaikanKataHubung.py` untuk aturan ejaan perbaikan kata hubung. Pada file ini, buatlah sebuah class yang namanya sama dengan filenya tanpa ekstensi `.py`. Class yang Anda buat **harus** *extends* dari class `PySipebiDiagnosticsBase`. Setelah itu, Anda harus melakukan *override* pada seluruh *method* yang ada pada class `PySipebiDiagnosticsBase`. Anda dapat melihat contoh pada file `PySipebiDiagExample.py` untuk lebih jelasnya.

2. Setelah Anda membuat sebuah skrip diagnostic, agar skrip yang Anda buat dijalankan oleh Sipebi Mini, Anda harus menambahkan sebuah *entry* pada file `App.config` yang terletak pada root folder `Sipebi-Mini-Sample`. Anda harus menaruh nama file skrip diagnostics Andas pada properti `value` dengan `key PyDiagnosticsScripts`.

3. Sebelum menjalankan aplikasi SipebiMini untuk mencoba skrip yang Anda buat, Anda harus menjalankan file `initiator.bat` yang bertujuan untuk menduplikasi file skrip Anda ke dalam folder `bin/debug`. Setelah menjalankan file `initiator.bat`, Anda dapat menjalankan aplikasi SipebiMini untuk mencoba skrip yang Anda buat.