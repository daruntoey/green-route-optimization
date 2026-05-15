import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google import genai
from google.genai import types

app = FastAPI(title="KEX Route Optimization API")

# ตั้งค่า Client สำหรับ Vertex AI / Gemini
def get_ai_client():
    api_key = os.environ.get("GOOGLE_CLOUD_API_KEY")
    if not api_key:
        raise ValueError("Environment variable GOOGLE_CLOUD_API_KEY is not set")
    return genai.Client(vertexai=True, api_key=api_key)

# โครงสร้างสำหรับการรับข้อมูลผ่าน API (หากต้องการส่ง CSV ใหม่ผ่าน API)
class RouteRequest(BaseModel):
    csv_data: str

# ย้าย System Instruction มาไว้เป็นตัวแปรกลาง
SYSTEM_PROMPT = """Role: You are a Logistics Route Optimization Specialist.
Task: Analyze the provided CSV data to calculate optimal fleet size and route sequence for KEX Express.
Definitions:
'1 - SHOP': High priority, must be completed before 12:00 PM.
'2 - PSP': Medium priority.
'3 - RTSP': Standard priority.
Load Balancing: Max capacity 200 parcels (Target 90%).
Output Format: Strictly JSON."""

@app.get("/")
def home():
    return {"status": "online", "message": "KEX Optimization API is ready"}

@app.post("/optimize")
async def optimize_route(request: RouteRequest):
    try:
        client = get_ai_client()
        
        # กำหนดเนื้อหาที่จะส่งให้ AI
        contents = [
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=f"Here is the CSV data:\n{request.csv_data}")]
            )
        ]

        # ตั้งค่าการเรียกใช้ Model
        generate_config = types.GenerateContentConfig(
            temperature=0.2, # ปรับลดลงเพื่อให้คำตอบนิ่งและแม่นยำขึ้น
            max_output_tokens=65535,
            system_instruction=[types.Part.from_text(text=SYSTEM_PROMPT)],
            response_mime_type="application/json" # บังคับให้ AI ตอบเป็น JSON
        )

        response = client.models.generate_content(
            model="gemini-2.0-flash", # แนะนำให้ใช้ตัวล่าสุด
            contents=contents,
            config=generate_config
        )

        return response.text # ส่งคืนผลลัพธ์ JSON จาก AI
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
