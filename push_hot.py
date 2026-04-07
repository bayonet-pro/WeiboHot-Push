import os
import requests

def get_weibo_hot():
    url = "https://renyuzhuo.github.io/WeiBoHot/weibohot.json"
    resp = requests.get(url, timeout=10)
    data = resp.json()
    hot_list = data["data"]

    content = "📌 微博实时热搜\n\n"
    for i, x in enumerate(hot_list[:20], 1):
        content += f"{i}. {x['title']} 🔥{x['hot_value']}\n"
    return content

def send(content):
    key = os.getenv("SERVER_KEY")
    api = f"https://sctapi.ftqq.com/{key}.send"
    data = {"title":"微博热搜推送","desp":content}
    requests.post(api, data=data)

if __name__ == "__main__":
    content = get_weibo_hot()
    send(content)
    print("✅ 推送成功！")
