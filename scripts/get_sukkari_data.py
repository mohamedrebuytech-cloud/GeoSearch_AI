import pystac_client
import planetary_computer
import stackstac
import xarray as xr
import os

# 1. الاتصال بمصدر البيانات
catalog = pystac_client.Client.open(
    "https://planetarycomputer.microsoft.com/api/stac/v1",
    ignore_conformance=True,
)

# 2. إحداثيات جبل السكري
bbox = [34.78, 24.93, 34.85, 24.97] 

# 3. البحث عن الصور
search = catalog.search(
    collections=["sentinel-2-l2a"],
    bbox=bbox,
    datetime="2023-01-01/2023-12-31",
    query={"eo:cloud_cover": {"lt": 2}}, 
)

items = search.item_collection()

if len(items) == 0:
    print("❌ ملقتش صور للمنطقة دي.")
else:
    selected_item = planetary_computer.sign(items[0])
    print(f"📡 لقيت صورة بتاريخ: {selected_item.properties['datetime']}")

    # 4. اختيار الطبقات
    bands = ["B04", "B03", "B02", "B08", "B11"]
    
    # تحويل لـ Stack
    stack = stackstac.stack(
        selected_item, 
        assets=bands, 
        bounds_latlon=bbox, 
        epsg=32636
    )

    print("⏳ جاري تنظيف البيانات العميقة (Deep Cleaning)...")
    data = stack.compute()
    
    # تحويل من DataArray لـ Dataset عشان الحفظ يكون أسهل
    ds = data.to_dataset(name="sukkari_data")

    # --- الحل الجذري لمشكلة الـ dtype والـ projection ---
    # بنحول أي "Object" معقد لنص أو بنحذفه لو مش ضروري للحفظ
    for v in list(ds.coords) + list(ds.data_vars):
        if ds[v].dtype == 'object':
            ds[v] = ds[v].astype(str)
            
    # حذف الـ attributes اللي بتعمل Crash
    ds.attrs = {} 
    for var in ds.variables:
        ds[var].attrs = {}
    # --------------------------------------------------

    output_path = "sukkari_sample.nc"
    
    # الحفظ بصيغة NetCDF
    ds.to_netcdf(output_path)
    
    print("-" * 30)
    print(f"✅ مبروك يا رضا! الملف اتحفظ أخيراً")
    print(f"📍 المسار: {os.path.abspath(output_path)}")
    print("-" * 30)