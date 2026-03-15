import os
import sys
import io
from googleapiclient.http import MediaFileUpload

def upload_video(youtube, file_path, title, description, tags, category_id="10", publish_at=None):
    print(f"🚀 유튜브 업로드를 시작합니다: [{title}]")
    if publish_at:
        print(f"⏰ 예약 업로드 설정: {publish_at}")
    
    if not os.path.exists(file_path):
        print(f"❌ 오류: 업로드할 파일('{file_path}')을 찾을 수 없습니다.")
        return False
        
    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": category_id
        },
        "status": {
            "privacyStatus": "public" if not publish_at else "private",
            "selfDeclaredMadeForKids": False
        }
    }

    if publish_at:
        body["status"]["publishAt"] = publish_at

    try:
        print("⏳ 대용량 파일을 유튜브 서버로 전송 중입니다...")
        media = MediaFileUpload(file_path, chunksize=-1, resumable=True)
        request = youtube.videos().insert(
            part="snippet,status",
            body=body,
            media_body=media
        )
        
        response = request.execute()
        print(f"✅ 비디오 업로드/예약 성공! ID: {response['id']}")
        return True
    except Exception as e:
        print(f"❌ 업로드 중 오류 발생: {e}")
        return False
