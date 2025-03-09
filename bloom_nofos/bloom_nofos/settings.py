"""
Django settings for bloom_nofos project.

Generated by 'django-admin startproject' using Django 4.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
import sys
from datetime import datetime
from pathlib import Path

import environ
import tomli
from django.utils.timezone import now

from .utils import cast_to_boolean, get_login_gov_keys

BASE_DIR = Path(__file__).resolve().parent.parent

# Initialise environment variables
env_file = ".env"

if cast_to_boolean(os.environ.get("IS_DOCKER", False)):
    env_file = ".env.docker"

is_prod = cast_to_boolean(os.environ.get("IS_PROD", False))
if is_prod:
    env_file = ".env.production"

env = environ.Env()
env_path = os.path.join(BASE_DIR, "bloom_nofos", env_file)

env_exists = os.path.exists(env_path)
if env_exists:
    environ.Env.read_env(env_path)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = cast_to_boolean(env.get_value("DEBUG", default=True))
print("=====")
print("DEBUG: {}".format(DEBUG))
if DEBUG:
    print("=====")
    if env_exists:
        print(".env file: {}".format(env_file))
    else:
        print("No .env file found at {}".format(env_path))

# Project version

DJVERSION_VERSION = None

with open(os.path.join(BASE_DIR, "..", "pyproject.toml"), "rb") as f:
    pyproject_data = tomli.load(f)
    DJVERSION_VERSION = pyproject_data["tool"]["poetry"]["version"]

# GitHub SHA

GITHUB_SHA = os.getenv("GITHUB_SHA", None)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

SECRET_KEY = env("SECRET_KEY", default="bad-secret-key-please-change")

API_TOKEN = env("API_TOKEN", default=None)

ALLOWED_HOSTS = [
    "0.0.0.0",
    "127.0.0.1",
    "localhost",
]

allowed_domain_string = env.get_value("DJANGO_ALLOWED_HOSTS", default="")
if allowed_domain_string:
    ALLOWED_HOSTS.extend(allowed_domain_string.split(","))


# SECURITY HEADERS
SECURE_SSL_REDIRECT = is_prod
SESSION_COOKIE_SECURE = is_prod
CSRF_COOKIE_SECURE = is_prod
CSRF_COOKIE_HTTPONLY = False
SECURE_BROWSER_XSS_FILTER = is_prod

# X-Frame-Options
X_FRAME_OPTIONS = "DENY"
# X-Content-Type-Options
SECURE_CONTENT_TYPE_NOSNIFF = is_prod

# Setting SECURE_SSL_REDIRECT on Google Cloud Run was causing infinite redirects without this
if is_prod:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# For sites that should only be accessed over HTTPS, instruct modern browsers to refuse to connect to your domain name via an insecure connection (for a given period of time)
if is_prod:
    SECURE_HSTS_SECONDS = 31536000

# Instructs the browser to send a full URL, but only for same-origin links. No referrer will be sent for cross-origin links.
SECURE_REFERRER_POLICY = "same-origin"

# Application definition

INSTALLED_APPS = [
    "martor",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "constance",
    "nofos.apps.NofosConfig",
    "users.apps.UsersConfig",
    "easyaudit",
    "djversion",
    "django_mirror",
    "ninja",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "easyaudit.middleware.easyaudit.EasyAuditMiddleware",
    "bloom_nofos.middleware.BadRequestMiddleware",
    "nofos.middleware.NofosLoginRequiredMiddleware",
]

ROOT_URLCONF = "bloom_nofos.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "bloom_nofos", "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "djversion.context_processors.version",
                "bloom_nofos.context_processors.template_context",
            ],
        },
    },
]

WSGI_APPLICATION = "bloom_nofos.wsgi.application"

# login backend

# Logging
# In production, log all errors to console
if not DEBUG:
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {
            "console": {
                "level": "ERROR",
                "class": "logging.StreamHandler",
            },
        },
        "loggers": {
            "django": {
                "handlers": ["console"],
                "level": "ERROR",
                "propagate": True,
            },
        },
    }

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

default_db_path = os.path.join(BASE_DIR, "db.sqlite3")

# if no "DATABASE_URL" env, fall back to the sqlite database
database_url = (
    env.get_value("DATABASE_URL", default=None) or f"sqlite:///{default_db_path}"
)

DATABASES = {"default": env.db_url_config(database_url)}

# If the flag as been set, configure to use proxy
if not is_prod and DATABASES["default"]["HOST"].startswith("/cloudsql"):
    DATABASES["default"]["HOST"] = "127.0.0.1"
    DATABASES["default"]["PORT"] = 5432

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, "static")

STATIC_URL = "static/"

# static files in the main app
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "bloom_nofos", "static"),
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Users
AUTH_USER_MODEL = "users.BloomUser"

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 8,
        },
    }
]


# MARTOR MARKDOWN FIELD

# Choices are: "semantic", "bootstrap"
MARTOR_THEME = "bootstrap"

# Global martor settings
# Input: string boolean, `true/false`
MARTOR_ENABLE_CONFIGS = {
    "emoji": "false",  # to enable/disable emoji icons.
    "imgur": "false",  # to enable/disable imgur/custom uploader.
    "mention": "false",  # to enable/disable mention
    "jquery": "true",  # to include/revoke jquery (require for admin default django)
    "living": "false",  # to enable/disable live updates in preview
    "spellcheck": "false",  # to enable/disable spellcheck in form textareas
    "hljs": "true",  # to enable/disable hljs highlighting in preview
}

# To show the toolbar buttons
MARTOR_TOOLBAR_BUTTONS = [
    "bold",
    "italic",
    # "horizontal",
    "heading",
    "pre-code",
    # "blockquote",
    "unordered-list",
    "ordered-list",
    #'image-link', 'image-upload', 'emoji',
    "link",
    "direct-mention",
    "toggle-maximize",
    "help",
]

# To setup the martor editor with title label or not (default is False)
MARTOR_ENABLE_LABEL = True

# Markdownify
MARTOR_MARKDOWNIFY_FUNCTION = "martor.utils.markdownify"  # default
MARTOR_MARKDOWNIFY_URL = "/martor/markdownify/"  # default

# Delay in miliseconds to update editor preview when in living mode.
MARTOR_MARKDOWNIFY_TIMEOUT = 0  # update the preview instantly
# or:
MARTOR_MARKDOWNIFY_TIMEOUT = 1000  # default

# Markdown extensions (default)
MARTOR_MARKDOWN_EXTENSIONS = [
    "markdown.extensions.extra",
    "markdown.extensions.nl2br",
    "markdown.extensions.smarty",
    "markdown.extensions.fenced_code",
    # Custom markdown extensions.
    # "martor.extensions.urlize",
    "martor.extensions.del_ins",  # ~~strikethrough~~ and ++underscores++
    "martor.extensions.mention",  # to parse markdown mention
    # "martor.extensions.emoji",  # to parse markdown emoji
    "martor.extensions.mdx_video",  # to parse embed/iframe video
    # "martor.extensions.escape_html",  # to handle the XSS vulnerabilities
]

# Markdown Extensions Configs
MARTOR_MARKDOWN_EXTENSION_CONFIGS = {}

# Markdown urls
MARTOR_UPLOAD_URL = ""  # Completely disable the endpoint
# or:
# MARTOR_UPLOAD_URL = "/martor/uploader/"  # default

MARTOR_SEARCH_USERS_URL = ""  # Completely disables the endpoint
# or:
# MARTOR_SEARCH_USERS_URL = "/martor/search-user/"  # default

# Markdown Extensions
# MARTOR_MARKDOWN_BASE_EMOJI_URL = 'https://www.webfx.com/tools/emoji-cheat-sheet/graphics/emojis/'     # from webfx
# MARTOR_MARKDOWN_BASE_EMOJI_URL = (
#     "https://github.githubassets.com/images/icons/emoji/"  # default from github
# )
# # or:
MARTOR_MARKDOWN_BASE_EMOJI_URL = ""  # Completely disables the endpoint
# MARTOR_MARKDOWN_BASE_MENTION_URL = (
#     "https://python.web.id/author/"  # please change this to your domain
# )

# If you need to use your own themed "bootstrap" or "semantic ui" dependency
# replace the values with the file in your static files dir
# MARTOR_ALTERNATIVE_JS_FILE_THEME = "semantic-themed/semantic.min.js"  # default None
# MARTOR_ALTERNATIVE_CSS_FILE_THEME = "semantic-themed/semantic.min.css"  # default None
# MARTOR_ALTERNATIVE_JQUERY_JS_FILE = "jquery/dist/jquery.min.js"  # default None

# URL schemes that are allowed within links
ALLOWED_URL_SCHEMES = [
    "data",  # allow images like "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD"
    "file",
    "ftp",
    "ftps",
    "http",
    "https",
    "irc",
    "mailto",
    "sftp",
    "ssh",
    "tel",
    "telnet",
    "tftp",
    "vnc",
    "xmpp",
]

# https://gist.github.com/mrmrs/7650266
ALLOWED_HTML_TAGS = [
    "a",
    "abbr",
    "b",
    "blockquote",
    "br",
    "cite",
    "code",
    "command",
    "dd",
    "del",
    "div",
    "dl",
    "dt",
    "em",
    "fieldset",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "h7",
    "hr",
    "i",
    "iframe",
    "img",
    "input",
    "ins",
    "kbd",
    "label",
    "legend",
    "li",
    "ol",
    "optgroup",
    "option",
    "p",
    "pre",
    "small",
    "span",
    "strong",
    "sub",
    "sup",
    "table",
    "tbody",
    "td",
    "tfoot",
    "th",
    "thead",
    "tr",
    "u",
    "ul",
]

# https://github.com/decal/werdlists/blob/master/html-words/html-attributes-list.txt
ALLOWED_HTML_ATTRIBUTES = [
    "alt",
    "aria-level",
    "class",
    "color",
    "colspan",
    "datetime",  # "data",
    "height",
    "href",
    "id",
    "name",
    "reversed",
    "rowspan",
    "role",
    "scope",
    "src",
    # "style",
    "start",
    "tabindex",
    "title",
    "type",
    "width",
]

# Django easy audit settings
# https://github.com/soynatan/django-easy-audit

DJANGO_EASY_AUDIT_READONLY_EVENTS = True
DJANGO_EASY_AUDIT_WATCH_REQUEST_EVENTS = False
# If the header is set it must be available on the request or an Error will be thrown
if is_prod:
    DJANGO_EASY_AUDIT_REMOTE_ADDR_HEADER = "HTTP_X_FORWARDED_FOR"

# Document IPs for our PDF generating app
DOCRAPTOR_IPS = env.get_value("DOCRAPTOR_IPS", default="")
DOCRAPTOR_API_KEY = env.get_value("DOCRAPTOR_API_KEY", default="")

# Add a field for constance
CONSTANCE_BACKEND = "constance.backends.database.DatabaseBackend"

CONSTANCE_CONFIG = {
    "DOCRAPTOR_IPS": (
        DOCRAPTOR_IPS,
        "IPs that are allowed to view and print NOFO documents. Latest IPs: https://docraptor.com/ips.txt",
        str,
    ),
    "DOCRAPTOR_LIVE_MODE": (
        now(),
        "Whether to print PDFs with watermarks. If timestamp is older than 5 mins, documents will be watermarked.",
        datetime,
    ),
    "WORD_IMPORT_STRICT_MODE": (
        False,
        "In strict mode, unhandled formatting in a .docx file throws an exception and prints the failure message to the screen.",
        bool,
    ),
}

# Disable migrations for constance in tests because there is a bug in their migration file
# https://github.com/jazzband/django-constance/issues/575
if "test" in sys.argv:
    MIGRATION_MODULES = {
        "constance": None,
    }

# Django codemirror
DJANGO_MIRROR_DEFAULTS = {
    "mode": "css",
    "addons": ["edit/matchbrackets", "hint/css-hint"],
    "line_wrapping": True,
    "line_numbers": True,
}

# "Groups" for categorizing users and NOFOs

GROUP_CHOICES = [
    ("bloom", "Bloomworks"),
    ("acf", "ACF: Administration for Children and Families"),
    ("acl", "ACL: Administration for Community Living"),
    ("aspr", "ASPR: Administration for Strategic Preparedness and Response"),
    ("cdc", "CDC: Centers for Disease Control and Prevention"),
    ("cms", "CMS: Centers for Medicare & Medicaid Services"),
    ("hrsa", "HRSA: Health Resources and Services Administration"),
    ("ihs", "IHS: Indian Health Service"),
    ("staging", "Staging environment"),
]

# Determine environment.  Until login.gov is fully deployed, we'll use staging as "prod"
ENVIRONMENT = "staging" if is_prod else "dev"

# Get Login.gov keys - always try Secret Manager first
LOGIN_GOV_PRIVATE_KEY, LOGIN_GOV_PUBLIC_KEY = get_login_gov_keys(ENVIRONMENT)

if LOGIN_GOV_PRIVATE_KEY and "test" not in sys.argv:
    print("=====")
    print(
        "Login.gov: enabled; env: {}; private_key: secrets manager".format(ENVIRONMENT)
    )

# If Secret Manager failed and we're in dev, try local files
if not LOGIN_GOV_PRIVATE_KEY and ENVIRONMENT == "dev":
    try:
        with open(
            BASE_DIR / "bloom_nofos" / "certs" / "login-gov-private-key-dev.pem"
        ) as f:
            LOGIN_GOV_PRIVATE_KEY = f.read()
            print("Login.gov enabled; env: {}; private_key: local".format(ENVIRONMENT))
    except Exception as e:
        print("Login.gov disabled; env: {}; private_key: None".format(ENVIRONMENT))


# Login/Logout URLs and settings
LOGIN_URL = "users:login"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

# Configure Login.gov based on key availability
LOGIN_GOV = {
    "ENABLED": bool(LOGIN_GOV_PRIVATE_KEY),
    "CLIENT_ID": env("LOGIN_GOV_CLIENT_ID", default=""),
    "OIDC_URL": env(
        "LOGIN_GOV_OIDC_URL", default="https://idp.int.identitysandbox.gov"
    ),
    "REDIRECT_URI": env("LOGIN_GOV_REDIRECT_URI", default=""),
    "ACR_VALUES": "http://idmanagement.gov/ns/assurance/ial/1",
    "PRIVATE_KEY": LOGIN_GOV_PRIVATE_KEY,
}
print("=====")


# Add Login.gov authentication backend
AUTHENTICATION_BACKENDS = [
    "users.auth.backend.LoginGovBackend",
    "django.contrib.auth.backends.ModelBackend",
]
