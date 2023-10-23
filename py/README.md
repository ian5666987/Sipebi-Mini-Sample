# Validasi Skrip Diagnosis

Skrip diagnosis tentunya harus melewati tahap validasi terlebih dahulu sebelum dimasukkan ke dalam kode Sipebi yang asli. Tahapan validasi ini dilakukan untuk memastikan bahwa skrip diagnosis yang dibuat tidak mengandung kesalahan sintaksis dan logika. 

Untuk melakukan validasi pada skrip diagnosis yang Anda telah buat, ikuti tahapan berikut ini:
1. Buat sebuah fail dengan nama `<nama-class-skrip-diagnosis>_Val.py` pada direktori `py/`. Misalnya, nama class skrip diagnosis Anda adalah `PySipebiDiagAturanTandaBacaPadaDialog`, maka nama fail validasi yang harus Anda buat adalah `PySipebiAturanTandaBacaPadaDialog_Val.py`.
2. Buat 2 fail `.txt` dasar yang dibutuhkan untuk dibaca pada proses validasi, yaitu fail `common_check` dan fail `test`. Fail tersebut dibuat pada folder `py/data`. Sesuaikan nama failnya dengan konvensi berikut. Misalnya, nama class skrip diagnosis Anda adalah `PySipebiDiagAturanTandaBacaPadaDialog`, maka nama fail `common_check` dan `test` yang harus Anda buat adalah `PySipebiDiagAturanTandaBacaPadaDialog_common_check.txt` dan `PySipebiDiagAturanTandaBacaPadaDialog_test.txt`. Isi dari kedua fail tersebut bisa lihat di contoh fail `common_check` dan `test` yang sudah ada.
3. Untuk pembuatan kode skrip validasi, ikuti saja alur kode yang ada pada fail validasi yang telah dibuat, seperti fail `PySipebiDiagAturanPartikelPun_Val.py`. Isi fail kurang lebih sama. Dipersilahkan jika ingin menambahkan beberapa validasi tambahan.
4. Untuk menjalankan fail validasi, pada baris paling bawah kode pada fail validasi, salin kode berikut dan ubah beberapa hal yang seharusnya diubah:

```python
if __name__ == "__main__":
    validation_runner = PySipebiCommonValidationRunner(<nama-kelas-validasi>)
    validation_runner.setup_and_run_validation()
```

Contohnya, 
```python
if __name__ == "__main__":
    validation_runner = PySipebiCommonValidationRunner(PySipebiDiagAturanPartikelLahKahTah_Val)
    validation_runner.setup_and_run_validation()
```
5. Setelah itu, jalankan fail skrip validasi tersebut. Setelah dijalankan, maka akan dibuat sebuah fail txt `result` yang merupakan hasil dari validasi skrip diagnosis yang telah dibuat. Fail tersebut akan berada pada folder `py/data/results`. Fail tersebut berisi hasil validasi dari skrip diagnosis yang telah dibuat. Jika hasil validasi tersebut tidak sesuai dengan yang diharapkan, maka perbaiki skrip diagnosis yang telah dibuat. Jika hasil validasi tersebut sesuai dengan yang diharapkan, maka skrip diagnosis tersebut dapat dimasukkan ke dalam kode Sipebi yang asli.