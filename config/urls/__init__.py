import environ, os
from ..settings.base import BASE_DIR

# 환경 변수 읽기
env = environ.Env()
# 프로젝트 루트의 .env 파일 경로를 명시적으로 지정/ .env가 있는 config의 상위 디렉토리까지 가야함
environ.Env.read_env(os.path.join(BASE_DIR.parent, '.env')) # .env 파일을 읽어옴

environment = env('DJANGO_ENV', default='development')

if environment == 'production':
    from .production import *
else:
    from .development import *