# Dua Komponen Penting Skrip Validasi

## 1. Fail `test`
Fail ini merupakan fail yang berisi data teks yang akan digunakan untuk proses validasi.

Berikut merupakan contoh dari isi fail test:
```txt
Saya mau pergi ke sana. saya mau pergi ke sini.
Dia kah? Dia lah!
```

## 2. Fail `common_check`
Fail ini merupakan fail yang digunakan sebagai acuan dari penyuntingan yang benar dan valid. Oleh karena itu, perlu diperhatikan bahwa setiap elemen perbaikan dari fail ini harus valid dan benar. 
Template isi dari fail ini adalah sebagai berikut:
```txt
<kode-kelas-skrip-diagnosis>, <kode-kelas-skrip-diagnosis>
<jumlah-data-teks-yang-mengandung-perbaikan>
<kode-kelas-skrip-diagnosis>|<paragraph-no>|<element-no>|<kata-original>|<perbaikan>|<is-ambigous>
```

Berikut merupakan contoh dari isi fail common_check:
```txt
KA01, KE01
3
KA01|01|06|saya|Saya|False 
KE01|02|01|Dia kah|Diakah|False 
KE01|02|02|Dia lah|Dialah|False
```