import os
import json
import requests
from fastapi import FastAPI, HTTPException
from google import genai
from google.genai import types

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

def get_latest_csv():
    response = requests.get(GITHUB_CSV_URL)
    response.raise_for_status()
    return response.text


# -----------------------
# Main API (AI Agent Version)
# -----------------------
@app.get("/ask-zone/{zone_name}")
async def query_zone(zone_name: str):
    try:
        # 1. ดึงข้อมูล CSV ดิบจาก GitHub
        csv_content = get_latest_csv()

        # 2. ตรวจสอบ API Key ของ Gemini
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise Exception("GOOGLE_API_KEY not found in Render environment variables")

        # 3. เริ่มต้นสร้าง Client ของ Gemini
        client = genai.Client(api_key=api_key)

        # 4. วางคำสั่ง (Prompt) มอบหมายงานให้ AI ไปคิดวิเคราะห์
        prompt_text = f"""
        Analyze the following CSV route data for Zone: '{zone_name}'.
        
        CSV Data:
        {csv_content}
        
        Please process this data and perform the optimization using the business rules strictly.
        """

        # 5. ใส่กฎเหล็ก (System Instruction) และกำหนด Output Format
        generate_config = types.GenerateContentConfig(
            temperature=0.1,  # ตั้งค่าต่ำเพื่อให้ AI ตอบนิ่งที่สุด ไม่คิดแหวกแนว
            system_instruction=(
                "You are a Logistics Route Optimization Specialist.\n"
                "Task: Analyze the provided CSV data to calculate the optimal fleet size and route sequence for KEX Express.\n\n"
                
                "Definitions & Business Rules:\n"
                "- Task Priority: '1 - SHOP' (High priority, before 12:00 PM), '2 - PSP' (Medium), '3 - RTSP' (Standard).\n"
                "- Stop Identification: Map 'Stop ID' to stop_number, 'Stop Name' to stop_name.\n"
                "- Work Volume: 'Parcels' indicates the item count at each stop.\n"
                "- Distance Calculation: 'Leg Dist (km)' is the distance between current and previous stop.\n"
                "- Estimated Completion Time: Operational hours 08:00 AM to 07:00 PM. Assume average truck speed of 30 km/h. "
                "Add exactly 25 minutes for stop processing time at each PICKUP/RETURN TO HUB stop.\n"
                "- Load Balancing: Maximum capacity of 4-wheel truck is 200 parcels. Aim for 90% load factor (approx 180 parcels) per vehicle.\n"
                "- Constraint Check: If a route cannot be completed within 08:00-19:00 due to high volume, split the route and suggest an additional vehicle.\n\n"
                
                "Output Format: You MUST return ONLY a raw JSON string matching this exact structure, with no markdown block formatting (do not wrap in ```json):\n"
                "{\n"
                "  \"zone_summary\": {\n"
                "    \"zone_name\": \"string\",\n"
                "    \"total_parcels\": integer,\n"
                "    \"total_vehicles_needed\": integer\n"
                "  },\n"
                "  \"routes\": [\n"
                "    {\n"
                "      \"truck_id\": \"string\",\n"
                "      \"load_percentage\": \"string\",\n"
                "      \"total_distance_km\": float,\n"
                "      \"estimated_completion_time\": \"HH:MM\",\n"
                "      \"stops_sequence\": [\n"
                "        {\n"
                "          \"stop_number\": \"string\",\n"
                "          \"stop_name\": \"string\",\n"
                "          \"priority\": \"string\",\n"
                "          \"action\": \"START/PICKUP/RETURN TO HUB\"\n"
                "        }\n"
                "      ]\n"
                "    }\n"
                "  ]\n"
                "}"
            ),
            response_mime_type="application/json"  # บังคับให้ Gemini จ่ายผลลัพธ์เป็นโครงสร้าง JSON
        )

        # 6. ส่งงานให้ AI โมเดลคำนวณ (ใช้ gemini-2.5-flash เพื่อความเร็วและฉลาดพอในงานนี้)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt_text,
            config=generate_config
        )

        # 7. แปลงผลลัพธ์ Text JSON จาก AI ให้กลายเป็นวัตถุ JSON ของ Python ส่งกลับไปที่หน้าเว็บ
        return json.loads(response.text)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
