def Response():
    # 响应的属性和方法
    # 获取响应状态码
    print(response.status_code)
    # 获取响应头
    print(response.headers)
    # 获取响应链接
    print(response.url)
    # 获取cookies
    print(response.cookies)
    # cookiejar格式转换为dict
    print(requests.utils.dict_from_cookiejar(response.cookies))
    # 根据响应头获取请求头
    print(response.request.headers)

if __name__ == '__main__':
    import json
    import requests

    # 请求地址
    url = 'https://movie.douban.com/j/search_subjects'

    # 构造请求头
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.204 Safari/537.36"
    }

    # 构造请求参数
    params = {
        "type": "movie",
        "tag": "热门",
        "sort": "recommend",
        "page_limit": "20",
        "page_start": "40"
    }

    # 发起请求/获取响应
    response = requests.get(url, params=params, headers=headers)

    Response()

    # 解码二进制响应数据
    # 方法一:手动解码,content-任意格式数据的二进制
    # subjects_json = response.content.decode()
    # 方法二:text-只能拿到html的内容
    subjects_json = response.text

    # 转换json字符串格式
    subjects = json.loads(subjects_json)["subjects"]

    # 打印数据
    for subject in subjects:
        print(subject)