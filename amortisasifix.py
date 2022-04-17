import time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
localtime = time.asctime( time.localtime(time.time()) )
data_total_angsuran=[]
bunga_sisa=[]
bunga_periodik=[]
pokok_periodik=[]
utang_periodik=[]
banyak_periode=[]
banyak_pengulangan=[]
angsuran_kumulatif=[]
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

print("="*64)
print('\t     Selamat datang dikalkulator amortisasi')
print('='*64)

#Kalkulator
pengulangan=0
while pengulangan==0:

    #Input
    while True:
        try:
            jumlah_pinjamanawal=int(input('\nMasukkan jumlah pinjaman awal\t   : '))
        except Exception:
            print('Tolong masukkan angka dan bukan karakter')
        else:
            break
    while True:
        try:
            suku_bunga=float(input('Masukkan suku bunga (persen)\t   : '))/100
        except Exception:
            print('Tolong masukkan angka dan bukan karakter')
        else:
            break
    while True:
        try:
            tenor_pengembalian=int(input('Masukkan tenor pengembalian (tahun): '))
        except Exception:
            print('Tolong masukkan angka dan bukan karakter')
        else:
            break

    print(' ')
    print('='*64)
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
                        print('Pilihan tidak tersedia!')
                break
        elif pelunasan in no:
            break
        else:
            print('Pilihan tidak tersedia!')
    
    print('\nJumlah pinjaman awal\t: ',jumlah_pinjamanawal )
    print('Suku bunga \t\t: ', suku_bunga*100,'%')
    print('Tenor Pengembalian\t: ',tenor_pengembalian,'Tahun')
    print(' ')
    print('='*64)
    #Menghitung Angsuran per Periode
    bunga=suku_bunga/12
    periode=tenor_pengembalian*12
    if pelunasan in no:
        waktu_pelunasan=periode
    pembayaran_perperiode=jumlah_pinjamanawal*bunga*((1+bunga)**periode)//(((1+bunga)**periode)-1)
    print('\nPembayaran perbulan\t: Rp.',int(pembayaran_perperiode))  
    for i in range(waktu_pelunasan):
        data_total_angsuran.append(pembayaran_perperiode)
    
    #Menghitung Total Angsuran
    total_angsuran=pembayaran_perperiode*periode
    print('Angsuran Kumulatif\t: Rp.',int(total_angsuran))
    angsuran_kumulatif.append(total_angsuran)

    #Menghitung Angsuran Pokok, Angsuran Bunga, dan Sisa Hutang per Periode
    periode_ke=1
    while periode_ke<=periode:
        bunga_periode=jumlah_pinjamanawal*bunga
        pokok_bayar=pembayaran_perperiode-bunga_periode
        sisa_hutang=jumlah_pinjamanawal-pokok_bayar
        jumlah_pinjamanawal=sisa_hutang
        bunga_periodik.append(bunga_periode)
        pokok_periodik.append(pokok_bayar)
        utang_periodik.append(sisa_hutang)
        periode_ke+=1
        if periode_ke==waktu_pelunasan:
            if pelunasan=='yes':
                bunga_periode=total_angsuran-(sum(pokok_periodik)+sum(bunga_periodik)+sisa_hutang)
                pokok_periodik.append(sisa_hutang)
                bunga_periodik.append(bunga_periode)
                utang_periodik.append(0)
                break

    #Tabel
    print('\nBerikut ini merupakan tabel data amortisasi\n')
    print('='*64)
    print('\t\t\tTabel Amortisasi')
    print('='*64)
    tabel={'Angsuran Pokok':(pokok_periodik),
           'Angsuran Bunga':(bunga_periodik),
           'Total Angsuran':(data_total_angsuran),
           'Sisa Utang':(utang_periodik)}
    df=pd.DataFrame(tabel,index=pd.RangeIndex(start=1,stop=len(pokok_periodik)+1)).astype(int)
    print(df)
    print('='*64)

    #Menampilkan PieChart
    y=np.array([sum(pokok_periodik),sum(bunga_periodik)])
    mylabels=["Angsuran Pokok","Angsuran Bunga"]
    plt.pie(y,labels=mylabels,autopct='%1.1f%%',startangle=90)
    plt.title('Perbandingan Agsuran Pokok dan Angsuran Bunga')
    plt.show()

    #Pengulangan
    while True:
        mengulang=input('Apakah anda ingin melakukan perhitungan peminjaman lainnya?: ').lower()
        if mengulang in no:
            pengulangan+=1
            break
        elif mengulang in yes:
            banyak_pengulangan.append(1)
            data_total_angsuran.clear()
            pokok_periodik.clear()
            bunga_periodik.clear()
            utang_periodik.clear()
            break
        else:
            print('Pilihan tidak tersedia!')

print('='*64)
if sum(banyak_pengulangan)>0:
    #Membandingkan Efektivitas Perhitungan
    while True:
        perbandingan=input('Apakah anda ingin mengetahui perbandingan pembayaran yang ada lakukan?: ').lower()
        if perbandingan in yes:
            print('\nPerhitungan ke-',angsuran_kumulatif.index(min(angsuran_kumulatif))+1,' lebih efektif karena angsuran kumulatifnya lebih kecil yaitu Rp.',min(angsuran_kumulatif))
            print('='*64)
            break
        elif perbandingan in no:
            break
        else:
            print('Pilihan tidak tersedia!')
print('Berikut ini adalah total angsuran semua pembayaran: Rp.',sum(angsuran_kumulatif))
print('='*64)
#Menampilkan pengguna dan waktu akses
print('\nTerima kasih telah menggunakan program kami')
print(userid,localtime,'\n')