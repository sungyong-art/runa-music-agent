import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

# API 권한 범위 설정 (유튜브 업로드 전용)
scopes = ["https://www.googleapis.com/auth/youtube.upload"]

# 클라우드 콘솔에서 다운받은 인증 파일 이름
client_secrets_file = "client_secret.json"

def get_authenticated_service():
    credentials = None
    # 이전에 저장된 인증 토큰(역할 접근 여권)이 있는지 확인
    if os.path.exists('token.json'):
        credentials = Credentials.from_authorized_user_file('token.json', scopes)
        
    # 유효한 인증 정보가 없거나 만료된 경우 재발급(로그인 유도)
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            # 브라우저를 열어 구글 계정 인증 창 호출
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                client_secrets_file, scopes)
            credentials = flow.run_local_server(port=0)
            
        # 획득한 토큰을 저장하여 추후 자동 로그인
        with open('token.json', 'w') as token_file:
            token_file.write(credentials.to_json())

    # 인증된 유튜브 서비스 객체 반환
    youtube = googleapiclient.discovery.build("youtube", "v3", credentials=credentials)
    return youtube

if __name__ == "__main__":
    print("루나 시스템 통신 시작: YouTube API 인증 접속 중...")
    try:
        if not os.path.exists(client_secrets_file):
            print(f"❌ 오류: '{client_secrets_file}' 파일이 폴더에 없습니다. 구글 클라우드에서 다운로드 후 넣어주세요.")
        else:
            youtube_service = get_authenticated_service()
            print("✅ 시스템 권한 획득 성공! 이제 루나가 해당 유튜브 계정의 컨트롤을 시작할 수 있습니다.")
    except Exception as e:
        print(f"❌ 인증 실패: {e}")
