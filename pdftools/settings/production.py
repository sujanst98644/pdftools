from .base import *
import os

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS","").split(",")

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

DEBUG = False
