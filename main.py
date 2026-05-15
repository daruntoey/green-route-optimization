import os
import requests
import pandas as pd
from fastapi import FastAPI, HTTPException
from google import genai
from google.genai import types

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/ask-zone/{zone_name}")
def ask_zone(zone_name: str):
    return {"zone": zone_name}

# URL ของไฟล์ CSV บน GitHub (ต้องเป็นลิ้งค์แบบ 'raw')
GITHUB_CSV_URL = "https://raw.githubusercontent.com/daruntoey/green-route-optimization/main/Kerry_RouteSum_with_Parcels.csv"

def get_latest_csv():
    try:
        response = requests.get(GITHUB_CSV_URL)
        response.raise_for_status()
        return response.text
    except Exception as e:
        return f"Error loading CSV: {str(e)}"

@app.get("/ask-zone/{zone_name}")
async def query_zone(zone_name: str):
    try:
        # 1. ดึงข้อมูล CSV ล่าสุดจาก GitHub
        csv_content = get_latest_csv()
        
        # 2. ตั้งค่า AI Client
        client = genai.Client(vertexai=True, api_key=os.environ.get("GOOGLE_CLOUD_API_KEY"))
        
        # 3. สร้าง Prompt ที่เน้นผลลัพธ์เป็น JSON
        prompt_text = f"""
        Analyze the following CSV data for the zone: {zone_name}.
        Data: {csv_content}
        
        Please provide the route optimization for this specific zone in JSON format only.
        Include total vehicles needed, stop sequences, and estimated completion time (within 08:00-19:00).
        """

        generate_config = types.GenerateContentConfig(
            temperature=0.1, # ต่ำเพื่อให้โครงสร้าง JSON นิ่ง
            system_instruction="You are a Logistics JSON Expert. Always return raw JSON code without Markdown backticks.",
            response_mime_type="application/json" # บังคับ Output เป็น JSON
        )

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt_text,
            config=generate_config
        )

        # 4. คืนค่าเป็น JSON Object ไปยัง User
        import json
        return json.loads(response.text)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
