# js逆向,微博登陆,没有处理验证码
import re
import rsa
import json
import base64
import binascii
import requests


class WeiboLogin:
    def __init__(self):
        self.session = requests.Session()
        self.prelogin_url = 'http://login.sina.com.cn/sso/prelogin.php'
        self.login_url = 'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.19)'
        self.headers = {
            "Cookie": "TC-Ugrow-G0=370f21725a3b0b57d0baaf8dd6f16a18; TC-Page-G0=1bbd8b9d418fd852a6ba73de929b3d0c; TC-V5-G0=634dc3e071d0bfd86d751caf174d764e; _s_tentry=sass.weibo.com; Apache=8732058590336.289.1539185526646; SINAGLOBAL=8732058590336.289.1539185526646; ULV=1539185526730:1:1:1:8732058590336.289.1539185526646:; cross_origin_proto=SSL; login_sid_t=43dc8614795fd340a6917abe4106a25f; wb_view_log=1366*7681; un=137899401@qq.com; wb_view_log_2461558403=1366*7681; appkey=; SCF=Auzv-9K98hjfCjzwcKPpDgTU1mRY9qh4OC3XqknRyTK0wmjDLmeYXRZFUcrd-OSlDfFuJWW2rTyKvJE_c0Zvj8U.; SUHB=06ZU4afjoWZgIW; SUB=_2AkMs4nN0dcPxrAFVnvkQyWPmbI5H-jyfNxqCAn7uJhMyAxh77ls3qSVutBF-XBl5Rm6DS6Ce0Qo4Z-eHlL-Zx0IQ; SUBP=0033WrSXqPxfM72wWs9jqgMF55529P9D9W5-O8OgAJ-rTvjv9-CiCWQV5JpV2h20S0n41KB7e-WpMC4odcXt; WBStorage=e8781eb7dee3fd7f|undefined; UOR=,,login.sina.com.cn",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.204 Safari/537.36"
        }

    @staticmethod
    def get_username():
        f = open('./user.dat', 'r')
        username = json.loads(f.read())["username"]
        f.close()
        username = base64.encodebytes(username.encode())[:-1]
        return username

    @staticmethod
    def get_password(pubkey, servertime, nonce):
        f = open('./user.dat', 'r')
        password = json.loads(f.read())["password"]
        f.close()

        rsapublickey = int(pubkey, 16)

        key = rsa.PublicKey(rsapublickey, 65537)  # 创建公钥

        message = str(servertime) + '\t' + str(nonce) + '\n' + str(password)  # 拼接明文 js加密文件中得到

        password = rsa.encrypt(message.encode(), key)  # 加密

        password = binascii.b2a_hex(password)  # 将加密信息转换为16进制。
        return password

    def get_prelogin(self):
        username = self.get_username()

        params = {
            "entry": "sso",
            "callback": "sinaSSOController.preloginCallBack",
            "su": username,
            "rsakt": "mod",
            "client": "ssologin.js(v1.4.15)",
            "_": "1539181197343"
        }

        response = self.session.get(self.prelogin_url, params=params, headers=self.headers)
        args = json.loads(re.findall(r'{.*}', response.text)[0])
        pubkey = args['pubkey']
        servertime = args['servertime']
        nonce = args['nonce']
        rsakv = args['rsakv']

        return pubkey, servertime, nonce, rsakv, username

    def post_login(self):
        pubkey, servertime, nonce, rsakv, username = self.get_prelogin()

        password = self.get_password(pubkey, servertime, nonce)

        data = {"entry": 'account',
                "gateway": '1',
                "from": '',
                "savestate": '30',
                "qrcode_flag": "true",
                "useticket": '0',
                "vsnf": "1",
                "ssosimplelogin": '1',
                "su": username,
                "servertime": servertime,
                "nonce": nonce,
                "pwencode": 'rsa2',
                "sp": password,
                "encoding": 'UTF-8',
                "rsakv": rsakv,
                "pagerefer": "http://my.sina.com.cn/",
                "service": "sso",
                "sr": "1366*768",
                "cdult": "3",
                "domain": "sina.com.cn",
                "prelt": "159",
                "returntype": "TEXT"
                }

        response = self.session.post(self.login_url, headers=self.headers, data=data)

        json_text = response.content.decode('gbk')
        res_info = json.loads(json_text)

        if res_info["retcode"] == "0":
            print('登陆成功')
        else:
            print(res_info["reason"])

    def run(self):
        self.post_login()


if __name__ == '__main__':
    login = WeiboLogin()
    login.run()
