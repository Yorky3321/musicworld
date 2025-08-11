import os
from pathlib import Path
import django_heroku
import dj_database_url
# ⚠ 正確設定 BASE_DIR：專案根目錄（與 manage.py 同層）
BASE_DIR = Path(__file__).resolve().parent.parent

# 安全設定
SECRET_KEY = '請換成你自己的 secret key'
DEBUG = True  # 開發用 True，部署請設 False
ALLOWED_HOSTS = ['*']

# 安裝的應用
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'myapp',
    'widget_tweaks',
    'music'

]

# 中介層
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mysite.urls'

# 模板設定
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # 如果有共用 templates 資料夾
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
LOGIN_REDIRECT_URL = '/'
WSGI_APPLICATION = 'mysite.wsgi.application'

# 資料庫本地開發用
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)
# 密碼驗證器
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# 語系與時區
LANGUAGE_CODE = 'zh-hant'
TIME_ZONE = 'Asia/Taipei'
USE_I18N = True
USE_TZ = True

# 靜態檔案（CSS, JS, 圖片）
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"] # 專案內 static 資料夾
# 靜態檔案優化（Optional）
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT = BASE_DIR / 'staticfiles'    # collectstatic 用
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')  # 加入 static support
# 自訂用戶模型（如果有用 CustomUser）
AUTH_USER_MODEL = 'myapp.CustomUser'

# 預設自動欄位型別
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_URL = '/login/'

django_heroku.settings(locals())