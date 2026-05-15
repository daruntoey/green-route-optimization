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


# ---------- Debug endpoint ----------
@app.get("/zones")
def get_zones():

    csv_content = get_latest_csv()

    df = pd.read_csv(
        StringIO(csv_content),
        encoding="cp874"
    )

    zones = (
        df["Zone"]
        .astype(str)
        .str.strip()
        .dropna()
        .unique()
        .tolist()
    )

    return {
        "zones": zones[:100]
    }


# ---------- API endpoint ----------
@app.get("/ask-zone/{zone_name}")
async def query_zone(zone_name: str):

    try:

        # 1. โหลด CSV
        csv_content = get_latest_csv()

        # 2. อ่าน CSV
        df = pd.read_csv(
            StringIO(csv_content),
            encoding="cp874"
        )

        # 3. clean columns
        df.columns = df.columns.str.strip()

        # 4. normalize zone column
        df["Zone_clean"] = (
            df["Zone"]
            .astype(str)
            .str.strip()
            .str.lower()
        )

        input_zone = zone_name.strip().lower()

        # 5. filter zone
        zone_df = df[
            df["Zone_clean"].str.contains(
                input_zone,
                na=False
            )
        ]

        # 6. ถ้าไม่เจอ
        if zone_df.empty:

            available_zones = (
                df["Zone"]
                .astype(str)
                .dropna()
                .unique()
                .tolist()
            )

            return {
                "zone": zone_name,
                "message": "No data found",
                "available_zones": available_zones[:20]
            }

        # 7. ลด rows
        zone_df = zone_df.head(50)

        # 8. ใช้เฉพาะ columns สำคัญ
        selected_df = zone_df[
            [
                "Zone",
                "Truck ID",
                "Stop Name",
                "Parcels",
                "Load %",
                "Cumul Parcels"
            ]
        ]

        filtered_csv = selected_df.to_csv(index=False)

        # 9. Prompt
        prompt_text = f"""
        Analyze logistics route data.

        Zone:
        {zone_name}

        CSV Data:
        {filtered_csv}

        Return JSON only.

        Required format:

        {{
          "zone": "...",
          "total_vehicles_needed": number,
          "stop_sequences": {{
              "truck_id": ["stop1", "stop2"]
          }},
          "estimated_completion_time": number
        }}
        """

        # 10. Config
        config = types.GenerateContentConfig(
            temperature=0.1,
            system_instruction=(
                "You are a logistics optimization expert. "
                "Always return valid clean JSON only. "
                "Preserve Thai language correctly."
            ),
            response_mime_type="application/json"
        )

        # 11. Generate
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt_text,
            config=config
        )

        # 12. Return JSON
        return json.loads(response.text)

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
