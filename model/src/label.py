import os
import json
import pandas as pd

# 1. Mineral isimlerini ID ile eşleştirme
mineral_ids = {
    "quartz": 0, "topaz": 1, "chalcedony": 2, "cassiterite": 3, "hematite": 4,
    "magnetite": 5, "agate": 6, "beryl": 7, "calcite": 8, "corundum": 9,
    "silver": 10, "gold": 11, "diopside": 12, "microcline": 13, "pyrite": 14,
    "amethyst": 15, "fluorite": 16, "albite": 17, "arsenopyrite": 18, "gypsum": 19
}

# 2. Excel dosyasını okuma
excel_path = r"C:\Users\90553\Downloads\archive (2)\minerals_full.xlsx"
data = pd.read_excel(excel_path)

# 3. Excel'deki path sütunundan dosya adını çıkartma
data['filename'] = data['path'].apply(lambda x: os.path.basename(x).lower())

# 4. En yüksek confidence değerli box seçme fonksiyonu
def get_highest_confidence_box(boxes):
    try:
        # ";" ile ayrılanları "," yap ve JSON'a çevir
        box_list = json.loads(boxes.replace(';', ','))
        # En yüksek confidence değerini seç
        highest_conf_box = max(box_list, key=lambda x: x['confidence'])
        return highest_conf_box
    except Exception as e:
        # Hata olursa terminale yazdır
        print(f"Hata: {e}")
        return None

# 5. Box koordinatlarını dönüştürme fonksiyonu
def convert_box_coordinates(box):
    xmin, ymin, xmax, ymax = box['box']
    width = xmax - xmin
    height = ymax - ymin
    x_center = (xmin + xmax) / 2
    y_center = (ymin + ymax) / 2
    return x_center, y_center, width, height

def get_correct_boxes(row):
    # Önce mineral_boxes'ı kontrol et
    boxes = row.iloc[0].get('mineral_boxes', None)
    if not boxes or 'label' not in boxes:
        # Eğer mineral_boxes'ta label yoksa diğer sütunları kontrol et
        for col, value in row.iloc[0].items():
            if isinstance(value, str) and 'label' in value:
                boxes = value
                break
    if not boxes or 'label' not in boxes:
        raise ValueError("Doğru bir 'boxes' değeri bulunamadı!")
    return boxes

# 6. Label dosyalarını oluşturma
base_dir = r"C:\Users\90553\Downloads\archive (2)\dataset_split"
output_base_dir = base_dir  # Çıktı yolu
os.makedirs(output_base_dir, exist_ok=True)

for split in ["train", "test", "valid"]:
    split_dir = os.path.join(base_dir, split)
    split_output_dir = os.path.join(output_base_dir, split, "images")
    os.makedirs(split_output_dir, exist_ok=True)

    for mineral_name in mineral_ids.keys():
        mineral_dir = os.path.join(split_dir, "images", mineral_name)
        if not os.path.exists(mineral_dir):
            continue

        mineral_output_dir = os.path.join(split_output_dir, mineral_name)
        os.makedirs(mineral_output_dir, exist_ok=True)

        for image_file in os.listdir(mineral_dir):
            if not image_file.endswith(".jpg"):
                continue

            image_path = os.path.join(mineral_dir, image_file)
            image_filename = os.path.basename(image_path).lower()  # Sadece dosya adını al

            # Excel'deki filename sütunu ile eşleşme kontrolü
            row = data[data['filename'] == image_filename]
            if row.empty:
                print(f"Filename not found in Excel: {image_filename}")
                print(f"Available filenames in Excel: {data['filename'].tolist()[:5]}")  # İlk 5 dosya adını göster
                continue

            # En yüksek confidence değerli box'u seçme
            boxes = get_correct_boxes(row)
            highest_conf_box = get_highest_confidence_box(boxes)
            x_center, y_center, width, height = convert_box_coordinates(highest_conf_box)

            # ID belirleme
            mineral_id = mineral_ids[mineral_name]

            # Terminalde gösterim
            print(f"Processing: {image_file}")
            print(f"ID: {mineral_id}, x_center: {x_center}, y_center: {y_center}, width: {width}, height: {height}")

            # Etiket dosyasını sadece mevcutsa oluşturma
            label_path = os.path.join(mineral_output_dir, f"{os.path.splitext(image_file)[0]}.txt")
            
            if not os.path.exists(label_path):  # Etiket dosyası zaten varsa, üzerine yazma
                with open(label_path, 'w') as f:
                    f.write(f"{mineral_id} {x_center} {y_center} {width} {height}\n")
            else:
                print(f"Label file already exists for {image_filename}, skipping...")

print("Label dosyaları başarıyla oluşturuldu!")