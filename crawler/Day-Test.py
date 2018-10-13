import json

import requests
from retrying import retry

url = 'http://www.xingtu.info/'
headers = {
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.204 Safari/537.36"
}

# 1.转换cookie为字典,将字典转换为cookie
# response = requests.get(url)
# cookies = requests.utils.dict_from_cookiejar(response.cookies)
# cookies = requests.utils.cookiejar_from_dict(cookies)


# 2.使用代理(proxies)
# proxies = {
#      "http":'218.14.115.211:3128'
# }
# response = requests.get(url,headers=headers,proxies=proxies)


# 3.处理证书错误(跳过证书验证)
# response = requests.get('https://www.12306.cn/mormhweb/',headers=headers,verify=False)
# with open('./1.html','wb') as f:
#     f.write(response.content)


# 4.超时处理(超时会报错),并重试(retrying)
@retry(stop_max_attempt_number = 3)
def retry_test():
    proxies = {
        "https": '120.33.247.207:8010'
    }
    response = requests.get('https://www.baidu.com',headers=headers,proxies=proxies,timeout=3)
    print(response.content)
# retry_test()


# 5.dump,dump2,load,loads
def dump_test():
    data = json.dumps([{"a":"1"},'3'])  # dumps-python格式转json格式

    print(json.loads(data))  # loads-json格式转python格式

    f = open('./1.dat','w')  # dump-向文件写入json
    json.dump(data,f)
    f.close()

    f = open('./1.dat','r')  # load-从文件读取json
    content = json.load(f)
    f.close()
    print(content)
# dump_test()


# 9.zip(),将可迭代的对象作为参数,将每个对象中相同下标的元素打包成一个元组，然后返回由这些元组组成的列表。
# a = [1,2,3]
# b = [4,5,6]
# c = [4,5,6,7,8]
# zipped = zip(a,b)     # 打包
# zip(a,c)              # 列表中元素的个数与最短的列表一致
# zip(*zipped)          # *zipped 可理解为解压，返回二维矩阵式


# 10.re(使用compile,re.S(使'.'包括换行符),re.I(忽略大小写))

# 12.xpath
# from lxml import etree
# f = open('./xpath.html','r')
# e = etree.HTML(f.read())
# f.close()
# print(e.xpath('//book'))
