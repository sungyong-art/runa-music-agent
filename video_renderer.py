import os
import sys
import io
from moviepy.editor import ImageClip, AudioFileClip
import moviepy.audio.fx.all as afx
import moviepy.video.fx.all as vfx

def render_video(image_path, audio_path, output_path, target_duration=None, is_shorts=False):
    print(f"🎬 비디오 렌더링 시작...")
    print(f"👉 이미지 소스: {image_path}")
    print(f"👉 오디오 소스: {audio_path}")
    
    if not os.path.exists(image_path):
        print(f"❌ 오류: 이미지 파일 '{image_path}'이(가) 존재하지 않습니다.")
        return
    if not os.path.exists(audio_path):
        print(f"❌ 오류: 오디오 파일 '{audio_path}'이(가) 존재하지 않습니다.")
        return
        
    try:
        # 오디오 파일 불러오기
        audio_clip = AudioFileClip(audio_path)
        
        # 1시간 연속 재생 등 긴 영상을 위해 오디오 루핑
        if target_duration and target_duration > audio_clip.duration:
            print(f"🎵 오디오를 {target_duration}초 길이로 루프 매핑합니다.")
            audio_clip = afx.audio_loop(audioclip=audio_clip, duration=target_duration)
        else:
            target_duration = audio_clip.duration
            
        # 이미지 파일 불러오기 (오디오 길이만큼 지속시간 설정)
        image_clip = ImageClip(image_path).set_duration(target_duration)
        
        # 쇼츠용 (9:16) 크롭
        if is_shorts:
            w, h = image_clip.size
            target_w = int(h * 9 / 16)
            if target_w < w:
                image_clip = vfx.crop(image_clip, width=target_w, height=h, x_center=w/2, y_center=h/2)
                print("📱 쇼츠 비율(9:16)로 이미지를 자르기 완료.")

        # 이미지에 오디오 합치기
        video_clip = image_clip.set_audio(audio_clip)
        
        # 최종 MP4 파일로 내보내기 (초당 24프레임)
        # fps=24, 비디오 코덱은 libx264, 오디오 코덱은 aac 사용
        print(f"⏳ 렌더링을 진행합니다. (길이: 약 {int(target_duration)}초) 잠시만 기다려주세요...")
        video_clip.write_videofile(
            output_path, 
            fps=24, 
            codec="libx264", 
            audio_codec="aac",
            preset="ultrafast",     # 렌더링 속도 우선
            threads=4               # CPU 스레드 사용 수
        )
        
        print(f"✅ 영상 렌더링 완료! 완성된 파일: {output_path}")

    except Exception as e:
        print(f"❌ 렌더링 중 오류 발생: {e}")

if __name__ == "__main__":
    # 방금 생성한 음악과 이미지가 잘 인 코딩되는지 테스트합니다.
    # 제공된 이미지 경로 (절대 경로나 현재 폴더로 옮긴 이미지 이름 지정)
    # 지금은 테스트 목적으로 아래 폴더의 이미지와 test_lyria.wav 를 합칩니다.
    IMAGE_FILE = r"C:\Users\UserK\.gemini\antigravity\brain\29275e9a-df0e-4e80-ad37-eaea1f3dff69\lofi_background_1773233345825.png"
    AUDIO_FILE = "test_lyria.wav"
    OUTPUT_FILE = "final_output.mp4"
    
    render_video(IMAGE_FILE, AUDIO_FILE, OUTPUT_FILE)
