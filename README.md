# 🚚 KEX Green Route Optimization API

ระบบ AI Agent สำหรับวิเคราะห์และจัดเส้นทางการรับพัสดุ (Pickup Optimization) ของ KEX Express โดยใช้ Google Gemini 2.0 Flash บน Vertex AI เพื่อคำนวณจำนวนรถและลำดับการวิ่งที่ประหยัดต้นทุนที่สุด

## 🌟 Features
- **Dynamic Data Fetching:** ดึงข้อมูล CSV ล่าสุดจาก GitHub โดยอัตโนมัติ
- **AI-Powered Analysis:** ใช้ Gemini 2.0 ในการคำนวณ Load Balancing (เป้าหมาย 200 ชิ้น/คัน)
- **Time-Aware Routing:** วางแผนงานภายใต้กรอบเวลา 08:00 - 19:00 น.
- **JSON Output:** คืนค่าผลลัพธ์เป็น JSON พร้อมนำไปเชื่อมต่อกับ Dashboard หรือ Mobile App

## 🏗️ Project Structure
```text
my-api/
├─ main.py            
├─ requirements.txt  
├─ Dockerfile         
└─ data/
   └─ Kerry_RouteSum_with_Parcels.csv 
