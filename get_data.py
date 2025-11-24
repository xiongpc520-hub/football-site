import requests
import json
import time
import random

def fetch_bilibili_football_videos():
    print("⚽ 正在潜入 Bilibili 获取足球数据...")
    
    # 这是B站的搜索接口，我们伪装成浏览器搜索“足球战术”
    url = "https://api.bilibili.com/x/web-interface/search/type"
    params = {
        "keyword": "足球战术",
        "search_type": "video",
        "page": 1,
        "order": "click" # 按点击量排序
    }
    # 必须加 User-Agent，否则会被B站拦截
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        data = response.json()
        
        # 提取我们需要的数据字段
        video_list = []
        if 'data' in data and 'result' in data['data']:
            for item in data['data']['result']:
                # 只保留核心字段
                video = {
                    "id": item['bvid'],           # 视频唯一ID
                    "title": item['title'].replace('<em class="keyword">', '').replace('</em>', ''), # 清洗标题
                    "pic": "https:" + item['pic'], # 封面图
                    "author": item['author'],     # UP主
                    "play": item['play'],         # 播放量
                    "duration": item['duration']  # 时长
                }
                video_list.append(video)
                
        print(f"✅ 成功抓取了 {len(video_list)} 条数据！")
        return video_list

    except Exception as e:
        print(f"❌ 抓取失败 (可能是B站开启了防御模式): {e}")
        return []

# 执行并保存为 data.json (模拟数据库)
if __name__ == "__main__":
    videos = fetch_bilibili_football_videos()
    
    # 为了演示，如果没抓到（比如网络问题），我们就造几条假数据保底
    if not videos:
        print("⚠️ 启用备用数据模式...")
        videos = [
            {"id": "BV1Yy4y1v7xy", "title": "【C罗】这就是这一年的所有进球！", "pic": "https://placehold.co/300x180/000000/FFF?text=CR7", "author": "曼联老特", "play": "100万", "duration": "10:00"},
            {"id": "BV1ZK411L7d9", "title": "瓜迪奥拉战术全解析", "pic": "https://placehold.co/300x180/87CEEB/000?text=Pep+Guardiola", "author": "足球只有圆的", "play": "50万", "duration": "15:20"}
        ]

    # 存入文件，这就相当于存入数据库了
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(videos, f, ensure_ascii=False, indent=2)
    print("💾 数据已保存到 data.json")