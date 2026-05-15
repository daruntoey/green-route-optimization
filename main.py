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
# Main API
# -----------------------
@app.get("/ask-zone/{zone_name}")
async def query_zone(zone_name: str):
    try:
        # โหลด CSV
        csv_content = get_latest_csv()

        # โหลด API key
        api_key = os.getenv("GOOGLE_API_KEY")

        if not api_key:
            raise Exception("GOOGLE_API_KEY not found in Render environment variables")

        # สร้าง Gemini client
        client = genai.Client(api_key=api_key)

        # Prompt
        prompt_text = f"""
        Analyze the following CSV route data.

        Zone: {zone_name}

        Data:
        {csv_content}

        Return JSON only with:

        {{
          "zone": "...",
          "vehicles_needed": ...,
          "stop_sequence": [...],
          "estimated_completion_time": "..."
        }}
        """

        # Config
        generate_config = types.GenerateContentConfig(
            temperature=0.1,
            system_instruction=(
                "You are a logistics optimization expert. "
                "Return only raw JSON."
            ),
            response_mime_type="application/json"
        )

        # Generate
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt_text,
            config=generate_config
        )

        return json.loads(response.text)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
