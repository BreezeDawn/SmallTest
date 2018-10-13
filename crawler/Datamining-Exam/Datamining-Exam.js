function getCookie(a) {
    var b = document.cookie;
    var c = b.split("; ");
    for (var i = 0; i < c.length; i++) {
        var d = c[i].split("=");
        if (a == d[0]) {
            return d[1]
        }
    }
    return ""
};

session = getCookie('session');
var encoderchars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";
url = location.href;

function f1(a) {
    var b, i, len;
    var c, c2, c3;
    len = a.length;
    i = 0;
    b = "";
    while (i < len) {
        c = a.charCodeAt(i++) & 0xff;
        if (i == len) {
            b += encoderchars.charAt(c >> 2);
            b += encoderchars.charAt((c & 0x3) << 4);
            b += "==";
            break
        }
        c2 = a.charCodeAt(i++);
        if (i == len) {
            b += encoderchars.charAt(c >> 2);
            b += encoderchars.charAt(((c & 0x3) << 4) | ((c2 & 0xf0) >> 4));
            b += encoderchars.charAt((c2 & 0xf) << 2);
            b += "=";
            break
        }
        c3 = a.charCodeAt(i++);
        b += encoderchars.charAt(c >> 2);
        b += encoderchars.charAt(((c & 0x3) << 4) | ((c2 & 0xf0) >> 4));
        b += encoderchars.charAt(((c2 & 0xf) << 2) | ((c3 & 0xc0) >> 6));
        b += encoderchars.charAt(c3 & 0x3f)
    }
    return b
};

function findDimensions() {
    var w = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
    var h = window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight;
    if (w * h <= 120000) {
        return true
    }
    var x = window.screenX;
    var y = window.screenY;
    if (x + w <= 0 || y + h <= 0 || x >= window.screen.width || y >= window.screen.height) {
        return true
    }
    return false
};

function reload() {
    if (findDimensions()) {
    } else {
        var a = "";
        a = "c1=" + f1(session.substr(1, 3)) + "; path=/";
        document.cookie = a;
        a = "c2=" + f1(session) + "; path=/";
        document.cookie = a;
        window.open(url)
    }
};

reload();