import requests
import my_fake_useragent
import time
import json
import os

def get_headers():
    """
    生成响应头
    :return: 生成的响应头
    """
    # 随机生成user_agent
    user_agent = my_fake_useragent.UserAgent()
    ua = str(user_agent.random())
    headers = {
        'user-agent': ua
    }
    return headers

def get_response(url, page=1, headers=None):
    """
    请求该url并获得响应
    :param url: 要请求的url
    :param page: 要请求的页数
    :param headers: 请求头部
    :return: 对于请求的响应
    """
    if headers is None:
        headers = get_headers()
    
    # 请求的参数
    params = {
        'ps': '20',
        'pn': str(page)
    }
    try:
        # 发出请求
        response = requests.get(url=url, params=params, headers=headers)
    except Exception as e:
        # 异常识别
        return None
    return response

def parse_text(text=None):
    """
    解析响应的文本
    :param text:响应的文本
    :return: 由信息字典组成的列表[{info1}, {info2}, {info3}]
    """
    # 将json文件解析为字典
    data = json.loads(text)

    """
    data['data']是一个字典，包含若干数据
    data['data']['list']是一个字典组成的list，包含每个视频的信息
    """
    ret_list = []
    temp_dict = {}

    # 提取数据，生成返回列表
    for list_dict in data['data']['list']:
        # 保存标题
        temp_dict['title'] = list_dict['title']
        # 保存封面图片的地址
        temp_dict['pic'] = list_dict['pic']
        # 保存描述
        temp_dict['desc'] = list_dict['desc']

        # 保存投稿用户id
        temp_dict['name'] = list_dict['owner']['name']

        # 保存观看量
        temp_dict['view'] = list_dict['stat']['view']
        # 保存收藏数
        temp_dict['favorite'] = list_dict['stat']['favorite']
        # 保存投币数
        temp_dict['coin'] = list_dict['stat']['coin']
        # 保存分享数
        temp_dict['share'] = list_dict['stat']['share']
        # 保存点赞数
        temp_dict['like'] = list_dict['stat']['like']

        # 保存BV号
        temp_dict['bvid'] = list_dict['bvid']

        # 将字典添加到返回列表
        ret_list.append(temp_dict.copy())
        # 清空字典
        temp_dict.clear()

    return ret_list

def save_infos(infos=None, page=1, main_path=None):
    """
    保存信息到指定的文件夹
    :param main_path: 主路径
    :param infos: 要保存的信息
    :param page: 要保存到的文件夹序号
    """
    # 让编译器识别一下列表，好把里面的方法识别出来。。。手懒
    # infos = [].append(infos)

    # 创建子文件夹
    dir_path = main_path + '/page%d' % page
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

    # 遍历读取到的信息
    for info in infos:
        # 以bv号命名文件
        file_path = dir_path + '/' +info['bvid'] + '.text'
        # 打开文件
        with open(file_path, 'w', encoding='utf-8') as fp:
            # 遍历字典
            for k, v in info.items():
                fp.write('%s: %s' % (str(k), str(v)))
                fp.write('\n')

def main():

    # 需要请求的url
    # 'https://api.bilibili.com/x/web-interface/popular?ps=20&pn=1'
    url = 'https://api.bilibili.com/x/web-interface/popular'

    # 创建主文件夹
    main_path = url.split('/')[-1]
    if not os.path.exists(main_path):
        os.mkdir(main_path)

    # 设定起始页码
    page_start = int(input('start: '))
    page_end = int(input('end: '))
    #page_start = 1
    #page_end = 1

    # 主循环开始
    for i in range(page_end - page_start + 1):
        page_num = page_start + i
        # 请求页面并获得响应
        print(f'第{page_num}页开始下载……')
        response = get_response(url=url, page=page_num, headers=get_headers())
        # 判断请求是否成功
        if response is not None and response.status_code == 200:
            # 请求成功
            # 获取并解析响应的内容
            text = response.text
            infos = parse_text(text)
            save_infos(infos=infos, page=page_num, main_path=main_path)
            print(f'第{page_num}页下载完成')
        else:
            # 请求失败
            print(f'！！第{page_num}页请求失败！！')
            continue

        # 文明爬虫！！！
        time.sleep(3)

if __name__ == '__main__':
    print('开始')
    start_time = time.time()
    main()
    end_time = time.time()
    print(f'完成<{end_time - start_time}>')
