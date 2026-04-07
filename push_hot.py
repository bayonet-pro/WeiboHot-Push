import os
import requests

def get_weibo_hot():
    url = "https://weibo.com/ajax/side/hotSearch"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    resp = requests.get(url, headers=headers, timeout=10)
    data = resp.json()
    hot_list = data["data"]["realtime"]

    content = "📌 微博实时热搜\n\n"
    for i, item in enumerate(hot_list[:15], 1):
        title = item["note"]
        hot = str(item.get("num", ""))
        content += f"{i}. {title} 🔥{hot}\n"
    return content

def send(content):
    key = os.getenv("SERVER_KEY")
    api = f"https://sctapi.ftqq.com/{key}.send"
    
    data = {
        "title": "微博热搜已更新",
        "desp": content,
        "channel": "wechat"  # 强制推送到公众号！关键！
    }
    
    response = requests.post(api, data=data)
    print("推送状态：", response.json())

if __name__ == "__main__":
    try:
        content = get_weibo_hot()
        send(content)
        print("✅ 推送成功！")
    except Exception as e:
        print("❌ 错误：", e)
