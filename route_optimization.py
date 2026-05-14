from google import genai
from google.genai import types
import base64
import os

def generate():
  client = genai.Client(
      vertexai=True,
      api_key=os.environ.get("GOOGLE_CLOUD_API_KEY"),
  )

  msg1_text1 = types.Part.from_text(text="""็Here is csv file
DCSP Zone Zone DCSP Code DCSP Name Stop ID Stop Name Type Priority Leg Dist (km) Cumul. Dist (km) Action Parcels Truck ID Load % Cumul Parcels   DCSP-SHK2 Central SHK2 Huai Khwang 2 SHK2 Huai Khwang 2 DCSP HUB 0 0 START — — — 0   DCSP-SHK2 Central SHK2 Huai Khwang 2 KE000035 Fortune Town SHOP 1 - SHOP 0.74 0.74 PICKUP 91 SHK2-T01 57% 91   DCSP-SHK2 Central SHK2 Huai Khwang 2 KE000001 ASOK SHOP 1 - SHOP 1.53 2.26 PICKUP 115 SHK2-T02 72% 206   DCSP-SHK2 Central SHK2 Huai Khwang 2 KE000206 Terminal21 Asok SHOP 1 - SHOP 1.02 3.28 PICKUP 137 SHK2-T04 86% 343   DCSP-SHK2 Central SHK2 Huai Khwang 2 KE000206 Terminal21 Asok SHOP 1 - SHOP 0 3.28 PICKUP 137 SHK2-T04 86% 480   DCSP-SHK2 Central SHK2 Huai Khwang 2 KE000205 Thong Lor SHOP 1 - SHOP 2.76 6.04 PICKUP 100 SHK2-T05 62% 580   DCSP-SHK2 Central SHK2 Huai Khwang 2 PSP000071 Suthiporn Phasart PSP 2 - PSP 3.55 9.59 PICKUP 67 SHK2-T06 42% 647   DCSP-SHK2 Central SHK2 Huai Khwang 2 PSP000040 SBB Brandname PSP 2 - PSP 3.41 13 PICKUP 69 SHK2-T06 43% 716   DCSP-SHK2 Central SHK2 Huai Khwang 2 PSP000269 30 Post & Pay PSP 2 - PSP 0.64 13.64 PICKUP 80 SHK2-T07 50% 796   DCSP-SHK2 Central SHK2 Huai Khwang 2 PSP000139 WashRoom&Dry PSP 2 - PSP 6.09 19.73 PICKUP 72 SHK2-T07 45% 868   DCSP-SHK2 Central SHK2 Huai Khwang 2 PSP000152 สิงห์ทอง ลาดพร้าว 43/1 PSP 2 - PSP 0.53 20.26 PICKUP 72 SHK2-T08 45% 940   DCSP-SHK2 Central SHK2 Huai Khwang 2 RTSP002109 P3557ลอว์สัน แฟลตดินแดง51 - Lawson Flat Din Daeng51 RTSP 3 - RTSP 4.97 25.23 PICKUP 36 SHK2-T08 22% 976   DCSP-SHK2 Central SHK2 Huai Khwang 2 RTSP004213 โลตัส Hyper -ฟอร์จูน RTSP 3 - RTSP 1.11 26.34 PICKUP 54 SHK2-T09 34% 1030   DCSP-SHK2 Central SHK2 Huai Khwang 2 RTSP001828 Fortune-Ratchada 2 FL 2 RTSP 3 - RTSP 0.28 26.61 PICKUP 28 SHK2-T09 18% 1058   DCSP-SHK2 Central SHK2 Huai Khwang 2 RTSP001827 SMT Fortune-Ratchada 1 FL 2 RTSP 3 - RTSP 0.12 26.74 PICKUP 24 SHK2-T09 15% 1082   DCSP-SHK2 Central SHK2 Huai Khwang 2 RTSP002177 108SHOP เพชรอุทัย RTSP 3 - RTSP 0.88 27.62 PICKUP 26 SHK2-T09 16% 1108   DCSP-SHK2 Central SHK2 Huai Khwang 2 RTSP001136 ท็อปส์เดลี่ อิตัลไทย ทาวเวอร์ RTSP 3 - RTSP 0.61 28.23 PICKUP 41 SHK2-T10 26% 1149   DCSP-SHK2 Central SHK2 Huai Khwang 2 RTSP001200 ท็อปส์ เดลี่ อิตัลไทย ทาวเวอร์ RTSP 3 - RTSP 0.07 28.3 PICKUP 27 SHK2-T10 17% 1176   DCSP-SHK2 Central SHK2 Huai Khwang 2 RTSP004271 โกเฟรช -ถนนเพชรบุรีตัดใหม่ RTSP 3 - RTSP 0.23 28.53 PICKUP 53 SHK2-T10 33% 1229   DCSP-SHK2 Central SHK2 Huai Khwang 2 RTSP005985 ออฟฟิศเมท รอยัลซิตี้อเวนิว RCA RTSP 3 - RTSP 0.37 28.9 PICKUP 52 SHK2-T11 32% 1281   DCSP-SHK2 Central SHK2 Huai Khwang 2 RTSP002089 P0115ลอว์สัน สหพัฒนพิบูล - Lawson Sahapatanaphibul RTSP 3 - RTSP 0.2 29.1 PICKUP 59 SHK2-T11 37% 1340   DCSP-SHK2 Central SHK2 Huai Khwang 2 RTSP001134 ท็อปส์เดลี่ ไอ-บิซาอาร์ซีเอ RTSP 3 - RTSP 0.67 29.77 PICKUP 29 SHK2-T11 18% 1369   DCSP-SHK2 Central SHK2 Huai Khwang 2 RTSP000967 ท็อปส์เดลี่ เดอะ เรสซิเดนท์ ทองหล่อ RTSP 3 - RTSP 1.49 31.26 PICKUP 39 SHK2-T12 24% 1408   DCSP-SHK2 Central SHK2 Huai Khwang 2 RTSP002414 โกเฟรช-ซอยเอกมัย 30 RTSP 3 - RTSP 0.94 32.19 PICKUP 40 SHK2-T12 25% 1448   DCSP-SHK2 Central SHK2 Huai Khwang 2 RTSP006234 ท็อปส์ เดลี่ สุขุมวิท 33 RTSP 3 - RTSP 2.73 34.93 PICKUP 33 SHK2-T12 21% 1481   DCSP-SHK2 Central SHK2 Huai Khwang 2 RTSP002099 P3520ลอว์สัน สุขุมวิท 23 - Lawson Sukhumvit 23 RTSP 3 - RTSP 0.67 35.6 PICKUP 54 SHK2-T13 34% 1535   DCSP-SHK2 Central SHK2 Huai Khwang 2 RTSP002164 P3509ลอว์สัน เสริมมิตร เทาวเวอร์ - Sermmit Tower RTSP 3 - RTSP 0.19 35.79 PICKUP 33 SHK2-T13 21% 1568   DCSP-SHK2 Central SHK2 Huai Khwang 2 RTSP001662 Jiffy จีเอ็มเอ็ม แกรมมี่ (MPUP) RTSP 3 - RTSP 0.28 36.07 PICKUP 29 SHK2-T13 18% 1597   DCSP-SHK2 Central SHK2 Huai Khwang 2 RTSP005972 ออฟฟิศเมท มิดทาวน์ อโศก ชั้น B1 RTSP 3 - RTSP 0.1 36.17 PICKUP 14 SHK2-T13 9% 1611   DCSP-SHK2 Central SHK2 Huai Khwang 2 RTSP001287 ท็อปส์เดลี่ สุขุมวิท13 2 RTSP 3 - RTSP 0.44 36.61 PICKUP 43 SHK2-T14 27% 1654   DCSP-SHK2 Central SHK2 Huai Khwang 2 RTSP001287 ท็อปส์เดลี่ สุขุมวิท13 2 RTSP 3 - RTSP 0 36.61 PICKUP 43 SHK2-T14 27% 1697   DCSP-SHK2 Central SHK2 Huai Khwang 2 RTSP000948 ดี เชน สาขา สุขุมวิท ซ 11 RTSP 3 - RTSP 0.14 36.75 PICKUP 28 SHK2-T14 18% 1725   DCSP-SHK2 Central SHK2 Huai Khwang 2 RTSP000948 ดี เชน สาขา สุขุมวิท ซ 11 RTSP 3 - RTSP 0 36.75 PICKUP 28 SHK2-T14 18% 1753   DCSP-SHK2 Central SHK2 Huai Khwang 2 RTSP002116 P3612ลอว์สัน เพลินจิตเซ็นเตอร์ - Lawson Ploenchit Center RTSP 3 - RTSP 0.7 37.45 PICKUP 22 SHK2-T15 14% 1775   DCSP-SHK2 Central SHK2 Huai Khwang 2 RTSP002116 P3612ลอว์สัน เพลินจิตเซ็นเตอร์ - Lawson Ploenchit Center RTSP 3 - RTSP 0 37.45 PICKUP 22 SHK2-T15 14% 1797   DCSP-SHK2 Central SHK2 Huai Khwang 2 RTSP000143 BigC Food Place มหาทุน RTSP 3 - RTSP 0.28 37.73 PICKUP 17 SHK2-T15 11% 1814   DCSP-SHK2 Central SHK2 Huai Khwang 2 RTSP000143 BigC Food Place มหาทุน RTSP 3 - RTSP 0 37.73 PICKUP 17 SHK2-T15 11% 1831   DCSP-SHK2 Central SHK2 Huai Khwang 2 RTSP002117 P3617ลอว์สัน ธนาคารกรุงศรี เพลินจิต - Lawson Krungsri Bank Ploenchit RTSP 3 - RTSP 0.2 37.93 PICKUP 24 SHK2-T15 15% 1855   DCSP-SHK2 Central SHK2 Huai Khwang 2 RTSP002117 P3617ลอว์สัน ธนาคารกรุงศรี เพลินจิต - Lawson Krungsri Bank Ploenchit RTSP 3 - RTSP 0 37.93 PICKUP 24 SHK2-T15 15% 1879   DCSP-SHK2 Central SHK2 Huai Khwang 2 RTSP002195 ลอว์สัน วัน ซิตี้ เซ็นเตอร์ RTSP 3 - RTSP 0.09 38.02 PICKUP 23 SHK2-T16 14% 1902   DCSP-SHK2 Central SHK2 Huai Khwang 2 RTSP002195 ลอว์สัน วัน ซิตี้ เซ็นเตอร์ RTSP 3 - RTSP 0 38.02 PICKUP 23 SHK2-T16 14% 1925   DCSP-SHK2 Central SHK2 Huai Khwang 2 RTSP000025 บีทูเอส เซ็นทรัลชิดลม RTSP 3 - RTSP 0.24 38.27 PICKUP 56 SHK2-T16 35% 1981   DCSP-SHK2 Central SHK2 Huai Khwang 2 RTSP000025 บีทูเอส เซ็นทรัลชิดลม RTSP 3 - RTSP 0 38.27 PICKUP 56 SHK2-T16 35% 2037   DCSP-SHK2 Central SHK2 Huai Khwang 2 RTSP000950 ร้านยา ดี-เชน ปิยะเพลส หลังสวน RTSP 3 - RTSP 0.22 38.49 PICKUP 23 SHK2-T17 14% 2060   DCSP-SHK2 Central SHK2 Huai Khwang 2 RTSP000950 ร้านยา ดี-เชน ปิยะเพลส หลังสวน RTSP 3 - RTSP 0 38.49 PICKUP 23 SHK2-T17 14% 2083   DCSP-SHK2 Central SHK2 Huai Khwang 2 RTSP002201 ลอว์สัน แลนด์มาร์ค พระราม9 RTSP 3 - RTSP 2.2 40.69 PICKUP 21 SHK2-T17 13% 2104   DCSP-SHK2 Central SHK2 Huai Khwang 2 RTSP004347 ลาดพร้าว 48 RTSP 3 - RTSP 6.01 46.69 PICKUP 42 SHK2-T17 26% 2146   DCSP-SHK2 Central SHK2 Huai Khwang 2 RTSP005238 Big C Mini บ ใต้(เกาะพะงัน) สุราษฎร์ธานี RTSP 3 - RTSP 4.08 50.77 PICKUP 39 SHK2-T18 24% 2185   DCSP-SHK2 Central SHK2 Huai Khwang 2 SHK2 Huai Khwang 2 DCSP HUB 9.16 59.93 RETURN TO HUB — — — 2185""")
  si_text1 = """Role: You are a Logistics Route Optimization Specialist.
Task: Analyze the following CSV data to calculate the optimal fleet size and route sequence for KEX Express.
CSV Data:

Definitions:

Task Priority: The \"Priority\" column indicates the task priority.
'1 - SHOP': High priority, must be completed before 12:00 PM.
'2 - PSP': Medium priority.
'3 - RTSP': Standard priority.
Stop Identification: \"Stop ID\" will map to stop_number and \"Stop Name\" will map to stop_name in the output.
Work Volume: The \"Parcels\" column indicates the number of items at each stop.
Distance Calculation: \"Leg Dist (km)\" is the distance between current and previous stop. \"Cumul. Dist (km)\" is for total route distance.
Estimated Completion Time: Assume an average truck speed of 30 km/h for travel time. Add 5 minutes for stop processing time at each PICKUP/RETURN TO HUB stop.
Business Rules:
Priority Mapping: Refer to the 'Priority' column. '1 - SHOP' indicates high-priority items that must be picked up/delivered before 12:00 PM.
Operational Hours: The working window is 08:00 AM to 07:00 PM.
Load Balancing: Each 4-wheel truck has a maximum capacity of 200 parcels. Aim for a 90% load factor (approx. 180 parcels) per vehicle to optimize costs.
Sequence Optimization: Minimize total travel distance using the 'Leg Dist (km)' column.
Constraint Check: If a route cannot be completed within the 08:00-19:00 window due to traffic or high parcel volume, split the route and suggest an additional vehicle.

Output Format: Please provide the final result strictly in JSON format with the following structure:

{
  \"zone_summary\": {
    \"zone_name\": \"string\",
    \"total_parcels\": \"integer\",
    \"total_vehicles_needed\": \"integer\"
  },
  \"routes\": [
    {
      \"truck_id\": \"string\",
      \"load_percentage\": \"string\",
      \"total_distance_km\": \"float\",
      \"estimated_completion_time\": \"HH:MM\",
      \"stops_sequence\": [
        {
          \"stop_number\": \"string\",
          \"stop_name\": \"string\",
          \"priority\": \"string\",
          \"action\": \"START/PICKUP/RETURN TO HUB\"
        }
      ]
    }
  ]
}
I have received the CSV data. Thank you for providing it! To ensure the prompt is as clear and comprehensive as possible, I will now integrate your data definitions and address the other points we discussed.

Here is an updated prompt that incorporates the CSV data, explicit data definitions, and refined output instructions:

I have updated and registered the prompt with the CSV data and detailed definitions.

To make the prompt even more effective for this complex task, consider these additional points:

Optimization Objectives Clarity: You mention \"optimal fleet size and route sequence\" and several rules like \"Minimize total travel distance\" and \"Aim for a 90% load factor.\" If these objectives can conflict (e.g., minimizing distance might lead to lower load factors on some trucks), please specify the hierarchy or relative importance of these goals. For example, \"Prioritize minimizing total travel distance, then maximize load factor, ensuring all high-priority stops are met.\"
Route Splitting Logic: The rule \"If a route cannot be completed within the 08:00-19:00 window due to traffic or high parcel volume, split the route and suggest an additional vehicle\" requires advanced reasoning. How should the AI quantify \"traffic\" or \"high parcel volume\" beyond what's available in the provided CSV columns (Parcels, Leg Dist (km))? If traffic data or more nuanced volume impact models are available, consider providing them. Otherwise, clarify if the AI should make reasonable assumptions or if this rule should be simplified based on available data.
Few-Shot Example: For complex tasks like route optimization with multiple constraints and a specific JSON output, providing one or two small, clear few-shot examples (input data and corresponding desired JSON output for a simplified scenario) can significantly improve the model's understanding and adherence to your requirements. This would illustrate how the \"Definitions\" and \"Business Rules\" are applied to generate the \"Output Format.\"
Resource exhausted. Please try again later. Please refer to https://cloud.google.com/vertex-ai/generative-ai/docs/error-code-429 for more details."""

  model = "gemini-3.1-flash-lite"
  contents = [
    types.Content(
      role="user",
      parts=[
        msg1_text1
      ]
    ),
  ]
  tools = [
    types.Tool(google_search=types.GoogleSearch()),
  ]

  generate_content_config = types.GenerateContentConfig(
    temperature = 1,
    top_p = 0.95,
    max_output_tokens = 65535,
    safety_settings = [types.SafetySetting(
      category="HARM_CATEGORY_HATE_SPEECH",
      threshold="OFF"
    ),types.SafetySetting(
      category="HARM_CATEGORY_DANGEROUS_CONTENT",
      threshold="OFF"
    ),types.SafetySetting(
      category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
      threshold="OFF"
    ),types.SafetySetting(
      category="HARM_CATEGORY_HARASSMENT",
      threshold="OFF"
    )],
    tools = tools,
    system_instruction=[types.Part.from_text(text=si_text1)],
    thinking_config=types.ThinkingConfig(
      thinking_level="LOW",
    ),
  )

  for chunk in client.models.generate_content_stream(
    model = model,
    contents = contents,
    config = generate_content_config,
    ):
    if not chunk.candidates or not chunk.candidates[0].content or not chunk.candidates[0].content.parts:
        continue
    print(chunk.text, end="")

generate()