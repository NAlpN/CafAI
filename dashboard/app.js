async function loadDaily() {
  const res = await fetch("http://127.0.0.1:8000/daily-summary");
  const data = await res.json();

  document.getElementById("daily-section").innerHTML = `
    <div class="card">
      <div class="label">Gelen Toplam Müşteri Sayısı</div>
      <div class="value">${data.toplam_musteri}</div>
    </div>
    <div class="card">
      <div class="label">Müşterilerin Ortalama Oturma Süresi (dk)</div>
      <div class="value">${data.ortalama_oturma}</div>
    </div>
    <div class="card">
      <div class="label">Verilen Siparişler ve Sayıları</div>
      <div class="value">${data.siparis_ozet}</div>
    </div>
    <div class="card">
      <div class="label">En Çok Sipariş Verilen Ürün</div>
      <div class="value">${data.en_cok_urun}</div>
    </div>
    <div class="card">
      <div class="label">Günün En Yoğun Zaman Dilimi</div>
      <div class="value">${data.yogun_zaman}</div>
      <div class="chart">📊 Grafik burada gösterilecek</div>
    </div>
  `;
}

async function loadWeekly() {
  const res = await fetch("http://127.0.0.1:8000/weekly-summary");
  const data = await res.json();

  document.getElementById("weekly-section").innerHTML = `
    <div class="card">
      <div class="label">Gelen Ortalama Müşteri Sayısı</div>
      <div class="value">${data.ortalama_musteri}</div>
    </div>
    <div class="card">
      <div class="label">Haftalık Ortalama Oturma Süresi</div>
      <div class="value">${data.ortalama_oturma}</div>
    </div>
    <div class="card">
      <div class="label">Haftalık En Çok ve En Az Sipariş Verilen Ürünler</div>
      <div class="value">En Çok: ${data.en_cok_urun} <br/> En Az: ${data.en_az_urun}</div>
    </div>
    <div class="card">
      <div class="label">Haftanın En Yoğun Günü ve Saati</div>
      <div class="value">${data.yogun_gun_saat}</div>
    </div>
    <div class="card">
      <div class="label">Günlük Saatlik Yoğunluk Analizi</div>
      <div class="chart">📊 Grafik burada gösterilecek</div>
    </div>
  `;
}

loadDaily();
loadWeekly();