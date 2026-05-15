import os 
import json 
import requests 
from fastapi import FastAPI, HTTPException 
from google import genai 
from google.genai 
import types 

app = FastAPI()

# ---------- Root endpoint ---------- 
@app.get("/") 
def root(): 
    return {"status": "ok"} 


# ---------- GitHub CSV ---------- 
GITHUB_CSV_URL = ( 
    "https://raw.githubusercontent.com/" 
    "daruntoey/green-route-optimization/main/" 
    "data/Kerry_RouteSum_with_Parcels.csv" ) 


def get_latest_csv(): 
    try: 
        response = requests.get(GITHUB_CSV_URL, timeout=30) 
        response.raise_for_status() 

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

        # 1. Load latest CSV 
        csv_content = get_latest_csv() 
        
        # 2. Build prompt 
        prompt_text = f""" Analyze the following CSV data for zone: {zone_name} Data: {csv_content} Return JSON only with: - total_vehicles_needed - stop_sequences - estimated_completion_time """ 
        
        # 3. Gemini config 
        config = types.GenerateContentConfig( temperature=0.1, system_instruction=( "You are a Logistics JSON Expert. " "Return only raw JSON." ), response_mime_type="application/json" ) 
        
        # 4. Generate response 
        response = client.models.generate_content( model="gemini-2.5-flash", contents=prompt_text, config=config ) 
        
        # 5. Return JSON return 
        json.loads(response.text) 
        
    except Exception as e: 
        
        raise HTTPException( 
            status_code=500, 
            detail=str(e) 
        )
