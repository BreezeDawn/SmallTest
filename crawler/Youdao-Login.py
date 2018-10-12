import requests

url = 'http://fanyi.youdao.com/'
login_url = 'http://dict.youdao.com/login/acc/login?cf=7'

headers = {
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
             "(KHTML, like Gecko) Chrome/64.0.3282.204 Safari/537.36"
}

username = input('username:')
# 有道的密码加密写在前端,用的加密是独有的,只能直接把加密后的密码直接拿过来用
password = input('password:')

session = requests.session()

data = {
    "username":username,
    "password":password,
    "app":"web",
    "product":"DICT",
    "tp":"urstoken",
    "cf":"7",
    "fr":"1",
    "ru":"http://fanyi.youdao.com/scripts/newweb/oncallback.html",
    "er":"http://fanyi.youdao.com/scripts/newweb/oncallback.html",
}

session.post(login_url,data=data)
