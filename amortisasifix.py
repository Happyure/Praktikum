import time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
localtime = time.asctime( time.localtime(time.time()) )
data_total_angsuran=[]
bunga_periodik=[]
pokok_periodik=[]
utang_periodik=[]
banyak_periode=[]
banyak_pengulangan=[]
yes=['yes','ya','y']
no=['no','tidak','n']

#Login
userpass={'icljaya':'123','iclkeren':'456','iclmantap':'789'}
kesempatan=2
while kesempatan>=0:
    userid=input("\nMasukkan username : ")
    password=input("Masukkan Password : ")
    if userid in userpass and password==userpass[userid]:
        print("Login berhasil\n")
        break
    else:
        print("Login gagal. Silahkan coba lagi.\nSisa kesempatan Anda: ",kesempatan,'\n')
    kesempatan-=1
    if kesempatan<0:
        print('Maaf Anda tidak bisa mengakses program\n')
        quit()

print("="*50)
print('Selamat datang dikalkulator amortisasi')
print('='*50)

#Kalkulator
pengulangan=0
while pengulangan==0:

    #Input
    while True:
        try:
            jumlah_pinjamanawal=int(input('\nMasukkan jumlah pinjaman awal\t   : '))
        except Exception:
            print('Tolong masukkan angka dan bukan karakter')
        try:
            suku_bunga=float(input('Masukkan suku bunga (persen)\t   : '))/100
        except Exception:
            print('Tolong masukkan angka dan bukan karakter')
        try:
            tenor_pengembalian=int(input('Masukkan tenor pengembalian (tahun): '))
        except Exception:
            print('Tolong masukkan angka dan bukan karakter')
        else:
            break


    #pelunasan
    while True:
        pelunasan=input('\nApakah anda ingin melunasi pada waktu tertentu?: ').lower()
        if pelunasan in yes:
            if tenor_pengembalian==1:
                while True:
                    try:
                        pelunasan_input=int(input('\nMasukkan waktu pelunasan (bulan ke-): '))
                        waktu_pelunasan=pelunasan_input
                    except Exception:
                        print('Tolong masukkan angka dan bukan karakter')
                    else:
                        break
                break
            else:
                print('\nBerikut ini bentuk waktu pelunasan yang tersedia:')
                waktu=['Tahun','Bulan']
                nomor=1
                for index in waktu:
                    print(nomor,'.',index)
                    nomor+=1
                while True:
                    while True:
                        try:
                            pilihan_waktu=int(input('Masukkan bentuk waktu pelunasan: '))
                        except Exception:
                            print('Tolong masukkan angka dan bukan karakter')
                        else:
                            break
                    if pilihan_waktu==1:
                        while True:
                            try:
                                pelunasan_input=int(input('Masukkan waktu pelunasan (tahun ke-): '))
                                waktu_pelunasan=pelunasan_input*12
                            except Exception:
                                print('Tolong masukkan angka dan bukan karakter')
                            else:
                                break
                        break
                    elif pilihan_waktu==2:
                        while True:
                            try:
                                pelunasan_input=int(input('Masukkan waktu pelunasan (bulan ke-): '))
                                waktu_pelunasan=pelunasan_input
                            except Exception:
                                print('Tolong masukkan angka dan bukan karakter')
                            else:
                                break
                        break
                    else:
                        print('Tolong masukkan sesuai dengan pilihan yang tersedia')
                break
        elif pelunasan in no:
            break
        else:
            print('Tolong masukkan sesuai dengan pilihan yang tersedia')
    
    #Menghitung Angsuran per Periode
    bunga=suku_bunga/12
    periode=tenor_pengembalian*12
    if pelunasan in no:
        waktu_pelunasan=periode
    pembayaran_perperiode=jumlah_pinjamanawal*bunga*((1+bunga)**periode)//(((1+bunga)**periode)-1)
    print('\nPembayaran perbulan\t: Rp.',int(pembayaran_perperiode))  

    #Menghitung Total Angsuran
    total_angsuran=pembayaran_perperiode*periode
    print('Total angsuran\t\t: Rp.',int(total_angsuran))
    data_total_angsuran.append(total_angsuran)

    #Menghitung Angsuran Pokok, Angsuran Bunga, dan Sisa Hutang per Periode
    periode_ke=1
    while periode_ke<=periode:
        bunga_periode=jumlah_pinjamanawal*bunga
        pokok_bayar=pembayaran_perperiode-bunga_periode
        print('\nAngsuran pokok periode ',periode_ke,': Rp.',int(pokok_bayar))
        print('Angsuran bunga periode ',periode_ke,': Rp.',int(bunga_periode))
        sisa_hutang=jumlah_pinjamanawal-pokok_bayar
        if sisa_hutang<=0:
            print('Sisa hutang periode    ',periode_ke,': Rp. 0')
        else:
            print('Sisa hutang periode    ',periode_ke,': Rp.',int(sisa_hutang))
        jumlah_pinjamanawal=sisa_hutang
        bunga_periodik.append(bunga_periode)
        pokok_periodik.append(pokok_bayar)
        utang_periodik.append(sisa_hutang)
        periode_ke+=1
        if periode_ke==waktu_pelunasan:
            if pelunasan=='yes':
                bunga_periode=total_angsuran-(sisa_hutang+sum(bunga_periodik))
                print('\nAngsuran pokok periode ',periode_ke,': Rp.', int(sisa_hutang))
                print('Angsuran bunga periode ',periode_ke,': Rp.', int(bunga_periode))
                print('Sisa hutang periode    ',periode_ke,': Rp. 0')
                pokok_periodik.append(sisa_hutang)
                bunga_periodik.append(bunga_periode)
                utang_periodik.append(0)
                break
     
    #Tabel
    print('\nBerikut ini merupakan tabel data amortisasi\n')
    print('='*65)
    print('\t\t\tTabel Amortisasi')
    print('='*65)
    tabel={'Angsuran Pokok':pd.Series(pokok_periodik),
           'Angsuran Bunga':pd.Series(bunga_periodik),
           'Total Angsuran':pd.Series(data_total_angsuran),
           'Sisa Utang':pd.Series(utang_periodik)}
    df=pd.DataFrame(tabel)
    print(df)

    #Menampilkan PieChart
    y=np.array([sum(pokok_periodik),sum(bunga_periodik)])
    mylabels=["Angsuran Pokok","Angsuran Bunga"]
    plt.pie(y,labels=mylabels,autopct='%1.1f%%',startangle=90)
    plt.title('Perbandingan Agsuran Pokok dan Angsuran Bunga')
    plt.show()

    #Pengulangan
    while True:
        mengulang=input('\nApakah anda ingin melakukan perhitungan peminjaman lainnya?: ').lower()
        if mengulang in no:
            pengulangan+=1
            break
        elif mengulang in yes:
            banyak_pengulangan.append(1)
            break
        else:
            print('Tolong masukkan sesuai dengan pilihan yang tersedia')

if sum(banyak_pengulangan)>0:
    #Membandingkan Efektivitas Perhitungan
    while True:
        perbandingan=input('\nApakah anda ingin mengetahui perbandingan pembayaran yang ada lakukan?: ').lower()
        if perbandingan in yes:
            print('\nPerhitungan ke-',data_total_angsuran.index(min(data_total_angsuran))+1,' lebih efektif karena total angsurannya lebih kecil yaitu Rp.',min(data_total_angsuran))
            break
        elif perbandingan in no:
            break
        else:
            print('Tolong masukkan sesuai dengan pilihan yang tersedia')
print('\nBerikut ini adalah total angsuran semua pembayaran: Rp.',sum(data_total_angsuran))

#Menampilkan pengguna dan waktu akses
print('\nTerima kasih telah menggunakan program kami')
print(userid,localtime,'\n')
