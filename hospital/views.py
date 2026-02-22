
from django.http.response import HttpResponse
import sqlite3
from django.shortcuts import render, redirect
from django.db import connection
from django.contrib import messages

def doktor_randevularim(request):
    if request.method == 'POST':
        if 'login' in request.POST:
            # Giriş işlemi
            doctor_id = request.POST.get('doctor_id')
            password = request.POST.get('password')

            conn = sqlite3.connect('hospital.db')
            cursor = conn.cursor()

            try:
                cursor.execute('SELECT doktorSifre FROM Doktorlar WHERE DoktorID=?', [doctor_id])
                result = cursor.fetchone()

                if result and result[0] == password:
                    cursor.execute('SELECT * FROM Randevular WHERE DoktorID=?', [doctor_id])
                    appointments = cursor.fetchall()
                    conn.close()
                    return render(request, "hospital/doktorRandevularim.html", {
                        'appointments': appointments,
                        'user_authenticated': True,
                        'doctor_id': doctor_id  # Doktor ID'sini görünüme aktar
                    })
                else:
                    error = "Geçersiz doktor ID veya şifre."
                    return render(request, "hospital/doktorRandevularim.html", {'error': error})
            except Exception as e:
                conn.close()
                return render(request, "hospital/doktorRandevularim.html", {'error': str(e)})

        elif 'book_appointment' in request.POST:
            # Randevu ekleme işlemi
            doctor_id = request.POST.get('doctor_id')
            patient_id = request.POST.get('patient_id')
            date = request.POST.get('date')
            time = request.POST.get('time')

            conn = sqlite3.connect('hospital.db')
            cursor = conn.cursor()

            try:
                cursor.execute(
                    'INSERT INTO Randevular (RandevuTarihi, RandevuSaati, HastaID, DoktorID) VALUES (?, ?, ?, ?)',
                    (date, time, patient_id, doctor_id)
                )
                conn.commit()
                cursor.execute('SELECT * FROM Randevular WHERE DoktorID=?', [doctor_id])
                appointments = cursor.fetchall()
                conn.close()
                return render(request, "hospital/doktorRandevularim.html", {
                    'appointments': appointments,
                    'user_authenticated': True,
                    'booking_success': 'Randevu başarıyla eklendi.',
                    'doctor_id': doctor_id  # Doktor ID'sini görünüme aktar
                })
            except Exception as e:
                conn.close()
                return render(request, "hospital/doktorRandevularim.html", {
                    'booking_error': str(e),
                    'user_authenticated': True,
                    'doctor_id': doctor_id  # Doktor ID'sini görünüme aktar
                })

        elif 'delete_appointment' in request.POST:
            # Randevu silme işlemi
            doctor_id = request.POST.get('doctor_id')
            appointment_id = request.POST.get('appointment_id')

            conn = sqlite3.connect('hospital.db')
            cursor = conn.cursor()

            try:
                cursor.execute('DELETE FROM Randevular WHERE RandevuID=?', [appointment_id])
                conn.commit()
                cursor.execute('SELECT * FROM Randevular WHERE DoktorID=?', [doctor_id])
                appointments = cursor.fetchall()
                conn.close()
                return render(request, "hospital/doktorRandevularim.html", {
                    'appointments': appointments,
                    'user_authenticated': True,
                    'booking_success': 'Randevu başarıyla silindi.',
                    'doctor_id': doctor_id  # Doktor ID'sini görünüme aktar
                })
            except Exception as e:
                conn.close()
                return render(request, "hospital/doktorRandevularim.html", {
                    'booking_error': str(e),
                    'user_authenticated': True,
                    'doctor_id': doctor_id  # Doktor ID'sini görünüme aktar
                })

    return render(request, 'hospital/doktorRandevularim.html')

def doktor_arayuz(request):
    return render(request, 'doktor/doktorArayuz.html')

def profilduzenle(request):
    hasta_bilgileri = None
    error_message = None
    username = None  # Kullanıcı adını saklamak için değişkeni tanımla
    
    if request.method == 'POST':
        if 'username' in request.POST and 'password' in request.POST:
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            conn = sqlite3.connect('hospital.db')
            cursor = conn.cursor()

            try:
                cursor.execute('SELECT HastaSifre, Ad, Soyad, DogumTarihi, Cinsiyet, Telefon, Adres FROM Hastalar WHERE HastaID=?', [username])
                result = cursor.fetchone()

                if result and result[0] == password:
                    hasta_bilgileri = {
                        'HastaID': username,
                        'Ad': result[1],
                        'Soyad': result[2],
                        'DogumTarihi': result[3],
                        'Cinsiyet': result[4],
                        'Telefon': result[5],
                        'Adres': result[6]
                    }
                else:
                    error_message = "Yanlış ID veya şifre."
            except Exception as e:
                error_message = f"Database error: {str(e)}"
            finally:
                conn.close()

        elif 'HastaID' in request.POST:
            # Bilgileri güncelle
            updated_data = {
                'HastaID': request.POST.get('HastaID'),
                'Ad': request.POST.get('Ad'),
                'Soyad': request.POST.get('Soyad'),
                'DogumTarihi': request.POST.get('DogumTarihi'),
                'Cinsiyet': request.POST.get('Cinsiyet'),
                'Telefon': request.POST.get('Telefon'),
                'Adres': request.POST.get('Adres')
            }
            
            conn = sqlite3.connect('hospital.db')
            cursor = conn.cursor()
            
            try:
                cursor.execute('''
                    UPDATE Hastalar 
                    SET Ad=?, Soyad=?, DogumTarihi=?, Cinsiyet=?, Telefon=?, Adres=? 
                    WHERE HastaID=?
                ''', [
                    updated_data['Ad'],
                    updated_data['Soyad'],
                    updated_data['DogumTarihi'],
                    updated_data['Cinsiyet'],
                    updated_data['Telefon'],
                    updated_data['Adres'],
                    updated_data['HastaID']
                ])
                conn.commit()
            except Exception as e:
                error_message = f"Update error: {str(e)}"
            finally:
                conn.close()
                return render(request, 'hospital/profilduzenle.html')  # İşlemden sonra aynı sayfaya yönlendir
    
    return render(request, 'hospital/profilduzenle.html', {
        'hasta_bilgileri': hasta_bilgileri,
        'error_message': error_message,
        'username': username  # Kullanıcı adını görünüme aktar
    })

# Create your views here.
def login_view(request):
    if request.method == 'POST':
        user_type = request.POST.get('user_type')
        username = request.POST.get('username')
        password = request.POST.get('password')

        conn = sqlite3.connect('hospital.db')
        cursor = conn.cursor()

        # Determine the appropriate SQL query based on the user type
        if user_type == 'patient':
            cursor.execute('SELECT hastaSifre FROM Hastalar WHERE HastaID=?', [username])
        elif user_type == 'doctor':
            cursor.execute('SELECT doktorSifre FROM Doktorlar WHERE DoktorID=?', [username])
        elif user_type == 'manager':
            cursor.execute('SELECT yoneticiSifre FROM Yoneticiler WHERE YoneticiID=?', [username])
        else:
            messages.error(request, 'Geçersiz kullanıcı türü.')
            return render(request,"hospital/homePage.html")

        # Fetch the result from the executed query
        row = cursor.fetchone()
        
        # Check if a result was found and if the password matches
        if row is not None and row[0] == password:
            # Redirect to the appropriate user interface
            if user_type == 'patient':
                return render(request,"hospital/hastaArayuz.html")
            elif user_type == 'doctor':
                return render(request,"hospital/doktorArayuz.html")
            elif user_type == 'manager':
                return render(request,"hospital/Manager.html")
        else:
            messages.error(request, 'Geçersiz kimlik veya şifre.')
            return render(request,"hospital/homePage.html")

    # Render the home page template if the request method is GET
    return render(request,"hospital/homePage.html")

def index(request):
    return render(request,"hospital/homePage.html")
def Doctors(request):
    return render(request,"hospital/doktorArayuz.html")

def SearchDoctor(request):
    if request.method == 'POST':
        query = request.POST.get('query', '')
        # Veritabanına bağlan
        conn = sqlite3.connect('hospital.db')
        cursor = conn.cursor()
        
        # Doktorları ada veya soyada göre arama
        cursor.execute("SELECT * FROM doktorlar WHERE Ad LIKE ? OR Soyad LIKE ?", ('%' + query + '%', '%' + query + '%'))
        results = cursor.fetchall()
         
        # Veritabanı bağlantısını kapat
        conn.close()
        
        return render(request, 'hospital/SearchDoctor.html', {'query': query, 'results': results})
    return render(request, 'hospital/SearchDoctor.html')

def SearchPatient(request):
    if request.method == 'POST':
        query = request.POST.get('query', '')
        # Veritabanına bağlan
        conn = sqlite3.connect('hospital.db')
        cursor = conn.cursor()
        
        # Doktorları ada veya soyada göre arama
        cursor.execute("SELECT * FROM hastalar WHERE Ad LIKE ? OR Soyad LIKE ?", ('%' + query + '%', '%' + query + '%'))
        results = cursor.fetchall()
         
        # Veritabanı bağlantısını kapat
        conn.close()
        
        return render(request, 'hospital/SearchPatient.html', {'query': query, 'results': results})
    return render(request, 'hospital/SearchPatient.html')

def rapor_view(request):
    hasta_id = request.GET.get('hasta_id')
    raporlar = []

    if hasta_id:
        conn = sqlite3.connect('hospital.db')
        cursor = conn.cursor()
        cursor.execute("SELECT RaporID, RaporTarihi, RaporIcerigi, HastaID, DoktorID FROM TibbiRaporlar WHERE HastaID=?", (hasta_id,))
        raporlar = cursor.fetchall()
        conn.close()

    context = {
        'raporlar': raporlar,
        'hasta_id': hasta_id
    }

    return render(request, 'hospital/RaporView.html', context)

def Manager(request):
    if request.method == "POST":
        # Doktor silme işlemi
        if 'sil_doktor' in request.POST:
            doktor_id_to_delete = request.POST.get("doktor_id")
            # Veritabanı bağlantısını oluştur
            conn = sqlite3.connect('hospital.db')
            cursor = conn.cursor()
            # Doktoru sil
            cursor.execute("DELETE FROM Doktorlar WHERE DoktorID=?", (doktor_id_to_delete,))
            # Değişiklikleri kaydet
            conn.commit()
            # Veritabanı bağlantısını kapat
            conn.close()
            # Başarılı silme mesajı ile birlikte yönlendirme yap
            return HttpResponse("Doktor başarıyla silindi.")
        
        # Hasta silme işlemi
        elif 'sil_hasta' in request.POST:
            hasta_id_to_delete = request.POST.get("hasta_id")
            # Veritabanı bağlantısını oluştur
            conn = sqlite3.connect('hospital.db')
            cursor = conn.cursor()
            # Hastayı sil
            cursor.execute("DELETE FROM Hastalar WHERE HastaID=?", (hasta_id_to_delete,))
            # Değişiklikleri kaydet
            conn.commit()
            # Veritabanı bağlantısını kapat
            conn.close()
            # Başarılı silme mesajı ile birlikte yönlendirme yap
            return HttpResponse("Hasta başarıyla silindi.")

        # Yeni doktor ekleme işlemi
        elif 'DoktorID' in request.POST:
            doktor_id = request.POST.get("DoktorID")
            doktor_sifre = request.POST.get("DoktorSifre")
            ad = request.POST.get("Ad")
            soyad = request.POST.get("Soyad")
            uzmanlik_alani = request.POST.get("UzmanlikAlani")
            
            # Yeni doktoru veritabanına ekle
            conn = sqlite3.connect('hospital.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Doktorlar (DoktorID, DoktorSifre, Ad, Soyad, UzmanlikAlani) VALUES (?, ?, ?, ?, ?)",
                           (doktor_id, doktor_sifre, ad, soyad, uzmanlik_alani))
            # Değişiklikleri kaydet
            conn.commit()
            # Veritabanı bağlantısını kapat
            conn.close()
        
        # Yeni hasta ekleme işlemi
        elif 'HastaID' in request.POST:
            hasta_id = request.POST.get("HastaID")
            hasta_sifre = request.POST.get("HastaSifre")
            ad = request.POST.get("Ad")
            soyad = request.POST.get("Soyad")
            dogum_tarihi = request.POST.get("DogumTarihi")
            cinsiyet = request.POST.get("Cinsiyet")
            telefon = request.POST.get("Telefon")
            adres = request.POST.get("Adres")
            
            # Yeni hastayı veritabanına ekle
            conn = sqlite3.connect('hospital.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Hastalar (HastaID, HastaSifre, Ad, Soyad, DogumTarihi, Cinsiyet, Telefon, Adres) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                           (hasta_id, hasta_sifre, ad, soyad, dogum_tarihi, cinsiyet, telefon, adres))
            # Değişiklikleri kaydet
            conn.commit()
            # Veritabanı bağlantısını kapat
            conn.close()

    # Veritabanı bağlantısını oluştur
    conn = sqlite3.connect('hospital.db')
    cursor = conn.cursor()

    # Mevcut doktorları getir
    cursor.execute("SELECT DoktorID, Ad, Soyad, UzmanlikAlani FROM Doktorlar")
    doktorlar = cursor.fetchall()

    # Mevcut hastaları getir
    cursor.execute("SELECT * FROM Hastalar")
    hastalar = cursor.fetchall()

    # Veritabanı bağlantısını kapat
    conn.close()

    return render(request, "hospital/Manager.html", {"success_message": "", "doktorlar": doktorlar, "hastalar": hastalar})

def hastaArayuz(request):
    return render(request,"hospital/hastaArayuz.html")
def Patient(request):
    return render(request,"hospital/Patient.html")
def randevuArayuz(request):
    return render(request,"hospital/randevuArayuz.html")

def doktorProfilim(request):
    if request.method == 'POST':
        doktor_id = request.POST['doktor_id']
        doktor_sifre = request.POST['doktor_sifre']
        ad = request.POST['ad']
        soyad = request.POST['soyad']
        uzmanlik_alani = request.POST['uzmanlik_alani']
        

        # Veritabanında profil bilgilerini güncelleme
        with connection.cursor() as cursor:
            cursor.execute("UPDATE Doktor SET DoktorSifre = %s, Ad = %s, Soyad = %s, UzmanlikAlani = %s WHERE DoktorID = %s",
                           [doktor_sifre, ad, soyad, uzmanlik_alani, doktor_id])

        return redirect('profilim')

    else:
        if 'doktor_id' in request.session and 'doktor_sifre' in request.session:
            doktor_id = request.session['doktor_id']
            doktor_sifre = request.session['doktor_sifre']

            # Veritabanından profil bilgilerini çekme
            with connection.cursor() as cursor:
                cursor.execute("SELECT DoktorID, DoktorSifre, Ad, Soyad, UzmanlikAlani FROM Doktor WHERE DoktorID = %s AND DoktorSifre = %s", [doktor_id, doktor_sifre])
                row = cursor.fetchone()
                if row:
                    doktor_id, _, ad, soyad, uzmanlik_alani = row
                else:
                    # Kullanıcı kimlik doğrulaması başarısız olduğunda, profil sayfasına yeniden yönlendir
                    return redirect('doktorProfilim')
        else:
            # Oturum verileri eksikse, profil sayfasına yeniden yönlendir
            return render(request, 'hospital/DoktorProfilim.html')

        return render(request, 'hospital/DoktorProfilim.html', {'doktor_id': doktor_id, 'doktor_sifre': doktor_sifre, 'ad': ad, 'soyad': soyad, 'uzmanlik_alani': uzmanlik_alani})


def profilim(request):
    if request.method == 'POST':
        hasta_id = request.POST['hasta_id']
        hasta_sifre = request.POST['hasta_sifre']
        ad = request.POST['ad']
        soyad = request.POST['soyad']
        dogum_tarihi = request.POST['dogum_tarihi']
        cinsiyet = request.POST['cinsiyet']
        telefon = request.POST['telefon']
        adres = request.POST['adres']

        # Veritabanında profil bilgilerini güncelleme
        with connection.cursor() as cursor:
            cursor.execute("UPDATE Hasta SET HastaSifre = %s, Ad = %s, Soyad = %s, DogumTarihi = %s, Cinsiyet = %s, Telefon = %s, Adres = %s WHERE HastaID = %s",
                           [hasta_sifre, ad, soyad, dogum_tarihi, cinsiyet, telefon, adres, hasta_id])

        return redirect('profilim')

    else:
        if 'hasta_id' in request.session and 'hasta_sifre' in request.session:
            hasta_id = request.session['hasta_id']
            hasta_sifre = request.session['hasta_sifre']

            # Veritabanından profil bilgilerini çekme
            with connection.cursor() as cursor:
                cursor.execute("SELECT HastaID, HastaSifre, Ad, Soyad, DogumTarihi, Cinsiyet, Telefon, Adres FROM Hasta WHERE HastaID = %s AND HastaSifre = %s", [hasta_id, hasta_sifre])
                row = cursor.fetchone()
                if row:
                    hasta_id, _, ad, soyad, dogum_tarihi, cinsiyet, telefon, adres = row
                else:
                    # Kullanıcı kimlik doğrulaması başarısız olduğunda, profil sayfasına yeniden yönlendir
                    return redirect('profilim')
        else:
            # Oturum verileri eksikse, profil sayfasına yeniden yönlendir
            return redirect('profilim')

        return render(request, 'profilim.html', {'hasta_id': hasta_id, 'hasta_sifre': hasta_sifre, 'ad': ad, 'soyad': soyad, 'dogum_tarihi': dogum_tarihi, 'cinsiyet': cinsiyet, 'telefon': telefon, 'adres': adres})

def randevularim(request):
    username = None  # Kullanıcı adını saklamak için değişkeni tanımla
    if request.method == 'POST':
        if 'username' in request.POST and 'password' in request.POST:
            # Giriş işlemi
            username = request.POST.get('username')
            password = request.POST.get('password')

            conn = sqlite3.connect('hospital.db')
            cursor = conn.cursor()

            try:
                cursor.execute('SELECT hastaSifre FROM Hastalar WHERE HastaID=?', [username])
                result = cursor.fetchone()

                if result and result[0] == password:
                    cursor.execute('SELECT * FROM Randevular WHERE HastaID=?', [username])
                    appointments = cursor.fetchall()
                    conn.close()
                    return render(request, "hospital/randevularim.html", {
                        'appointments': appointments,
                        'user_authenticated': True,
                        'username': username  # Kullanıcı adını görünüme aktar
                    })
                else:
                    error = "Geçersiz kullanıcı ID veya şifre."
                    return render(request, "hospital/randevularim.html", {'error': error})
            except Exception as e:
                conn.close()
                return render(request, "hospital/randevularim.html", {'error': str(e)})

        elif 'book_appointment' in request.POST:
            # Randevu alma işlemi
            username = request.POST.get('username')
            doctor_id = request.POST.get('doctor_id')
            date = request.POST.get('date')
            time = request.POST.get('time')
 
            conn = sqlite3.connect('hospital.db')
            cursor = conn.cursor()

            try:
                cursor.execute(
                    'INSERT INTO Randevular (RandevuTarihi, RandevuSaati, HastaID, DoktorID) VALUES (?, ?, ?, ?)',
                    (date, time, username , doctor_id)
                )
                conn.commit()
                cursor.execute('SELECT * FROM Randevular WHERE HastaID=?', [username])
                appointments = cursor.fetchall()
                conn.close()
                return render(request, "hospital/randevularim.html", {
                    'appointments': appointments,
                    'user_authenticated': True,
                    'booking_success': 'Randevu başarıyla alındı.',
                    'username': username  # Kullanıcı adını görünüme aktar
                })
            except Exception as e:
                conn.close()
                return render(request, "hospital/randevularim.html", {
                    'booking_error': str(e),
                    'user_authenticated': True,
                    'username': username  # Kullanıcı adını görünüme aktar
                })

        elif 'delete_appointment' in request.POST:
            # Randevu silme işlemi
            username = request.POST.get('username')
            appointment_id = request.POST.get('appointment_id')

            conn = sqlite3.connect('hospital.db')
            cursor = conn.cursor()

            try:
                cursor.execute('DELETE FROM Randevular WHERE RandevuID=?', [appointment_id])
                conn.commit()
                cursor.execute('SELECT * FROM Randevular WHERE HastaID=?', [username])
                appointments = cursor.fetchall()
                conn.close()
                return render(request, "hospital/randevularim.html", {
                    'appointments': appointments,
                    'user_authenticated': True,
                    'booking_success': 'Randevu başarıyla silindi.',
                    'username': username  # Kullanıcı adını görünüme aktar
                })
            except Exception as e:
                conn.close()
                return render(request, "hospital/randevularim.html", {
                    'booking_error': str(e),
                    'user_authenticated': True,
                    'username': username  # Kullanıcı adını görünüme aktar
                })

    return render(request, "hospital/randevularim.html")

def hasta_arayuz(request):
    return render(request, 'hastaArayuz.html')
    