import os
import shutil
import random

# Kaynak klasör yolu ve yeni klasör oluşturulacak dizin
base_dir = r"C:\Users\90553\Downloads\archive (2)\model_images_limited"
output_base_dir = r"C:\Users\90553\Downloads\archive (2)\dataset_split"

# Eğitim, doğrulama ve test oranları
train_ratio = 0.75
valid_ratio = 0.15
test_ratio = 0.10

# Mineral adları
mineral_names = [
    "agate", "albite", "amethyst", "arsenopyrite", "beryl", "calcite", "cassiterite", "chalcedony", 
    "corundum", "diopside", "fluorite", "gold", "gypsum", "hematite", "magnetite", "microcline", 
    "pyrite", "quartz", "silver", "topaz"
]

# Eğitim, doğrulama ve test için verileri ayıran fonksiyon
def split_data(base_dir, output_base_dir, mineral_names, train_ratio, valid_ratio, test_ratio):
    # Eğer output klasörleri yoksa oluştur
    os.makedirs(output_base_dir, exist_ok=True)
    
    for split in ["train", "test", "valid"]:
        split_images_dir = os.path.join(output_base_dir, split, "images")
        os.makedirs(split_images_dir, exist_ok=True)

    for mineral_name in mineral_names:
        mineral_folder_path = os.path.join(base_dir, mineral_name)
        if not os.path.isdir(mineral_folder_path):
            print(f"{mineral_name} klasörü bulunamadı.")
            continue
        
        # Görselleri al
        image_files = [f for f in os.listdir(mineral_folder_path) if f.lower().endswith('.jpg')]
        
        # Görselleri karıştır
        random.shuffle(image_files)

        # Görselleri eğitim, doğrulama ve test setlerine ayır
        total_images = len(image_files)
        train_count = int(total_images * train_ratio)
        valid_count = int(total_images * valid_ratio)
        test_count = total_images - train_count - valid_count

        # Verileri ayırma
        train_images = image_files[:train_count]
        valid_images = image_files[train_count:train_count + valid_count]
        test_images = image_files[train_count + valid_count:]

        # Yeni klasörler oluştur
        for split, image_list in zip(["train", "valid", "test"], [train_images, valid_images, test_images]):
            split_images_dir = os.path.join(output_base_dir, split, "images", mineral_name)
            os.makedirs(split_images_dir, exist_ok=True)
            
            for image_file in image_list:
                src_path = os.path.join(mineral_folder_path, image_file)
                dst_path = os.path.join(split_images_dir, image_file)
                shutil.copy(src_path, dst_path)
        
        print(f"{mineral_name} için eğitim: {len(train_images)}, doğrulama: {len(valid_images)}, test: {len(test_images)} görsel ayrıldı.")

# İşlemi başlat
split_data(base_dir, output_base_dir, mineral_names, train_ratio, valid_ratio, test_ratio)
