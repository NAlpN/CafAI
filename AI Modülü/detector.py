import cv2
import requests
import time
from ultralytics import YOLO

# YOLOv8s modelini yükle
model = YOLO("yolov8s.pt")

# Kamera başlat
cap = cv2.VideoCapture(0)

# Flask API URL
API_URL = "http://127.0.0.1:5000/log-entry"

# Zaman kontrolü için başlangıç
last_sent = 0
SEND_INTERVAL = 3  # saniyede bir gönderim

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # YOLO ile nesne tespiti
    results = model(frame)
    detections = results[0].boxes.data

    # Sadece "person" sınıfını say (class id: 0)
    person_count = sum(int(box[5] == 0) for box in detections)

    # Zaman kontrolü (3 saniyede 1 gönderim)
    current_time = time.time()
    if current_time - last_sent >= SEND_INTERVAL:
        try:
            response = requests.post(API_URL, json={"musteri_sayisi": person_count})
            print(f"[INFO] Gönderildi: {person_count} kişi")
            last_sent = current_time
        except Exception as e:
            print(f"[ERROR] API gönderimi başarısız: {e}")

    # Görsel gösterim (istediğin zaman kapatabilirsin)
    cv2.imshow("YOLOv8s - Müşteri Takibi", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Temizlik
cap.release()
cv2.destroyAllWindows()