# 🌍 GeoSearch_AI: Mineral Exploration using Satellite Data
### مشروع منجم السكري - التعرف على المناطق التي بها نفس المعادن

هذا المشروع يستخدم الذكاء الاصطناعي وتحليل البيانات الجيومكانية (Geospatial Data) للبحث عن البصمات الطيفية للمعادن في المناطق الجيولوجية، مع التركيز على بيانات منجم السكري.

## 🚀 المميزات (Features)
* **Signature Extraction:** استخراج البصمة الطيفية للمعادن من ملفات `.nc`.
* **Mineral Detection:** خوارزمية لتحديد أماكن تواجد المعادن بناءً على العينات المرجعية.
* **Data Handling:** التعامل مع ملفات البيانات العلمية المعقدة (NetCDF4).

## 🛠️ المتطلبات (Setup)
لتشغيل البرنامج على جهازك، تأكد من تثبيت المكتبات التالية:
`pip install numpy xarray netCDF4 matplotlib`

## 📂 هيكل المشروع (Project Structure)
* `scripts/mineral_detector.py`: المحرك الأساسي للكشف عن المعادن.
* `scripts/signature_extractor.py`: معالج البصمات الطيفية.
* `sukkari_sample.nc`: عينة البيانات الجغرافية المستخدمة.

---
*Developed by: [Mohamed Reda]* *reBuyTech Cloud Solutions*
