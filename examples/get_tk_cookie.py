import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from conf import BASE_DIR
from uploader.tk_uploader.main_chrome import tiktok_setup

if __name__ == '__main__':
    account_file = Path(BASE_DIR / "cookies" / "tk_uploader" / "account.json")
    account_file.parent.mkdir(exist_ok=True)
    cookie_setup = asyncio.run(tiktok_setup(str(account_file), handle=True))
