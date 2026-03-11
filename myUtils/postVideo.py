import asyncio
import base64
import binascii
from http.client import HTTPException
import os
from pathlib import Path

from conf import BASE_DIR, DOUYIN_CREDENTIALS_FILE, VIDEO_DOWNLOAD_DIR
from uploader.douyin_uploader.main import DouYinVideo
from uploader.ks_uploader.main import KSVideo
from uploader.tencent_uploader.main import TencentVideo
from uploader.xiaohongshu_uploader.main import XiaoHongShuVideo
from utils.constant import TencentZoneTypes
from utils.files_times import generate_schedule_time_next_day


def post_video_tencent(title,files,tags,account_file,category=TencentZoneTypes.LIFESTYLE.value,enableTimer=False,videos_per_day = 1, daily_times=None,start_days = 0, is_draft=False):
    # 生成文件的完整路径
    account_file = [Path(BASE_DIR / "cookiesFile" / file) for file in account_file]
    files = [Path(BASE_DIR / "videoFile" / file) for file in files]
    if enableTimer:
        publish_datetimes = generate_schedule_time_next_day(len(files), videos_per_day, daily_times, start_days=start_days)
    else:
        publish_datetimes = [0 for i in range(len(files))]
    for index, file in enumerate(files):
        for cookie in account_file:
            print(f"文件路径{str(file)}")
            # 打印视频文件名、标题和 hashtag
            print(f"视频文件名：{file}")
            print(f"标题：{title}")
            print(f"Hashtag：{tags}")
            app = TencentVideo(title, str(file), tags, publish_datetimes[index], cookie, category, is_draft)
            asyncio.run(app.main(), debug=False)



def post_video_DouYin(title,files,tags,video_id,category=TencentZoneTypes.LIFESTYLE.value,enableTimer=False,videos_per_day = 1, daily_times=None,start_days = 0,
                      thumbnail_path = '',
                      productLink = '', productTitle = ''):
    # 生成文件的完整路径
    account_file = [ DOUYIN_CREDENTIALS_FILE ]
    filenames = []
    for file_base64 in files:
        if file_base64:
            normalized = file_base64.replace("-", "+").replace("_", "/")
            normalized += "=" * (-len(normalized) % 4)
            filename = base64.b64decode(normalized).decode("utf-8")
            filenames.append(filename)
    
    files = [Path(VIDEO_DOWNLOAD_DIR / video_id / file) for file in filenames]

    # 根据thumbnail_path文件后缀名判断图片格式，如果不是jpg,jpeg,png, 则转换图片格式为jpg
    if thumbnail_path:
        if not thumbnail_path.lower().endswith(('.jpg', '.jpeg', '.png')):
            print(f"缩略图文件{thumbnail_path}格式不受支持，正在转换为jpg格式...")
            try:
                from PIL import Image
                thumbnail_path_obj = Path(VIDEO_DOWNLOAD_DIR / video_id / thumbnail_path)
                with Image.open(thumbnail_path_obj) as img:
                    new_thumbnail_path = thumbnail_path_obj.with_suffix('.jpg')
                    img.convert('RGB').save(new_thumbnail_path, 'JPEG')
                    thumbnail = new_thumbnail_path.name
                    print(f"缩略图已成功转换为{thumbnail_path}")
            except ImportError:
                print("PIL库未安装，无法转换缩略图格式。请安装Pillow库以支持缩略图格式转换。")
        else:
            thumbnail = Path(VIDEO_DOWNLOAD_DIR / video_id / thumbnail_path) if thumbnail_path else None
    else:
        # 读取视频文件所在目录下的所有图片文件，作为缩略图候选列表
        video_dir = Path(VIDEO_DOWNLOAD_DIR / video_id)
        # list all image files in the video directory
        image_files = [f for f in video_dir.iterdir() if f.is_file() and f.suffix.lower() in ['.jpg', '.jpeg', '.png', '.webp']]
        if image_files:
            # 如果有图片文件，选择第一个作为缩略图
            thumbnail = image_files[0]
            if thumbnail.suffix.lower() not in ['.jpg', '.jpeg', '.png']:
                print(f"视频目录下的图片文件{thumbnail}格式不受支持，正在转换为jpg格式...")
                try:
                    from PIL import Image
                    with Image.open(thumbnail) as img:
                        new_thumbnail_path = thumbnail.with_suffix('.jpg')
                        img.convert('RGB').save(new_thumbnail_path, 'JPEG')
                        thumbnail = new_thumbnail_path
                        print(f"缩略图已成功转换为{thumbnail}")
                except ImportError:
                    print("PIL库未安装，无法转换缩略图格式。请安装Pillow库以支持缩略图格式转换。")
            else:
                print(f"未提供缩略图路径，已自动选择视频目录下的图片文件{thumbnail}作为缩略图。")
        else:
            thumbnail = None
            print("未提供缩略图路径，且视频目录下没有图片文件，无法设置缩略图。")
        
    

    print(f"thumbnail_path: {thumbnail}")

    if enableTimer:
        publish_datetimes = generate_schedule_time_next_day(len(files), videos_per_day, daily_times, start_days=start_days)
    else:
        publish_datetimes = [0 for i in range(len(files))]
    for index, file in enumerate(files):
        # 对file进行检查，确保它存在且是一个文件
        if not file.exists() or not file.is_file():
            print(f"文件路径{str(file)}无效，跳过该文件。")
            continue
        for cookie in account_file:
            print(f"文件路径{str(file)}")
            # 打印视频文件名、标题和 hashtag
            print(f"视频文件名：{file}")
            print(f"标题：{title}")
            print(f"Hashtag：{tags}")
            print(f"缩略图路径：{thumbnail}" )
            app = DouYinVideo(title, str(file), tags, publish_datetimes[index], cookie, thumbnail, productLink, productTitle)
            result = asyncio.run(app.main(), debug=False)
            # 检查返回结果是否为错误
            if result and isinstance(result, dict) and result.get("status") == "error":
                print(f"Upload failed: {result.get('message')}")  # 日志可以是中文，但API返回信息是英文
                return result  # 返回错误信息而不是抛出异常

    # 如果所有视频都上传成功，返回None表示成功
    return None


def post_video_ks(title,files,tags,account_file,category=TencentZoneTypes.LIFESTYLE.value,enableTimer=False,videos_per_day = 1, daily_times=None,start_days = 0):
    # 生成文件的完整路径
    account_file = [Path(BASE_DIR / "cookiesFile" / file) for file in account_file]
    files = [Path(BASE_DIR / "videoFile" / file) for file in files]
    if enableTimer:
        publish_datetimes = generate_schedule_time_next_day(len(files), videos_per_day, daily_times, start_days=start_days)
    else:
        publish_datetimes = [0 for i in range(len(files))]
    for index, file in enumerate(files):
        for cookie in account_file:
            print(f"文件路径{str(file)}")
            # 打印视频文件名、标题和 hashtag
            print(f"视频文件名：{file}")
            print(f"标题：{title}")
            print(f"Hashtag：{tags}")
            app = KSVideo(title, str(file), tags, publish_datetimes[index], cookie)
            asyncio.run(app.main(), debug=False)

def post_video_xhs(title,files,tags,account_file,category=TencentZoneTypes.LIFESTYLE.value,enableTimer=False,videos_per_day = 1, daily_times=None,start_days = 0):
    # 生成文件的完整路径
    account_file = [Path(BASE_DIR / "cookiesFile" / file) for file in account_file]
    files = [Path(BASE_DIR / "videoFile" / file) for file in files]
    file_num = len(files)
    if enableTimer:
        publish_datetimes = generate_schedule_time_next_day(file_num, videos_per_day, daily_times, start_days=start_days)
    else:
        publish_datetimes = 0
    for index, file in enumerate(files):
        for cookie in account_file:
            # 打印视频文件名、标题和 hashtag
            print(f"视频文件名：{file}")
            print(f"标题：{title}")
            print(f"Hashtag：{tags}")
            app = XiaoHongShuVideo(title, file, tags, publish_datetimes, cookie)
            asyncio.run(app.main(), debug=False)



# post_video("333",["demo.mp4"],"d","d")
# post_video_DouYin("333",["demo.mp4"],"d","d")