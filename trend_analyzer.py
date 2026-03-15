import json
import os
import sys
import io
import datetime
import re
from google import genai

async def fetch_global_trends(client):
    print("🌐 [에이전트 레오] 실시간 글로벌 음악 트렌드 분석 및 기획 중...")
    
    # AI Music Factory v2 사양에 맞춘 고도화된 프롬프트
    prompt = """
    You are 'Leo', a World-Class YouTube Algorithm Expert & Music Producer.
    Your mission is to identify the most viral music trends for 2026.
    
    Target high-view, evergreen genres:
    1. LoFi Study/Focus Music
    2. Deep Sleep/Ambient
    3. City Pop/Nostalgic Nights
    4. Phonk/Drift Music
    5. Asian Chill Lofi
    
    For each of the top 3 trends, provide:
    - 'title': Catchy YouTube title with emojis
    - 'music_prompt': Detailed Lyria-style music prompt (English, 2-3 sentences)
    - 'image_prompt': High-quality Imagen-style prompt (Anime/Aesthetic, 9:16 ratio)
    
    Respond in STRICT JSON format like this:
    {
        "last_updated": "2026-03-13",
        "trends": [
            {
                "title": "Title here",
                "music_prompt": "prompt here",
                "image_prompt": "prompt here"
            }
        ]
    }
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt
        )
        text = response.text.strip()
        
        # ```json ... ``` 블록 제거
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
            
        # JSON 유효성 확인
        data = json.loads(text)
        data["last_updated"] = datetime.datetime.now().strftime("%Y-%m-%d")
        
        with open("music_trends.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        print(f"✅ [레오] 트렌드 지도 업데이트 완료! (수집된 테마: {len(data['trends'])}개)")
        return data
    except Exception as e:
        print(f"⚠️ 트렌드 분석 중 오류 발생: {e}")
        # 기본값 유지
        return None
