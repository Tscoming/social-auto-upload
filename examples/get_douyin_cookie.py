import asyncio
import sys
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))

from conf import BASE_DIR
from uploader.douyin_uploader.main import douyin_setup


if __name__ == '__main__':
    account_file = Path(BASE_DIR / "cookies" / "douyin_uploader" / "account.json")
    account_file.parent.mkdir(exist_ok=True)
    cookie_setup = asyncio.run(douyin_setup(str(account_file), handle=True))
