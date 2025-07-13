from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
from collections import Counter, defaultdict

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def read_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

@app.get("/daily-summary")
def daily_summary():
    camera_data = read_json("data/camera_data.json")
    sales_data = read_json("data/sales_data.json")

    toplam_musteri = len(camera_data)
    ortalama_oturma = round(sum(x["oturma_suresi"] for x in camera_data) / toplam_musteri, 2)

    urunler = []
    saatler = []
    siparis_ozet_dict = defaultdict(int)

    for s in sales_data:
        saatler.append(s["saat"])
        for u in s["siparisler"]:
            urunler.append(u["urun"])
            siparis_ozet_dict[u["urun"]] += 1

    en_cok_urun = Counter(urunler).most_common(1)[0][0]
    yogun_saat = Counter(saatler).most_common(1)[0][0]
    siparis_ozet = ", ".join(f"{k}: {v}" for k, v in siparis_ozet_dict.items())

    return {
        "toplam_musteri": toplam_musteri,
        "ortalama_oturma": ortalama_oturma,
        "en_cok_urun": en_cok_urun,
        "siparis_ozet": siparis_ozet,
        "yogun_zaman": f"{yogun_saat}:00 - {int(yogun_saat)+1}:00"
    }

@app.get("/weekly-summary")
def weekly_summary():
    weekly_data = read_json("data/weekly_sales_data.json")

    toplam_musteri = 0
    toplam_sure = 0
    musteri_gun_sayisi = 0
    genel_urunler = []

    saat_yoğunluk = defaultdict(int)
    gun_saat_yoğunluk = defaultdict(lambda: defaultdict(int))

    for gun in weekly_data:
        toplam_musteri += gun["toplam_musteri"]
        toplam_sure += gun["ortalama_oturma"]
        musteri_gun_sayisi += 1

        for s in gun["veriler"]:
            saat_yoğunluk[s["saat"]] += 1
            gun_saat_yoğunluk[gun["tarih"]][s["saat"]] += 1
            for u in s["siparisler"]:
                genel_urunler.append(u["urun"])

    ort_musteri = round(toplam_musteri / musteri_gun_sayisi)
    ort_sure = round(toplam_sure / musteri_gun_sayisi)

    urun_counter = Counter(genel_urunler)
    en_cok = urun_counter.most_common(1)[0][0]
    en_az = urun_counter.most_common()[-1][0]

    en_yogun_saat = max(saat_yoğunluk, key=saat_yoğunluk.get)
    en_yogun_gun_saat = max(gun_saat_yoğunluk.items(), key=lambda g: sum(g[1].values()))
    en_yogun_gun = en_yogun_gun_saat[0]

    return {
        "ortalama_musteri": ort_musteri,
        "ortalama_oturma": ort_sure,
        "en_cok_urun": en_cok,
        "en_az_urun": en_az,
        "yogun_gun_saat": f"{en_yogun_gun} günü, {en_yogun_saat}:00 - {int(en_yogun_saat)+1}:00"
    }