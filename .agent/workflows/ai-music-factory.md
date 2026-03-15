---
description: AI 음악 대량 생산 시스템 - 하루 100곡 자동 생성 (Music Factory v2)
---

# AI MUSIC FACTORY WORKFLOW v2
(조회수 최적화 대량 생산 시스템)

## 목표

AI가 다음을 자동 생성:
- 음악 아이디어 100~300개/일
- 음악 스타일, 제목, 가사, 생성 프롬프트
- 유튜브 메타데이터 (제목, 설명, 태그)

---

## 전체 시스템 구조

```
TREND ANALYZER
     ↓
IDEA GENERATOR
     ↓
STYLE GENERATOR
     ↓
TITLE GENERATOR
     ↓
LYRICS GENERATOR
     ↓
AI MUSIC GENERATOR
     ↓
AUDIO EXPORT
     ↓
VIDEO GENERATOR
     ↓
THUMBNAIL GENERATOR
     ↓
YOUTUBE SEO ENGINE
     ↓
UPLOAD SYSTEM
```

---

## STEP 1: TREND ANALYZER

분석 대상:
- YouTube music trends
- Spotify viral charts
- TikTok viral sounds

조회수 안정적 장르 (검증된 카테고리):
```
lofi study music     ← 가장 안정적
sleep music          ← 수요 지속
ambient music        ← 경쟁 낮음
phonk / dark phonk   ← 바이럴 가능성
city pop             ← 감성 소비층 타겟
synthwave / retro    ← 회고 감성
```

---

## STEP 2: IDEA GENERATOR

자동 아이디어 생성 예시:
```
rainy tokyo night
lonely astronaut in space
summer beach golden hour
nostalgic 90s street walk
cyberpunk city neon drive
cherry blossom spring afternoon
midnight coffee shop solitude
```

일일 생성 목표: 100~300 ideas

---

## STEP 3: SONG GENERATOR

각 아이디어에 대해 아래 4블록 생성:

1. STYLE
2. TITLE (3~5개)
3. LYRICS ([Intro][Verse1][Chorus][Bridge][Outro])
4. GENERATION_PROMPT

---

## STEP 4: BATCH GENERATION 시스템

Python 구조 예시:
```python
idea_list = load_ideas("ideas.csv")

for idea in idea_list:
    style = generate_style(idea)
    titles = generate_titles(idea)
    lyrics = generate_lyrics(idea)
    prompt = generate_music_prompt(idea)
    
    save_to_csv({
        "idea": idea,
        "style": style,
        "titles": titles,
        "lyrics": lyrics,
        "prompt": prompt
    })
    
    send_to_ai_music_generator(prompt)
```

---

## STEP 5: VIDEO GENERATOR

음악 → 영상 자동 변환

사용 가능한 영상 AI:
- Runway
- Pika
- Kling
- HeyGen (캐릭터용)

영상 스타일 예시:
```
lofi anime study girl with rain window
cyberpunk neon city night drive loop
aesthetic rainy window with candle
vintage cassette player rotating
```

---

## STEP 6: THUMBNAIL GENERATOR

이미지 AI:
- Midjourney
- Stable Diffusion
- Imagen 3 (Google, 현재 Runa Music 프로젝트에서 사용 중)

썸네일 스타일 예시:
```
anime girl in neon rainy city
retro cassette tape aesthetic background
lofi cozy study room warm lighting
synthwave sunset gradient horizon
```

---

## STEP 7: YOUTUBE SEO ENGINE

AI 자동 생성:

제목 형식:
```
[곡 제목] 🎵 [장르] [용도] Music | [감성 키워드]
예: Neon Rain 🌧️ Relaxing City Pop Night Drive Music | Lofi Study Chill
```

설명 형식:
```
[장르] music for [용도1], [용도2], and [용도3].
Perfect for [상황].

🎵 Track: [곡 제목]
🎨 Genre: [장르]
🌙 Mood: [분위기]

#[태그1] #[태그2] #[태그3]
```

태그 예시:
```
city pop, night drive, lofi music, study music, relaxing music,
chill beats, japanese music, aesthetic music, focus music
```

---

## STEP 8: UPLOAD AUTOMATION

업로드 구조:
- YouTube Data API v3 활용 (현재 프로젝트 youtube_uploader.py)
- 하루 3~10개 영상 예약 업로드
- 골든타임: 08:00 / 15:00 / 22:00 KST

---

## 자동화 JSON 구조 (전체)

```json
{
  "idea": "",
  "style": "",
  "titles": [],
  "lyrics": {
    "intro": "",
    "verse1": "",
    "chorus": "",
    "bridge": "",
    "outro": ""
  },
  "music_prompt": "",
  "video_prompt": "",
  "thumbnail_prompt": "",
  "youtube": {
    "title": "",
    "description": "",
    "tags": [],
    "scheduled_time": ""
  }
}
```

---

## 추천 채널 유형 (조회수 안정성 순위)

1. LoFi Study Music ★★★★★
2. Sleep / Ambient Music ★★★★★
3. City Pop Nights ★★★★
4. Synthwave / Retro Wave ★★★★
5. Phonk / Dark Phonk ★★★
6. AI Character Singer ★★★
