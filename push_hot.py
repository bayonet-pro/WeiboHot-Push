import os
import requests

# 获取微博热搜
def get_weibo_hot():
    url = "https://renyuzhuo.github.io/WeiBoHot/weibohot.json"
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    data = resp.json()
    hot_list = data.get("data", [])

    content = "📌 微博实时热搜\n\n"
    for i, item in enumerate(hot_list[:20], 1):
        title = item.get("title", "")
        hot = item.get("hot_value", "")
        content += f"{i}. {title} 🔥{hot}\n"
    return content

# Server酱推送到微信
def send_msg(content):
    key = os.getenv("SERVER_KEY")
    api = f"https://sctapi.ftqq.com/{key}.send"
    data = {
        "title": "微博热搜已更新",
        "desp": content
    }
    r = requests.post(api, data=data)
    return r.json()

if __name__ == "__main__":
    try:
        content = get_weibo_hot()
        res = send_msg(content)
        print("推送成功:", res)
    except Exception as e:
        print("推送失败:", e)
        raise e
