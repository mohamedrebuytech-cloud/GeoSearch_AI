import pystac_client
import planetary_computer
import stackstac
import rasterio

# 1. الاتصال بمخزن الصور (Planetary Computer التابع لمايكروسوفت)
catalog = pystac_client.Client.open(
    "https://planetarycomputer.microsoft.com/api/stac/v1",
    ignore_conformance=True,
)

# 2. تحديد المنطقة (مثلاً منطقة جبلية في البحر الأحمر مشهورة بالمعادن)
# إحداثيات تقريبية لمنطقة جبلية
area_of_interest = {
    "type": "Polygon",
    "coordinates": [[
        [33.5, 26.5], [33.6, 26.5], [33.6, 26.6], [33.5, 26.6], [33.5, 26.5]
    ]],
}

# 3. البحث عن أحدث صورة بدون سحب (Low Cloud Cover)
search = catalog.search(
    collections=["sentinel-2-l2a"],
    intersects=area_of_interest,
    datetime="2023-01-01/2023-12-31",
    query={"eo:cloud_cover": {"lt": 5}},
)

items = search.item_collection()
selected_item = planetary_computer.sign(items[0])

# 4. سحب الصورة وتحويلها لملف .tif عندنا
print(f"📡 لقيت صورة بتاريخ: {selected_item.properties['datetime']}")
# هنا بنسحب الـ Bands الأساسية (RGB + Infrared للبحث عن المعادن)
bands = ["B04", "B03", "B02", "B08", "B11", "B12"]
stack = stackstac.stack(selected_item, assets=bands)

# حفظ الصورة كتجربة
# ملاحظة: التحميل قد يستغرق دقيقة حسب سرعة النت
print("📥 جاري تحميل الصورة كـ Sample...")
# تكملة الكود للحفظ (هنستخدم rasterio)