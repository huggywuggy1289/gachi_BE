# 베이스 이미지로 Python 3.12 사용
FROM python:3.12-slim

# 컨테이너 내에서 작업할 디렉토리 설정
WORKDIR / earth

# 필요 파일들을 복사
COPY requirements.txt .

# 필요한 패키지 설치 (필요한 경우, Linux 패키지 포함)
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get remove -y gcc && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

# 프로젝트의 소스 코드 복사
COPY ./earth /earth

# 환경 변수를 설정 (개발 모드의 예)
ENV DJANGO_SETTINGS_MODULE=earth.settings
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV SECRET_KEY_FILE=/earth/secret_key.json

# Django 프로젝트가 필요로 하는 static 파일 모으기
# RUN python manage.py collectstatic --noinput

# 컨테이너 실행 시 명령어
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
