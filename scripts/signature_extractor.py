import rasterio
import numpy as np
import matplotlib.pyplot as plt

def extract_spectral_signature(image_path, x_coord, y_coord):
    with rasterio.open(image_path) as src:
        # قراءة جميع الطبقات (Bands) للنقطة المحددة
        # src.index(lon, lat) لو معاك إحداثيات، أو x, y لو بكسل
        pixel_values = [band[x_coord, y_coord] for band in src.read()]
        
        print(f"✅ تم استخراج البصمة الطيفية للنقطة ({x_coord}, {y_coord}):")
        print(pixel_values)
        return np.array(pixel_values)

# دي تجربة بسيطة لرسم الصورة عشان تدوس عليها
def prototype_viewer(image_path):
    with rasterio.open(image_path) as src:
        # قراءة الصورة للعرض (بناخد أول 3 Bands اللي هما RGB)
        img = src.read([1, 2, 3])
        # تعديل الترتيب للعرض
        img_display = np.moveaxis(img, 0, -1)
        
        plt.imshow(img_display)
        plt.title("Click on the mineral area")
        plt.show()

print("Script Ready! Waiting for data...")