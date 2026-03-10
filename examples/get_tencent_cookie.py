import asyncio
import sys
from pathlib import Path

# Add parent directory to path to import conf module
sys.path.insert(0, str(Path(__file__).parent.parent))

from conf import BASE_DIR
from uploader.tencent_uploader.main import weixin_setup

if __name__ == '__main__':
    account_file = Path(BASE_DIR / "cookies" / "tencent_uploader" / "account.json")
    account_file.parent.mkdir(exist_ok=True)
    cookie_setup = asyncio.run(weixin_setup(str(account_file), handle=True))
