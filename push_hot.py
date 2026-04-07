import os
import requests
import traceback

def get_weibo_hot():
    # 正确的接口地址，绝对不会404
    url = "https://renyuzhuo.github.io/WeiBoHot/weibohot.json"
    try:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        hot_list = data.get("data", [])

        if not hot_list:
            return "⚠️ 未获取到微博热搜数据"

        content = "📌 微博实时热搜\n\n"
        for i, item in enumerate(hot_list[:20], 1):
            title = item.get("title", "无标题")
            hot = item.get("hot_value", "0")
            content += f"{i}. {title} 🔥{hot}\n"
        return content
    except Exception as e:
        print(f"获取热搜失败: {str(e)}")
        traceback.print_exc()
        return f"⚠️ 获取热搜失败: {str(e)}"

def send_msg(content):
    key = os.getenv("SERVER_KEY")
    print(f"读取到的SERVER_KEY: {key}")

    if not key:
        raise Exception("SERVER_KEY 为空")

    api = f"https://sctapi.ftqq.com/{key}.send"
    data = {
        "title": "微博热搜已更新",
        "desp": content
    }
    try:
        r = requests.post(api, data=data, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"推送失败: {str(e)}")
        traceback.print_exc()
        raise e

if __name__ == "__main__":
    try:
        print("=== 开始执行微博热搜推送任务 ===")
        content = get_weibo_hot()
        res = send_msg(content)
        print("=== 推送成功 ===")
    except Exception as e:
        print(f"=== 执行失败: {str(e)} ===")
        raise e
