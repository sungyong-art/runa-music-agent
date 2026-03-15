import os
import sys
import io
import glob
import random
import asyncio
import datetime
import traceback
import json

import google.genai as genai
from google.genai import types

from lyria_generator import generate_music
from video_renderer import render_video
from youtube_uploader import upload_video
from youtube_auth import get_authenticated_service
from trend_analyzer import fetch_global_trends

def add_watermark(image_path, title):
    print(f"✨ Pure Visual Mode: Keeping video clean without text overlays...")
    # 텍스트를 넣지 않기로 결정함 (미니멀리즘 글로벌 트렌드 반영)
    return

async def generate_seo_metadata(client, topic):
    print("\n🧠 Global Strategy Activation: Generating English SEO Metadata...")
    if not client:
        return None
    
    prompt = f"""
You are a World-Class Global YouTube Content Strategist.
Create HIGH-CLICK-THROUGH-RATE YouTube Title, Description, and Tags for a GLOBAL audience in ENGLISH.

- Theme: {topic['title']}
- Music Style: {topic['music_prompt']}

Respond ONLY in pure JSON format (without backticks) as follows:
{{
    "title": "Stunning catchy title with emojis (English)",
    "description": "Engaging description in English including keywords for global reach, music info, and relevant hashtags.",
    "tags": ["Lofi", "AI_Music", "Global_Beats", "Chill", "Electronic"]
}}
"""
    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash', # Using 2.0-flash for speed/reliability
            contents=prompt
        )
        text = response.text.strip()
        if text.startswith("```json"):
            text = text[7:-3]
        elif text.startswith("```"):
            text = text[3:-3]
            
        data = json.loads(text.strip())
        print(f"✅ Global SEO Success! (Title: {data.get('title', 'N/A')})")
        return data
    except Exception as e:
        print(f"⚠️ SEO Generation Error (Using Fallback): {e}")
        return None
def find_fallback_image(index=0, image_prompt=""):
    """테마에 맞는 고품질 이미지를 Unsplash에서 다운로드합니다."""
    import urllib.request
    
    # 테마에 맞는 Unsplash 큐레이션 이미지 (세로 9:16 비율)
    # Unsplash 특정 사진 ID를 사용해 항상 분위기 있는 이미지 보장
    curated_images = [
        "https://images.unsplash.com/photo-1519501025264-65ba15a82390?w=1080&h=1920&fit=crop",  # 네온 도시 야경
        "https://images.unsplash.com/photo-1508739773434-c26b3d09e071?w=1080&h=1920&fit=crop",  # 벚꽃 / 평화로운 자연
        "https://images.unsplash.com/photo-1534796636912-3b95b3ab5986?w=1080&h=1920&fit=crop",  # 레트로 신스웨이브
        "https://images.unsplash.com/photo-1515462277126-2dd0c162007a?w=1080&h=1920&fit=crop",  # 사이버펑크 비 오는 거리
        "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=1080&h=1920&fit=crop",  # 카페 커피
        "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1080&h=1920&fit=crop",  # 열대 해변 석양
        "https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=1080&h=1920&fit=crop",  # 도서관 / 공부
        "https://images.unsplash.com/photo-1462331940025-496dfbfc7564?w=1080&h=1920&fit=crop",  # 우주 / 은하
    ]
    
    url = curated_images[index % len(curated_images)]
    output_path = f"fallback_img_{index}.jpg"
    
    try:
        print(f"🌐 테마 큐레이션 이미지 다운로드 중... (index={index})")
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response, open(output_path, 'wb') as out_file:
            out_file.write(response.read())
        print(f"✅ 테마 이미지 다운로드 완료: {output_path}")
        return output_path
    except Exception as e:
        print(f"⚠️ 이미지 다운로드 실패: {e}")
        image_files = glob.glob("*.png") + glob.glob("*.jpg")
        if image_files:
            return image_files[0]
    return None

async def generate_new_thumbnail(client, prompt, output_path="generated_bg.png", is_shorts=False):
    print(f"🎨 구글 Imagen 엔진 접속 중: 썸네일/배경 이미지 실시간 합성 시도...")
    if not client:
        return None
    try:
        aspect_ratio = "9:16" if is_shorts else "16:9"
        result = client.models.generate_images(
            model='imagen-3.0-generate-002',
            prompt=prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
                aspect_ratio=aspect_ratio,
            )
        )
        if result.generated_images:
            image_data = result.generated_images[0].image.image_bytes
            with open(output_path, 'wb') as f:
                f.write(image_data)
            print(f"✅ 새 배경 이미지 생성 완료! ({output_path})")
            return output_path
    except Exception as e:
        print(f"⚠️ Imagen 3 생성 권한/오류 문제로 기존 이미지를 우선 사용합니다. 사유: {e}")
    return None

def get_topics():
    # 글로벌 트렌드 및 다양한 장르를 반영한 랜덤 주제 풀
    return [
        # Lofi / Chill
        {
            "music_prompt": "Lofi chill beats for coding, minimal melody, cozy vibe, rainy day", 
            "image_prompt": "A beautiful lo-fi style anime illustration of a rainy night. Cozy room, a person coding on laptop. Purple and orange neon lighting.",
            "title": "Cozy Lofi Beats for Coding ☕ (AI Generated)"
        },
        {
            "music_prompt": "Asian lofi hip hop, traditional instruments mixed with modern beats, peaceful", 
            "image_prompt": "A serene traditional Asian temple at dusk, lo-fi anime art style, cherry blossoms falling, soft glowing lanterns.",
            "title": "Asian Lofi Hip Hop 🌸 Peaceful Vibes (AI Music)"
        },
        # Electronic / Synthwave
        {
            "music_prompt": "Synthwave midnight drive, retro 80s, driving bass, electronic", 
            "image_prompt": "Retrowave 80s synthwave style digital art. A cool sports car driving on a neon highway under a digital sunset grid.",
            "title": "Midnight Drive Synthwave 🚗 [Retro AI Music]"
        },
        {
            "music_prompt": "Cyberpunk dark mid-tempo bass, futuristic, intense, gritty electronic", 
            "image_prompt": "Cyberpunk city street at night, neon lights, highly detailed, futuristic sci-fi metropolis, pouring rain.",
            "title": "Dark Cyberpunk Bass 🦾 Dystopian Mix (AI Original)"
        },
        # Jazz / Café
        {
            "music_prompt": "Smooth jazz for a rainy coffee shop, saxophone and piano, relaxing, cozy background", 
            "image_prompt": "A cozy Parisian cafe interior on a rainy afternoon, warm yellow lighting, a cup of coffee on a wooden table, outside street view.",
            "title": "Rainy Cafe Smooth Jazz ☕ Relaxing BGM [AI Generated]"
        },
        {
            "music_prompt": "Bossa nova acoustic guitar, sunny beach vibe, light percussion, relaxing summer", 
            "image_prompt": "A beautiful tropical beach at sunset, vibrant colors, gentle waves, a hammock between two palm trees, aesthetic illustration.",
            "title": "Sunset Bossa Nova 🌴 Relaxing Summer Vibes [AI Music]"
        },
        # Ambient / Focus
        {
            "music_prompt": "Ambient study music, piano and soft textures, relaxing, focus", 
            "image_prompt": "A peaceful aesthetic scene of an open window overlooking a calm lake at dawn. Soft pastel colors, studio ghibli style, relaxing.",
            "title": "Relaxing Piano Ambient for Focus 📚 [AI Original]"
        },
        {
            "music_prompt": "Deep space ambient drone, cosmic, relaxing, infinite, atmospheric", 
            "image_prompt": "A breathtaking view of a nebula in deep space, glowing stars, vast cosmic galaxy, hyper-realistic, majestic.",
            "title": "Deep Space Ambient 🌌 Cosmic Focus Music (AI generated)"
        }
    ]

async def get_trendy_topics(client):
    # 트렌드 파일이 있는지 확인
    trend_file = "music_trends.json"
    if not os.path.exists(trend_file):
        await fetch_global_trends(client)
    
    try:
        with open(trend_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("trends", [])
    except:
        return []

async def run_single_mission(client, index, topics):
    print(f"\n" + "-"*30)
    print(f"🎬 [콘텐츠 {index+1}/3] 생성 시퀀스 시작")
    print("-"*30)
    
    # 0. 설정 (55초 = 유튜브 쇼츠 피드 최적화, 60초 이상은 쇼츠 제외됨!)
    MUSIC_GENERATE_DURATION = 30
    TARGET_VIDEO_DURATION = 55
    IS_SHORTS = True
    AUDIO_FILE = f"luna_track_{index}.wav"
    VIDEO_FILE = f"luna_upload_{index}.mp4"
    
    # 1. 테마 선정 (동적 트렌드 반영)
    if topics:
        topic = topics[index % len(topics)]
    else:
        topic = random.choice(get_topics()) 
        
    print(f"🌍 글로벌 트렌드 테마 적용: {topic['title']}")
    
    image_file = await generate_new_thumbnail(client, topic['image_prompt'], output_path=f"bg_{index}.png", is_shorts=IS_SHORTS)
    if not image_file:
        image_file = find_fallback_image(index=index, image_prompt=topic.get('image_prompt',''))
        
    if not image_file:
        print("❌ 이미지 에셋 누락으로 중단")
        return
        
    add_watermark(image_file, topic['title'])
    
    # 2. 음악 생성 (실패 시 재시도 1회)
    for attempt in range(2):
        await generate_music(prompt=topic['music_prompt'], duration_seconds=MUSIC_GENERATE_DURATION, output_filename=AUDIO_FILE)
        if os.path.exists(AUDIO_FILE) and os.path.getsize(AUDIO_FILE) > 1024:
            print(f"✅ 음악 파일 확인 완료 ({os.path.getsize(AUDIO_FILE)//1024}KB)")
            break
        elif attempt == 0:
            print(f"⚠️ 음악 생성 실패, 1회 재시도 중...")
            await asyncio.sleep(3)
        else:
            print(f"❌ 음악 생성 최종 실패 - 영상 미생성")
            return
    
    # 3. 비디오 렌더링
    render_video(image_file, AUDIO_FILE, VIDEO_FILE, target_duration=TARGET_VIDEO_DURATION, is_shorts=IS_SHORTS)
    
    # 4. 예약 시간 계산 (오후 6시, 8시, 10시)
    now = datetime.datetime.now()
    publish_hour = [18, 20, 22][index]
    publish_time = datetime.datetime(now.year, now.month, now.day, publish_hour, 0, 0)
    
    if now >= publish_time:
        publish_time += datetime.timedelta(days=1)
        
    publish_at_iso = (publish_time - datetime.timedelta(hours=9)).isoformat() + "Z"
    
    # 5. 유튜브 예약 업로드
    seo_data = await generate_seo_metadata(client, topic)
    if seo_data:
        upload_title = seo_data.get('title', topic['title'])
        desc = f"{seo_data.get('description', '')}\n\n[Runa Music AI Automation]\nPrompt: {topic['music_prompt']}\n#AI #Music #GlobalTrends"
        tags = seo_data.get('tags', ["AI", "GlobalMusic"])
    else:
        upload_title = topic['title']
        desc = "AI Generated Global Music by Luna."
        tags = ["AI"]

    try:
        youtube_service = get_authenticated_service()
        upload_video(youtube_service, VIDEO_FILE, upload_title, desc, tags, publish_at=None)
        print(f"✅ 유튜브 즉시 공개 업로드 완료! [{upload_title}]")
    except Exception as e:
        print(f"❌ 업로드 실패: {e}")
        traceback.print_exc()
        # 실패한 업로드 정보 저장 (다음 실행에서 재시도 가능)
        try:
            failed = []
            if os.path.exists("failed_uploads.json"):
                with open("failed_uploads.json", "r") as f:
                    failed = json.load(f)
            failed.append({"file": VIDEO_FILE, "title": upload_title, "desc": desc, "tags": tags, "time": datetime.datetime.now().isoformat()})
            with open("failed_uploads.json", "w") as f:
                json.dump(failed, f, ensure_ascii=False, indent=2)
            print(f"💾 실패 정보 저장 완료 -> failed_uploads.json")
        except:
            pass

async def main():
    print("="*60)
    print(f"🚀 [에이전트 루나] {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - 글로벌 트렌드 자동화")
    print("="*60)
    
    client = None
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.environ.get("GEMINI_API_KEY")
    try:
        client = genai.Client(api_key=api_key, http_options={'api_version': 'v1alpha'})
    except:
        pass
    
    # 미션 시작 전 실시간 트렌드 수집 및 업데이트
    await fetch_global_trends(client)
    topics = await get_trendy_topics(client)
        
    for i in range(3):
        await run_single_mission(client, i, topics)
        await asyncio.sleep(5)

    print("\n" + "="*60)
    print("✨ [루나 시스템] 글로벌 트렌드 반영 미션 완료")
    print("="*60)

if __name__ == "__main__":
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    except AttributeError:
        pass
    
    asyncio.run(main())
