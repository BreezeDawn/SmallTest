import pprint

import requests
import json

url = "https://fanyi.baidu.com/basetrans"

# 使用手机端的请求头
headers = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 "
                  "(KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1"
}

query = input("请输入查询内容")

data = {
    "query": query,
    "from": "en",
    "to": "zh"
}

# 发送post请求
# get使用params发送参数,post使用data
response = requests.post(url, data=data, headers=headers)
res = response.text

pprint.pprint(json.loads(res)['trans'][0]['result'][0][1])
