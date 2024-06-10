import time
import hashlib
import csv
import requests

# 定义函数，将字典列表转换为文本
def convert_to_text(video_list):
    text = ""
    for video in video_list:
        video_info = (
            f"标题: {video['标题']}\n"
            f"视频号: {video['视频号']}\n"
            f"作者: {video['作者']}\n"
            f"点赞: {video['点赞']}\n"
            f"投币: {video['投币']}\n"
            f"转发: {video['转发']}\n"
            f"播放量: {video['播放量']}\n"
            f"评论: {video['评论']}\n"
            "--------------------------\n"
        )
        text += video_info
    return text


def bilibili_popular():
    # 当前时间戳
    wts = int(time.time())

    # 构建请求参数
    u = [
        'ids=2837%2C2836%2C2870%2C2953%2C2954%2C2955%2C2956%2C5672',
        'pf=0',
        f'wts={wts}'
    ]
    m = '&'.join(u)
    o = 'ea1db124af3c7062474693fa704f4ff8'
    string = m + o

    # 计算MD5哈希
    md = hashlib.md5(string.encode())
    w_rid = md.hexdigest()

    # 打开CSV文件进行写入
    with open('bilibili_popular.csv', 'w', encoding='utf-8', newline='') as fp:
        csv_writer = csv.DictWriter(fp, fieldnames=['标题', '视频号', '作者', '点赞', '投币', '转发', '播放量', '评论'])
        csv_writer.writeheader()

        all_videos = []

        # 循环获取多个页面的数据
        for page in range(1, 5):
            url = f'https://api.bilibili.com/x/web-interface/popular?ps=20&pn={page}&web_location=333.934&w_rid={w_rid}&wts={wts}'
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0'
            }
            json_data = requests.get(url=url, headers=headers).json()
            video_list = json_data['data']['list']

            for li in video_list:
                title = li['title']  # 标题
                aid = li['aid']  # 视频号
                owner = li['owner']['name']  # 作者
                favorite = li['stat']['favorite']  # 点赞
                coin = li['stat']['coin']  # 投币
                share = li['stat']['share']  # 转发
                view = li['stat']['view']  # 播放量
                reply = li['stat']['reply']  # 评论

                video_data = {
                    '标题': title,
                    '视频号': aid,
                    '作者': owner,
                    '点赞': favorite,
                    '投币': coin,
                    '转发': share,
                    '播放量': view,
                    '评论': reply
                }

                all_videos.append(video_data)

        # 按播放量排序
        all_videos.sort(key=lambda x: x['播放量'], reverse=True)
        top_10 = all_videos[:5]
    
        # 写入排序后的前十名数据到CSV文件
        csv_writer.writerows(top_10)

        # 将前十名数据转换为文本
        top_10_text = convert_to_text(top_10)
        #print(top_10_text)  # 打印或保存文本
        return(top_10_text)
        