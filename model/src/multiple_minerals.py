import os
import shutil

# Kaynak klasör yolu
base_dir = r"C:\Users\90553\Downloads\archive (2)\model_images"
# Yeni klasörlerin oluşturulacağı dizin
output_base_dir = r"C:\Users\90553\Downloads\archive (2)\model_images_limited"

# Sabit görsel sayısı
fixed_image_count = 200

# Mineral adları
mineral_names = [
    "agate", "albite", "amethyst", "arsenopyrite", "beryl", "calcite", "cassiterite", "chalcedony", 
    "corundum", "diopside", "fluorite", "gold", "gypsum", "hematite", "magnetite", "microcline", 
    "pyrite", "quartz", "silver", "topaz"
]

# Yeni klasörlerdeki görselleri kopyalama
def create_limited_folders(base_dir, output_base_dir, fixed_image_count, mineral_names):
    # Eğer output klasörü yoksa oluştur
    os.makedirs(output_base_dir, exist_ok=True)

    for mineral_name in mineral_names:
        mineral_folder_path = os.path.join(base_dir, mineral_name)
        if not os.path.isdir(mineral_folder_path):
            print(f"{mineral_name} klasörü bulunamadı.")
            continue
        
        # Görselleri al
        image_files = [f for f in os.listdir(mineral_folder_path) if f.lower().endswith('.jpg')]
        
        # Eğer 'pyrite' klasörü ise 196 görsel al
        if mineral_name == "pyrite":
            selected_images = image_files[:196]
        else:
            selected_images = image_files[:fixed_image_count]  # Sabit sayıda görsel seç

        # Yeni mineral klasörü oluştur
        new_mineral_folder_path = os.path.join(output_base_dir, mineral_name)
        os.makedirs(new_mineral_folder_path, exist_ok=True)

        # Seçilen görselleri yeni klasöre kopyala
        for image_file in selected_images:
            src_path = os.path.join(mineral_folder_path, image_file)
            dst_path = os.path.join(new_mineral_folder_path, image_file)
            shutil.copy(src_path, dst_path)
        
        print(f"{mineral_name} klasörüne {len(selected_images)} görsel kopyalandı.")

# İşlemi başlat
create_limited_folders(base_dir, output_base_dir, fixed_image_count, mineral_names)
