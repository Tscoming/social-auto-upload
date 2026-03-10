import asyncio
import sys
from pathlib import Path

# Add parent directory to path to import conf module
sys.path.insert(0, str(Path(__file__).parent.parent))

from conf import BASE_DIR
from uploader.ks_uploader.main import ks_setup

if __name__ == '__main__':
    account_file = Path(BASE_DIR / "cookies" / "ks_uploader" / "account.json")
    account_file.parent.mkdir(exist_ok=True)
    cookie_setup = asyncio.run(ks_setup(str(account_file), handle=True))
