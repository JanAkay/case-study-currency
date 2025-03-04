>scheduler.py çalıştığında uygulama periyodik olarak (şu an 30dk) fetch_rates.py'daki fetch_exchange_rates() fonksiyonu aracılığıyla API'lardan veri çekecek. 
>API'lar kendime ait API anahtarı ile açtığım hesap üzerinden veri fetchliyor, key'ler fetchrates.py'da hardcoded şekilde mevcut.
>Alınan veri config.py'da bulunan (PostgreSQL) veritabanım ile bağlantı kuruyor. Veritabanı ile ilgili credential'lar config.py'da hardcoded şekilde mevcut. DB modeli models.py'da mevcut
>app.py uygulamanın localhost ile bağlantısı ve API'dan veri alınması ile sorumlu.
>API'dan veri almak için gerekli metodlar routes.py'da belirlendi.
>requirements.txt dosyasını güncellemeyi unuttuğumdan dolayı bazı ekstra dependency'lerin kurulması gerekebilir. 


bağlı bir veri tabanı olduğuna, api keylerin kullanılabilir olduğuna emin olun
scheduler.py'ı çalıştırın, durdurulmadığı sürece arka planda periyodik olarak veri çekimi yapacak.
app.py'ı çalıştırın, artık veritabanından query'ler ile veri çekebilirsiniz