# 使用requests.session,github模拟登陆,并访问需要登陆的页面
import requests

# 输入账号密码
username = input('用户名:')
password = input('密码:')

# 请求地址
url = "https://github.com/session"

# 请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                  " (KHTML, like Gecko) Chrome/64.0.3282.204 Safari/537.36",
    "Referer": "https://github.com/login",
    "Cookie": "_octo=GH1.1.1952784514.1538128263; _ga=GA1.2.430432752.1538128272; tz=Asia%2FShanghai; has_recent_activity=1; _gat=1; logged_in=no; _gh_sess=bldINmNNUXkvRWRiUTU1b2V4UThWNWZ6Z1FlUkl2akxrSlZwcGYwV1lLa3ZKS1RYeEZrRnpQU0poSXhRdnIwMWRKMmRGdUZhSTVqbjY0dFRRcWFQUDlLS2N5bHB1QUZGRXBEYW10eW9kU1BHQVdtQng1SmplVks0V2xQMUJNSjdVNHplc2ZiVCtOdUtGayt1QVhHenlZM0F4UmtZWkFGdTF2Q3IwN3BuNk5YSjdyc3dCdFJtS09LYVBHd3J5bjlNZGc3TnBXeEZFcEt1QXlpL1lDR3NReGFiNTBibTI0N1FIcExxMnBsblN2c2NCK0t6V3AvdnN0ZU9CMjhZMXdTSkE1WUJtKzVoalRpLzdaWDRvYTg3dzdkeWtIWEpkSUZQdXRSemFxVUUzUDBQWkcrU1FCLzRUcXhCTHVUeWxnU1F1MEpiaGdnclR6cW52ZnA0YzA0cjIrcXppbFdQNGc2YUh1djhWT0NXWHhSYllZVTgyanVibndrR1dVekpCZHZia3FxQ1lGN1lBQU5jVHhySGJySHk2UW00TFNjWDZ3SDRHcCt4ZEFpaldvdz0tLVdOOGNGK05qelloS2R5S09hdnFSanc9PQ%3D%3D--d66dc5b4e66df1830f4f3196c57d705409a85e51"
}

# 请求参数
data = {
    "commit": "Sign in",
    "utf8": "✓",
    "authenticity_token": "LW8DpnfE8QX6jcMKjmmwsAeAE2XaPul6gQ9naWoLdxhjau0gYGceZSwhj/gpdCc1PeglcvHv5MHEK1LRNvcNAw==",
    "login": username,
    "password": password
}

# 使用session - 携带cookie
session = requests.session()

# 先登录,使session中的cookie更新为登陆后的cookie
session.post(url, data=data, headers=headers)

# 现在请求时使用的session,里面的cookie是登陆后的
response = session.get('https://github.com/settings/profile')

# 获取登陆后才可以访问的页面
html = response.content

# 保存本地
with open('./1.html', 'wb') as f:
    f.write(html)
