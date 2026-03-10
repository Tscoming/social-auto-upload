
curl -X POST http://localhost:5409/postVideo   -H "Content-Type: application/json"   -d '{
    "fileList": ["Vladimir ｜ Inside Rachel Weisz & Leo Woodall’s Lustful Limited Series ｜ Netflix_zh.mp4"],
    "video_id": "up76zC363d4",
    "type": 3,
    "title": "测试视频标题\n换行测试",
    "tags": ["标签1","标签2"],
    "category": 0,
    "enableTimer": false,
    "videosPerDay": 1,
    "dailyTimes": [],
    "startDays": 0,
    "isDraft": false
  }'