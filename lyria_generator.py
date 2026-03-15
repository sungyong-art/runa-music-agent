import asyncio
import wave
import os
import sys
import io
from google import genai
from google.genai import types

# 구글 제미나이 API 키 설정
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("❌ 오류: GEMINI_API_KEY 환경 변수가 설정되지 않았습니다.")
client = genai.Client(api_key=api_key, http_options={'api_version': 'v1alpha'})

async def generate_music(prompt="lo-fi hip hop, chill", duration_seconds=15, output_filename="generated_music.wav"):
    print(f"🎵 Lyria 3 음악 생성을 시작합니다. (프롬프트: '{prompt}', 길이: {duration_seconds}초)")
    
    audio_chunks = []
    
    async def receive_audio(session):
        try:
            async for message in session.receive():
                if message.server_content and message.server_content.audio_chunks:
                    audio_chunks.append(message.server_content.audio_chunks[0].data)
        except asyncio.CancelledError:
            pass
            
    try:
        # 모델은 'models/lyria-realtime-exp' 사용
        async with client.aio.live.music.connect(model='models/lyria-realtime-exp') as session, asyncio.TaskGroup() as tg:
            # 서버 메시지를 받을 태스크 생성
            audio_task = tg.create_task(receive_audio(session))
            
            # 1. 원하는 음악 프롬프트와 가중치 설정
            await session.set_weighted_prompts(
                prompts=[
                    types.WeightedPrompt(text=prompt, weight=1.0),
                ]
            )
            
            # 2. 음악 생성 설정 (BPM, 온도 등 지정 가능 / 기본값 작동)
            await session.set_music_generation_config(
                config=types.LiveMusicGenerationConfig(bpm=90, temperature=1.0)
            )
            
            # 3. 재생 (스트리밍 시작) 요청
            await session.play()
            
            # 원하는 초(duration_seconds) 만큼 스트리밍을 수신하며 대기합니다.
            print(f"⏳ 데이터를 수신하는 중... ({duration_seconds}초)")
            await asyncio.sleep(duration_seconds)
            
            # 대기가 끝나면 오디오 수신 태스크를 강제 종료합니다.
            audio_task.cancel()
            
    except Exception as e:
        print(f"❌ API 연결 오류 발생: {e}")
        return

    # 수신된 바이너리 오디오 조각(PCM)들을 하나의 wav 파일로 묶기
    if audio_chunks:
        full_audio_data = b''.join(audio_chunks)
        # Lyria 실시간 오디오 사양: 48kHz, 16-bit, 2 channels (Stereo)
        with wave.open(output_filename, 'wb') as wf:
            wf.setnchannels(2)        
            wf.setsampwidth(2)        
            wf.setframerate(48000)    
            wf.writeframes(full_audio_data)
        print(f"✅ 음악 성공적으로 완성! 저장된 파일: {output_filename}")
    else:
        print("❌ 수신된 오디오 데이터가 없습니다.")

if __name__ == "__main__":
    # 실행 예시
    asyncio.run(generate_music(prompt="Lofi chill beats for coding, minimal melody", duration_seconds=15, output_filename="test_lyria.wav"))
