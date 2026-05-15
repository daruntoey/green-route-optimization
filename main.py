import os
import json
import requests
import pandas as pd
from io import StringIO
from fastapi import FastAPI, HTTPException
from google import genai
from google.genai import types

app = FastAPI()

# ---------- Root endpoint ----------
@app.get("/")
def root():
    return {"status": "ok"}


# ---------- GitHub CSV ----------
GITHUB_CSV_URL = (
    "https://raw.githubusercontent.com/"
    "daruntoey/green-route-optimization/main/"
    "data/Kerry_RouteSum_with_Parcels.csv"
)


# ---------- Load CSV ----------
def get_latest_csv():
    try:
        response = requests.get(GITHUB_CSV_URL, timeout=30)
        response.raise_for_status()

        # FIX THAI ENCODING
        response.encoding = "cp874"

        return response.text

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error loading CSV: {str(e)}"
        )


# ---------- Gemini Client ----------
client = genai.Client(
    api_key=os.environ["GOOGLE_API_KEY"]
)


# ---------- API endpoint ----------
@app.get("/ask-zone/{zone_name}")
async def query_zone(zone_name: str):

    try:
        # 1. โหลด CSV
        csv_content = get_latest_csv()

        # 2. อ่าน CSV ด้วย pandas
        df = pd.read_csv(
            StringIO(csv_content),
            encoding="cp874"
        )

        # 3. filter เฉพาะ zone
        zone_df = df[
            df["Zone"].astype(str).str.contains(
                zone_name,
                case=False,
                na=False
            )
        ]

        # ถ้าไม่เจอข้อมูล
        if zone_df.empty:
            return {
                "zone": zone_name,
                "message": "No data found"
            }

        # 4. ลดจำนวน rows เพื่อลด token
        zone_df = zone_df.head(50)

        # 5. convert กลับเป็น CSV
        filtered_csv = zone_df.to_csv(index=False)

        # 6. Prompt
        prompt_text = f"""
        Analyze logistics route data for zone: {zone_name}

        CSV Data:
        {filtered_csv}

        Return JSON only.

        Required JSON structure:

        {{
          "zone": "...",
          "total_vehicles_needed": number,
          "stop_sequences": {{
              "route_id": ["stop1", "stop2"]
          }},
          "estimated_completion_time": number
        }}
        """

        # 7. Config
        config = types.GenerateContentConfig(
            temperature=0.1,
            system_instruction=(
                "You are a logistics optimization expert. "
                "Always return clean JSON only. "
                "Preserve Thai language correctly."
            ),
            response_mime_type="application/json"
        )

        # 8. Generate
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt_text,
            config=config
        )

        # 9. Parse JSON
        return json.loads(response.text)

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
