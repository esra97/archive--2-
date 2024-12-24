from ultralytics import YOLO

# Modeli yükle (YOLOv8'in küçük versiyonunu kullanıyoruz)
model = YOLO("yolov8n.pt")  # İstediğiniz önceden eğitilmiş model dosyasını kullanabilirsiniz

# Eğitim başlat
model.train(data='C:/Users/90553/Downloads/archive (2)/model/dataset.yaml', epochs=50, batch=16)
