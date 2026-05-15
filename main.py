import os
import json
import io
import datetime
import requests
import pandas as pd
from fastapi import FastAPI, HTTPException

app = FastAPI()

# -----------------------
# Health check
# -----------------------
@app.get("/")
def root():
    return {"status": "ok"}


# -----------------------
# CSV source
# -----------------------
GITHUB_CSV_URL = (
    "https://raw.githubusercontent.com/"
    "daruntoey/green-route-optimization/main/"
    "data/Kerry_RouteSum_with_Parcels.csv"
)

def get_latest_csv_dataframe() -> pd.DataFrame:
    """ดาวน์โหลด CSV จาก GitHub แล้วแปลงเป็น Pandas DataFrame"""
    response = requests.get(GITHUB_CSV_URL)
    response.raise_for_status()
    # ใช้ io.StringIO เพื่อให้อ่าน text เป็น dataframe ได้โดยตรง
    df = pd.read_csv(io.StringIO(response.text))
    return df


# -----------------------
# Optimization Logic (Python Function)
# -----------------------
def optimize_logistics_data(df: pd.DataFrame, zone_filter: str) -> dict:
    """
    ฟังก์ชันประมวลผลคำนวณเส้นทางและจัดกลุ่มข้อมูลตามกฎธุรกิจ
    """
    # 1. กรองข้อมูลเฉพาะโซนที่ต้องการ (ทำ Case-insensitive เพื่อป้องกันพิมพ์ใหญ่-เล็กไม่ตรง)
    # สมมติว่าใน CSV มีคอลัมน์ชื่อ 'Zone' หรือ 'zone_name' (ปรับให้ตรงกับคอลัมน์จริงใน CSV ของคุณ)
    # ในที่นี้ขอกรองแบบแปลงเป็น string และหาคำที่ใกล้เคียง
    zone_column = 'Zone' if 'Zone' in df.columns else df.columns[0] 
    df_filtered = df[df[zone_column].astype(str).str.contains(zone_filter, case=False, na=False)].copy()
    
    if df_filtered.empty:
        raise ValueError(f"No data found for zone: {zone_filter}")

    # แทนค่า NaN/Null ด้วยค่าว่างหรือ 0 ป้องกัน Error ตอนคำนวณ
    df_filtered.fillna({
        'Parcels': 0, 
        'Leg Dist (km)': 0.0, 
        'Priority': '3 - RTSP', 
        'Stop ID': '', 
        'Stop Name': ''
    }, inplace=True)

    # 2. ค้นหาคอลัมน์รถยนต์ (สมมติว่าชื่อ 'Truck ID' หรือ 'Vehicle ID')
    truck_column = 'Truck ID' if 'Truck ID' in df_filtered.columns else 'Vehicle ID'
    if truck_column not in df_filtered.columns:
        # ถ้าไม่มีคอลัมน์รถ ให้สร้าง Mock ขึ้นมาจำลอง หรือใช้คอลัมน์แรกๆ ที่ระบุตัวรถ
        df_filtered[truck_column] = 'SHK2-T-Default'

    routes_output = []
    total_parcels_zone = 0

    # 3. จัดกลุ่มข้อมูลตามคันรถ (Truck ID)
    grouped = df_filtered.groupby(truck_column, sort=False)

    for truck_id, group in grouped:
        stops_sequence = []
        total_parcels_truck = 0
        total_distance_truck = 0
        
        # เวลาเริ่มต้นทำงาน 08:00 น. ตามกฎ
        current_time = datetime.datetime.strptime("08:00", "%H:%M")
        
        for idx, row in group.iterrows():
            parcels = int(row.get('Parcels', 0))
            leg_dist = float(row.get('Leg Dist (km)', 0))
            
            total_parcels_truck += parcels
            total_distance_truck += leg_dist
            
            # คำนวณเวลาเดินทาง: เวลา (ชั่วโมง) = ระยะทาง / 30 กม./ชม.
            travel_time_minutes = (leg_dist / 30) * 60
            
            # บวกเวลาจอด (Processing Time) จุดละ 25 นาทีสำหรับทุกจุดที่มี action
            processing_time_minutes = 25
            
            # อัปเดตเวลาปัจจุบัน
            current_time += datetime.timedelta(minutes=travel_time_minutes + processing_time_minutes)
            
            # กำหนด Action
            stop_name_str = str(row.get('Stop Name', ''))
            if "HUB" in stop_name_str.upper() or "SHK2" in stop_name_str.upper():
                action = "RETURN TO HUB"
            elif idx == group.index[0]:
                action = "START"
            else:
                action = "PICKUP"
                
            stops_sequence.append({
                "stop_number": str(row.get('Stop ID', f"ST{idx}")),
                "stop_name": stop_name_str,
                "priority": str(row.get('Priority', '3 - RTSP')),
                "action": action
            })
            
        # คำนวณ % การโหลดรถ (ความจุสูงสุด 200 ชิ้น, เป้าหมาย 90% คือ 180 ชิ้น)
        # load_percentage = (จำนวนพัสดุจริง / ความจุสูงสุด 200 ชิ้น) * 100
        load_pct_val = min(int((total_parcels_truck / 200) * 100), 100)
        
        total_parcels_zone += total_parcels_truck
        
        routes_output.append({
            "truck_id": str(truck_id),
            "load_percentage": f"{load_pct_val}%",
            "total_distance_km": round(total_distance_truck, 2),
            "estimated_completion_time": current_time.strftime("%H:%M"),
            "stops_sequence": stops_sequence
        })

    # 4. ประกอบร่าง JSON สรุปภาพรวมของโซน
    final_result = {
        "zone_summary": {
            "zone_name": zone_filter,
            "total_parcels": total_parcels_zone,
            "total_vehicles_needed": len(routes_output)
        },
        "routes": routes_output
    }
    
    return final_result


# -----------------------
# Main API Endpoint
# -----------------------
@app.get("/ask-zone/{zone_name}")
async def query_zone(zone_name: str):
    try:
        # 1. โหลดข้อมูล CSV ล่าสุดจาก GitHub
        df = get_latest_csv_dataframe()

        # 2. คำนวณผ่านฟังก์ชัน Python (รวดเร็ว, แม่นยำ และโครงสร้างตรงตามต้องการแน่นอน)
        result = optimize_logistics_data(df, zone_name)
        
        return result

    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
