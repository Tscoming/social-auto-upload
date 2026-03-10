import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()
VIDEO_DOWNLOAD_DIR = Path(os.getenv("VIDEO_DOWNLOAD_PATH")).resolve() if os.getenv("VIDEO_DOWNLOAD_PATH") else Path(__file__).parent.resolve()
DOUYIN_CREDENTIALS_FILE = Path(os.getenv("DOUYIN_CREDENTIALS_FILE")).resolve() if os.getenv("DOUYIN_CREDENTIALS_FILE") else BASE_DIR / "douyin_credentials.json"
XHS_SERVER = "http://127.0.0.1:11901"
LOCAL_CHROME_PATH = ""   # change me necessary！ for example C:/Program Files/Google/Chrome/Application/chrome.exe
LOCAL_CHROME_HEADLESS = True
