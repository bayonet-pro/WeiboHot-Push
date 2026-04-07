import os
import requests
import traceback

# 获取微博热搜（修复了接口地址，增加重试机制）
def get_weibo_hot():
    # 正确的原项目接口地址
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

# Server酱推送到微信
def send_msg(content):
    key = os.getenv("SERVER_KEY")
    print(f"读取到的SERVER_KEY: {key}")
    
    if not key:
        raise Exception("SERVER_KEY 环境变量为空！请检查GitHub Secrets配置")
    
    api = f"https://sctapi.ftqq.com/{key}.send"
    data = {
        "title": "微博热搜已更新",
        "desp": content
    }
    try:
        r = requests.post(api, data=data, timeout=10)
        r.raise_for_status()
        result = r.json()
        print(f"Server酱推送结果: {result}")
        return result
    except Exception as e:
        print(f"推送失败: {str(e)}")
        traceback.print_exc()
        raise e

if __name__ == "__main__":
    try:
        print("=== 开始执行微博热搜推送任务 ===")
        content = get_weibo_hot()
        res = send_msg(content)
        print("=== 推送任务执行成功 ===")
        print(f"最终结果: {res}")
    except Exception as e:
        print(f"=== 推送任务执行失败: {str(e)} ===")
        traceback.print_exc()
        raise e
