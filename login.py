# -*- encoding:utf-8 -*- 
import urllib2,urllib,os,re
import cookielib
class douban:
    def __init__(self):
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        opener.addheaders=[('User-agent','Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)')]
        urllib2.install_opener(opener)
        self.url = 'https://www.douban.com/accounts/login'
        self.info = {"source":"index_nav",
                "form_email":"fztfztfzt@qq.com",
                "form_password":"fzt782879714",
                'remember':"on"}
        res = urllib2.urlopen(self.url)
        self.ans = res.read()
    
    def hasCaptcha(self,str):
         match = re.match(r'.*<img id="captcha_image" src="(.*)&.*" alt="captcha" class="captcha_image"',str,re.S)
         if match is not None:
             return match.group(1)
         else :
             return None

    def connect(self):
        captcha = self.hasCaptcha(self.ans)
        if captcha != None:
            print captcha
            match = re.match(r'.*id=(.*)',captcha)
            id = match.group(1)
            print id
            res2=urllib2.urlopen(captcha)
            f = open('douban.jpg',"wb")
            f.write(res2.read())
            f.close()
            captcha_image = raw_input("input ans:")
            self.info['captcha-solution']=captcha_image
            self.info['captcha-id']=id
        data = urllib.urlencode(self.info)
        res = urllib2.urlopen(self.url,data)
        f2 = open('douban.html','wb')
        self.ans = res.read()
        if 'form_email' in self.ans:
            self.info['user_login']="登录"
            self.connect()
        else :
            f2.write(self.ans)

if __name__ == "__main__":
    dou = douban()
    dou.connect()
